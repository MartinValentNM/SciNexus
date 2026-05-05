# SciNexus

**Verze:** v1  
**Autor:** Martin Valent, Národní Muzeum Praha — Oddělení Paleontologie  
**Projekt:** DKRVO 2024–2028/2.I.c (NM 00023272)

Streamlit aplikace pro vědecké zpracování dokumentů pomocí lokálních LLM modelů (LM Studio / llama.cpp). Navržena primárně pro paleontologický výzkum, konkrétně taxonomii Hyolitha, ale použitelná pro obecné vědecké dokumenty.

---

## Funkce

| Záložka | Popis |
|---------|-------|
| 🔍 Extrakce | Dávková extrakce strukturovaných dat z PDF/DOCX do JSON/CSV |
| 🌐 Překlad | Překlad vědeckých textů (CZ/EN/DE/FR/RU/ZH…) s terminologickými slovníky |
| 🧬 Validace | Batch validace taxonomických jmen přes GNverifier API |
| 💬 Chat | Konverzační rozhraní pro dotazy k dokumentům |
| 🧹 Čištění dat | Normalizace a deduplikace extrahovaných záznamů |
| ✍️ Stylistika | Stylistická úprava vědeckých textů |
| ⚙️ Workflow | Automatizovaný pipeline: extrakce → validace → export |
| 📜 Historie | Přehled provedených operací a verzí výstupů |
| ❓ Nápověda | Dokumentace a tipy |

---

## Požadavky

- **Python 3.10+**
- **[LM Studio](https://lmstudio.ai/)** — lokální LLM server (OpenAI-compatible API na `http://localhost:1234`)
- Doporučené modely: Qwen3-32B, Qwen2.5-72B, DeepSeek-R1-Distill-Qwen-32B

---

## Instalace

### Windows — automaticky

```bat
install.bat
```

### Ručně (Windows / Linux / macOS)

```bash
# Klonuj repozitář
git clone https://github.com/<tvuj-username>/scinexus.git
cd scinexus

# Vytvoř virtuální prostředí a aktivuj ho
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# Nainstaluj závislosti
pip install -r requirements.txt
```

---

## Spuštění

### Windows

```bat
run.bat
```

### Ručně

```bash
streamlit run scinexus.py
```

Aplikace bude dostupná na **http://localhost:8501**

---

## Struktura projektu

```
scinexus/
├── scinexus.py          # Hlavní aplikace (16 000+ řádků)
├── presence.py          # Modul sledování přihlášených uživatelů
├── requirements.txt     # Python závislosti
├── install.bat          # Instalační skript (Windows)
├── run.bat              # Spouštěcí skript (Windows)
├── .gitignore
├── README.md
│
├── users/               # Per-user data (gitignore)
│   └── <jméno>/
│       ├── settings.json
│       ├── templates/
│       └── presets/
│
├── _temp/               # Průběžné zálohy (gitignore)
├── extraction_history/  # Snapshoty extrakcí (gitignore)
└── presence.db          # SQLite — online uživatelé + fronta (gitignore)
```

---

## Architektura

- **LLM backend:** LM Studio (llama.cpp) přes OpenAI-compatible REST API
- **Session persistence:** JSON autosave + SQLite FTS5 cache
- **Překlad:** chunk-per-rerun architektura (UI zůstává responzivní)
- **Souběžnost:** `_LLMConcurrencyManager` + `ThreadPoolExecutor`
- **Validace taxonů:** GNverifier batch API
- **Multi-user:** per-user adresáře, `presence.py` sleduje online uživatele
- **Bilinguální UI:** CZ/EN přes `tt()`/`t()` helpery

---

## Hardwarové doporučení

| Komponenta | Minimum | Doporučeno |
|------------|---------|------------|
| GPU VRAM | 8 GB | 24 GB (RTX 4090) |
| RAM | 32 GB | 128 GB |
| CPU | 8 jader | 16+ jader |

---

## Citace

Pokud SciNexus používáte ve výzkumu, citujte prosím:

> Valent, M. (2025). SciNexus — LM Studio Utility Pro: LLM-assisted taxonomic data extraction tool. Národní Muzeum Praha. https://github.com/<tvuj-username>/scinexus

---

## Licence

Tento projekt je určen pro výzkumné účely v rámci projektu DKRVO 2024–2028/2.I.c (NM 00023272).  
Pro jiné použití kontaktujte autora.
