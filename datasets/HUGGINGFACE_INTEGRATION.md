# Hugging Face Integration for TaniBot

**Setup Date:** 2026-04-28  
**Purpose:** Free unlimited dataset hosting + streaming API for RAG pipeline

---

## 🎯 Why Hugging Face?

| Feature | Supabase | Hugging Face |
|---------|----------|--------------|
| **Storage Limit** | 500 MB (free) | Unlimited (public) |
| **File Size** | Limited | Up to 50 GB per file |
| **API Access** | SQL queries | Streaming API |
| **Version Control** | Manual | Git-based |
| **Cost** | Free (Pro: $25/mo) | Free (public datasets) |
| **Best For** | Structured data, vectors | Large text, embeddings, archives |

---

## 🔐 Authentication

### Option 1: Environment Variable (Recommended)
```bash
export HF_TOKEN="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"
```

### Option 2: Login Command
```bash
huggingface-cli login
# Enter token: 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
```

### Option 3: In Python Script
```python
from huggingface_hub import login
login(token="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")
```

---

## 📦 Dataset Structure

### 1. `tani-bot-qa` - Q&A Pairs
**Purpose:** Core conversation training + RAG retrieval

**Schema:**
```json
{
  "id": "qa_0001",
  "question_id": "q_0001",
  "question_text": "Cara mengatasi wereng coklat pada padi?",
  "question_language": "id",
  "answer_text": "Wereng coklat dapat dikendalikan dengan...",
  "answer_language": "id",
  "cluster": "pest_disease",
  "tags": ["rice", "pest", "wereng", "brown-planthopper"],
  "confidence_score": 0.95,
  "source": "plantix_irri",
  "verified": false
}
```

**Size Estimate:**
- 100 Q&A pairs: ~50 KB
- 1,000 Q&A pairs: ~500 KB
- 10,000 Q&A pairs: ~5 MB

**Repo:** https://huggingface.co/datasets/baguswicak/tani-bot-qa

---

### 2. `tani-bot-keywords` - YouTube Keyword Research
**Purpose:** SEO optimization + content planning

**Schema:**
```json
{
  "keyword_id": "kw_0001",
  "query_text": "cara mengatasi hama padi",
  "language": "id",
  "cluster": "pest_disease",
  "intent": "troubleshooting",
  "search_volume_est": null,
  "competition": "high",
  "priority": 10
}
```

**Repo:** https://huggingface.co/datasets/baguswicak/tani-bot-keywords

---

### 3. `tani-bot-transcripts` - Video Transcripts (Future)
**Purpose:** Rich RAG context from YouTube videos

**Schema:**
```json
{
  "id": "trans_0001",
  "youtube_url": "https://youtube.com/watch?v=...",
  "video_title": "Cara Mengatasi Wereng Coklat",
  "channel_name": "Petani Sukses",
  "transcript_text": "...",
  "language": "id",
  "duration_seconds": 600,
  "view_count": 50000,
  "published_date": "2025-06-15",
  "topics": ["pest", "rice", "wereng"],
  "chunk_id": "chunk_001",
  "embedding_ref": "emb_001"
}
```

**Size Estimate:**
- 50 transcripts: ~10 MB
- 500 transcripts: ~100 MB

**Repo:** https://huggingface.co/datasets/baguswicak/tani-bot-transcripts

---

## 🚀 Upload Workflow

### Step 1: Install Dependencies
```bash
pip install huggingface_hub datasets pandas
```

### Step 2: Prepare Dataset
```bash
cd /mnt/data/openclaw/workspace/.openclaw/workspace
python scripts/huggingface_dataset_upload.py
```

### Step 3: Verify Upload
Visit:
- https://huggingface.co/datasets/baguswicak/tani-bot-qa
- https://huggingface.co/datasets/baguswicak/tani-bot-keywords

---

## 📥 Load Dataset in TaniBot

### Method 1: Full Load (Small Datasets)
```python
from datasets import load_dataset

# Load entire dataset into memory
dataset = load_dataset("baguswicak/tani-bot-qa", split="train")

# Access first Q&A
print(dataset[0]["question_text"])
print(dataset[0]["answer_text"])
```

### Method 2: Streaming (Large Datasets) ⭐ RECOMMENDED
```python
from datasets import load_dataset

# Stream without downloading
dataset = load_dataset("baguswicak/tani-bot-qa", split="train", streaming=True)

# Iterate efficiently
for example in dataset:
    print(example["question_text"])
```

