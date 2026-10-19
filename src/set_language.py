"""Change the alert language of a parcel.   python -m src.set_language en     (or kn, hi)
Optional second argument: the parcel label, if you watch more than one."""
import sys

from dotenv import load_dotenv

load_dotenv()
from .db import conn

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("kn", "hi", "en"):
        raise SystemExit("usage: python -m src.set_language kn|hi|en [parcel label]")
    lang = sys.argv[1]
    db = conn()
    if len(sys.argv) > 2:
        cur = db.execute("UPDATE parcels SET language=? WHERE label=?", (lang, sys.argv[2]))
    else:
        cur = db.execute("UPDATE parcels SET language=?", (lang,))
    db.commit()
    print(f"language set to {lang} for {cur.rowcount} parcel(s)")
