#!/usr/bin/env python3
"""Send HF rebuild status"""

import sys
sys.path.insert(0, '/mnt/data/openclaw/workspace/tani-bot/src')

from integrations.telegram_bot import TaniBotTelegram
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8693067374:AAEGnQrRfIXMvWf7wwhn8ELo_IiaOcBNKS0")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8689301832")

bot = TaniBotTelegram(TOKEN)

print("Sending rebuild update...")
message = (
    "HF SPACES REBUILD TRIGGERED!\n\n"
    "Issue: Old code still deployed\n"
    "Fix: Triggered rebuild\n\n"
    "Code is correct:\n"
    "✅ No API input field\n"
    "✅ Loads from env variable\n"
    "✅ Committed to GitHub\n\n"
    "Wait 2-3 minutes for rebuild.\n\n"
    "Check: https://huggingface.co/spaces/baguswicak/tani-bot"
)

result = bot.send_message(chat_id=CHAT_ID, text=message)
print("Update sent!" if result.get('ok') else f"Error: {result}")
