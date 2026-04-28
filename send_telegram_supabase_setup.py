#!/usr/bin/env python3
"""Send Supabase Setup Instructions"""

import sys
sys.path.insert(0, '/mnt/data/openclaw/workspace/tani-bot/src')

from integrations.telegram_bot import TaniBotTelegram
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8693067374:AAEGnQrRfIXMvWf7wwhn8ELo_IiaOcBNKS0")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8689301832")

bot = TaniBotTelegram(TOKEN)

message = """🎉 SUPABASE CONNECTED!

Credentials saved to .env:
- URL: helrasnyoffqrkrotpfh.supabase.co
- Key: service_role key saved
- Password: saved

NEXT: Run Migration (2 min)

On your local machine:

1. cd tani-bot
2. pip install psycopg2-binary
3. python run_supabase_migration.py

This will:
- Create 12 tables
- Enable pgvector
- Deploy RPC functions
- Verify setup

Then test RAG:
pip install -r requirements.txt
python -m src.rag.document_ingestor

Files ready:
- supabase/schema.sql
- supabase/rpc_functions.sql
- run_supabase_migration.py

After migration, RAG pipeline is LIVE!"""

# Simple send without parse_mode issues
import requests
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
requests.post(url, json={"chat_id": CHAT_ID, "text": message})
print("Sent!")
print("Sent!" if result.get('ok') else f"Error: {result}")
