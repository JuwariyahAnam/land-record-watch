"""VerbX client with spending protection.

speak() never calls VerbX more than the limits below allow, and reuses audio it already made:
  VERBX_MAX_CALLS_PER_DAY  default 10   calls per day
  VERBX_MAX_CHARS_PER_CALL default 400  longer text is cut at a sentence end
  VERBX_MAX_CHARS_TOTAL    default 4000 characters over the whole free credit
A refused call raises VoiceBudgetStop. main.py already treats voice as optional, so the text alert
still goes out. Usage is kept in data/verbx_usage.json (not committed)."""
import hashlib
import json
import os
import time
from pathlib import Path

USAGE = Path(os.environ.get("VERBX_USAGE", "data/verbx_usage.json"))
CACHE = Path(os.environ.get("VERBX_CACHE", "data/audio"))


class VoiceBudgetStop(Exception):
    pass


def _limit(name, default):
    return int(os.environ.get(name, default))


def _trim(text, cap):
    if len(text) <= cap:
        return text
    cut = text[:cap]
    for mark in ("।", ".", "!", "?"):
        i = cut.rfind(mark)
        if i > cap // 2:
            return cut[: i + 1]
    return cut


def _load():
    try:
        return json.loads(USAGE.read_text())
    except (OSError, ValueError):
        return {}


def _spend(text):
    """Check the limits, then record the use. Raises VoiceBudgetStop if over."""
    u = _load()
    today = time.strftime("%Y-%m-%d")
    if u.get("day") != today:
        u["day"], u["calls_today"] = today, 0
    if u["calls_today"] >= _limit("VERBX_MAX_CALLS_PER_DAY", 10):
        raise VoiceBudgetStop("daily VerbX call limit reached")
    if u.get("chars_total", 0) + len(text) > _limit("VERBX_MAX_CHARS_TOTAL", 4000):
        raise VoiceBudgetStop("VerbX character budget used up")
    u["calls_today"] += 1
    u["chars_total"] = u.get("chars_total", 0) + len(text)
    USAGE.parent.mkdir(parents=True, exist_ok=True)
    USAGE.write_text(json.dumps(u))


BASE = "https://api.verbxeco.com"
# From VerbX's own schema: POST /v1/tts, header x-api-key, body {"text": ..., "options": {"language", "format", ...}}.
DEFAULT_PATH = "/v1/tts"


def _audio_from(resp):
    """Accept either JSON {audio_b64: ...} or raw audio bytes."""
    import base64

    ctype = resp.headers.get("content-type", "")
    if "json" in ctype:
        data = resp.json()
        b64 = data.get("audio_b64") or data.get("audio") or ""
        if not b64:
            raise RuntimeError("VerbX answered without audio")
        return base64.b64decode(b64)
    return resp.content


def _refund(text):
    u = _load()
    u["calls_today"] = max(0, u.get("calls_today", 1) - 1)
    u["chars_total"] = max(0, u.get("chars_total", len(text)) - len(text))
    USAGE.write_text(json.dumps(u))


LANG_NAMES = {"kn": "Kannada", "hi": "Hindi", "en": "English"}
LANG_LOCALE = {"kn": "kn-IN", "hi": "hi-IN", "en": "en-IN"}


def language_value(language):
    """How VerbX wants the language written. Set VERBX_LANG_STYLE to short (kn), locale (kn-IN) or name (Kannada)."""
    style = os.environ.get("VERBX_LANG_STYLE", "short")
    return {"short": language, "locale": LANG_LOCALE.get(language, language),
            "name": LANG_NAMES.get(language, language)}.get(style, language)


def request_body(text, language):
    """Confirmed with VerbX's schema: text plus an options object (the language goes inside options)."""
    # WAV, not MP3: Kannada with format=mp3 came back as a 0.5 second clip (measured on a real call).
    return {"text": text, "options": {"language": language_value(language), "format": os.environ.get("VERBX_FORMAT", "wav")}}


def _call_verbx(text, language):
    """POST to VerbX /v1/tts and return audio bytes (WAV). The language goes inside `options`.
    If VerbX does not like the language code, retry with the regional form, then without it."""
    import requests

    url = os.environ.get("VERBX_BASE", BASE) + os.environ.get("VERBX_TTS_PATH", DEFAULT_PATH)
    headers = {"x-api-key": os.environ["VERBX_API_KEY"]}
    first = request_body(text, language)
    fallbacks = [{"text": text, "options": {"format": first["options"]["format"], "language": f"{language}-IN"}},
                 {"text": text, "options": {"format": first["options"]["format"]}}]
    last = None
    for body in [first] + fallbacks:
        for attempt in range(3):  # VerbX sometimes answers 504 TTS_TIMEOUT; a retry usually works
            try:
                r = requests.post(url, json=body, headers=headers, timeout=90)
            except requests.RequestException as e:
                last = f"network error {type(e).__name__}"
            else:
                if r.ok:
                    audio = _audio_from(r)
                    if len(audio) < 1000:
                        raise RuntimeError(f"VerbX returned almost no audio ({len(audio)} bytes)")
                    return audio
                last = f"HTTP {r.status_code}: {r.text[:200]}"
                if r.status_code == 422:
                    break  # wrong value: try the next language form
                if r.status_code not in (502, 503, 504):
                    raise RuntimeError(f"VerbX refused the request ({last})")
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"VerbX did not return audio ({last})")


def speak(text, language):
    """Return audio bytes for text in the language ('kn', 'hi', 'en')."""
    text = _trim(text, _limit("VERBX_MAX_CHARS_PER_CALL", 400))
    # the key includes the settings, so changing them never serves old audio
    settings = f"{os.environ.get('VERBX_FORMAT', 'wav')}|{os.environ.get('VERBX_LANG_STYLE', 'short')}|v2"
    name = hashlib.sha256(f"{language}|{text}|{settings}".encode()).hexdigest()[:24] + ".audio"
    hit = CACHE / name
    if hit.exists() and hit.stat().st_size > 0:  # the same alert again costs nothing
        return hit.read_bytes()
    _spend(text)
    try:
        audio = _call_verbx(text, language)
    except Exception:
        _refund(text)  # a failed call is not charged, so it must not use up the allowance
        raise
    CACHE.mkdir(parents=True, exist_ok=True)
    hit.write_bytes(audio)
    return audio


def transcribe(audio_bytes, language):
    """Optional: speech to text for voice questions. Same rule, from the docs."""
    raise NotImplementedError("fill in from the VerbX docs")
