import os
import sqlite3
from pathlib import Path


def conn():
    path = Path(os.environ.get("WATCH_DB", "data/watch.db"))
    path.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(path)
    c.row_factory = sqlite3.Row
    c.executescript("""
    CREATE TABLE IF NOT EXISTS parcels(
        id INTEGER PRIMARY KEY, label TEXT, district TEXT, taluk TEXT, hobli TEXT,
        village TEXT, survey_no TEXT, surnoc TEXT, hissa TEXT,
        language TEXT DEFAULT 'kn', chat_id TEXT,
        own_land_confirmed_at REAL,
        watch_closely INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS snapshots(
        id INTEGER PRIMARY KEY, parcel_id INTEGER, fetched_at REAL,
        source TEXT, fingerprint TEXT, summary TEXT);
    CREATE TABLE IF NOT EXISTS alerts(
        id INTEGER PRIMARY KEY, parcel_id INTEGER, created_at REAL,
        severity TEXT, diff TEXT, message TEXT, decision TEXT);
    """)
    try:
        c.execute("ALTER TABLE alerts ADD COLUMN decision TEXT")
    except sqlite3.OperationalError:
        pass  # column already exists
    return c
