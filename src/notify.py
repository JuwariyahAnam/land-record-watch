import os

import requests

API = "https://api.telegram.org/bot{token}/{method}"


def _dry():
    return os.environ.get("DRY_RUN") == "1"


def _url(method):
    return API.format(token=os.environ["TELEGRAM_BOT_TOKEN"], method=method)


def send_text(chat_id, text):
    if _dry():
        print(f"[dry run] telegram text to {chat_id}: {text}")
        return
    r = requests.post(_url("sendMessage"), json={"chat_id": chat_id, "text": text}, timeout=20)
    r.raise_for_status()


def send_audio(chat_id, audio_bytes, caption=""):
    """sendAudio accepts MP3. sendVoice needs OGG with Opus, so switch if VerbX returns that."""
    if _dry():
        print(f"[dry run] telegram audio to {chat_id}: {len(audio_bytes)} bytes")
        return
    r = requests.post(_url("sendAudio"),
                      data={"chat_id": chat_id, "caption": caption[:900]},
                      files={"audio": ("alert.mp3", audio_bytes)}, timeout=60)
    r.raise_for_status()
