import os
import time

import pytest

os.environ["DEV_NO_BROWSER"] = "1"
os.environ["DRY_RUN"] = "1"
os.environ["SOURCE"] = "fixture"
os.environ["RETRY_DELAY"] = "0"


@pytest.fixture
def db(tmp_path, monkeypatch):
    monkeypatch.setenv("WATCH_DB", str(tmp_path / "t.db"))
    from src.db import conn
    c = conn()
    c.execute("""INSERT INTO parcels(label, district, taluk, hobli, village, survey_no, surnoc, hissa,
                 language, chat_id, own_land_confirmed_at)
                 VALUES ('Test plot','D','T','H','V','1','1','1','kn','123',?)""", (time.time(),))
    c.commit()
    return c


@pytest.fixture
def parcel(db):
    return db.execute("SELECT * FROM parcels").fetchone()
