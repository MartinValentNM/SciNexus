# SciNexus - Architecture Overview

> Technical documentation for developers

---

## 📐 System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend (UI)                   │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐   │
│  │Extract   │Translate │Validate  │Chat      │Workflow  │   │
│  │Tab       │Tab       │Tab       │Tab       │Tab       │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Core (app_grok.py)             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Session State Management (st.session_state)        │    │
│  │  - Auto-save (JSON checkpoint system)               │    │
│  │  - Auto-resume (interrupted operations)             │    │
│  │  - Multi-user presence tracking                     │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Business Logic                                      │    │
│  │  - do_translate()        - validate_taxon_name()    │    │
│  │  - chat_completion()     - chunk_text_smart()       │    │
│  │  - extract_taxa()        - normalize_stratigraphy() │    │
│  └─────────────────────────────────────────────────────┘    │
└────────────────────┬───────────────────┬────────────────────┘
                     │                   │
         ┌───────────┴──────┐   ┌────────┴─────────┐
         ▼                  ▼   ▼                  ▼
┌──────────────────┐  ┌──────────────────────────────┐
│  LM Studio API   │  │  External Databases (HTTP)   │
│  (llama.cpp)     │  │  - PaleoDB    - GBIF         │
│                  │  │  - WoRMS      - IRMNG        │
│  - Chat endpoint │  │  - Fossilworks - CoL         │
│  - Streaming     │  │  - ITIS       - IPNI         │
│  - Batching      │  │  + 6 more...                 │
└──────────────────┘  └──────────────────────────────┘
         │                         │
         ▼                         ▼
┌──────────────────┐  ┌──────────────────────────────┐
│  Local Storage   │  │  SQLite Cache                │
│  - _temp/        │  │  - Validation results (30d)  │
│  - _backup/      │  │  - FTS5 search index         │
│  - chat_history/ │  │  - Offline database          │
│  - session JSON  │  │  - WAL mode (concurrent R/W) │
└──────────────────┘  └──────────────────────────────┘
```

---

## 🏗️ Core Components

### 1. LLM Communication Layer

**Module:** `chat_completion()`, `chat_completion_stream()`

**Features:**
- Connection pooling (`_LLM_SESSION`)
- Broken pipe recovery
- Retry with exponential backoff + jitter
- Stop sequences for JSON/XML
- Streaming support

**Code:**
```python
def chat_completion(
    base_url: str,
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 4000,
    stop: Optional[List[str]] = None
) -> str:
    # Shared session with connection pooling
    session = _get_llm_session()
    
    # Build request
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if stop:
        payload["stop"] = stop
    
    # Retry logic (3 attempts)
    for attempt in range(3):
        try:
            response = session.post(
                f"{base_url}/chat/completions",
                json=payload,
                timeout=300
            )
            return response.json()["choices"][0]["message"]["content"]
        except (ConnectionError, ChunkedEncodingError):
            if attempt == 2:
                raise
            _reset_llm_session()  # Rebuild session on error
            time.sleep(1.5 * (1.5 ** attempt))  # Backoff
```

### 2. Parallel Processing

**Concurrency Manager:**
```python
class _LLMConcurrencyManager:
    """Thread-safe semaphore for LLM requests."""
    
    def __init__(self, max_concurrent: int = 4):
        self._semaphore = threading.BoundedSemaphore(max_concurrent)
        self._lock = threading.Lock()
    
    def set_max(self, new_max: int):
        """Safely update max concurrent requests."""
        with self._lock:
            current = self._semaphore._value
            diff = new_max - current
            
            if diff > 0:
                # Increase capacity
                for _ in range(diff):
                    self._semaphore.release()
            elif diff < 0:
                # Decrease capacity
                for _ in range(-diff):
                    self._semaphore.acquire(blocking=False)
    
    def acquire(self, blocking=True):
        return self._semaphore.acquire(blocking)
    
    def release(self):
        return self._semaphore.release()
