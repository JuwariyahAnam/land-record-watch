import os

import requests

API = "https://api.telegram.org/bot{token}/{method}"


def _dry():
    return os.environ.get("DRY_RUN") == "1"


def _url(method):
    return API.format(token=os.environ["TELEGRAM_BOT_TOKEN"], method=method)


def _check(r):
    """Raise an error that never contains the bot token (the URL does)."""
    if not r.ok:
        try:
            why = r.json().get("description", "")
        except ValueError:
            why = ""
        raise RuntimeError(f"Telegram refused the message (HTTP {r.status_code}): {why}")


def send_text(chat_id, text):
    if _dry():
        print(f"[dry run] telegram text to {chat_id}: {text}")
        return
    r = requests.post(_url("sendMessage"), json={"chat_id": chat_id, "text": text}, timeout=20)
    _check(r)


def wav_seconds(audio):
    """Length of a WAV in whole seconds (0 if it cannot be read). Telegram shows 0:00 without it."""
    import io
    import wave
    try:
        with wave.open(io.BytesIO(audio)) as w:
            return max(1, round(w.getnframes() / float(w.getframerate())))
    except Exception:
        return 0


def to_opus(wav):
    """WAV to OGG/Opus with ffmpeg, so Telegram can show it as a voice note with a waveform.
    Returns None when ffmpeg is missing or fails (the WAV is then sent as audio)."""
    import shutil
    import subprocess
    if os.environ.get("VOICE_NOTE", "1") != "1" or not shutil.which("ffmpeg"):
        return None
    try:
        p = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "pipe:0", "-c:a", "libopus", "-b:a", "32k",
                            "-f", "ogg", "pipe:1"], input=wav, capture_output=True, timeout=60)
        return p.stdout if p.returncode == 0 and len(p.stdout) > 500 else None
    except Exception:
        return None


def send_audio(chat_id, audio_bytes, caption=""):
    """Voice note (OGG/Opus) when ffmpeg is there, else the WAV as audio with its length, else as a file."""
    if _dry():
        print(f"[dry run] telegram audio to {chat_id}: {len(audio_bytes)} bytes")
        return
    wav = audio_bytes[:4] == b"RIFF"  # VerbX returns WAV
    seconds = wav_seconds(audio_bytes) if wav else 0
    data = {"chat_id": chat_id, "caption": caption[:900]}
    if wav:
        ogg = to_opus(audio_bytes)
        if ogg:
            r = requests.post(_url("sendVoice"), data={**data, "duration": seconds},
                              files={"voice": ("alert.ogg", ogg)}, timeout=60)
            if r.ok:
                return
            print("voice note refused, sending the audio file instead")
    name = "alert.wav" if wav else "alert.mp3"
    r = requests.post(_url("sendAudio"), data={**data, **({"duration": seconds} if seconds else {}),
                                               "title": "Land Record Watch"},
                      files={"audio": (name, audio_bytes)}, timeout=60)
    if not r.ok and wav:  # some clients refuse WAV as music: send it as a file instead
        r = requests.post(_url("sendDocument"), data=data, files={"document": (name, audio_bytes)}, timeout=60)
    _check(r)
