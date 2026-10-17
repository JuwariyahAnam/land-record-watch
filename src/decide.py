"""The agent's decision step.

After a change is detected, the model chooses the next action. Rules stay in charge of safety:
- a critical or high change is ALWAYS alerted, the model cannot suppress it
- the model only sees change types, ids, dates, statuses and extents (never owner names)
- the model never writes the alert text, so nothing ungrounded reaches the user
- if the model is missing, slow, or answers badly, the rules decide
"""
import json
import os

from .llm import complete, configured

ACTIONS = {"alert", "alert_and_recheck"}

SYSTEM = (
    "You are the decision step of a land-record monitoring agent. A change was found in a public "
    "land record. Reply with JSON only: "
    '{"action": "alert" or "alert_and_recheck", "reason": "<one short sentence>"}. '
    "An alert is always sent. Choose alert_and_recheck when a mutation is still pending or the "
    "change may still be in progress, so the record should be checked again this evening. "
    "Choose alert when the change looks settled. Use only the facts you are given."
)


def rule_decision(pending):
    action = "alert_and_recheck" if pending else "alert"
    return {"action": action, "recheck": pending, "source": "rules",
            "reason": "pending mutation, so check again this evening" if pending
            else "no pending mutation"}


def _parse(raw):
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON in model reply")
    data = json.loads(raw[start:end + 1])
    if data.get("action") not in ACTIONS:
        raise ValueError(f"unknown action {data.get('action')!r}")
    return data


def decide(changes, severity, pending):
    base = rule_decision(pending)
    if os.environ.get("LLM_ENABLED", "1") != "1" or not configured():
        return base
    facts = {"severity": severity, "mutation_pending": pending, "changes": changes}
    try:
        data = _parse(complete(SYSTEM, json.dumps(facts, ensure_ascii=False)))
        return {"action": data["action"], "recheck": data["action"] == "alert_and_recheck",
                "source": "llm", "reason": str(data.get("reason", ""))[:200]}
    except Exception as e:
        print("model decision failed, using rules:", e)
        return base
