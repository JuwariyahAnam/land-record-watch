"""Passwords, CSRF tokens, input checks and the app secret. Standard library only."""
import hashlib
import hmac
import os
import re
import secrets
from pathlib import Path

_DUMMY = None


def secret_key():
    """Signing key for sessions. Set PORTAL_SECRET_KEY on a server. Locally it is created once in data/."""
    env = os.environ.get("PORTAL_SECRET_KEY")
    if env:
        return env
    path = Path(os.environ.get("PORTAL_DB", "data/portal.db")).parent / "portal_secret.key"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(secrets.token_hex(32))
        try:
            path.chmod(0o600)
        except OSError:
            pass
    return path.read_text().strip()


def hash_password(password):
    salt = os.urandom(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    return f"scrypt${salt.hex()}${digest.hex()}"


def verify_password(password, stored):
    try:
        _, salt, digest = stored.split("$")
        check = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=2 ** 14, r=8, p=1, dklen=32)
        return hmac.compare_digest(check.hex(), digest)
    except (ValueError, TypeError):
        return False


def burn_time(password):
    """Same work for unknown emails, so response time does not reveal which emails exist."""
    global _DUMMY
    if _DUMMY is None:
        _DUMMY = hash_password("dummy-password-for-timing")
    verify_password(password, _DUMMY)


def new_token():
    return secrets.token_urlsafe(16)


def same(a, b):
    return hmac.compare_digest(str(a), str(b))


EMAIL = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,120}\.[^@\s]{2,20}$")
EXTENT = re.compile(r"^\d{1,3}-\d{1,2}$")          # acres-guntas, for example 2-10
SURVEY = re.compile(r"^[A-Za-z0-9/\-]{1,20}$")
PLACE = re.compile(r"^[A-Za-z0-9 .'\-]{2,60}$")


def clean(text, maxlen=80):
    """Trim, drop control characters, cap the length."""
    text = "".join(ch for ch in (text or "") if ch.isprintable()).strip()
    return text[:maxlen]


def password_problem(password, email="", name=""):
    if len(password) < 10:
        return "Use at least 10 characters."
    if not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
        return "Use both letters and numbers."
    local = email.split("@")[0].lower()
    if local and len(local) >= 4 and local in password.lower():
        return "Do not put your email name in your password."
    return None


def mask_name(name):
    """T*** O*** : enough to recognise, not enough to identify."""
    return " ".join((w[0] + "***") for w in name.split() if w) or "***"


def owner_ref(name):
    """Short code that changes when the owner changes, so a transfer is detectable even if initials match."""
    key = secret_key().encode()
    return hmac.new(key, name.strip().lower().encode(), hashlib.sha256).hexdigest()[:4]
