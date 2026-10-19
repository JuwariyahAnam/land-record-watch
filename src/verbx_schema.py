"""Print what VerbX's /v1/tts accepts (fields, allowed values) and the voice list. Free lookups only.
  python -m src.verbx_schema"""
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
BASE = os.environ.get("VERBX_BASE", "https://api.verbxeco.com")


def resolve(spec, node, depth=0):
    """Follow $ref links so the whole field list shows in one place."""
    if depth > 4 or not isinstance(node, dict):
        return node
    if "$ref" in node:
        name = node["$ref"].split("/")[-1]
        return {"<" + name + ">": resolve(spec, spec["components"]["schemas"].get(name, {}), depth + 1)}
    return {k: resolve(spec, v, depth + 1) if isinstance(v, (dict, list)) else v for k, v in node.items()} \
        if isinstance(node, dict) else node


if __name__ == "__main__":
    key = os.environ.get("VERBX_API_KEY", "")
    spec = requests.get(BASE + "/openapi.json", headers={"x-api-key": key}, timeout=30).json()
    for name in ("TTSRequestBody",):
        print(name, json.dumps(resolve(spec, spec["components"]["schemas"].get(name, {})), ensure_ascii=False)[:2500])
    print()
    r = requests.get(BASE + "/v1/tts/voices", headers={"x-api-key": key}, timeout=30)
    print("voices: HTTP", r.status_code, r.text[:1800])
