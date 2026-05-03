# 📊 TANIBOT DATASET CONTEXT REPORT

**Generated:** 2026-05-02 17:45 UTC
**Purpose:** Complete overview of all datasets for Page 3 (Crop Advisor) development

---

## 🗺️ LOCATION DATASETS

### 1. Kecamatan Coordinates (7,215 entries) ✅
**File:** `datasets/kecamatan_coords.json`
**Size:** 1.2 MB
**Status:** 100% Complete, Deployed

**Structure:**
```json
{
  "1101010": {
    "kecamatan": "TEUPAH SELATAN",
    "kabupaten_code": "1101",
    "province": "Aceh",
    "lat": 2.36667,
    "lon": 96.43694,
    "actual": true
  }
}
```

**Quality:**
- Total: 7,215 kecamatan (34 provinces)
- Real coordinates (`actual: true`): 31 (0.4%)
- Approximated (`actual: false`): 7,184 (99.6%)
- Invalid IDs: 0 ✅ (all validated against CSV)

**Source of Truth:** `datasets/kecamatan_raw.csv` (official government list)

**Access:**
- Local: `datasets/kecamatan_coords.json`
- GitHub CDN: `raw.githubusercontent.com/wizzleweasel/tani-bot/main/datasets/kecamatan_coords.json`
- HF Space: `hf_spaces/tani-bot/src/data/kecamatan_coords.json`

---

### 2. Kabupaten Coordinates (514 entries) ✅
**File:** `datasets/kecamatan_with_coords.json`
**Size:** 44 KB
**Status:** 100% Complete, Deployed

**Structure:**
```json
{
  "1101": {
    "kabupaten": "Simeulue",
    "province": "Aceh",
    "lat": 2.644,
    "lon": 96.026
  }
}
```

**Coverage:**
- All 514 kabupaten/kota across 34 provinces
- 100% real coordinates (web-search verified)

**Access:**
- Local: `datasets/kecamatan_with_coords.json`
- GitHub CDN: Available via raw.githubusercontent.com

---

### 3. Official Kecamatan CSV (Source of Truth) ✅
**File:** `datasets/kecamatan_raw.csv`
**Size:** 166 KB
**Rows:** 7,215 + header

**Structure:**
```csv
id,foreign,name
1101010,1101,TEUPAH SELATAN
1101020,1101,SIMEULUE TIMUR
...
```

**Columns:**
- `id`: 7-digit kecamatan code (unique)
- `foreign`: 4-digit kabupaten code
- `name`: Kecamatan name (uppercase)

**Usage:** Validate all kecamatan IDs against this file (prevents invalid entries)

---

## 🌾 AGRICULTURAL KNOWLEDGE DATASETS

### 4. YouTube Keyword Research (Q&A Goldmine) ✅
**File:** `datasets/youtube_keyword_research_agriculture_indonesia.md`
**Size:** 13 KB
**Status:** Complete, Ready for Dataset Creation

**Content:**
- 7 keyword clusters (pest, fertilizer, planting, harvest, organic, weather, business)
- 100+ Indonesian farmer search queries
- Long-tail questions (Kenapa, Bagaimana, Apa, Kapan, Berapa)
- Sample Q&A pairs (3 complete examples)
- Supabase schema ready

**Clusters:**
1. **Pest & Disease** (HIGH PRIORITY) - wereng, blas, hawar daun
2. **Fertilizer & Nutrients** (HIGH PRIORITY) - NPK, pupuk organik, urea
3. **Planting Techniques** - jaraktanam, jajar legowo, semai
4. **Harvest & Post-Harvest** - panen, penyimpanan gabah
5. **Organic Farming** (GROWING) - pestisida alami, pertanian organik
6. **Weather & Climate** - cuaca ekstrim, kekeringan
7. **Business & Marketing** - harga gabah, modal usaha

**Sample Q&A:**
```
Q: "Cara mengatasi wereng coklat pada padi?"
A: "Wereng coklat dapat dikendalikan dengan: (1) Tanam varietas tahan seperti IR64,
    (2) Keringkan sawah bergantian, (3) Gunakan insektisida buprofezin jika populasi >10
    ekor per rumpun, (4) Pertahankan musuh alami seperti laba-laba..."
Tags: ['rice', 'pest', 'wereng', 'brown-planthopper', 'ipm']
Confidence: 0.95
```

**Next Step:** Convert to structured JSON for Page 3 Crop Advisor

---

## 🤖 RAG DATASETS (Supabase + Hugging Face)

### 5. Supabase RAG Documents (3,000 docs) ✅
**Table:** `documents`
**Status:** Deployed, Connected

**3 Dataset Categories (1,000 each):**

1. **tani-bot-qa** - Q&A Pairs (1,000 entries)
   - Purpose: Core conversation training + RAG retrieval
   - Content: Pest, disease, fertilizer, cultivation Q&A
   - Language: 100% Bahasa Indonesia
   - Source: Plantix, IRRI, Ministry of Agriculture

