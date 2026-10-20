import re

import pytest

from src.portal import security as sec
from src.portal import store
from src.portal.app import create_app
from src.sources import parse_fixture

PW = "Sunflower2026!"
LAND = {"district": "Tumakuru", "taluk": "Sira", "hobli": "Kasaba", "village": "Demo Village",
        "survey_no": "12", "surnoc": "*", "hissa": "1", "extent": "2-10", "owner_name": "Test Owner One", "own": "yes"}


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setenv("PORTAL_DB", str(tmp_path / "portal.db"))
    monkeypatch.delenv("PORTAL_SECRET_KEY", raising=False)
    return create_app()


def csrf_of(client, path="/login"):
    html = client.get(path).get_data(as_text=True)
    return re.search(r'name="csrf" value="([^"]+)"', html).group(1)


def signup(app, role, email, name="Test Person"):
    c = app.test_client()
    t = csrf_of(c, f"/register?role={role}")
    r = c.post("/register", data={"csrf": t, "role": role, "name": name, "email": email, "password": PW, "confirm": PW})
    assert r.status_code == 302, r.get_data(as_text=True)
    return c


def make_registrar(app, email="reg@demo.example"):
    db = store.conn()
    store.create_user(db, email, "Demo Registrar", "registrar", sec.hash_password(PW))
    c = app.test_client()
    t = csrf_of(c)
    assert c.post("/login", data={"csrf": t, "email": email, "password": PW}).status_code == 302
    return c


def post(c, path, page, **data):
    return c.post(path, data={"csrf": csrf_of(c, page), **data})


def register_land(c):
    return post(c, "/lands/new", "/lands/new", **LAND)


def test_password_is_hashed_not_stored(app):
    signup(app, "landlord", "l@demo.example")
    stored = store.conn().execute("SELECT pw_hash FROM users").fetchone()[0]
    assert PW not in stored and stored.startswith("scrypt$")
    assert sec.verify_password(PW, stored) and not sec.verify_password("wrong", stored)


def test_weak_password_and_bad_email_refused(app):
    c = app.test_client()
    t = csrf_of(c, "/register")
    r = c.post("/register", data={"csrf": t, "role": "buyer", "name": "A B", "email": "a@b.example", "password": "short1", "confirm": "short1"})
    assert r.status_code == 400
    r = c.post("/register", data={"csrf": t, "role": "buyer", "name": "A B", "email": "nope", "password": PW, "confirm": PW})
    assert r.status_code == 400


def test_post_without_csrf_is_refused(app):
    c = app.test_client()
    assert c.post("/login", data={"email": "x@y.example", "password": PW}).status_code == 400


def test_wrong_password_then_lockout(app):
    signup(app, "buyer", "b@demo.example")
    c = app.test_client()
    t = csrf_of(c)
    for _ in range(5):
        assert c.post("/login", data={"csrf": t, "email": "b@demo.example", "password": "WrongPass123"}).status_code == 401
    assert c.post("/login", data={"csrf": t, "email": "b@demo.example", "password": PW}).status_code == 429


def test_roles_are_enforced(app):
    landlord, buyer = signup(app, "landlord", "l@demo.example"), signup(app, "buyer", "b@demo.example")
    assert buyer.get("/lands/new").status_code == 403
    assert buyer.get("/registrar").status_code == 403
    assert landlord.get("/search").status_code == 403
    assert app.test_client().get("/dashboard").status_code == 302  # not logged in


def test_landlord_registers_land_and_duplicates_are_refused(app):
    c = signup(app, "landlord", "l@demo.example")
    assert register_land(c).status_code == 302
    assert register_land(c).status_code == 400
    assert "Demo Village" in c.get("/dashboard").get_data(as_text=True)


def test_own_land_confirmation_required(app):
    c = signup(app, "landlord", "l@demo.example")
    data = {k: v for k, v in LAND.items() if k != "own"}
    assert post(c, "/lands/new", "/lands/new", **data).status_code == 400


def test_landlord_cannot_open_someone_elses_land(app):
    a = signup(app, "landlord", "a@demo.example")
    register_land(a)
    b = signup(app, "landlord", "b@demo.example")
    assert b.get("/lands/1").status_code == 404
    assert post(b, "/lands/1/mutation", "/dashboard", kind="Sale").status_code == 404


def test_mutation_flow_landlord_files_registrar_approves_buyer_sees(app):
    landlord = signup(app, "landlord", "l@demo.example")
    register_land(landlord)
    assert post(landlord, "/lands/1/mutation", "/lands/1", kind="Sale", note="demo").status_code == 302
    buyer = signup(app, "buyer", "b@demo.example")
    page = buyer.get("/record/1").get_data(as_text=True)
    assert "MR-1001" in page and "Pending" in page and "1 mutation pending" in page
    reg = make_registrar(app)
    assert "MR-1001" in reg.get("/registrar").get_data(as_text=True)
    assert post(reg, "/mutations/1/decide", "/registrar", decision="approve", note="ok").status_code == 302
    page = buyer.get("/record/1").get_data(as_text=True)
    assert "Approved" in page and "No pending mutations" in page
    assert landlord.post("/mutations/1/decide", data={"decision": "approve"}).status_code in (400, 403)


