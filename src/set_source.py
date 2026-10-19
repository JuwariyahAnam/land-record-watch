"""Point your parcel at the demo registry:
  python -m src.set_source https://YOUR-REGISTRY/public/TOKEN [parcel label]
Then set SOURCE=portal and PORTAL_BASE=https://YOUR-REGISTRY in .env"""
import sys

from dotenv import load_dotenv

load_dotenv()
from .db import conn

if __name__ == "__main__":
    if len(sys.argv) < 2 or "/public/" not in sys.argv[1]:
        raise SystemExit(__doc__)
    db = conn()
    if len(sys.argv) > 2:
        cur = db.execute("UPDATE parcels SET source_ref=? WHERE label=?", (sys.argv[1], sys.argv[2]))
    else:
        cur = db.execute("UPDATE parcels SET source_ref=?", (sys.argv[1],))
    db.commit()
    print(f"watch link saved for {cur.rowcount} parcel(s)")
