"""Try the Kannada sentence on every VerbX speech endpoint and keep what works.
  python -m src.verbx_kn
Audio is saved in data\\voice-test\\probe\\ . Send me the printed table; the biggest file is usually the good one."""
import base64
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()
BASE = os.environ.get("VERBX_BASE", "https://api.verbxeco.com")
KN = "ನಿಮ್ಮ ಜಮೀನಿನ ದಾಖಲೆಯಲ್ಲಿ ಬದಲಾವಣೆ ಕಂಡುಬಂದಿದೆ."
BODIES = [
    {"text": KN, "language": "kn"},
    {"text": KN, "language": "kn-IN"},
    {"text": KN, "language_code": "kn-IN"},
    {"text": KN, "target_language_code": "kn-IN"},
    {"text": KN, "lang": "kn"},
    {"text": KN, "options": {"language": "kn", "format": "wav"}},
    {"text": KN, "options": {"language": "kn-IN", "format": "wav"}},
]
PATHS = ["/tts", "/v1/personal/tts", "/v1/travel/tts", "/v1/tts"]


def audio_of(r):
    if "json" in r.headers.get("content-type", ""):
        d = r.json()
        for k in ("audio_b64", "audio", "audio_base64", "wav_b64", "data"):
            if isinstance(d.get(k), str) and len(d[k]) > 200:
                return base64.b64decode(d[k])
        return None
    return r.content


if __name__ == "__main__":
    key = os.environ.get("VERBX_API_KEY", "")
    if not key.startswith("vx_"):
        raise SystemExit("put your key in .env as VERBX_API_KEY=vx_...")
    out = Path("data/voice-test/probe")
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for path in PATHS:
        for auth in ({"x-api-key": key}, {"Authorization": "Bearer " + key}):
            for body in BODIES:
                label = f"{path} {list(auth)[0]} {sorted(k for k in body if k != 'text')}"
                try:
                    r = requests.post(BASE + path, json=body, headers=auth, timeout=90)
                except requests.RequestException as e:
                    print(f"{label}: network {type(e).__name__}")
                    continue
                if not r.ok:
                    try:
                        why = json.loads(r.text)["error"]
                        why = why.get("details", {}).get("fields") or why.get("message")
                    except Exception:
                        why = r.text[:80]
                    print(f"{label}: HTTP {r.status_code} {why}")
                    if r.status_code in (401, 403) and "Authorization" in auth:
                        break
                    continue
                audio = audio_of(r)
                n += 1
                if not audio:
                    print(f"{label}: HTTP 200 but no audio found: {r.text[:100]}")
                    continue
                kind = "wav" if audio[:4] == b"RIFF" else "ogg" if audio[:4] == b"OggS" else "mp3"
                f = out / f"{n:02d}-{path.strip('/').replace('/', '_')}.{kind}"
                f.write_bytes(audio)
                print(f"{label}: OK {len(audio)} bytes -> {f}")
    print("\nDone. Play the biggest files; a full sentence is roughly 100 kB or more.")
