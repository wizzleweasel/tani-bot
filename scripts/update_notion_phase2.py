#!/usr/bin/env python3
"""
Update Notion with Phase 2 Completion Status
"""

import requests
import json
from datetime import datetime

NOTION_TOKEN = "ntn_43868512784160807145128085128512851285"  # From your integration
DATABASE_ID = "350dbe4f78a681e1812ecc3e59cdab7a"  # TaniBot Project Tracker

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Phase 2 Completion Data
phase2_data = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "Name": {
            "title": [{"text": {"content": "Phase 2: Dataset Development - COMPLETE"}}]
        },
        "Status": {
            "select": {"name": "✅ Complete"}
        },
        "Priority": {
            "select": {"name": "High"}
        },
        "Due Date": {
            "date": {"start": "2026-04-28"}
        }
    },
    "children": [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "🎉 Phase 2 Complete!"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Date: 2026-04-28"}}]}
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "📊 Achievements"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "✅ 3,000 datasets (100% Bahasa Indonesia)"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "✅ Supabase: 3,000/3,000 uploaded"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "✅ Hugging Face: 3 datasets + 1 Space"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "✅ 20 test cases executed"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "✅ 5 critical bugs fixed"}}]}
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "🚀 Next: Phase 3"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "RAG Testing & Production Deployment"}}]}
        }
    ]
}

try:
    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json=phase2_data
    )
    
    if response.status_code in [200, 201]:
        print("✅ Notion updated successfully!")
        print(f"Page URL: {response.json().get('url', 'N/A')}")
    else:
        print(f"⚠️ Notion update failed: {response.status_code}")
        print(response.text[:200])
except Exception as e:
    print(f"❌ Error: {str(e)}")
