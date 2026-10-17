"""Browserbase access. Imports are lazy so tests and dev mode need no browser packages."""
import os


class NeedsHuman(Exception):
    """A CAPTCHA or OTP appeared. Stop and ask the user. Never solve it."""


CAPTCHA_HINTS = ("captcha", "recaptcha", "hcaptcha", "enter the code shown")


def check_captcha(html):
    lowered = html.lower()
    if any(h in lowered for h in CAPTCHA_HINTS):
        raise NeedsHuman("CAPTCHA detected, check paused")


def with_page(fn, timeout_s=120):
    """Open a Browserbase session in ap-southeast-1, call fn(page), return its result.
    Confirm parameter names against the current Browserbase docs before relying on them."""
    from browserbase import Browserbase
    from playwright.sync_api import sync_playwright

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


def fetch_html(url, timeout_ms=20000):
    def run(page):
        page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        return page.content()

    html = with_page(run)
    check_captcha(html)
    return html
