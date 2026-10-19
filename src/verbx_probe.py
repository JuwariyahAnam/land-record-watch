"""Find how VerbX wants the language written. Costs about one rupee in total at most.
  python -m src.verbx_probe
A good Kannada answer is tens of kilobytes; the broken one was about 6 KB."""
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()
BASE = os.environ.get("VERBX_BASE", "https://api.verbxeco.com")
PATH = os.environ.get("VERBX_TTS_PATH", "/v1/tts")
KN = "ನಿಮ್ಮ ಜಮೀನಿನ ದಾಖಲೆಯಲ್ಲಿ ಬದಲಾವಣೆ ಕಂಡುಬಂದಿದೆ."
STYLES = {"short": "kn", "locale": "kn-IN", "name": "Kannada"}

if __name__ == "__main__":
    key = os.environ.get("VERBX_API_KEY", "")
    if not key.startswith("vx_"):
        raise SystemExit("put your key in .env as VERBX_API_KEY=vx_...")
    best = None
    for style, value in STYLES.items():
        body = {"text": KN, "options": {"language": value, "format": "wav"}}
        try:
            r = requests.post(BASE + PATH, json=body, headers={"x-api-key": key}, timeout=90)
        except requests.RequestException as e:
            print(f"{style} ({value}): network error {type(e).__name__}")
            continue
        if r.ok:
            import base64
            data = r.json().get("audio_b64") if "json" in r.headers.get("content-type", "") else None
            size = len(base64.b64decode(data)) if data else len(r.content)
            print(f"{style} ({value}): HTTP 200, audio {size} bytes")
            if best is None or size > best[1]:
                best = (style, size)
        else:
            print(f"{style} ({value}): HTTP {r.status_code} {r.text[:200]}")
        time.sleep(1)
    if best:
        print(f"\nBest: VERBX_LANG_STYLE={best[0]}  (add this line to .env)")
    else:
        print("\nNone worked. Send me this output.")
