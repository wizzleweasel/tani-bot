# 🔐 GitHub Secrets Configuration

These secrets must be configured in **GitHub Repository Settings** → **Secrets and variables** → **Actions**

## Required Secrets

| Secret Name | Description | Where to Get |
|-------------|-------------|--------------|
| `HF_TOKEN` | Hugging Face access token | https://huggingface.co/settings/tokens |
| `SUPABASE_KEY` | Supabase API key for RAG database | https://app.supabase.com/project/_/settings/api |
| `GROQ_API_KEY` | Groq API key for LLM inference | https://console.groq.com/keys |

## How to Add Secrets

1. Go to your GitHub repository
2. Click **Settings** tab
3. Click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Enter the secret name and value
6. Click **Add secret**

## Token Permissions

### HF_TOKEN
- ✅ **Read** access to repositories
- ✅ **Write** access to Spaces
- Type: **Fine-grained token** or **Classic token**

### SUPABASE_KEY
- ✅ **Full** access to Supabase project
- Used for: RAG document storage and retrieval

### GROQ_API_KEY
- ✅ **API access** to Groq models
- Used for: LLM inference in RAG chat

## Security Notes

- ⚠️ **NEVER** commit these secrets to git
- ⚠️ **NEVER** hardcode tokens in source files
- ✅ Secrets are only accessible to GitHub Actions
- ✅ Rotation: Update in GitHub Settings, no code changes needed

## Local Development

For local testing, create a `.env` file (gitignored):

```bash
cp .env.example .env
# Edit .env with your actual values
```

---

**After adding secrets:** The GitHub Actions workflow will automatically deploy on every push to `main`.