def test_landlord_cannot_approve_own_mutation(app):
    landlord = signup(app, "landlord", "l@demo.example")
    register_land(landlord)
    post(landlord, "/lands/1/mutation", "/lands/1", kind="Sale")
    assert post(landlord, "/mutations/1/decide", "/lands/1", decision="approve").status_code == 403
    assert store.conn().execute("SELECT status FROM mutations").fetchone()[0] == "Pending"


def test_buyer_search_masks_owner_and_needs_district_and_survey(app):
    landlord = signup(app, "landlord", "l@demo.example")
    register_land(landlord)
    buyer = signup(app, "buyer", "b@demo.example")
    html = buyer.get("/search?district=tumakuru&survey_no=12").get_data(as_text=True)
    assert "Demo Village" in html
    full = buyer.get("/record/1").get_data(as_text=True)
    assert "Test Owner One" not in full and "T*** O***" in full
    assert "Enter at least" in buyer.get("/search?district=Tumakuru").get_data(as_text=True)


def test_agent_can_read_public_link_and_detect_changes(app):
    from src.differ import diff, summarize
    landlord = signup(app, "landlord", "l@demo.example")
    register_land(landlord)
    token = store.conn().execute("SELECT public_token FROM lands").fetchone()[0]
    anon = app.test_client()
    first = summarize(parse_fixture(anon.get(f"/public/{token}").get_data(as_text=True)))
    post(landlord, "/lands/1/mutation", "/lands/1", kind="Sale")
    reg = make_registrar(app)
    second = summarize(parse_fixture(anon.get(f"/public/{token}").get_data(as_text=True)))
    assert [c["type"] for c in diff(first, second)] == ["new_mutation"]
    post(reg, "/mutations/1/decide", "/registrar", decision="approve")
    third = summarize(parse_fixture(anon.get(f"/public/{token}").get_data(as_text=True)))
    assert diff(second, third) == [{"type": "mutation_status_changed", "id": "MR-1001", "old": "Pending", "new": "Approved"}]
    post(reg, "/registrar/lands/1/extent", "/registrar/lands/1", extent="2-05")
    fourth = summarize(parse_fixture(anon.get(f"/public/{token}").get_data(as_text=True)))
    assert diff(third, fourth)[0]["type"] == "extent_changed"
    post(reg, "/registrar/lands/1/owner", "/registrar/lands/1", owner_name="Test Owner Two")
    fifth = summarize(parse_fixture(anon.get(f"/public/{token}").get_data(as_text=True)))
    assert diff(fourth, fifth)[0]["type"] == "owner_changed"


def test_public_page_hides_owner_name_and_unknown_token_404(app):
    landlord = signup(app, "landlord", "l@demo.example")
    register_land(landlord)
    token = store.conn().execute("SELECT public_token FROM lands").fetchone()[0]
    html = app.test_client().get(f"/public/{token}").get_data(as_text=True)
    assert "Test Owner One" not in html
    assert app.test_client().get("/public/not-a-real-token").status_code == 404


def test_output_is_escaped(app):
    c = signup(app, "landlord", "l@demo.example", name="<script>alert(1)</script>")
    html = c.get("/dashboard").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html


def test_security_headers_and_logout(app):
    c = signup(app, "buyer", "b@demo.example")
    r = c.get("/search")
    assert "default-src 'self'" in r.headers["Content-Security-Policy"] and r.headers["Cache-Control"] == "no-store"
    assert post(c, "/logout", "/search").status_code == 302
    assert c.get("/search").status_code == 302


def test_portal_source_only_reads_configured_portal(monkeypatch):
    from src.sources import LayoutChanged, PortalSource
    monkeypatch.setenv("PORTAL_BASE", "https://registry.example")
    with pytest.raises(LayoutChanged):
        PortalSource().fetch({"source_ref": "https://evil.example/public/abc"})
    with pytest.raises(LayoutChanged):
        PortalSource().fetch({"source_ref": ""})


def test_setup_page_creates_registrar_once(tmp_path, monkeypatch):
    monkeypatch.setenv("PORTAL_DB", str(tmp_path / "p.db"))
    monkeypatch.delenv("PORTAL_SETUP_CODE", raising=False)
    from src.portal.app import create_app
    c = create_app().test_client()
    page = c.get("/setup")
    assert page.status_code == 200
    import re
    tok = re.search(r'name="csrf" value="([^"]+)"', page.get_data(as_text=True)).group(1)
    r = c.post("/setup", data={"csrf": tok, "name": "Demo Registrar", "email": "r@demo.example",
                               "password": "Strong-pass-123", "confirm": "Strong-pass-123"})
    assert r.status_code == 302
    assert c.get("/setup").status_code == 404


