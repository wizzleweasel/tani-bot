#!/usr/bin/env python3
"""Document Ingestion for TaniBot RAG"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from supabase import create_client
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Initialize
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Model loaded")

# Sample agricultural documents
DOCUMENTS = [
    {
        "title": "Rice Cultivation Guide - Indonesia",
        "content": """Rice (Oryza sativa) is Indonesia's staple crop. Optimal growing conditions:

Temperature: 20-35°C (optimal 25-30°C)
Rainfall: 1500-2000mm annually
Soil pH: 5.5-7.0
Altitude: 0-1500m above sea level

Planting Seasons:
- Wet season: October-March
- Dry season: April-September (requires irrigation)

Varieties:
- IR64: High yield, disease resistant
- Ciherang: Popular, good taste
- Mekongga: Drought tolerant

Fertilizer Requirements:
- Nitrogen (N): 200-250 kg/ha
- Phosphorus (P): 60-80 kg/ha
- Potassium (K): 100-150 kg/ha

Common Pests:
- Brown planthopper
- Rice stem borer
- Rice blast disease""",
        "category": "cultivation"
    },
    {
        "title": "Corn Farming Best Practices",
        "content": """Corn (Zea mays) is Indonesia's second most important crop.

Growing Conditions:
Temperature: 18-35°C (optimal 23-27°C)
Rainfall: 850-2000mm annually
Soil pH: 5.5-7.5
Altitude: 0-1000m

Planting:
- Spacing: 75cm x 25cm
- Seed rate: 20-25 kg/ha
- Harvest: 90-110 days after planting

Fertilizer:
- N: 150-200 kg/ha
- P: 50-75 kg/ha
- K: 75-100 kg/ha

Pests & Diseases:
- Corn borer
- Leaf blight
- Rust disease""",
        "category": "cultivation"
    },
    {
        "title": "Cassava Cultivation Guide",
        "content": """Cassava (Manihot esculenta) is a drought-tolerant staple crop.

Growing Conditions:
Temperature: 25-29°C
Rainfall: 1000-1500mm (tolerates drought)
Soil pH: 4.5-7.5
Altitude: 0-1500m

Planting:
- Cutting length: 20-25cm
- Spacing: 100cm x 100cm
- Harvest: 8-12 months

Fertilizer:
- N: 50-80 kg/ha
- P: 30-50 kg/ha
- K: 100-150 kg/ha (cassava needs high K)

Uses:
- Food (tapioca, flour)
- Animal feed
- Bioethanol production""",
        "category": "cultivation"
    }
]

print("\n" + "=" * 60)
print("🌱 INGESTING AGRICULTURAL DOCUMENTS")
print("=" * 60)

for i, doc in enumerate(DOCUMENTS, 1):
    print(f"\n{i}. Ingesting: {doc['title']}")
    
    try:
        # Insert document
        doc_result = supabase.table("documents").insert({
            "title": doc["title"],
            "content": doc["content"],
            "category": doc["category"]
        }).execute()
        
        doc_id = doc_result.data[0]["id"]
        print(f"   ✅ Document created: {doc_id}")
        
        # Create embedding
        embedding = model.encode(doc["content"]).tolist()
        
        # Insert embedding
        supabase.table("document_embeddings").insert({
            "document_id": doc_id,
            "embedding": embedding
        }).execute()
        
        print(f"   ✅ Embedding created")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ INGESTION COMPLETE!")
print("=" * 60)
print("\n🎉 Your RAG pipeline is ready!")
print("\nTest retrieval with:")
print("  python src/rag/rag_retriever.py")
