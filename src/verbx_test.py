"""Make one short sample in each language and save it, so you can listen. Costs about one rupee in total.
  python -m src.verbx_test      then open the files in data\\voice-test\\"""
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
from .verbx_client import speak

SAMPLES = {
    "kn": "ನಿಮ್ಮ ಜಮೀನಿನ ದಾಖಲೆಯಲ್ಲಿ ಬದಲಾವಣೆ ಕಂಡುಬಂದಿದೆ.",
    "hi": "आपकी ज़मीन के रिकॉर्ड में बदलाव मिला है।",
    "en": "A change was found in your land record.",
}

if __name__ == "__main__":
    out = Path("data/voice-test")
    out.mkdir(parents=True, exist_ok=True)
    for lang, text in SAMPLES.items():
        try:
            audio = speak(text, lang)
        except Exception as e:
            print(f"{lang}: FAILED - {e}")
            continue
        ext = "wav" if audio[:4] == b"RIFF" else "mp3"
        (out / f"{lang}.{ext}").write_bytes(audio)
        print(f"{lang}: saved {len(audio)} bytes -> {out / (lang + '.' + ext)}")
