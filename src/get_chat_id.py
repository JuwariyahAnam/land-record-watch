"""Message your bot once in Telegram, then run: python -m src.get_chat_id"""
import os

import requests
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/getUpdates"
    data = requests.get(url, timeout=20).json()
    seen = {u["message"]["chat"]["id"] for u in data.get("result", []) if "message" in u}
    print("chat ids:", sorted(seen) or "none yet, send your bot a message first")
