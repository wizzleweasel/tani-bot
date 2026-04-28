#!/usr/bin/env python3
"""
TaniBot Dataset Upload to Hugging Face Hub

This script uploads agricultural Q&A datasets to Hugging Face for:
- Free unlimited public dataset hosting
- Streaming API access for RAG pipeline
- Version control and collaboration

Usage:
    python huggingface_dataset_upload.py

Requirements:
    pip install huggingface_hub datasets pandas
"""

import os
import json
from pathlib import Path
from huggingface_hub import HfApi, login
from datasets import Dataset, DatasetDict
import pandas as pd

# Configuration
HF_USERNAME = "baguswicak"  # Your Hugging Face username
DATASET_NAME = "tani-bot-agri-indonesia"  # Dataset repo name
HF_TOKEN = os.getenv("HF_TOKEN", "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")  # From TOOLS.md

# Paths
WORKSPACE_ROOT = Path(__file__).parent.parent
DATASETS_DIR = WORKSPACE_ROOT / "datasets"
OUTPUT_DIR = WORKSPACE_ROOT / "hf_datasets"

def authenticate():
    """Login to Hugging Face Hub"""
    print("🔐 Authenticating with Hugging Face...")
    login(token=HF_TOKEN)
    print("✅ Authentication successful!")

def create_qa_dataset():
    """
    Create Q&A dataset from Supabase export or manual curation
    Returns: Dataset object
    """
    print("\n📚 Creating Q&A dataset...")
    
    # Sample data structure (will be populated from Supabase export)
    qa_data = {
        "id": [],
        "question_id": [],
        "question_text": [],
        "question_language": [],
        "answer_text": [],
        "answer_language": [],
        "cluster": [],
        "tags": [],
        "confidence_score": [],
        "source": [],
        "verified": []
    }
    
    # Example entries from our keyword research
    examples = [
        {
            "question_text": "Cara mengatasi wereng coklat pada padi?",
            "question_language": "id",
            "answer_text": "Wereng coklat dapat dikendalikan dengan: (1) Tanam varietas tahan seperti IR64 atau Ciherang, (2) Keringkan sawah bergantian (intermittent irrigation), (3) Gunakan insektisida buprofezin jika populasi >10 ekor per rumpun, (4) Pertahankan musuh alami seperti laba-laba dan kumbang mirid. Hindari penyemprotan dini yang merusak musuh alami.",
            "answer_language": "id",
            "cluster": "pest_disease",
            "tags": ["rice", "pest", "wereng", "brown-planthopper", "ipm"],
            "confidence_score": 0.95,
            "source": "plantix_irri",
            "verified": False
        },
        {
            "question_text": "Why are rice leaves turning yellow?",
            "question_language": "en",
            "answer_text": "Yellow rice leaves can be caused by: (1) Nitrogen deficiency - apply urea 100-200 kg/ha, (2) Planthopper attack - check stem base, (3) Water shortage - ensure adequate irrigation, (4) Acidic soil - apply agricultural lime. Check other symptoms for accurate diagnosis.",
            "answer_language": "en",
            "cluster": "nutrient_deficiency",
            "tags": ["rice", "nitrogen", "yellow-leaves", "diagnosis"],
            "confidence_score": 0.90,
            "source": "extension_guides",
            "verified": False
        },
        {
            "question_text": "Cara membuat pupuk organik cair dari limbah dapur?",
            "question_language": "id",
            "answer_text": "Bahan: (1) Sisa sayur/buah 5kg, (2) Gula merah 100g, (3) Air cucian beras 2L, (4) EM4 50ml. Cara: Campur semua, fermentasi 2-3 minggu, aduk setiap 3 hari. Siap saat bau busuk hilang dan warna coklat tua. Encerkan 1:10 sebelum semprot.",
            "answer_language": "id",
            "cluster": "fertilizer",
            "tags": ["organic-fertilizer", "kitchen-waste", "fermentation", "poc", "mol"],
            "confidence_score": 0.92,
            "source": "wikibooks_indonesia",
            "verified": False
        }
    ]
    
    # Add examples to dataset
    for i, ex in enumerate(examples):
        qa_data["id"].append(f"qa_{i:04d}")
        qa_data["question_id"].append(f"q_{i:04d}")
        qa_data["question_text"].append(ex["question_text"])
        qa_data["question_language"].append(ex["question_language"])
        qa_data["answer_text"].append(ex["answer_text"])
        qa_data["answer_language"].append(ex["answer_language"])
        qa_data["cluster"].append(ex["cluster"])
        qa_data["tags"].append(ex["tags"])
        qa_data["confidence_score"].append(ex["confidence_score"])
        qa_data["source"].append(ex["source"])
        qa_data["verified"].append(ex["verified"])
    
    # Create Hugging Face Dataset
    dataset = Dataset.from_dict(qa_data)
    print(f"✅ Created dataset with {len(dataset)} Q&A pairs")
    
    return dataset

