import time

from dotenv import load_dotenv

load_dotenv()
from .db import conn

FIELDS = ["label", "district", "taluk", "hobli", "village", "survey_no", "surnoc", "hissa"]

if __name__ == "__main__":
    print("Only add land that belongs to you or your family. No papers are uploaded.")
    values = {f: input(f"{f}: ").strip() for f in FIELDS}
    lang = input("language (kn, hi, en) [kn]: ").strip() or "kn"
    chat_id = input("telegram chat id: ").strip()
    if input("Is this your own land? type yes: ").strip().lower() != "yes":
        raise SystemExit("not added")
    db = conn()
    db.execute("""INSERT INTO parcels(label, district, taluk, hobli, village, survey_no, surnoc, hissa,
                  language, chat_id, own_land_confirmed_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
               (*[values[f] for f in FIELDS], lang, chat_id, time.time()))
    db.commit()
    print("added")
