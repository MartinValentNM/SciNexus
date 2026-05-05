# SciNexus - Installation Guide

> Quick installation guide. For detailed documentation, see [USER_GUIDE_CZ.md](USER_GUIDE_CZ.md) or [USER_GUIDE_EN.md](USER_GUIDE_EN.md).

---

## 📋 Prerequisites

### Required

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **LM Studio 0.4+** ([Download](https://lmstudio.ai/))
- **16+ GB RAM** (recommended 32 GB)
- **GPU with 16+ GB VRAM** (RTX 3090/4090) OR **CPU with 128 GB RAM**

### Recommended LLM Models

Download one of these in LM Studio:

- **Qwen/Qwen2.5-32B-Instruct-Q4_K_M** (best quality/speed balance)
- **Qwen/Qwen2.5-14B-Instruct-Q4_K_M** (faster, lower VRAM)
- **Qwen/Qwen2.5-72B-Instruct-Q4_K_M** (highest quality, requires 24GB VRAM)

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/martin-valent/lm-studio-utility-pro.git
cd lm-studio-utility-pro
```

### 2. Create Virtual Environment

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Optional - development tools:**
```bash
pip install -r requirements-dev.txt
pre-commit install
```

---

## ⚙️ Configuration

### LM Studio Setup

1. **Open LM Studio**
2. **Download model** (e.g., Qwen2.5-32B-Instruct)
3. **Click "Load Model"** and wait for loading
4. **Start server:**
   - Click **Developer → Start Server**
   - Set **Max Concurrent Predictions** to **4** (or **8** for RTX 4090)
   - Copy Server URL (default: `http://localhost:1234/v1`)

### Application Launch

```bash
streamlit run app_grok.py
```

Application opens at `http://localhost:8501`

---

## 🔧 First Run

### 1. Connect to LM Studio

- **Sidebar** → Server URL: `http://localhost:1234/v1`
- Click **🔄 Load models**
- Select your model from dropdown

### 2. Test Extraction (5 minutes)

1. **Extraction tab** (🔍)
2. Upload PDF (taxonomic article)
3. Optional: specify page range (e.g., `5-12`)
4. Click **▶️ Run extraction**
5. Download JSON result

### 3. Test Translation (3 minutes)

1. **Translation tab** (🌐)
2. Paste text or upload file
3. Set source/target language
4. ✅ Check "Parallel" for speed
5. Click **▶️ Translate text**

---

## 📊 Performance Tuning

### GPU Settings (RTX 4090)

```python
# LM Studio
Max Concurrent Predictions: 8

# App Sidebar
⚡ Max concurrent LLM requests: 8
```

### GPU Settings (RTX 3080/3090)

```python
# LM Studio
Max Concurrent Predictions: 4

# App Sidebar
⚡ Max concurrent LLM requests: 4
```

### CPU-only Setup

```python
# LM Studio
Use CPU inference
Threads: [number of CPU cores]

# App Sidebar
⚡ Max concurrent LLM requests: 2
```

**Note:** CPU inference is ~10× slower than GPU but produces identical quality.

---

## 🐛 Troubleshooting

### "Connection refused"

**Cause:** LM Studio server not running

**Fix:**
```bash
# In LM Studio:
Developer → Start Server
```

### "Context size exceeded"

**Cause:** Text too large for model context window

**Fix:**
```python
# Reduce chunk size
chunk_size = 2000  # Instead of 3500

# Or use model with larger context
# Qwen2.5 has 128k context window
```

### "No models available"

**Cause:** Model not loaded

**Fix:**
```bash
# In LM Studio:
1. Select model in left panel
2. Click "Load Model"
3. Wait 10-30 seconds
4. In app: 🔄 Load models
```

### Import errors

**Cause:** Missing dependencies

**Fix:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or install specific package
pip install streamlit --upgrade
```

---

## 📖 Documentation

### User Guides

- **[🇨🇿 Czech Guide](USER_GUIDE_CZ.md)** - Complete guide (200+ pages)
- **[🇬🇧 English Guide](USER_GUIDE_EN.md)** - Full documentation (200+ pages)

### Quick Links

- [Installation](USER_GUIDE_CZ.md#-instalace)
- [Performance Optimization](USER_GUIDE_CZ.md#-optimalizace-výkonu)
- [Troubleshooting](USER_GUIDE_CZ.md#-řešení-problémů)
- [API Reference](USER_GUIDE_CZ.md#-api-reference)
- [Examples](USER_GUIDE_CZ.md#-příklady-použití)

---

## 🆘 Support

### Issues & Bugs

Report at [GitHub Issues](https://github.com/martin-valent/lm-studio-utility-pro/issues)

### Questions & Discussions

Ask at [GitHub Discussions](https://github.com/martin-valent/lm-studio-utility-pro/discussions)

### Email

martin.valent@nm.cz (National Museum Prague)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

**Version:** 24.36  
**Last Updated:** April 2026