2. **tani-bot-keywords** - YouTube Keyword Research (1,000 entries)
   - Purpose: SEO optimization + content planning
   - Content: 7 clusters (pest, fertilizer, planting, harvest, organic, weather, business)
   - Source: YouTube autocomplete, farmer search queries

3. **tani-bot-transcripts** - Video Transcripts (1,000 entries)
   - Purpose: Rich RAG context from YouTube videos
   - Content: Transcribed agriculture tutorials
   - Source: Indonesian farming YouTube channels

**Schema:**
```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY,
  title TEXT,
  content TEXT,
  category TEXT,
  source_type TEXT,
  embedding VECTOR(384)
);
```

**Content:**
- 3,000 agricultural documents (100% Bahasa Indonesia)
- Categories: pest, disease, fertilizer, planting, harvest, organic, weather, business
- Used by: Page 5 (RAG Chat)
- **Not yet integrated with Page 3 (Crop Advisor)**

**Integration Status:**
- ✅ Page 5 (RAG Chat): Full integration
- ❌ Page 3 (Crop Advisor): No integration yet

**Hugging Face Backup:**
- `baguswicak/tani-bot-qa` - Q&A pairs
- `baguswicak/tani-bot-keywords` - Keywords
- `baguswicak/tani-bot-transcripts` - Transcripts

---

## ❌ MISSING DATASETS FOR PAGE 3

### 6. Crop Database (MISSING) ⚠️
**Needed File:** `datasets/crop_database.json`
**Status:** NOT CREATED

**Proposed Structure:**
```json
{
  "rice": {
    "name_id": "Padi",
    "name_en": "Rice",
    "scientific_name": "Oryza sativa",
    "growing_seasons": {
      "Jawa Barat": {"planting": ["Jan", "Feb", "Jul", "Aug"], "harvest": "Apr-May, Sep-Oct"},
      "Jawa Timur": {"planting": ["Jan", "Feb", "Jul"], "harvest": "Apr-May, Sep"}
    },
    "soil_requirements": {
      "type": "Clay loam",
      "ph_min": 5.5,
      "ph_max": 7.0,
      "drainage": "Flooded/irrigated"
    },
    "climate_requirements": {
      "temp_min": 20,
      "temp_max": 35,
      "rainfall_mm_year": 1500,
      "humidity": "High"
    },
    "fertilizer": {
      "npk_ratio": "15-15-15",
      "urea_kg_per_ha": 200,
      "schedule": ["Basal", "Tillering (30 days)", "Panicle initiation (60 days)"]
    },
    "pests_diseases": [
      {"name": "Wereng Coklat", "type": "pest", "treatment": "Buprofezin, resistant varieties"},
      {"name": "Penyakit Blas", "type": "disease", "treatment": "Tricyclazole, Carbendazim"}
    ],
    "days_to_harvest": 110,
    "yield_range_ton_per_ha": {"min": 5, "max": 8},
    "market_price_idr_per_kg": 4500
  },
  "corn": {...},
  "cassava": {...}
}
```

**Priority:** HIGH - Needed for structured crop advice

---

### 7. Fertilizer Database (MISSING) ⚠️
**Needed File:** `datasets/fertilizer_database.json`
**Status:** NOT CREATED

**Proposed Structure:**
```json
{
  "urea": {
    "name_id": "Urea",
    "n_content": 46,
    "p_content": 0,
    "k_content": 0,
    "application_rate": {
      "rice": "200 kg/ha",
      "corn": "150 kg/ha"
    },
    "timing": "Basal + top dressing",
    "warnings": "Jangan campur dengan kapur"
  },
  "npk_15_15_15": {...}
}
```

**Priority:** MEDIUM - Can be integrated into crop database

---

### 8. Pest & Disease Database (MISSING) ⚠️
**Needed File:** `datasets/pest_disease_database.json`
**Status:** NOT CREATED

**Proposed Structure:**
```json
{
  "wereng_coklat": {
    "name_id": "Wereng Coklat",
    "name_en": "Brown Planthopper",
    "scientific_name": "Nilaparvata lugens",
    "affected_crops": ["rice"],
    "symptoms": [
      "Daun menguning dari pinggir",
      "Tanaman kering seperti terbakar",
      "Serangga kecil di pangkal batang"
    ],
    "treatment_chemical": "Buprofezin 25% WP",
    "treatment_organic": "Air rendaman bawang putih + cabe",
    "prevention": "Varietas tahan, pengeringan bergantian"
  }
}
```

**Priority:** HIGH - Critical for crop advisor

---

### 9. Planting Calendar (MISSING) ⚠️
**Needed File:** `datasets/planting_calendar.json`
**Status:** NOT CREATED

**Proposed Structure:**
```json
{
  "Jawa Barat": {
    "rice": {
      "musim_hujan": {"planting": "Oct-Dec", "harvest": "Feb-Apr"},
      "musim_kemarau": {"planting": "Apr-Jun", "harvest": "Aug-Oct"}
    },
    "corn": {...}
  }
}
```

**Priority:** MEDIUM - Enhances location-specific advice

---

## 📊 DATASET USAGE BY PAGE