def test_demo_land_comes_back_with_the_same_link(tmp_path, monkeypatch):
    monkeypatch.setenv("PORTAL_DB", str(tmp_path / "p.db"))
    monkeypatch.setenv("PORTAL_DEMO_TOKEN", "x" * 24)
    from src.portal.app import create_app
    c = create_app().test_client()
    r = c.get("/public/" + "x" * 24)
    assert r.status_code == 200 and b"demo-village" in r.data
    create_app()  # restart: must not duplicate or fail
    assert c.get("/public/" + "x" * 24).status_code == 200


def test_demo_landlord_can_log_in_when_password_is_set(tmp_path, monkeypatch):
    import re
    monkeypatch.setenv("PORTAL_DB", str(tmp_path / "p.db"))
    monkeypatch.setenv("PORTAL_DEMO_TOKEN", "y" * 24)
    monkeypatch.setenv("PORTAL_DEMO_PASSWORD", "Demo-pass-2026")
    from src.portal.app import create_app
    c = create_app().test_client()
    page = c.get("/login").get_data(as_text=True)
    tok = re.search(r'name="csrf" value="([^"]+)"', page).group(1)
    r = c.post("/login", data={"csrf": tok, "email": "demo-landlord@demo.example", "password": "Demo-pass-2026"})
    assert r.status_code == 302 and "/dashboard" in r.headers["Location"]


def test_landlord_sets_alert_language_and_agent_can_read_it(app):
    landlord = signup(app, "landlord", "l@demo.example")
    register_land(landlord)
    token = store.conn().execute("SELECT public_token FROM lands").fetchone()[0]
    anon = app.test_client()
    assert parse_fixture(anon.get(f"/public/{token}").get_data(as_text=True)).language == "kn"
    assert post(landlord, "/lands/1/language", "/lands/1", language="hi").status_code == 302
    assert parse_fixture(anon.get(f"/public/{token}").get_data(as_text=True)).language == "hi"
    assert 'value="hi" selected' in landlord.get("/lands/1").get_data(as_text=True)
    assert post(landlord, "/lands/1/language", "/lands/1", language="xx").status_code == 400


def test_language_setting_is_owner_only_and_does_not_look_like_a_record_change(app):
    from src.differ import diff, summarize
    landlord = signup(app, "landlord", "l@demo.example")
    register_land(landlord)
    other = signup(app, "landlord", "o@demo.example")
    assert post(other, "/lands/1/language", "/dashboard", language="en").status_code in (403, 404, 302)
    assert store.conn().execute("SELECT alert_language FROM lands").fetchone()[0] == "kn"
    token = store.conn().execute("SELECT public_token FROM lands").fetchone()[0]
    anon = app.test_client()
    before = summarize(parse_fixture(anon.get(f"/public/{token}").get_data(as_text=True)))
    post(landlord, "/lands/1/language", "/lands/1", language="en")
    after = summarize(parse_fixture(anon.get(f"/public/{token}").get_data(as_text=True)))
    assert diff(before, after) == []


def test_old_database_gets_language_column(tmp_path, monkeypatch):
    import sqlite3
    path = tmp_path / "old.db"
    c = sqlite3.connect(path)
    c.execute("CREATE TABLE lands(id INTEGER PRIMARY KEY, owner_id INTEGER, district TEXT, taluk TEXT, hobli TEXT, village TEXT, survey_no TEXT, surnoc TEXT, hissa TEXT, extent TEXT, owner_name TEXT, public_token TEXT, created_at REAL, updated_at REAL)")
    c.commit(); c.close()
    monkeypatch.setenv("PORTAL_DB", str(path))
    cols = [r["name"] for r in store.conn().execute("PRAGMA table_info(lands)")]
    assert "alert_language" in cols


def test_site_can_be_shown_in_kannada_and_hindi(app):
    landlord = signup(app, "landlord", "l@demo.example")
    for code, word in (("kn", "ಲಾಗಿನ್"), ("hi", "लॉग इन")):
        c = app.test_client()
        assert c.get(f"/lang/{code}").status_code == 302
        html = c.get("/login").get_data(as_text=True)
        assert word in html and f'lang="{code}"' in html
    assert app.test_client().get("/lang/xx").status_code == 404


def test_public_watch_page_stays_english_so_the_agent_can_read_it(app):
    landlord = signup(app, "landlord", "l@demo.example")
    register_land(landlord)
    post(landlord, "/lands/1/mutation", "/lands/1", kind="Sale")
    token = store.conn().execute("SELECT public_token FROM lands").fetchone()[0]
    c = app.test_client()
    c.get("/lang/kn")
    rec = parse_fixture(c.get(f"/public/{token}").get_data(as_text=True))
    assert rec.extent == "2-10" and rec.mutations[0]["status"] == "Pending"


def test_missing_translation_never_breaks_a_page():
    from src.portal import i18n
    assert i18n.translate_html("<p>Some brand new sentence</p>", "kn") == "<p>Some brand new sentence</p>"