def create_keyword_dataset():
    """
    Create YouTube keyword research dataset
    Returns: Dataset object
    """
    print("\n🔍 Creating keyword dataset...")
    
    keyword_data = {
        "keyword_id": [],
        "query_text": [],
        "language": [],
        "cluster": [],
        "intent": [],
        "search_volume_est": [],
        "competition": [],
        "priority": []
    }
    
    # Sample keywords from our research
    keywords = [
        ("cara mengatasi hama padi", "id", "pest_disease", "troubleshooting", "high", 10),
        ("wereng coklat gejala dan cara mengatasi", "id", "pest_disease", "troubleshooting", "high", 10),
        ("cara membuat pupuk organik cair", "id", "fertilizer", "how_to", "medium", 9),
        ("kenapa daun padi menguning", "id", "diagnosis", "why", "high", 10),
        ("how to control brown planthopper rice", "en", "pest_disease", "troubleshooting", "medium", 7),
        ("organic fertilizer from kitchen waste", "en", "fertilizer", "how_to", "low", 6),
    ]
    
    for i, (query, lang, cluster, intent, competition, priority) in enumerate(keywords):
        keyword_data["keyword_id"].append(f"kw_{i:04d}")
        keyword_data["query_text"].append(query)
        keyword_data["language"].append(lang)
        keyword_data["cluster"].append(cluster)
        keyword_data["intent"].append(intent)
        keyword_data["search_volume_est"].append(None)  # To be filled with actual data
        keyword_data["competition"].append(competition)
        keyword_data["priority"].append(priority)
    
    dataset = Dataset.from_dict(keyword_data)
    print(f"✅ Created keyword dataset with {len(dataset)} keywords")
    
    return dataset

def upload_to_huggingface(dataset, dataset_name, private=False):
    """
    Upload dataset to Hugging Face Hub
    
    Args:
        dataset: Hugging Face Dataset object
        dataset_name: Name of the dataset (e.g., "tani-bot-agri-indonesia")
        private: Whether to make dataset private (default: False)
    """
    print(f"\n🚀 Uploading {dataset_name} to Hugging Face Hub...")
    
    api = HfApi()
    repo_id = f"{HF_USERNAME}/{dataset_name}"
    
    try:
        # Create repo if doesn't exist
        api.create_repo(repo_id=repo_id, repo_type="dataset", private=private, exist_ok=True)
        print(f"✅ Repository created/verified: {repo_id}")
        
        # Upload dataset
        dataset.push_to_hub(repo_id)
        print(f"✅ Dataset uploaded successfully!")
        print(f"📍 View at: https://huggingface.co/datasets/{repo_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")
        return False

def save_local_backup(dataset, dataset_name):
    """Save local backup as JSON and Parquet"""
    print(f"\n💾 Saving local backup...")
    
    backup_dir = OUTPUT_DIR / dataset_name
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as JSON
    json_path = backup_dir / f"{dataset_name}.json"
    dataset.to_json(json_path, orient="records", force_ascii=False, indent=2)
    print(f"✅ JSON saved: {json_path}")
    
    # Save as Parquet (more efficient)
    parquet_path = backup_dir / f"{dataset_name}.parquet"
    dataset.to_parquet(parquet_path)
    print(f"✅ Parquet saved: {parquet_path}")
    
    # Save README
    readme_content = f"""# {dataset_name}

TaniBot Agricultural Q&A Dataset for Indonesian Farmers

## Description
This dataset contains question-answer pairs for agricultural topics relevant to Indonesian farmers, including:
- Pest and disease management
- Fertilizer and nutrient guidance
- Planting techniques
- Harvest and post-harvest handling
- Organic farming practices

## Language Distribution
- Indonesian (Bahasa): ~80%
- English: ~20%

## Usage

```python
from datasets import load_dataset

# Load dataset
dataset = load_dataset("{HF_USERNAME}/{dataset_name}")

# Stream dataset (for large datasets)
dataset = load_dataset("{HF_USERNAME}/{dataset_name}", split="train", streaming=True)
```

## License
CC BY-SA 4.0

## Source
TaniBot Project - https://github.com/wizzleweasel/tani-bot
"""
    
    readme_path = backup_dir / "README.md"
    readme_path.write_text(readme_content)
    print(f"✅ README saved: {readme_path}")

def main():
    """Main execution flow"""
    print("=" * 60)
    print("🌾 TaniBot Dataset Upload to Hugging Face")
    print("=" * 60)
    
    # Authenticate
    authenticate()
    
    # Create datasets
    qa_dataset = create_qa_dataset()
    keyword_dataset = create_keyword_dataset()
    
    # Save local backups
    save_local_backup(qa_dataset, "tani-bot-qa")
    save_local_backup(keyword_dataset, "tani-bot-keywords")
    
    # Upload to Hugging Face
    print("\n" + "=" * 60)
    print("📤 UPLOADING TO HUGGING FACE HUB")
    print("=" * 60)
    
    upload_qa = upload_to_huggingface(qa_dataset, "tani-bot-qa", private=False)
    upload_keywords = upload_to_huggingface(keyword_dataset, "tani-bot-keywords", private=False)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 UPLOAD SUMMARY")
    print("=" * 60)
    print(f"Q&A Dataset: {'✅ Uploaded' if upload_qa else '❌ Failed'}")
    print(f"Keyword Dataset: {'✅ Uploaded' if upload_keywords else '❌ Failed'}")
    print(f"\n📍 Datasets available at:")
    print(f"   - https://huggingface.co/datasets/{HF_USERNAME}/tani-bot-qa")
    print(f"   - https://huggingface.co/datasets/{HF_USERNAME}/tani-bot-keywords")
    print("\n✅ Done!")

if __name__ == "__main__":
    main()