| Dataset | Page 2 (Weather) | Page 3 (Crop Advisor) | Page 4 (Yield) | Page 5 (RAG Chat) |
|---------|-----------------|----------------------|----------------|-------------------|
| **kecamatan_coords.json** | ✅ Autocomplete | ❌ Not used | ❌ Not used | ❌ Not used |
| **kecamatan_with_coords.json** | ✅ Fallback | ❌ Not used | ❌ Not used | ❌ Not used |
| **crop_database.json** | ❌ N/A | ❌ MISSING | ❌ MISSING | ❌ MISSING |
| **pest_disease_db.json** | ❌ N/A | ❌ MISSING | ❌ MISSING | ⚠️ In RAG docs |
| **fertilizer_db.json** | ❌ N/A | ❌ MISSING | ❌ MISSING | ⚠️ In RAG docs |
| **planting_calendar.json** | ❌ N/A | ❌ MISSING | ❌ MISSING | ❌ MISSING |
| **Supabase RAG (3k docs)** | ❌ N/A | ❌ Not integrated | ❌ N/A | ✅ Full integration |
| **YouTube keyword research** | ❌ N/A | ✅ Source for dataset | ❌ N/A | ✅ Source for Q&A |

---

## 🎯 RECOMMENDATIONS FOR PAGE 3 DEVELOPMENT

### Phase 1: Build Core Crop Database (Week 1)
1. Create `datasets/crop_database.json` with 10 major crops:
   - Rice (Padi)
   - Corn (Jagung)
   - Cassava (Singkong)
   - Soybeans (Kedelai)
   - Peanuts (Kacang Tanah)
   - Chili (Cabe)
   - Coffee (Kopi)
   - Coconut (Kelapa)
   - Banana (Pisang)
   - Mango (Mangga)

2. Extract data from:
   - YouTube keyword research file (already done ✅)
   - Supabase RAG documents (3,000 docs)
   - Indonesian Ministry of Agriculture guides
   - IRRI (International Rice Research Institute)

### Phase 2: Integrate Location Intelligence (Week 2)
1. Reuse `kecamatan_db.py` from Weather page
2. Add climate zone detection (tropical highland vs coastal)
3. Link to weather data (Page 2 integration)
4. Add soil type mapping by kabupaten

### Phase 3: Add Pest & Disease Module (Week 2-3)
1. Create `datasets/pest_disease_database.json`
2. Extract from YouTube keyword research (Cluster 1)
3. Integrate with Supabase RAG search
4. Add image recognition (future enhancement)

### Phase 4: Structured Response Templates (Week 3)
1. Create response templates for each crop section:
   - 🌱 Planting season
   - 💧 Water requirements
   - 🌿 Fertilizer schedule
   - 🐛 Pest & disease management
   - 🌾 Harvest timing
   - 💰 Market price estimate

---

## 🔗 DATA FLOW FOR PAGE 3

```
User selects crop + location
         ↓
Load crop data from crop_database.json
         ↓
Get location climate from kecamatan_coords.json
         ↓
Search Supabase RAG for crop-specific docs
         ↓
Query pest_disease_db for common issues
         ↓
Generate structured advice (LLM + templates)
         ↓
Display with sections, tables, timelines
```

---

## 📁 FILE STRUCTURE (Current vs Needed)

### Current Structure:
```
datasets/
├── kecamatan_coords.json ✅ (7,215 entries)
├── kecamatan_with_coords.json ✅ (514 entries)
├── kecamatan_raw.csv ✅ (source of truth)
├── youtube_keyword_research_agriculture_indonesia.md ✅
└── coords_progress.json ✅
```

### Needed Structure:
```
datasets/
├── kecamatan_coords.json ✅
├── kecamatan_with_coords.json ✅
├── kecamatan_raw.csv ✅
├── youtube_keyword_research_agriculture_indonesia.md ✅
├── crop_database.json ❌ (MISSING - HIGH PRIORITY)
├── pest_disease_database.json ❌ (MISSING - HIGH PRIORITY)
├── fertilizer_database.json ❌ (MISSING - MEDIUM)
└── planting_calendar.json ❌ (MISSING - MEDIUM)
```

---

## 📊 DATASET QUALITY METRICS

| Dataset | Completeness | Accuracy | Coverage | Priority |
|---------|-------------|----------|----------|----------|
| **kecamatan_coords.json** | 100% ✅ | 0.4% real | 34 provinces | ✅ Done |
| **kecamatan_with_coords.json** | 100% ✅ | 100% real | 514 kabupaten | ✅ Done |
| **kecamatan_raw.csv** | 100% ✅ | Official | 7,215 entries | ✅ Source |
| **youtube_keyword_research.md** | 100% ✅ | Verified | 7 clusters | ✅ Ready |
| **crop_database.json** | 0% ❌ | N/A | 0 crops | 🔴 URGENT |
| **pest_disease_db.json** | 0% ❌ | N/A | 0 pests | 🔴 URGENT |
| **Supabase RAG** | 100% ✅ | Curated | 3,000 docs | ✅ Done |

---

**Report Generated:** 2026-05-02 17:45 UTC
**Next Action:** Build `datasets/crop_database.json` for Page 3 Crop Advisor
