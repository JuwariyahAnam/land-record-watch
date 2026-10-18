"""Tiny read-only web server: serves web/app.html and /api/state from the real database.
Run:  python -m src.server   then open http://localhost:8000"""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from src import db as database
from src.explain import build_message, ops_message

WEB = Path(__file__).resolve().parent.parent / "web"
LANGS = ("en", "kn", "hi")


def state():
    c = database.conn()
    out = []
    for p in c.execute("SELECT * FROM parcels ORDER BY id"):
        snap = c.execute("SELECT * FROM snapshots WHERE parcel_id=? ORDER BY id DESC LIMIT 1", (p["id"],)).fetchone()
        alerts = []
        for a in c.execute("SELECT * FROM alerts WHERE parcel_id=? ORDER BY id DESC LIMIT 20", (p["id"],)):
            changes = json.loads(a["diff"] or "[]")
            if a["severity"] == "ops":
                msgs = {l: ops_message(p["label"], l) for l in LANGS}
            else:
                msgs = {l: build_message(p["label"], changes, l) for l in LANGS}
            alerts.append({"id": a["id"], "at": a["created_at"], "severity": a["severity"],
                           "changes": changes, "messages": msgs, "decision": a["decision"] or ""})
        out.append({"id": p["id"], "label": p["label"], "language": p["language"],
                    "place": ", ".join(x for x in (p["village"], p["hobli"], p["taluk"], p["district"]) if x),
                    "survey": "/".join(x for x in (p["survey_no"], p["surnoc"], p["hissa"]) if x),
                    "confirmed_own": bool(p["own_land_confirmed_at"]),
                    "watch_closely": bool(p["watch_closely"]),
                    "last_check": snap["fetched_at"] if snap else None,
                    "source": snap["source"] if snap else None,
                    "alerts": alerts})
    return {"parcels": out, "live": os.environ.get("SOURCE", "fixture") != "fixture"}


class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/api/state":
            return self._send(200, json.dumps(state()).encode(), "application/json")
        if path in ("/", "/index.html"):
            return self._send(200, (WEB / "app.html").read_bytes(), "text/html; charset=utf-8")
        self._send(404, b"not found", "text/plain")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Land Record Watch UI: http://localhost:{port}")
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
