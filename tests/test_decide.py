import json

import pytest

import src.decide as decide_mod
from src.decide import decide
from src.main import check_parcel

CHANGES = [{"type": "new_mutation", "id": "MR-1002", "date": "2026-10-10", "status": "Pending"}]


@pytest.fixture(autouse=True)
def configured(monkeypatch):
    monkeypatch.setattr(decide_mod, "configured", lambda: True)


def fake(reply, seen=None):
    def _complete(system, user, timeout=20):
        if seen is not None:
            seen.append(user)
        if isinstance(reply, Exception):
            raise reply
        return reply
    return _complete


def test_no_model_configured_uses_rules(monkeypatch):
    monkeypatch.setattr(decide_mod, "configured", lambda: False)
    d = decide(CHANGES, "high", True)
    assert d["source"] == "rules" and d["recheck"] is True


def test_model_choice_is_used(monkeypatch):
    monkeypatch.setattr(decide_mod, "complete",
                        fake('```json\n{"action": "alert", "reason": "looks settled"}\n```'))
    d = decide(CHANGES, "high", True)
    assert d["source"] == "llm" and d["recheck"] is False and d["reason"] == "looks settled"


@pytest.mark.parametrize("bad", ["not json at all", '{"action": "delete_everything"}',
                                 RuntimeError("timeout")])
def test_bad_model_output_falls_back_to_rules(monkeypatch, bad):
    monkeypatch.setattr(decide_mod, "complete", fake(bad))
    d = decide(CHANGES, "high", True)
    assert d["source"] == "rules" and d["recheck"] is True


def test_model_cannot_suppress_an_alert(monkeypatch, db, parcel):
    monkeypatch.setattr(decide_mod, "complete", fake('{"action": "alert", "reason": "ok"}'))
    assert check_parcel(db, parcel, "before") == "first"
    assert check_parcel(db, parcel, "mutation") == "alert:high"  # still alerted
    row = db.execute("SELECT decision FROM alerts").fetchone()
    assert json.loads(row["decision"])["source"] == "llm"
    assert db.execute("SELECT watch_closely FROM parcels").fetchone()[0] == 0  # model's choice honoured


def test_model_never_sees_owner_names(monkeypatch, db, parcel):
    seen = []
    monkeypatch.setattr(decide_mod, "complete", fake('{"action": "alert", "reason": "ok"}', seen))
    check_parcel(db, parcel, "before")
    check_parcel(db, parcel, "owner")
    assert seen and all("Test Owner" not in s and "Test plot" not in s for s in seen)