```

**Parallel Translation:**
```python
def do_translate(text: str, parallel: bool = True, max_workers: int = 4):
    if not parallel:
        # Sequential mode - preserves context
        return _translate_sequential(text)
    
    # Parallel mode - faster, no shared context
    chunks = chunk_text_smart(text, chunk_size=3500)
    
    # Thread-safe progress tracking
    count_lock = threading.Lock()
    completed = [0]
    
    def translate_chunk(chunk):
        result = chat_completion(base_url, model, [
            {"role": "system", "content": "Translate to English."},
            {"role": "user", "content": chunk}
        ])
        
        with count_lock:
            completed[0] += 1
            progress_callback(completed[0] / len(chunks))
        
        return result
    
    # Parallel execution
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(translate_chunk, c) for c in chunks]
        results = [f.result() for f in as_completed(futures)]
    
    return "\n\n".join(results)
```

### 3. Database Validation System

**Architecture:**
```python
def validate_taxon_name(
    taxon: str,
    databases: List[str],
    cache: Dict
) -> Dict:
    """Parallel validation across 14 databases."""
    
    # Check cache first (30-day TTL)
    cache_key = f"{taxon}:{','.join(sorted(databases))}"
    if cache_key in cache:
        return cache[cache_key]
    
    # Parallel DB queries (ThreadPoolExecutor)
    result_lock = threading.Lock()
    results = {}
    
    def query_single_db(db_code: str):
        try:
            if db_code == "paleodb":
                return _validate_paleodb(taxon)
            elif db_code == "gbif":
                return _validate_gbif(taxon)
            # ... 12 more databases
        except Exception as e:
            return {"found": False, "error": str(e)}
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(query_single_db, db): db
            for db in databases
        }
        
        for future in as_completed(futures):
            db = futures[future]
            with result_lock:
                results[db] = future.result()
    
    # Cache result
    cache[cache_key] = {
        "taxon": taxon,
        "results": results,
        "summary": _summarize_validation(results)
    }
    
    return cache[cache_key]
```

### 4. Chunking System

**Token-aware chunking:**
```python
def advanced_chunk_with_token_estimate(
    text: str,
    model_name: str = "",
    target_tokens: int = 3800,
    overlap_tokens: int = 350
) -> List[str]:
    """Language-aware chunking with token estimation."""
    
    def est_tokens(s: str) -> int:
        # CJK detection
        if any(ord(c) > 0x4E00 for c in s):
            return int(len(s) * 1.65)  # Chinese: ~1.65 tokens/char
        
        # Slavic detection
        if any(c in "ěščřžýáíéůďťňĚŠČŘŽÝÁÍÉŮĎŤŇ" for c in s):
            return int(len(s) * 1.28)  # Czech/Slovak: ~1.28 tokens/char
        
        # Default (English/Latin)
        return len(s) // 4 + len(re.findall(r'\b\w+\b', s))
    
    target_chars = int(target_tokens * 4.1)
    chunks = []
    i = 0
    
    while i < len(text):
        end = min(i + target_chars, len(text))
        
        # Find natural boundary (paragraph/sentence end)
        for sep in ("\n\n", ".\n", "?\n", "!\n"):
            pos = text.rfind(sep, i, end + 600)
            if pos > i + 1200:
                end = pos + len(sep)
                break
        
        chunk = text[i:end].strip()
        if chunk:
            chunks.append(chunk)
        
        i = max(i + 1, end - overlap_tokens)
    
    return deduplicate_chunks(chunks)
```

### 5. Auto-save & Resume

**Checkpoint system:**
```python
def save_checkpoint(operation: str, step: int, data: Dict):
    """Save operation checkpoint for auto-resume."""
    checkpoint_dir = Path("_temp/checkpoints")
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    checkpoint = {
        "operation": operation,
        "step": step,
        "data": data,
        "timestamp": datetime.now().isoformat(),
        "version": "24.36"
    }
    
    # Atomic write
    tmp_file = checkpoint_dir / f"{operation}_{step}.tmp"
    final_file = checkpoint_dir / f"{operation}_{step}.json"
    
    tmp_file.write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2))
    tmp_file.replace(final_file)  # Atomic rename

def load_checkpoint(operation: str, step: int) -> Optional[Dict]:
    """Load checkpoint for resume."""
    checkpoint_file = Path(f"_temp/checkpoints/{operation}_{step}.json")
    
    if not checkpoint_file.exists():
        return None
    
    try:
        checkpoint = json.loads(checkpoint_file.read_text())
        return checkpoint.get("data")
    except Exception:
        return None
