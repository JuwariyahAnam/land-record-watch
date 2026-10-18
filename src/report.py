"""Writes docs/test-evidence.md: input, expected result, actual result for each scenario.
Runs against the local test pages in dev mode (no Browserbase, no Telegram, no VerbX).
For the submission, re-run the same scenarios with DEV_NO_BROWSER=0 so each one goes
through a real Browserbase session, and attach the replay links as evidence."""
import json
import os
import tempfile
import time
from pathlib import Path

os.environ.setdefault("DEV_NO_BROWSER", "1")
os.environ.setdefault("DRY_RUN", "1")
os.environ.setdefault("SOURCE", "fixture")
os.environ.setdefault("RETRY_DELAY", "0")
os.environ["WATCH_DB"] = str(Path(tempfile.mkdtemp()) / "report.db")

from .db import conn
from .main import check_parcel

# (name, pages read in order, expected result of the last one)
CASES = [
    ("1 Unchanged record", ["before", "before"], "nochange"),
    ("2 New mutation entry", ["before", "mutation"], "alert:high"),
    ("3 Mutation approved", ["before", "mutation", "approved"], "alert:medium"),
    ("4 Owner changed", ["before", "owner"], "alert:critical"),
    ("5 Extent changed", ["before", "extent"], "alert:high"),
    ("6 Layout changed", ["before", "layout"], "ops"),
    ("7 CAPTCHA shown", ["before", "captcha"], "ops"),
    ("8 Page missing", ["before", "does-not-exist"], "ops"),
    ("10 Same change twice", ["before", "mutation", "mutation"], "nochange"),
]


def fresh_parcel(confirmed=True):
    os.environ["WATCH_DB"] = str(Path(tempfile.mkdtemp()) / "c.db")
    db = conn()
    db.execute("""INSERT INTO parcels(label, district, taluk, hobli, village, survey_no, surnoc, hissa,
                  language, chat_id, own_land_confirmed_at)
                  VALUES ('Test plot','D','T','H','V','1','1','1','kn','0',?)""",
               (time.time() if confirmed else None,))
    db.commit()
    return db, db.execute("SELECT * FROM parcels").fetchone()


def main():
    rows = ["# Test evidence", "",
            "## Automated runs (local, labelled test pages)", "", "No Browserbase, Telegram or VerbX calls in this section; see the live runs below.", "",
            "| Scenario | Pages read in order | Expected | Actual | Result |",
            "|---|---|---|---|---|"]
    for name, pages, expected in CASES:
        db, parcel = fresh_parcel()
        actual = None
        for page in pages:
            actual = check_parcel(db, parcel, page)
        rows.append(f"| {name} | {' then '.join(pages)} | {expected} | {actual} | "
                    f"{'PASS' if actual == expected else 'FAIL'} |")
    db, parcel = fresh_parcel(confirmed=False)
    actual = check_parcel(db, parcel, "before")
    rows.append(f"| 9 Parcel not confirmed as own | before | skipped | {actual} | "
                f"{'PASS' if actual == 'skipped' else 'FAIL'} |")
    start = rows.index("|---|---|---|---|---|") + 1
    rows[start:] = sorted(rows[start:], key=lambda r: int(r.split()[1]))
    live = Path("docs/live-runs.json")
    if live.exists():
        rows += ["", "## Live runs through Browserbase (18 Oct 2026, region ap-southeast-1)", "",
                 "Each row is one real cloud-browser session reading the labelled test pages on GitHub Pages.",
                 "Replays are in the Browserbase dashboard (private link, so screenshots are attached to the submission).", "",
                 "| Scenario | Page | Expected | Actual | Browserbase session |", "|---|---|---|---|---|"]
        for r in json.loads(live.read_text(encoding="utf-8")):
            rows.append(f"| {r['scenario']} | {r['page']} | {r['expected']} | {r['actual']} | `{r['session']}` |")
    out = Path("docs/test-evidence.md")
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print("\n".join(rows))


if __name__ == "__main__":
    main()
