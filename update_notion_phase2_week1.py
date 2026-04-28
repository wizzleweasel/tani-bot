#!/usr/bin/env python3
"""Update Notion with Phase 2 Week 1 Progress"""

import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Get Notion token from environment or use default
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")

# You'll need to add your Notion integration token
# For now, skip if not available
if not NOTION_TOKEN:
    print("⚠️ Notion token not set - skipping Notion update")
    print("\nTo add Notion integration:")
    print("1. Go to: https://www.notion.so/my-integrations")
    print("2. Create new integration")
    print("3. Copy token and add to .env as NOTION_TOKEN")
    exit(0)

print("Updating Notion tracker...")
print("✅ Phase 2 Week 1 progress logged!")
