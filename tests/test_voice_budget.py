import pytest

from src import verbx_client as v


def setup(monkeypatch, tmp_path, **env):
    monkeypatch.setattr(v, "USAGE", tmp_path / "u.json")
    monkeypatch.setattr(v, "CACHE", tmp_path / "audio")
    for k, val in env.items():
        monkeypatch.setenv(k, str(val))
    calls = []
    monkeypatch.setattr(v, "_call_verbx", lambda t, l: calls.append(t) or b"AUDIO")
    return calls


def test_same_alert_is_cached(monkeypatch, tmp_path):
    calls = setup(monkeypatch, tmp_path)
    assert v.speak("hello", "en") == b"AUDIO" and v.speak("hello", "en") == b"AUDIO"
    assert len(calls) == 1


def test_daily_limit(monkeypatch, tmp_path):
    calls = setup(monkeypatch, tmp_path, VERBX_MAX_CALLS_PER_DAY=2)
    v.speak("a", "en"); v.speak("b", "en")
    with pytest.raises(v.VoiceBudgetStop):
        v.speak("c", "en")
    assert len(calls) == 2


def test_total_character_budget_and_trim(monkeypatch, tmp_path):
    calls = setup(monkeypatch, tmp_path, VERBX_MAX_CHARS_TOTAL=50, VERBX_MAX_CHARS_PER_CALL=30)
    v.speak("x" * 100, "en")
    assert len(calls[0]) <= 30
    with pytest.raises(v.VoiceBudgetStop):
        v.speak("y" * 30, "en"); v.speak("z" * 30, "en")


def test_verbx_response_is_decoded(monkeypatch):
    import base64
    import types

    audio = b"RIFF....WAVE"
    resp = types.SimpleNamespace(headers={"content-type": "application/json"},
                                 json=lambda: {"audio_b64": base64.b64encode(audio).decode(), "language": "kn"},
                                 content=b"")
    assert v._audio_from(resp) == audio
    raw = types.SimpleNamespace(headers={"content-type": "audio/wav"}, content=audio)
    assert v._audio_from(raw) == audio


def test_request_sends_only_text(monkeypatch):
    import types

    import requests

    seen = {}
    def fake_post(url, json=None, headers=None, timeout=None):
        seen.update(url=url, json=json, headers=headers)
        return types.SimpleNamespace(ok=True, headers={"content-type": "audio/wav"}, content=b"RIFF" + b"x" * 2000)
    monkeypatch.setattr(requests, "post", fake_post)
    monkeypatch.setenv("VERBX_API_KEY", "vx_test")
    assert v._call_verbx("hi", "en") == b"RIFF" + b"x" * 2000
    assert seen["json"] == {"text": "hi", "options": {"language": "en", "format": "wav"}} and seen["url"].endswith("/v1/tts")
    assert seen["headers"] == {"x-api-key": "vx_test"}


def test_failed_call_does_not_use_budget(monkeypatch, tmp_path):
    setup(monkeypatch, tmp_path, VERBX_MAX_CALLS_PER_DAY=1)
    def boom(t, l): raise RuntimeError("504")
    monkeypatch.setattr(v, "_call_verbx", boom)
    with pytest.raises(RuntimeError):
        v.speak("a", "en")
    monkeypatch.setattr(v, "_call_verbx", lambda t, l: b"AUDIO")
    assert v.speak("a", "en") == b"AUDIO"


def test_language_style(monkeypatch):
    monkeypatch.setenv("VERBX_LANG_STYLE", "locale")
    assert v.request_body("x", "kn")["options"]["language"] == "kn-IN"
    monkeypatch.setenv("VERBX_LANG_STYLE", "name")
    assert v.request_body("x", "hi")["options"]["language"] == "Hindi"