```

**Session auto-save:**
```python
SESSION_AUTOSAVE_KEYS = [
    "last_extracted_text",
    "last_extraction_text",  # Alias for compatibility
    "translation_ready",
    "last_validation_results",
    "hyolitha_export_records",
    "ab_results",
    "style_polish_result"
]

def _autosave_if_due():
    """Auto-save session every 3 reruns or on data change."""
    if "autosave_counter" not in st.session_state:
        st.session_state.autosave_counter = 0
        st.session_state.autosave_hash = ""
    
    st.session_state.autosave_counter += 1
    
    # Calculate hash of autosave data
    data = {k: st.session_state.get(k) for k in SESSION_AUTOSAVE_KEYS}
    current_hash = hashlib.md5(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()
    
    # Save if 3 reruns OR data changed
    if (st.session_state.autosave_counter >= 3 or
        current_hash != st.session_state.autosave_hash):
        
        save_session_to_disk(SESSION_AUTOSAVE_FILE, SESSION_AUTOSAVE_KEYS)
        st.session_state.autosave_counter = 0
        st.session_state.autosave_hash = current_hash
```

---

## 🗄️ Data Flow

### Extraction Workflow

```
1. User uploads PDF
         ↓
2. Read PDF (PyPDF2)
   - Extract text per page
   - Optional OCR (if needed)
         ↓
3. Chunking
   - Smart split at paragraph boundaries
   - Target: 3800 tokens
   - Overlap: 350 tokens
         ↓
4. LLM Extraction (parallel)
   - Send chunks to LM Studio
   - System prompt: JSON schema
   - Parse responses
   - DLQ (Dead Letter Queue) for errors
         ↓
5. Deduplication
   - Hash-based chunk dedup
   - Taxon-level dedup
         ↓
6. Result assembly
   - Merge all JSON blocks
   - FTS5 indexing
   - Save to _temp/ (checkpoint)
         ↓
7. User download
   - JSON file
   - XLSX (optional)
   - Auto-save to session
```

### Translation Workflow

```
1. Input text (paste or upload)
         ↓
2. Language detection
   - Auto-detect OR manual selection
   - Supported: zh, ru, fr, de, ja, cs → en
         ↓
3. Glossary application (optional)
   - Load user glossary
   - Pre-compile regex patterns
   - Cache compiled regexes
         ↓
4. Chunking
   - Smart boundaries (sentences/paragraphs)
   - Language-aware token estimation
         ↓
5. Translation modes:
   
   A) Parallel (default)
      - Split into chunks
      - Translate concurrently (4–8 workers)
      - No shared context
      - Fast (~3 min for 100 pages)
   
   B) Sequential
      - Preserve context across chunks
      - Each chunk sees previous translation
      - Slower (~15 min for 100 pages)
         ↓
6. Post-processing
   - Glossary reapplication
   - Style polishing (optional)
   - Save to _temp/ (checkpoint)
         ↓
7. Output
   - Translated text
   - Back-translation (quality check)
   - Download TXT/DOCX
```

### Validation Workflow

```
1. Input taxa (list or from extraction)
         ↓
2. Parse taxa names
   - Split by newline
   - Trim whitespace
   - Deduplicate
         ↓
3. Cache check (SQLite)
   - Key: "{taxon}:{databases}"
   - TTL: 30 days
   - Hit → return cached result
         ↓
4. Parallel DB queries (if cache miss)
   - ThreadPoolExecutor (8 workers)
   - Each DB in separate thread
   - HTTP connection pooling
   - Timeout: 10 seconds per DB
         ↓
5. Database-specific parsers:
   - PaleoDB → REST API → JSON
   - GBIF → REST API → JSON
   - WoRMS → REST API → JSON
   - Fossilworks → HTML scraping → BeautifulSoup
   - ... (14 total)
         ↓
6. Result aggregation
   - Collect all DB results
   - Calculate confidence (high/medium/low)
   - Determine rank (species/genus/family)
   - Cache result (SQLite)
         ↓
7. Output
   - Summary table (DataFrame)
   - Detail links per DB
   - Export CSV
   - Genus expansion (wildcard search)
```

---

## 🧩 Key Design Patterns

### 1. Connection Pooling

**Problem:** Creating new HTTP connections for every request is slow.

**Solution:** Shared session with connection pool.

```python
_HTTP_SESSION = None
_SESSION_LOCK = threading.Lock()

