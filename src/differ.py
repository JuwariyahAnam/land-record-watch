import hashlib
import json


def _h(text):
    return hashlib.sha256(text.strip().lower().encode()).hexdigest()[:16]


def summarize(rec):
    """Safe summary: owner names become hashes and are never stored."""
    return {
        "owners": sorted(_h(o) for o in rec.owners),
        "extent": rec.extent,
        "mutations": sorted([m["id"], m["date"], m["status"]] for m in rec.mutations),
    }


def fingerprint(summary):
    return _h(json.dumps(summary, sort_keys=True))


def has_pending(summary):
    return any(m[2].strip().lower().startswith("pend") for m in summary["mutations"])


def diff(old, new):
    changes = []
    if old["owners"] != new["owners"]:
        changes.append({"type": "owner_changed"})
    if old["extent"] != new["extent"]:
        changes.append({"type": "extent_changed", "old": old["extent"], "new": new["extent"]})
    old_m = {m[0]: m for m in old["mutations"]}
    for mid, date, status in new["mutations"]:
        if mid not in old_m:
            changes.append({"type": "new_mutation", "id": mid, "date": date, "status": status})
        elif old_m[mid][2] != status:
            changes.append({"type": "mutation_status_changed", "id": mid,
                            "old": old_m[mid][2], "new": status})
    return changes


ORDER = ["critical", "high", "medium"]
SEVERITY = {"owner_changed": "critical", "new_mutation": "high",
            "extent_changed": "high", "mutation_status_changed": "medium"}


def top_severity(changes):
    found = {SEVERITY[c["type"]] for c in changes}
    return next((s for s in ORDER if s in found), None)
