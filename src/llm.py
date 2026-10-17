"""One small function that talks to a chat model over HTTP.
It assumes an OpenAI-style /chat/completions endpoint, which many providers offer.
If your provider uses a different request format, change only this file."""
import os

import requests


class LLMUnavailable(Exception):
    """No model configured, so the agent falls back to its rules."""


def configured():
    return all(os.environ.get(k) for k in ("LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL"))


def complete(system, user, timeout=20):
    if not configured():
        raise LLMUnavailable("set LLM_BASE_URL, LLM_API_KEY and LLM_MODEL in .env")
    base = os.environ["LLM_BASE_URL"].rstrip("/")
    r = requests.post(
        f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['LLM_API_KEY']}"},
        json={"model": os.environ["LLM_MODEL"], "temperature": 0,
              "messages": [{"role": "system", "content": system},
                           {"role": "user", "content": user}]},
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
