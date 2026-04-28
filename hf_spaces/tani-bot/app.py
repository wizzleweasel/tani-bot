"""
TaniBot - Streamlit App v2.0
Agricultural Assistant for Indonesian Farmers
✅ No API key input required - uses HF Secrets!
"""

import streamlit as st
import requests
import os
from datetime import datetime

# Configuration - Use HF Space Secrets
# You've set: GROQ_API_KEY
# Need to add: SUPABASE_KEY
SUPABASE_URL = "https://cdlybfnpphzzphwathjx.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")  # Add this to HF Secrets
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # ✅ Already set
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "qwen/qwen3-32b"

# Page config
st.set_page_config(
    page_title="🌾 TaniBot - Asisten Pertanian",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-badge {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)
def rag_search(query: str, limit: int = 5):
    """Search Supabase documents"""
    url = f"{SUPABASE_URL}/rest/v1/documents"
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    params = {"select": "title,content,category,source_type", "limit": limit}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            results = response.json()
            query_words = query.lower().split()
            scored = []
            for doc in results:
                score = 0
                content = doc.get("content", "").lower()
                title = doc.get("title", "").lower()
                for word in query_words:
                    if word in content: score += 2
                    if word in title: score += 1
                doc["_score"] = score
                scored.append(doc)
            scored.sort(key=lambda x: x["_score"], reverse=True)
            return scored[:limit]
        return []
    except:
        return []


def generate_answer(query: str, context: list) -> str:
    """Generate answer using Groq LLM"""
    context_text = ""
    for i, doc in enumerate(context):
        context_text += f"📄 {doc.get('title', '')}: {doc.get('content', '')[:400]}...\n\n"
    
    if not context:
        context_text = "Tidak ada dokumen relevan."
    
    prompt = f"""Anda asisten pertanian Indonesia. Jawab dengan jelas dan ramah dalam Bahasa Indonesia.

Konteks:
{context_text}

Pertanyaan: {query}

Jawaban (2-4 kalimat):"""

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Asisten pertanian Indonesia. Jawab dalam Bahasa Indonesia."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"].strip()
            if "<think>" in answer:
                answer = answer.split("</think>")[-1].strip()
            return answer
        elif response.status_code == 429:
            return "⏳ Server sibuk, coba lagi."
        return f"⚠️ Error: {response.status_code}"
    except Exception as e:
        return f"⚠️ Error: {str(e)[:80]}"


# Header
st.markdown('<h1 class="main-header">🌾 TaniBot</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Asisten Pertanian Indonesia Berbasis AI</p>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center;"><span class="status-badge">✅ Online • 3,000+ Dokumen</span></div>', unsafe_allow_html=True)

# Stats
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("📚 Dokumen", "3,000+")
with col2: st.metric("🌱 Komoditas", "19")
with col3: st.metric("🇮🇩 Bahasa", "Indonesia")
with col4: st.metric("⚡ Response", "<2s")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Tanya tentang pertanian..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🔍 Mencari..."):
            context = rag_search(prompt, limit=5)
            if context:
                st.caption(f"📖 {len(context)} dokumen relevan")
            with st.spinner("🤖 Menjawab..."):
                answer = generate_answer(prompt, context)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# Sidebar
with st.sidebar:
    st.header("ℹ️ Tentang")
    st.markdown("""
    **TaniBot** membantu petani Indonesia:
    ✅ 3,000+ dokumen pertanian
    ✅ 100% Bahasa Indonesia
    ✅ 19 komoditas
    ✅ Response <2 detik
    """)
    
    st.divider()
    st.markdown("**📊 Dataset:** [Hugging Face](https://huggingface.co/baguswicak)")
    st.markdown("**🐙 GitHub:** [TaniBot](https://github.com/wizzleweasel/tani-bot)")
    st.caption(f"v2.0 • {datetime.now().strftime('%Y-%m-%d')}")
