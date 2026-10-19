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


def send_audio(chat_id, audio_bytes, caption=""):
    """sendAudio accepts MP3. sendVoice needs OGG with Opus, so switch if VerbX returns that."""
    if _dry():
        print(f"[dry run] telegram audio to {chat_id}: {len(audio_bytes)} bytes")
        return
    wav = audio_bytes[:4] == b"RIFF"  # VerbX returns WAV
    name = "alert.wav" if wav else "alert.mp3"
    r = requests.post(_url("sendAudio"),
                      data={"chat_id": chat_id, "caption": caption[:900]},
                      files={"audio": (name, audio_bytes)}, timeout=60)
    if not r.ok and wav:  # some clients refuse WAV as music: send it as a file instead
        r = requests.post(_url("sendDocument"),
                          data={"chat_id": chat_id, "caption": caption[:900]},
                          files={"document": (name, audio_bytes)}, timeout=60)
    _check(r)
