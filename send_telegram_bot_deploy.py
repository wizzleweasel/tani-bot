#!/usr/bin/env python3
"""Send bot deployment status"""

import sys
sys.path.insert(0, '/mnt/data/openclaw/workspace/tani-bot/src')

from integrations.telegram_bot import TaniBotTelegram
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8693067374:AAEGnQrRfIXMvWf7wwhn8ELo_IiaOcBNKS0")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8689301832")

bot = TaniBotTelegram(TOKEN)

print("Sending deployment update...")
message = """🤖 ASSISTANT BOT DEPLOYED!

✅ Files uploaded to HF Spaces

🔗 Space:
https://huggingface.co/spaces/baguswicak/usual-bot

⚙️ NEXT STEPS (You do this):

1. Go to Space Settings
2. Click "Repository secrets"
3. Add these secrets:
   - BOT_TOKEN = 8676588212:AAGs9wKmvdf4zfdHPFqwua5CXMA_9o7E1Nw
   - CHAT_ID = 8689301832

4. Wait 3-5 min for build

📱 Bot: @usualclaw_bot

Once built, bot will auto-respond!"""

result = bot.send_message(chat_id=CHAT_ID, text=message)
print("Update sent!" if result.get('ok') else f"Error: {result}")
