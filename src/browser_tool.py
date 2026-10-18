"""Browserbase access. Imports are lazy so tests and dev mode need no browser packages."""
import json
import os
import time
from pathlib import Path


class NeedsHuman(Exception):
    """A CAPTCHA or OTP appeared. Stop and ask the user. Never solve it."""


CAPTCHA_HINTS = ("captcha", "recaptcha", "hcaptcha", "enter the code shown")


def check_captcha(html):
    lowered = html.lower()
    if any(h in lowered for h in CAPTCHA_HINTS):
        raise NeedsHuman("CAPTCHA detected, check paused")


class BudgetStop(Exception):
    """Daily Browserbase session cap reached. Protects the free allowance from runaway loops."""


def _use_budget():
    """Count today's sessions in data/bb_usage.json. Default cap 20 a day, change with BB_MAX_SESSIONS_PER_DAY."""
    cap = int(os.environ.get("BB_MAX_SESSIONS_PER_DAY", "20"))
    path = Path(os.environ.get("WATCH_DB", "data/watch.db")).parent / "bb_usage.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    today = time.strftime("%Y-%m-%d")
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError):
        data = {}
    if data.get("day") != today:
        data = {"day": today, "count": 0}
    if data["count"] >= cap:
        raise BudgetStop(f"Browserbase daily cap of {cap} sessions reached, check skipped")
    data["count"] += 1
    path.write_text(json.dumps(data))


def with_page(fn, timeout_s=120):
    """Open a Browserbase session in ap-southeast-1, call fn(page), return its result.
    Confirm parameter names against the current Browserbase docs before relying on them."""
    from browserbase import Browserbase
    from playwright.sync_api import sync_playwright

    _use_budget()
    bb = Browserbase(api_key=os.environ["BROWSERBASE_API_KEY"])
    session = bb.sessions.create(
        project_id=os.environ["BROWSERBASE_PROJECT_ID"],
        region="ap-southeast-1",
        timeout=timeout_s,
        # Keeps the "no CAPTCHA bypass" promise true. Check the exact setting name in the docs.
        browser_settings={"solve_captchas": False},
    )
    print("browserbase session:", session.id, "(open it in the dashboard replay)")
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(session.connect_url)
        try:
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else context.new_page()
            return fn(page)
        finally:
            browser.close()
            try:  # ask Browserbase to end the session now so it stops counting
                bb.sessions.update(session.id, project_id=os.environ["BROWSERBASE_PROJECT_ID"], status="REQUEST_RELEASE")
            except Exception:
                pass  # the 2 minute timeout still ends it


def fetch_html(url, timeout_ms=20000):
    def run(page):
        page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        page.wait_for_timeout(3000)  # lets the session replay record the page before we close
        try:  # screenshot as backup evidence next to the replay
            ev = Path(os.environ.get("WATCH_DB", "data/watch.db")).parent / "evidence"
            ev.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(ev / (time.strftime("%Y%m%d-%H%M%S") + ".png")))
        except Exception:
            pass
        return page.content()

    html = with_page(run)
    check_captcha(html)
    return html
