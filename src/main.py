import argparse
import json
import os
import time

from dotenv import load_dotenv

load_dotenv()

from .browser_tool import NeedsHuman
from .db import conn
from .decide import decide
from .differ import diff, fingerprint, has_pending, summarize, top_severity
from .explain import build_message, grounded, ops_message
from .notify import send_audio, send_text
from .sources import LayoutChanged, get_source
from .verbx_client import speak


def alert(db, parcel, severity, diff_json, message, decision=""):
    cur = db.execute("INSERT INTO alerts(parcel_id, created_at, severity, diff, message, decision) VALUES (?,?,?,?,?,?)",
                     (parcel["id"], time.time(), severity, diff_json, message, decision))
    db.commit()
    try:
        send_text(parcel["chat_id"], message)
    except Exception:
        db.execute("DELETE FROM alerts WHERE id=?", (cur.lastrowid,))  # it was never delivered
        db.commit()
        raise
    if os.environ.get("DRY_RUN") == "1":
        print("[dry run] voice skipped")
        return
    try:
        send_audio(parcel["chat_id"], speak(message, parcel["language"]), caption=message)
    except Exception as e:  # the text alert has already gone out
        print("voice failed, text alert already sent:", e)


def ops_alert(db, parcel):
    alert(db, parcel, "ops", "[]", ops_message(parcel["label"], parcel["language"]))
    return "ops"


def check_parcel(db, parcel, scenario="before"):
    """Returns what happened: skipped, first, nochange, ops, or alert:<severity>."""
    if not parcel["own_land_confirmed_at"]:
        print("skipped: parcel not confirmed as the user's own")
        return "skipped"
    lang, label = parcel["language"], parcel["label"]
    source = get_source(scenario)
    delay = float(os.environ.get("RETRY_DELAY", "5"))
    rec = None
    for attempt in range(3):
        try:
            rec = source.fetch(parcel)
            break
        except (NeedsHuman, LayoutChanged) as e:
            print("cannot continue:", e)
            return ops_alert(db, parcel)
        except Exception as e:
            print("fetch failed:", e)
            time.sleep(delay * (attempt + 1))
    if rec is None:
        return ops_alert(db, parcel)

    if rec.language and rec.language != parcel["language"]:  # the owner changed it on the website
        db.execute("UPDATE parcels SET language=? WHERE id=?", (rec.language, parcel["id"]))
        db.commit()
        print(f"alert language is now {rec.language}")
        lang = rec.language
        parcel = db.execute("SELECT * FROM parcels WHERE id=?", (parcel["id"],)).fetchone()
    new = summarize(rec)
    snap_id = None
    last = db.execute("SELECT summary FROM snapshots WHERE parcel_id=? ORDER BY id DESC LIMIT 1",
                      (parcel["id"],)).fetchone()
    snap_id = db.execute("INSERT INTO snapshots(parcel_id, fetched_at, source, fingerprint, summary) VALUES (?,?,?,?,?)",
                         (parcel["id"], time.time(), source.name, fingerprint(new), json.dumps(new))).lastrowid
    # Agent decision: a pending mutation means check again in the evening.
    db.execute("UPDATE parcels SET watch_closely=? WHERE id=?",
               (1 if has_pending(new) else 0, parcel["id"]))
    db.commit()
    if last is None:
        print("first snapshot saved")
        return "first"
    changes = diff(json.loads(last["summary"]), new)
    severity = top_severity(changes)
    if severity is None:
        print("no change")
        return "nochange"
    message = build_message(label, changes, lang)
    if not grounded(message, changes):
        return ops_alert(db, parcel)
    # The model chooses the next action. The alert itself is always sent (see decide.py).
    d = decide(changes, severity, has_pending(new))
    print(f"decision ({d['source']}): {d['action']} - {d['reason']}")
    db.execute("UPDATE parcels SET watch_closely=? WHERE id=?", (1 if d["recheck"] else 0, parcel["id"]))
    db.commit()
    try:
        alert(db, parcel, severity, json.dumps(changes), message, json.dumps(d, ensure_ascii=False))
    except Exception as e:
        # Delivery failed: forget this snapshot so the next run sees the change again and retries.
        db.execute("DELETE FROM snapshots WHERE id=?", (snap_id,))
        db.commit()
        print("alert NOT delivered, will retry on the next check:", e)
        return "send-failed"
    return f"alert:{severity}"


def run_all(scenario="before", only_closely=False):
    db = conn()
    query = "SELECT * FROM parcels" + (" WHERE watch_closely=1" if only_closely else "")
    for parcel in db.execute(query).fetchall():
        check_parcel(db, parcel, scenario)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="run one check of every parcel")
    ap.add_argument("--scenario", default="before", help="test page to read when SOURCE=fixture")
    ap.add_argument("--closely", action="store_true", help="with --once: only parcels that have a pending mutation")
    ap.add_argument("--schedule", action="store_true", help="run the daily scheduler")
    args = ap.parse_args()
    if args.schedule:
        from apscheduler.schedulers.blocking import BlockingScheduler
        hour = int(os.environ.get("CHECK_HOUR", "7"))
        s = BlockingScheduler(timezone="Asia/Kolkata")
        s.add_job(run_all, "cron", hour=hour)  # every parcel, once a day
        s.add_job(run_all, "cron", hour=(hour + 12) % 24, kwargs={"only_closely": True})
        print("scheduler running, press Ctrl+C to stop")
        s.start()
    else:
        run_all(args.scenario, only_closely=args.closely)
