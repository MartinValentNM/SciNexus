
## SciNexus

**Version:** v1  **Author:** Martin Valent, National Museum Prague — Department of Paleontology  **Project:** DKRVO 2024–2028/2.I.c (NM 00023272)

Streamlit application for scientific document processing using local LLM models (LM Studio / llama.cpp). Designed primarily for paleontological research—specifically Hyolitha taxonomy—but applicable to general scientific documents.

### Features

| Tab | Description |
|----|----|
| 🔍 Extraction | Batch extraction of structured data from PDF/DOCX into JSON/CSV |
| 🌐 Translation | Translation of scientific texts (CZ/EN/DE/FR/RU/ZH…) with terminology dictionaries |
| 🧬 Validation | Batch validation of taxonomic names via GNverifier API |
| 💬 Chat | Conversational interface for document queries |
| 🧹 Data cleaning | Normalization and deduplication of extracted records |
| ✍️ Styling | Stylistic refinement of scientific texts |
| ⚙️ Workflow | Automated pipeline: extraction → validation → export |
| 📜 History | Overview of performed operations and output versions |
| ❓ Help | Documentation and tips |

### Requirements

- **Python 3.10+**
- [**LM Studio**](https://lmstudio.ai/) — local LLM server (OpenAI‑compatible API at http://localhost:1234)
- Recommended models: Qwen3‑32B, Qwen2.5‑72B, DeepSeek‑R1‑Distill‑Qwen‑32B

### Installation

#### Windows — automatic

```
install.bat
```

#### Manual (Windows / Linux / macOS)

```
# Clone repository
git clone https://github.com/<your-username>/scinexus.git
cd scinexus

# Create virtual environment and activate it
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### Running the application

#### Windows

```
run.bat
```

#### Manual

```
streamlit run scinexus.py
```

The application will be available at **http://localhost:8501**

### Project structure

```
scinexus/
├── scinexus.py           # Main application (16,000+ lines)
├── presence.py           # Logged‑in user tracking module
├── requirements.txt      # Python dependencies
├── install.bat           # Installation script (Windows)
├── run.bat               # Startup script (Windows)
├── .gitignore
├── README.md
│
├── users/                # Per‑user data (gitignored)
│   └── <name>/
│       ├── settings.json
│       ├── templates/
│       └── presets/
│
├── _temp/                # Interim backups (gitignored)
├── extraction_history/   # Extraction snapshots (gitignored)
└── presence.db           # SQLite — online users + queue (gitignored)
```

### Architecture

- **LLM backend:** LM Studio (llama.cpp) via OpenAI‑compatible REST API
- **Session persistence:** JSON autosave + SQLite FTS5 cache
- **Translation:** chunk‑per‑rerun architecture (UI remains responsive)
- **Concurrency:** _LLMConcurrencyManager + ThreadPoolExecutor
- **Taxon validation:** GNverifier batch API
- **Multi‑user:** per‑user directories; presence.py tracks online users
- **Bilingual UI:** CZ/EN via tt()/t() helpers

### Hardware recommendations

| Component | Minimum | Recommended |
|---------|---------|------------|
| GPU VRAM | 8 GB | 24 GB (RTX 4090) |
| RAM | 32 GB | 128 GB |
| CPU | 8 cores | 16+ cores |

### Citation

If you use SciNexus in your research, please cite:

Valent, M. (2025). *SciNexus — LM Studio Utility Pro: LLM‑assisted taxonomic data extraction tool.* National Museum Prague. https://github.com/scinexus

### License

This project is intended for research purposes within the DKRVO 2024–2028/2.I.c project (NM 00023272).  
For other uses, please contact the author.
