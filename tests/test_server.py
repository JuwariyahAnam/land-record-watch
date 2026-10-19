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


def test_set_language_changes_alert_language(tmp_path, monkeypatch):
    import subprocess, sys
    monkeypatch.setenv("WATCH_DB", str(tmp_path / "t.db"))
    c = database.conn()
    c.execute("INSERT INTO parcels(id,label,language,own_land_confirmed_at) VALUES (1,'P','kn',1)")
    c.commit()
    r = subprocess.run([sys.executable, "-m", "src.set_language", "hi"], capture_output=True, text=True,
                       env={**__import__("os").environ})
    assert "1 parcel" in r.stdout
    assert database.conn().execute("SELECT language FROM parcels").fetchone()[0] == "hi"


def test_web_language_choice_is_saved_and_used(tmp_path, monkeypatch):
    import json as _json, threading, urllib.request, urllib.error
    from http.server import ThreadingHTTPServer
    from src.server import H
    monkeypatch.setenv("WATCH_DB", str(tmp_path / "t.db"))
    c = database.conn()
    c.execute("INSERT INTO parcels(id,label,language,own_land_confirmed_at) VALUES (1,'P','kn',1)")
    c.commit()
    srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        def post(lang, origin=None):
            req = urllib.request.Request(f"http://127.0.0.1:{port}/api/language",
                                         data=_json.dumps({"language": lang}).encode(),
                                         headers={"Content-Type": "application/json", **({"Origin": origin} if origin else {})})
            return urllib.request.urlopen(req)
        assert post("hi").status == 200
        assert database.conn().execute("SELECT language FROM parcels").fetchone()[0] == "hi"
        for bad in (lambda: post("xx"), lambda: post("en", origin="http://evil.example")):
            try:
                bad()
                assert False, "should have been refused"
            except urllib.error.HTTPError as e:
                assert e.code in (400, 403)
        assert database.conn().execute("SELECT language FROM parcels").fetchone()[0] == "hi"
    finally:
        srv.shutdown()


def test_failed_send_is_retried_next_run(tmp_path, monkeypatch):
    import src.main as m
    from src.db import conn
    monkeypatch.setenv("WATCH_DB", str(tmp_path / "w.db"))
    monkeypatch.setenv("DRY_RUN", "0")
    monkeypatch.setenv("RETRY_DELAY", "0")
    monkeypatch.setenv("DEV_NO_BROWSER", "1")
    monkeypatch.setenv("SOURCE", "fixture")
    db = conn()
    db.execute("""INSERT INTO parcels(label,district,taluk,hobli,village,survey_no,surnoc,hissa,language,chat_id,
                  own_land_confirmed_at) VALUES ('t','d','t','h','v','1','*','0','en','1',1)""")
    db.commit()
    parcel = lambda: db.execute("SELECT * FROM parcels").fetchone()
    sent = []
    monkeypatch.setattr(m, "send_text", lambda c, t: sent.append(t))
    monkeypatch.setattr(m, "speak", lambda *a: (_ for _ in ()).throw(RuntimeError("no voice")))
    assert m.check_parcel(db, parcel(), "before") == "first"
    def boom(c, t): raise RuntimeError("telegram down")
    monkeypatch.setattr(m, "send_text", boom)
    assert m.check_parcel(db, parcel(), "mutation") == "send-failed"
    assert db.execute("SELECT COUNT(*) FROM alerts").fetchone()[0] == 0
    monkeypatch.setattr(m, "send_text", lambda c, t: sent.append(t))
    assert m.check_parcel(db, parcel(), "mutation").startswith("alert:")
    assert sent
