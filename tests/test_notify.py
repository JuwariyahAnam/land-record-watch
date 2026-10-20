import io
import wave

from src import notify


def make_wav(seconds=3, rate=8000):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(b"\x00\x00" * rate * seconds)
    return buf.getvalue()


class Resp:
    def __init__(self, ok=True): self.ok, self.status_code = ok, 200 if ok else 400
    def json(self): return {}


def test_wav_length_is_read():
    assert notify.wav_seconds(make_wav(3)) == 3
    assert notify.wav_seconds(b"not audio") == 0


def test_audio_is_sent_with_its_length(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t"); monkeypatch.delenv("DRY_RUN", raising=False)
    monkeypatch.setattr(notify, "to_opus", lambda wav: None)
    calls = []
    monkeypatch.setattr(notify.requests, "post", lambda url, **k: calls.append((url, k)) or Resp())
    notify.send_audio("1", make_wav(4), caption="hi")
    url, k = calls[0]
    assert url.endswith("sendAudio") and k["data"]["duration"] == 4


def test_voice_note_is_used_when_ffmpeg_works_and_falls_back_when_refused(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t"); monkeypatch.delenv("DRY_RUN", raising=False)
    monkeypatch.setattr(notify, "to_opus", lambda wav: b"o" * 900)
    calls = []
    answers = [Resp(False), Resp(True)]
    monkeypatch.setattr(notify.requests, "post", lambda url, **k: calls.append(url) or answers.pop(0))
    notify.send_audio("1", make_wav(2))
    assert calls[0].endswith("sendVoice") and calls[1].endswith("sendAudio")


def test_no_ffmpeg_means_plain_wav(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda name: None)
    assert notify.to_opus(make_wav(1)) is None
