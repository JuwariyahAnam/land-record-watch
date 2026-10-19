"""Create the watched parcel from settings if the database is empty. Used by the scheduled check, because
a fresh runner has no database yet. Needs PARCEL_CHAT_ID and PARCEL_SOURCE_REF (the registry watch link)."""
import os
import time

from dotenv import load_dotenv

load_dotenv()
from .db import conn

if __name__ == "__main__":
    db = conn()
    if db.execute("SELECT COUNT(*) FROM parcels").fetchone()[0]:
        print("parcel already exists")
        raise SystemExit(0)
    chat, ref = os.environ.get("PARCEL_CHAT_ID", "").strip(), os.environ.get("PARCEL_SOURCE_REF", "").strip()
    if not chat or not ref:
        raise SystemExit("set PARCEL_CHAT_ID and PARCEL_SOURCE_REF")
    db.execute("""INSERT INTO parcels(label, district, taluk, hobli, village, survey_no, surnoc, hissa, language,
                  chat_id, own_land_confirmed_at, source_ref) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
               (os.environ.get("PARCEL_LABEL", "My demo land"), "demo-district", "demo-taluk", "demo-hobli",
                "demo-village", "101", "*", "1", os.environ.get("PARCEL_LANGUAGE", "en"), chat, time.time(), ref))
    db.commit()
    print("parcel added")