### Method 3: Filtered Load
```python
from datasets import load_dataset

# Load only pest_disease cluster
dataset = load_dataset(
    "baguswicak/tani-bot-qa",
    split="train",
    streaming=True
)

# Filter by cluster
pest_qa = dataset.filter(lambda x: x["cluster"] == "pest_disease")
```

---

## 🔄 Sync Strategy: Supabase ↔ Hugging Face

### What Goes Where

| Data Type | Primary Storage | Backup | Why |
|-----------|----------------|--------|-----|
| Q&A pairs | **Supabase** | Hugging Face | Fast SQL queries + RAG |
| Embeddings | **Supabase** (pgvector) | None | Vector search needs DB |
| Keywords | **Supabase** | Hugging Face | Planning + analytics |
| Transcripts | **Hugging Face** | Supabase (metadata) | Large files, stream on-demand |
| Documents (PDF) | Supabase Storage | Hugging Face | Direct access via API |

### Sync Workflow
```
1. New Q&A created → Insert to Supabase
2. Batch export (daily/weekly) → Push to Hugging Face
3. Hugging Face = versioned archive + backup
4. Supabase = live query + RAG
```

---

## 📊 Usage Monitoring

### Hugging Face Dashboard
- **Storage:** https://huggingface.co/settings/billing
- **Downloads:** https://huggingface.co/datasets/baguswicak/tani-bot-qa/tree/main
- **API Calls:** Not limited for public datasets

### Supabase Dashboard
- **Database Size:** https://app.supabase.com/project/cdlybfnpphzzphwathjx/database
- **Storage:** https://app.supabase.com/project/cdlybfnpphzzphwathjx/storage

**Alert Threshold:**
- Supabase > 400 MB → Move transcripts to HF
- Supabase > 450 MB → Archive old conversations to HF

---

## 🔧 Maintenance

### Update Dataset (New Version)
```python
from datasets import load_dataset
from huggingface_hub import HfApi

# Load existing
dataset = load_dataset("baguswicak/tani-bot-qa")

# Add new data
new_data = {"question_text": [...], "answer_text": [...]}
dataset = dataset.add_item(new_data)

# Push new version
api = HfApi()
dataset.push_to_hub("baguswicak/tani-bot-qa", commit_message="Add 50 new Q&A pairs")
```

### Delete Dataset
```bash
huggingface-cli delete-repo baguswicak/tani-bot-qa --repo-type dataset
```

---

## 🎯 Integration with TaniBot RAG

### Current RAG Flow (Supabase-only)
```
User Query → Embedding → pgvector similarity → Documents → LLM → Answer
```

### Enhanced RAG Flow (Hybrid)
```
User Query → Embedding → pgvector similarity → 
  ├─ Supabase: Q&A pairs (fast)
  └─ Hugging Face: Transcripts (streaming)
→ Combined context → LLM → Answer
```

### Implementation
```python
from supabase import create_client
from datasets import load_dataset

# Supabase for embeddings + Q&A
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
similar_docs = supabase.rpc('match_documents', {
    'query_embedding': query_embedding,
    'threshold': 0.7,
    'count': 5
}).execute()

# Hugging Face for additional context
hf_dataset = load_dataset("baguswicak/tani-bot-transcripts", split="train", streaming=True)
transcripts = [doc for doc in hf_dataset.take(3)]

# Combine contexts
context = similar_docs.data + transcripts
```

---

## 📈 Scaling Plan

### Phase 1 (Now - Week 4)
- ✅ Q&A dataset on Hugging Face (backup)
- ✅ Keywords dataset on Hugging Face (backup)
- Supabase: Primary storage + RAG

### Phase 2 (Month 2)
- Video transcripts → Hugging Face (primary)
- Supabase: Metadata + embeddings only

### Phase 3 (Month 3+)
- Multi-language datasets (Bahasa, English, Javanese)
- Fine-tuning dataset for custom model
- Community contributions via HF PRs

---

## 📝 Checklist

- [x] Hugging Face token configured
- [x] Upload script created
- [x] Dataset schema defined
- [ ] Initial upload completed
- [ ] README.md on each HF dataset
- [ ] TaniBot RAG integration updated
- [ ] Sync workflow documented
- [ ] Monitoring dashboard set up

---

**Last Updated:** 2026-04-28  
**Maintained By:** TaniBot Team
