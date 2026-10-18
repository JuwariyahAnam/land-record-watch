import json
import time

from src import db as database
from src.server import state


def test_state_shows_alert_in_three_languages(tmp_path, monkeypatch):
    monkeypatch.setenv("WATCH_DB", str(tmp_path / "t.db"))
    c = database.conn()
    c.execute("INSERT INTO parcels(id,label,district,survey_no,language,own_land_confirmed_at) VALUES (1,'My plot','Tumakuru','12',  'kn', 1)")
    diff = [{"type": "mutation_status_changed", "id": "MR-1001", "old": "Pending", "new": "Recorded"}]
    c.execute("INSERT INTO alerts(parcel_id,created_at,severity,diff,message,decision) VALUES (1,?,?,?,?,?)",
              (time.time(), "medium", json.dumps(diff), "x", "rules"))
    c.commit()
    s = state()
    a = s["parcels"][0]["alerts"][0]
    assert set(a["messages"]) == {"en", "kn", "hi"}
    assert "MR-1001" in a["messages"]["kn"] and "Recorded" in a["messages"]["en"]


def test_browser_budget_stops_runaway_loops(tmp_path, monkeypatch):
    import pytest
    from src.browser_tool import BudgetStop, _use_budget
    monkeypatch.setenv("WATCH_DB", str(tmp_path / "t.db"))
    monkeypatch.setenv("BB_MAX_SESSIONS_PER_DAY", "2")
    _use_budget(); _use_budget()
    with pytest.raises(BudgetStop):
        _use_budget()
