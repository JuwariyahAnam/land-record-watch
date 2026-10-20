"""Database for the demo registry (separate from the agent's own database)."""
import os
import sqlite3
import time
from pathlib import Path

from . import security

SCHEMA = """
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE COLLATE NOCASE, name TEXT NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('landlord','buyer','registrar')),
  pw_hash TEXT NOT NULL, created_at REAL NOT NULL,
  failed INTEGER NOT NULL DEFAULT 0, locked_until REAL NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS lands(
  id INTEGER PRIMARY KEY, owner_id INTEGER NOT NULL REFERENCES users(id),
  district TEXT NOT NULL COLLATE NOCASE, taluk TEXT NOT NULL COLLATE NOCASE,
  hobli TEXT NOT NULL COLLATE NOCASE, village TEXT NOT NULL COLLATE NOCASE,
  survey_no TEXT NOT NULL COLLATE NOCASE, surnoc TEXT NOT NULL DEFAULT '*',
  hissa TEXT NOT NULL DEFAULT '0' COLLATE NOCASE,
  extent TEXT NOT NULL, owner_name TEXT NOT NULL, alert_language TEXT NOT NULL DEFAULT 'kn',
  public_token TEXT NOT NULL UNIQUE, created_at REAL NOT NULL, updated_at REAL NOT NULL,
  UNIQUE(district, taluk, hobli, village, survey_no, surnoc, hissa));
CREATE TABLE IF NOT EXISTS mutations(
  id INTEGER PRIMARY KEY, land_id INTEGER NOT NULL REFERENCES lands(id), ref TEXT UNIQUE,
  kind TEXT NOT NULL, note TEXT NOT NULL DEFAULT '', filed_on TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending','Approved','Rejected')),
  filed_by INTEGER NOT NULL REFERENCES users(id), decided_by INTEGER, decided_on TEXT,
  decision_note TEXT NOT NULL DEFAULT '');
CREATE TABLE IF NOT EXISTS events(
  id INTEGER PRIMARY KEY, land_id INTEGER NOT NULL REFERENCES lands(id),
  at REAL NOT NULL, actor TEXT NOT NULL, text TEXT NOT NULL);
"""

LANGUAGES = {"kn": "ಕನ್ನಡ (Kannada)", "hi": "हिन्दी (Hindi)", "en": "English"}
KINDS = ["Sale", "Inheritance", "Partition", "Gift", "Correction"]


def conn():
    path = Path(os.environ.get("PORTAL_DB", "data/portal.db"))
    path.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(path)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    c.executescript(SCHEMA)
    cols = [r["name"] for r in c.execute("PRAGMA table_info(lands)")]
    if "alert_language" not in cols:  # database made before the language setting existed
        c.execute("ALTER TABLE lands ADD COLUMN alert_language TEXT NOT NULL DEFAULT 'kn'")
        c.commit()
    return c


# ---- users
def create_user(c, email, name, role, pw_hash):
    cur = c.execute("INSERT INTO users(email,name,role,pw_hash,created_at) VALUES (?,?,?,?,?)",
                    (email, name, role, pw_hash, time.time()))
    c.commit()
    return cur.lastrowid


def user_by_email(c, email):
    return c.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()


def user_by_id(c, uid):
    return c.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()


def has_registrar(c):
    return c.execute("SELECT 1 FROM users WHERE role='registrar'").fetchone() is not None


# ---- lands
def log(c, land_id, actor, text):
    c.execute("INSERT INTO events(land_id,at,actor,text) VALUES (?,?,?,?)", (land_id, time.time(), actor, text))


