---
title: TaniBot - Asisten Pertanian Indonesia
emoji: 🌾
colorFrom: green
colorTo: blue
sdk: streamlit
pinned: false
license: mit
---

# 🌾 TaniBot - Agricultural AI Assistant

**Unified Dashboard: MVP + RAG Chat**

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

## 🔗 Links

- **GitHub:** https://github.com/wizzleweasel/tani-bot
- **Datasets:** https://huggingface.co/baguswicak

---

**Version:** v3.0 - Unified  
**Date:** 2026-04-29
