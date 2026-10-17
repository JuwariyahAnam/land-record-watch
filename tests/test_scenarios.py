"""The ten scenarios from the test plan, run against the local test pages in dev mode."""
import time

from src.main import check_parcel


def alerts(db):
    return [dict(r) for r in db.execute("SELECT severity, message, diff FROM alerts")]


def prime(db, parcel):
    assert check_parcel(db, parcel, "before") == "first"


def test_1_unchanged(db, parcel):
    prime(db, parcel)
    assert check_parcel(db, parcel, "before") == "nochange"
    assert alerts(db) == []


def test_2_new_mutation_switches_to_closer_watch(db, parcel):
    prime(db, parcel)
    assert check_parcel(db, parcel, "mutation") == "alert:high"
    assert db.execute("SELECT watch_closely FROM parcels").fetchone()[0] == 1
    assert alerts(db)[0]["severity"] == "high"


def test_3_status_change_is_medium(db, parcel):
    prime(db, parcel)
    check_parcel(db, parcel, "mutation")
    assert check_parcel(db, parcel, "approved") == "alert:medium"
    assert db.execute("SELECT watch_closely FROM parcels").fetchone()[0] == 0


def test_4_owner_change_is_critical_without_names(db, parcel):
    prime(db, parcel)
    assert check_parcel(db, parcel, "owner") == "alert:critical"
    assert "Owner Two" not in alerts(db)[0]["message"]


def test_5_extent_change_is_high(db, parcel):
    prime(db, parcel)
    assert check_parcel(db, parcel, "extent") == "alert:high"
    msg = alerts(db)[0]["message"]
    assert "2-10" in msg and "2-05" in msg


def test_6_layout_change_is_ops_not_all_clear(db, parcel):
    prime(db, parcel)
    assert check_parcel(db, parcel, "layout") == "ops"
    assert alerts(db)[0]["severity"] == "ops"


def test_7_captcha_pauses_the_check(db, parcel):
    prime(db, parcel)
    assert check_parcel(db, parcel, "captcha") == "ops"


def test_8_page_down_retries_then_ops(db, parcel):
    prime(db, parcel)
    assert check_parcel(db, parcel, "does-not-exist") == "ops"


def test_9_unconfirmed_parcel_is_never_looked_up(db):
    db.execute("""INSERT INTO parcels(label, district, taluk, hobli, village, survey_no, surnoc, hissa,
                  language, chat_id, own_land_confirmed_at) VALUES ('X','D','T','H','V','1','1','1','kn','1',NULL)""")
    db.commit()
    p = db.execute("SELECT * FROM parcels WHERE label='X'").fetchone()
    assert check_parcel(db, p, "before") == "skipped"
    assert db.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0] == 0


def test_10_same_change_is_alerted_once(db, parcel):
    prime(db, parcel)
    assert check_parcel(db, parcel, "mutation") == "alert:high"
    assert check_parcel(db, parcel, "mutation") == "nochange"
    assert len(alerts(db)) == 1