def add_land(c, owner, f, token=None):
    now = time.time()
    cur = c.execute("""INSERT INTO lands(owner_id,district,taluk,hobli,village,survey_no,surnoc,hissa,
                       extent,owner_name,public_token,created_at,updated_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (owner["id"], f["district"], f["taluk"], f["hobli"], f["village"], f["survey_no"],
                     f["surnoc"], f["hissa"], f["extent"], f["owner_name"], token or security.new_token(), now, now))
    log(c, cur.lastrowid, owner["name"], f"Land registered, extent {f['extent']}")
    c.commit()
    return cur.lastrowid


def land(c, land_id):
    return c.execute("SELECT * FROM lands WHERE id=?", (land_id,)).fetchone()


def land_by_token(c, token):
    return c.execute("SELECT * FROM lands WHERE public_token=?", (token,)).fetchone()


def lands_of(c, owner_id):
    return c.execute("SELECT * FROM lands WHERE owner_id=? ORDER BY id DESC", (owner_id,)).fetchall()


def search(c, f, limit=20):
    sql, args = "SELECT * FROM lands WHERE district=? AND survey_no=?", [f["district"], f["survey_no"]]
    for key in ("taluk", "hobli", "village", "hissa"):
        if f.get(key):
            sql += f" AND {key}=?"
            args.append(f[key])
    return c.execute(sql + " ORDER BY id LIMIT ?", (*args, limit)).fetchall()


# ---- mutations
def mutations(c, land_id):
    return c.execute("SELECT * FROM mutations WHERE land_id=? ORDER BY id", (land_id,)).fetchall()


def pending_count(c, land_id):
    return c.execute("SELECT COUNT(*) FROM mutations WHERE land_id=? AND status='Pending'", (land_id,)).fetchone()[0]


def file_mutation(c, land_id, user, kind, note, today):
    cur = c.execute("INSERT INTO mutations(land_id,kind,note,filed_on,filed_by) VALUES (?,?,?,?,?)",
                    (land_id, kind, note, today, user["id"]))
    ref = f"MR-{1000 + cur.lastrowid}"
    c.execute("UPDATE mutations SET ref=? WHERE id=?", (ref, cur.lastrowid))
    c.execute("UPDATE lands SET updated_at=? WHERE id=?", (time.time(), land_id))
    log(c, land_id, user["name"], f"Mutation {ref} filed ({kind})")
    c.commit()
    return ref


def decide(c, mutation_id, registrar, decision, note, today):
    m = c.execute("SELECT * FROM mutations WHERE id=? AND status='Pending'", (mutation_id,)).fetchone()
    if m is None:
        return None
    status = "Approved" if decision == "approve" else "Rejected"
    c.execute("UPDATE mutations SET status=?, decided_by=?, decided_on=?, decision_note=? WHERE id=?",
              (status, registrar["id"], today, note, mutation_id))
    c.execute("UPDATE lands SET updated_at=? WHERE id=?", (time.time(), m["land_id"]))
    log(c, m["land_id"], registrar["name"], f"Mutation {m['ref']} {status.lower()}")
    c.commit()
    return m


def pending_queue(c):
    return c.execute("""SELECT m.*, l.district, l.taluk, l.village, l.survey_no, l.hissa
                        FROM mutations m JOIN lands l ON l.id=m.land_id
                        WHERE m.status='Pending' ORDER BY m.id""").fetchall()


def set_extent(c, land_id, registrar, extent):
    old = land(c, land_id)["extent"]
    c.execute("UPDATE lands SET extent=?, updated_at=? WHERE id=?", (extent, time.time(), land_id))
    log(c, land_id, registrar["name"], f"Extent changed from {old} to {extent}")
    c.commit()


def set_language(c, land_id, user, lang):
    if lang not in LANGUAGES:
        raise ValueError("unknown language")
    c.execute("UPDATE lands SET alert_language=? WHERE id=?", (lang, land_id))
    log(c, land_id, user["name"], "Alert language changed to " + lang)
    c.commit()


def set_owner(c, land_id, registrar, name):
    c.execute("UPDATE lands SET owner_name=?, updated_at=? WHERE id=?", (name, time.time(), land_id))
    log(c, land_id, registrar["name"], "Ownership transfer recorded")
    c.commit()


def events(c, land_id):
    return c.execute("SELECT * FROM events WHERE land_id=? ORDER BY id DESC LIMIT 30", (land_id,)).fetchall()


# ---- what a reader is allowed to see
def record_view(c, row):
    muts = mutations(c, row["id"])
    pending = [m for m in muts if m["status"] == "Pending"]
    return {
        "id": row["id"], "district": row["district"], "taluk": row["taluk"], "hobli": row["hobli"],
        "village": row["village"], "survey": "/".join([row["survey_no"], row["surnoc"], row["hissa"]]),
        "extent": row["extent"],
        "owner_display": f"{security.mask_name(row['owner_name'])} (ref {security.owner_ref(row['owner_name'])})",
        "mutations": muts, "pending": len(pending), "updated_at": row["updated_at"],
        "status": "pending" if pending else "clear", "alert_language": row["alert_language"],
    }
