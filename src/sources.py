import os
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup

from .browser_tool import check_captcha, fetch_html, with_page

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


class LayoutChanged(Exception):
    """The page no longer has the fields we expect."""


@dataclass
class Record:
    owners: list      # as shown on the page, hashed straight away, never stored
    extent: str       # as shown, for example "2-10"
    mutations: list   # [{"id": "...", "date": "...", "status": "..."}]


def parse_fixture(html):
    """Parser for the labelled test pages. The live portal needs its own parser."""
    soup = BeautifulSoup(html, "html.parser")
    owners = [e.get_text(strip=True) for e in soup.select("[data-field=owner]")]
    extent = soup.select_one("[data-field=extent]")
    if not owners or extent is None:
        raise LayoutChanged("expected fields missing")
    muts = []
    for row in soup.select("tr[data-mutation]"):
        date = row.select_one("[data-field=date]")
        status = row.select_one("[data-field=status]")
        if date is None or status is None:
            raise LayoutChanged("mutation row incomplete")
        muts.append({"id": row["data-mutation"], "date": date.get_text(strip=True),
                     "status": status.get_text(strip=True)})
    return Record(owners, extent.get_text(strip=True), muts)


class FixtureSource:
    """Labelled test pages. Say so in the demo and in the README."""
    name = "fixture"

    def __init__(self, scenario="before"):
        self.scenario = scenario

    def fetch(self, parcel):
        if os.environ.get("DEV_NO_BROWSER") == "1":
            html = (FIXTURES / f"parcel-{self.scenario}.html").read_text(encoding="utf-8")
            check_captcha(html)
        else:
            url = f"{os.environ['FIXTURE_BASE']}/parcel-{self.scenario}.html"
            html = fetch_html(url)
        return parse_fixture(html)


class LiveSource:
    """The real portal. Fill this in from your Day 0 notes, and only after the
    organisers confirm that read-only automated checks are acceptable."""
    name = "live"

    def fetch(self, parcel):
        def run(page):
            # 1. page.goto(<RTC and mutation status page>)
            # 2. Fill district, taluk, hobli, village, survey number, surnoc, hissa
            #    from `parcel`, using selectors you noted by hand. Keep them in one dict.
            # 3. Click the view button, wait for the result table.
            # 4. html = page.content(); check_captcha(html)
            # 5. Build and return a Record. Raise LayoutChanged if fields are missing.
            raise NotImplementedError("write the live adapter from your portal notes")

        return with_page(run)


class PortalSource:
    """The demo registry we built. Reads the owner's private watch link for the parcel.
    Only links on the configured PORTAL_BASE are ever opened."""
    name = "portal"

    def fetch(self, parcel):
        url = (parcel["source_ref"] or "").strip()
        base = os.environ.get("PORTAL_BASE", "").rstrip("/")
        if not url or not base or not url.startswith(base + "/public/"):
            raise LayoutChanged("portal link missing, or not on the configured portal")
        if os.environ.get("DEV_NO_BROWSER") == "1":
            import requests
            r = requests.get(url, timeout=20)
            r.raise_for_status()
            html = r.text
            check_captcha(html)
        else:
            html = fetch_html(url)
        return parse_fixture(html)


def get_source(scenario="before"):
    kind = os.environ.get("SOURCE")
    if kind == "live":
        return LiveSource()
    if kind == "portal":
        return PortalSource()
    return FixtureSource(scenario)