def _get_http_session():
    """Double-checked locking pattern."""
    global _HTTP_SESSION
    
    if _HTTP_SESSION is None:
        with _SESSION_LOCK:
            if _HTTP_SESSION is None:
                _HTTP_SESSION = requests.Session()
                _HTTP_SESSION.mount("https://", HTTPAdapter(
                    pool_connections=20,  # 14 DBs × 8 workers
                    pool_maxsize=20,
                    max_retries=3
                ))
    
    return _HTTP_SESSION
```

### 2. Dead Letter Queue (DLQ)

**Problem:** One failed chunk shouldn't stop entire batch.

**Solution:** Collect errors, continue processing, report at end.

```python
def do_translate_parallel(chunks):
    dlq = []  # Dead Letter Queue
    results = []
    
    for chunk in chunks:
        try:
            result = translate_chunk(chunk)
            results.append(result)
        except Exception as e:
            dlq.append({
                "chunk": chunk[:100],  # Preview
                "error": str(e)
            })
    
    # Continue even if some chunks failed
    if dlq:
        st.warning(f"⚠️ {len(dlq)} chunks failed. See DLQ report.")
        with st.expander("DLQ Report"):
            st.json(dlq)
    
    return "\n\n".join(results)
```

### 3. Progress Callback (Thread-Safe)

**Problem:** Streamlit progress bar from worker threads → ScriptRunContext error.

**Solution:** Wrap progress callback with try/except.

```python
def _safe_progress(progress_cb, value: float):
    """Safe progress update from worker threads."""
    try:
        progress_cb(value)
    except Exception:
        # Worker thread doesn't have ScriptRunContext
        # Silently ignore (main thread will show progress)
        pass

# Usage in worker thread
def translate_chunk(chunk, progress_cb):
    result = chat_completion(...)
    _safe_progress(progress_cb, 0.5)  # Won't crash if called from thread
    return result
```

---

## 📊 Performance Optimizations

### 1. Prefix Indexing (Levenshtein)

**Problem:** Comparing 1500 taxa → 1,124,250 comparisons (O(n²))

**Solution:** 3-char prefix index → skip 95% comparisons

```python
def find_duplicate_taxa(taxa: List[str], threshold: float = 0.85):
    # Build prefix index
    prefix_map = {}
    for taxon in taxa:
        prefix = taxon[:3].lower()
        prefix_map.setdefault(prefix, []).append(taxon)
    
    duplicates = []
    for taxon in taxa:
        prefix = taxon[:3].lower()
        candidates = prefix_map.get(prefix, [])  # ~5% of total taxa
        
        for candidate in candidates:
            if candidate == taxon:
                continue
            
            similarity = levenshtein_ratio(taxon, candidate)
            if similarity >= threshold:
                duplicates.append([taxon, candidate])
    
    return duplicates

# Before: 1,124,250 comparisons, 5 seconds
# After: 56,212 comparisons, 0.3 seconds
```

### 2. SQLite WAL Mode

**Problem:** Concurrent read/write causes locking.

**Solution:** Write-Ahead Logging mode.

```python
conn = sqlite3.connect("cache.db")
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA synchronous=NORMAL")
conn.execute("PRAGMA cache_size=2000")

# Benefits:
# - Readers don't block writers
# - Writers don't block readers
# - ~30% faster than DELETE mode
```

### 3. Pre-compiled Regex

**Problem:** Compiling regex on every call is slow.

**Solution:** Module-level pre-compiled patterns.

```python
# ❌ Before (slow)
def clean_json(text):
    text = re.sub(r"```json|```", "", text)
    text = re.sub(r"\n\n+", "\n", text)
    return text

# ✅ After (fast)
_JSON_FENCE_RE = re.compile(r"```json|```")
_MULTI_NEWLINE_RE = re.compile(r"\n\n+")

def clean_json(text):
    text = _JSON_FENCE_RE.sub("", text)
    text = _MULTI_NEWLINE_RE.sub("\n", text)
    return text

