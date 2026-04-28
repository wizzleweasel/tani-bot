#!/usr/bin/env python3
"""Update Notion Directly - Phase 2 Week 1 Progress"""

import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# You need to add Notion integration token to .env
# Get it from: https://www.notion.so/my-integrations
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
DATABASE_ID = "350dbe4f78a681e1812ecc3e59cdab7a"

if not NOTION_TOKEN:
    print("⚠️ NOTION_TOKEN not found in .env")
    print("\n📋 Setup Instructions:")
    print("1. Go to: https://www.notion.so/my-integrations")
    print("2. Click '+ New integration'")
    print("3. Name it: TaniBot")
    print("4. Copy the token (starts with 'secret_...')")
    print("5. Add to .env file:")
    print("   NOTION_TOKEN=secret_xxxxx")
    print("6. Share your Notion database with the integration")
    print("\nFor now, I'll create a local Notion update file...")
    
    # Create a file with the update content
    with open('/mnt/data/openclaw/workspace/.openclaw/workspace/notion_update_draft.md', 'w') as f:
        f.write("""# Phase 2 Week 1: Supabase + RAG Migration ✅

**Date:** 2026-04-28  
**Status:** Complete  
**GitHub:** https://github.com/wizzleweasel/tani-bot/commit/f342d03

## Completed Tasks

### Supabase Setup ✅
- [x] Created Supabase project (cdlybfnpphzzphwathjx)
- [x] Enabled pgvector extension
- [x] Created 12 tables (weather, crops, fields, documents, etc.)
- [x] Deployed 3 RPC functions for semantic search
- [x] Fixed embedding dimension (384 for all-MiniLM-L6-v2)

### RAG Pipeline ✅
- [x] Document ingestion pipeline created
- [x] 3 agricultural documents indexed:
  - Rice Cultivation Guide - Indonesia
  - Corn Farming Best Practices
  - Cassava Cultivation Guide
- [x] Semantic search working via pgvector
- [x] RAG retriever module created

### Integration ✅
- [x] Supabase credentials saved to .env
- [x] Migration verified
- [x] GitHub updated (commit f342d03)
- [x] Mempalace context saved

## Metrics
- **Tables Created:** 12
- **RPC Functions:** 3
- **Documents Indexed:** 3
- **Embedding Model:** all-MiniLM-L6-v2 (384-dim)
- **Time Spent:** ~2 hours

## Next Steps (Week 2)
- [ ] User authentication system
- [ ] Session management
- [ ] Save consultation history per user
- [ ] Personalized recommendations

## Challenges & Solutions
- **Challenge:** Supabase API doesn't support raw SQL execution
  - **Solution:** Manual migration via SQL Editor
- **Challenge:** Embedding dimension mismatch (1536 vs 384)
  - **Solution:** Updated schema to use 384-dim
- **Challenge:** GitHub secret scanning
  - **Solution:** Removed credentials from code, used .env

---
*Updated: 2026-04-28 16:58 UTC*
""")
    
    print("\n✅ Created: notion_update_draft.md")
    print("   You can manually copy this to Notion!")
    exit(0)

print("Updating Notion directly...")

# Create page in Notion
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

page_data = {
    "parent": {
        "database_id": DATABASE_ID
    },
    "properties": {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": "Phase 2 Week 1: Supabase + RAG ✅"
                    }
                }
            ]
        },
        "Status": {
            "select": {
                "name": "Complete"
            }
        }
    },
    "children": [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Completed Tasks"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Supabase project created & migrated"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "12 tables with pgvector (384-dim)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "3 agricultural documents indexed"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "RAG pipeline working"}}]
            }
        }
    ]
}

try:
    response = requests.post(
        f"https://api.notion.com/v1/pages",
        headers=headers,
        json=page_data,
        timeout=30
    )
    
    if response.status_code == 200:
        print("✅ Notion page created!")
        page_id = response.json().get('id', 'N/A')
        print(f"   Page ID: {page_id}")
        print(f"   URL: https://notion.so/{page_id.replace('-', '')}")
    else:
        print(f"❌ Status: {response.status_code}")
        print(f"   {response.text[:300]}")
        
except Exception as e:
    print(f"❌ Error: {e}")
