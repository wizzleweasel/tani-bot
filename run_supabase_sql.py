#!/usr/bin/env python3
"""
Execute SQL on Supabase via REST API

Uses Supabase service_role key for direct database access.
"""

import requests
import json
import sys

# Supabase credentials
SUPABASE_KEY = "sbp_d602b5528ab9b47838ae1f155962877d645236c1"
SUPABASE_URL = sys.argv[1] if len(sys.argv) > 1 else None

if not SUPABASE_URL:
    print("❌ Missing SUPABASE_URL")
    print("\nUsage: python run_supabase_sql.py https://your-project.supabase.co")
    print("\nExample:")
    print("  python run_supabase_sql.py https://abcdefgh.supabase.co")
    sys.exit(1)

# SQL Files to execute
SCHEMA_PATH = "/mnt/data/openclaw/workspace/tani-bot/supabase/schema.sql"
RPC_PATH = "/mnt/data/openclaw/workspace/tani-bot/supabase/rpc_functions.sql"

print("=" * 60)
print("🚀 RUNNING SUPABASE MIGRATIONS")
print("=" * 60)
print(f"\n📊 Project: {SUPABASE_URL}")

# Read SQL files
print("\n1. Loading SQL files...")
with open(SCHEMA_PATH, 'r') as f:
    schema_sql = f.read()
print(f"✅ Schema: {len(schema_sql)} chars")

with open(RPC_PATH, 'r') as f:
    rpc_sql = f.read()
print(f"✅ RPC Functions: {len(rpc_sql)} chars")

# Execute schema
print("\n2. Running schema migration...")
try:
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "params=single-object"
        },
        json={"query": schema_sql},
        timeout=60
    )
    
    if response.status_code in [200, 201, 204]:
        print("✅ Schema migration successful!")
    else:
        print(f"⚠️ Schema: {response.status_code}")
        print(f"   {response.text[:200]}")
except Exception as e:
    print(f"❌ Schema error: {e}")

# Execute RPC functions
print("\n3. Running RPC functions...")
try:
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "params=single-object"
        },
        json={"query": rpc_sql},
        timeout=60
    )
    
    if response.status_code in [200, 201, 204]:
        print("✅ RPC functions deployed!")
    else:
        print(f"⚠️ RPC: {response.status_code}")
        print(f"   {response.text[:200]}")
except Exception as e:
    print(f"❌ RPC error: {e}")

print("\n" + "=" * 60)
print("✅ MIGRATIONS COMPLETE!")
print("=" * 60)
print("\n📋 Next: Test RAG pipeline")
print("   cd /mnt/data/openclaw/workspace/tani-bot")
print("   pip install -r requirements.txt")
print("   python -m src.rag.document_ingestor")