# 10× faster for repeated calls
```

---

## 🔐 Security Considerations

### Input Validation

- **File uploads:** Max size 100 MB, allowed extensions: PDF, DOCX, TXT
- **Page ranges:** Parsed and validated before use
- **SQL injection:** Parameterized queries only
- **XSS:** All user input escaped before HTML rendering

### Data Privacy

- **Local processing:** No data sent to cloud
- **LM Studio:** Runs locally on user's machine
- **Databases:** HTTP queries only (no data uploaded)
- **Cache:** SQLite on local disk (not shared)

### Authentication

- **Multi-user presence:** Simple file-based tracking
- **No passwords:** Streamlit native auth (if enabled)
- **Session isolation:** Each user has own `session_state`

---

## 🧪 Testing Strategy

### Unit Tests

```python
# tests/test_validation.py
def test_paleodb_query():
    result = _validate_paleodb("Hyolithes communis")
    assert result["found"] == True
    assert "paleobiodb.org" in result["url"]

def test_cache_usage():
    cache = {}
    result1 = validate_taxon_name("Alnus", ["gbif"], cache)
    result2 = validate_taxon_name("Alnus", ["gbif"], cache)
    assert result1 == result2
    assert len(cache) == 1  # Only one entry
```

### Integration Tests

```python
# tests/test_workflow.py
def test_full_extraction_pipeline():
    # Upload PDF
    pdf_path = "tests/fixtures/sample.pdf"
    
    # Extract
    results = extract_from_pdf(pdf_path, pages="1-5")
    assert len(results) > 0
    
    # Validate schema
    for record in results:
        assert "taxon_name" in record
        assert "author" in record
```

### Performance Benchmarks

```python
# tests/benchmark_translation.py
import time

def benchmark_parallel_translation():
    text = load_sample_text(pages=100)  # ~50k words
    
    start = time.time()
    result = do_translate(text, parallel=True, max_workers=4)
    elapsed = time.time() - start
    
    assert elapsed < 300  # Should complete in <5 minutes
    assert len(result) > len(text) * 0.8  # Reasonable length
```

---

## 📁 File Structure

```
lm-studio-utility-pro/
├── app_grok.py              # Main application (16,404 lines)
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Development dependencies
├── pyproject.toml           # Project configuration
├── README.md                # GitHub landing page
├── USER_GUIDE_CZ.md         # Czech user guide (200+ pages)
├── USER_GUIDE_EN.md         # English user guide (200+ pages)
├── CONTRIBUTING.md          # Contribution guidelines
├── CHANGELOG.md             # Version history
├── INSTALL.md               # Installation guide
├── ARCHITECTURE.md          # This file
├── LICENSE                  # MIT license
├── .gitignore               # Git ignore rules
├── .flake8                  # Flake8 configuration
├── .pre-commit-config.yaml  # Pre-commit hooks
│
├── _temp/                   # Temporary files (gitignored)
│   ├── checkpoints/         # Auto-save checkpoints
│   ├── extraction_*.txt     # Partial extractions
│   ├── translation_*.txt    # Partial translations
│   └── wf_*.json            # Workflow states
│
├── _backup/                 # Database backups (gitignored)
│   └── session_*.json.bak   # Rotating backups
│
├── tests/                   # Test suite
│   ├── test_validation.py
│   ├── test_translation.py
│   ├── test_extraction.py
│   └── fixtures/
│       └── sample.pdf
│
└── docs/                    # Additional documentation
    ├── API.md
    ├── DATABASES.md
    └── FAQ.md
```

---

## 🔄 Development Workflow

### Setup Development Environment

```bash
# Clone and setup
git clone https://github.com/martin-valent/lm-studio-utility-pro.git
cd lm-studio-utility-pro
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run application in dev mode
streamlit run app_grok.py --logger.level=debug
```

### Before Committing

```bash
# Format code
black app_grok.py

# Sort imports
isort app_grok.py

# Lint
flake8 app_grok.py

# Type check
mypy app_grok.py

# Run tests
pytest --cov=app_grok --cov-report=term-missing

# Or run all checks via pre-commit
pre-commit run --all-files
```

---

## 📚 Further Reading

- [Streamlit Documentation](https://docs.streamlit.io)
- [LM Studio API Reference](https://lmstudio.ai/docs/api)
- [llama.cpp Documentation](https://github.com/ggerganov/llama.cpp)
- [PEP 8 Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

**Last Updated:** April 2026  
**Version:** 24.36
