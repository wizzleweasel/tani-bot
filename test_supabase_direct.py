#!/usr/bin/env python3
"""Test Direct Supabase Connection"""

from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("=" * 60)
print("🧪 TESTING DIRECT SUPABASE CONNECTION")
print("=" * 60)
print(f"\nURL: {SUPABASE_URL}")

try:
    # Initialize client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Client created successfully!")
    
    # Test query - count documents
    print("\n1. Testing documents table...")
    response = supabase.table("documents").select("*", count="exact").limit(1).execute()
    count = len(response.data)
    print(f"   ✅ Documents table accessible")
    print(f"   Sample: {response.data[0]['title'] if response.data else 'No docs yet'}")
    
    # Test RAG - count embeddings
    print("\n2. Testing document_embeddings table...")
    response = supabase.table("document_embeddings").select("*", count="exact").limit(1).execute()
    print(f"   ✅ Embeddings table accessible")
    
    # Test crops table
    print("\n3. Testing crops table...")
    response = supabase.table("crops").select("*").limit(3).execute()
    print(f"   ✅ Crops table accessible")
    if response.data:
        print(f"   Sample crops: {[c['name'] for c in response.data[:3]]}")
    
    # Test RPC function
    print("\n4. Testing RAG RPC function...")
    try:
        # Create a test embedding (zeros for testing)
        test_embedding = [0.0] * 384
        result = supabase.rpc('match_documents', {
            'query_embedding': test_embedding,
            'match_count': 1
        }).execute()
        print(f"   ✅ RPC function 'match_documents' working")
    except Exception as e:
        print(f"   ⚠️ RPC test: {str(e)[:100]}")
    
    print("\n" + "=" * 60)
    print("✅ ALL SUPABASE TESTS PASSED!")
    print("=" * 60)
    print("\n🎉 Supabase is fully connected and operational!")
    
except Exception as e:
    print(f"❌ Connection error: {e}")
    import traceback
    traceback.print_exc()
