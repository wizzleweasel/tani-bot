# 🌾 TaniBot - Agricultural AI Assistant

**Unified Streamlit App for Indonesian Farmers**

## 📄 5 Pages

1. **🏠 Home** - Overview & statistics
2. **🌤️ Weather** - Live Open-Meteo data + 7-day forecast
3. **🌾 Crop Advisor** - LLM-powered crop recommendations
4. **📊 Yield Prediction** - XGBoost ML model (R² = 0.96)
5. **💬 RAG Chat** - AI chat with 3,000+ agricultural documents

## ✨ Features

- ✅ 3,000+ RAG documents (100% Bahasa Indonesia)
- ✅ 19 crops supported
- ✅ Weather insights (Open-Meteo)
- ✅ ML yield prediction (XGBoost)
- ✅ LLM crop advisor (Groq)
- ✅ Response <2 seconds

## 🔐 Required Secrets

Add these in **Settings → Repository secrets**:

| Secret | Description |
|--------|-------------|
| `GROQ_API_KEY` | Groq API key for LLM features |
| `SUPABASE_KEY` | Supabase service role key for RAG |

## 📊 Dataset

- **QA Pairs:** 1,000 entries
- **Keywords:** 1,000 entries  
- **Transcripts:** 1,000 entries
- **Total:** 3,000 entries (100% Bahasa Indonesia)

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY="your-groq-key"
export SUPABASE_KEY="your-supabase-key"

# Run the app
streamlit run hf_spaces/tani-bot/app.py
```

## 🌐 Live Demo

- **Hugging Face Space:** https://huggingface.co/spaces/baguswicak/tani-bot

## 📚 Project Structure

```
tani-bot/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment variables template
├── hf_spaces/
│   └── tani-bot/
│       ├── app.py              # Main Streamlit app (5 pages)
│       ├── requirements.txt    # App dependencies
│       └── README.md           # App documentation
├── src/
│   ├── pipelines/              # Weather pipeline (Open-Meteo)
│   ├── llm/                    # Groq LLM client
│   ├── ml/                     # XGBoost yield predictor
│   ├── rag/                    # RAG document ingestor
│   ├── data/                   # Synthetic data generator
│   └── integrations/           # Telegram bot integration
├── datasets/                   # Dataset files
└── supabase/                   # Database schema
```

## 🔗 Links

- **GitHub:** https://github.com/wizzleweasel/tani-bot
- **Datasets:** https://huggingface.co/baguswicak
- **HF Space:** https://huggingface.co/spaces/baguswicak/tani-bot

---

**Version:** v3.0 - Unified MVP + RAG  
**Date:** 2026-04-29
