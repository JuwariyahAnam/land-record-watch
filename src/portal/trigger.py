"""Tell the agent that the record changed, so it checks now instead of waiting for the schedule.

Needs two settings on the registry host (Render): GITHUB_DISPATCH_TOKEN (a fine-grained token with only
Actions read and write on this repository) and GITHUB_REPO (owner/name). It starts the workflow with GitHub's
"run workflow" call (the same as the Run workflow button), which that token permission covers. Without them nothing happens.
The ping is sent about 20 seconds after the LAST change, so a burst of edits starts one check.
The agent still opens the record itself and decides what to say; this only wakes it up.
A failed ping never affects the registry page: the scheduled check is the backup."""
import os
import threading

import requests

DELAY = 20.0
_timer = None
_lock = threading.Lock()


def configured():
    return bool(os.environ.get("GITHUB_DISPATCH_TOKEN") and os.environ.get("GITHUB_REPO"))


def _send():
    try:
        r = requests.post(
            f"https://api.github.com/repos/{os.environ['GITHUB_REPO']}/actions/workflows/"
            f"{os.environ.get('GITHUB_WORKFLOW_FILE', 'check.yml')}/dispatches",
            headers={"Authorization": f"Bearer {os.environ['GITHUB_DISPATCH_TOKEN']}",
                     "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"},
            json={"ref": os.environ.get("GITHUB_BRANCH", "main")}, timeout=15)
        print("agent ping:", r.status_code, "" if r.status_code == 204 else r.text[:200], flush=True)
    except Exception as e:  # never include the token
        print("agent ping failed:", type(e).__name__, flush=True)


def ping_agent(delay=None):
    """Schedule one ping; a newer change replaces the pending one."""
    global _timer
    if not configured():
        return False
    with _lock:
        if _timer is not None:
            _timer.cancel()
        _timer = threading.Timer(DELAY if delay is None else delay, _send)
        _timer.daemon = True
        _timer.start()
    return True
