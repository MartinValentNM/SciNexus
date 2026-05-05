# Contributing to SciNexus

Děkujeme za váš zájem přispět k SciNexus. Tento dokument obsahuje pravidla a best practices pro přispívání.

## 📋 Obsah

1. [Code of Conduct](#code-of-conduct)
2. [Jak přispět](#jak-přispět)
3. [Hlášení chyb](#hlášení-chyb)
4. [Feature requests](#feature-requests)
5. [Pull requests](#pull-requests)
6. [Vývojové prostředí](#vývojové-prostředí)
7. [Kódovací standardy](#kódovací-standardy)
8. [Testování](#testování)
9. [Dokumentace](#dokumentace)

---

## Code of Conduct

Tento projekt dodržuje [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct. Účastí se zavazujete dodržovat tyto standardy. Prosím hlaste nepřijatelné chování na martin.valent@nm.cz.

**Zásady:**
- Buďte přátelští a respektující
- Vítejte různé pohledy a zkušenosti
- Přijímejte konstruktivní kritiku
- Zaměřte se na to, co je nejlepší pro komunitu

---

## Jak přispět

### Oblasti pro přispění

1. **Kód**
   - Nové funkce
   - Opravy chyb
   - Optimalizace výkonu
   - Refaktoring

2. **Dokumentace**
   - Uživatelské návody
   - API dokumentace
   - Tutoriály a příklady
   - Překlady

3. **Testování**
   - Unit testy
   - Integrační testy
   - Testování různých modelů
   - Benchmarky

4. **Design**
   - UI/UX vylepšení
   - CSS/styling
   - Ikony a grafika

### První kroky

1. **Fork repozitáře**
   ```bash
   # Klikněte na "Fork" tlačítko na GitHubu
   # Pak naklonujte váš fork:
   git clone https://github.com/YOUR_USERNAME/lm-studio-utility-pro.git
   cd lm-studio-utility-pro
   ```

2. **Vytvořte branch**
   ```bash
   git checkout -b feature/amazing-feature
   # nebo
   git checkout -b fix/bug-description
   ```

3. **Nastavte upstream**
   ```bash
   git remote add upstream https://github.com/martin-valent/lm-studio-utility-pro.git
   ```

---

## Hlášení chyb

### Před hlášením

1. **Zkontrolujte existující issues** – váš problém už možná někdo nahlásil
2. **Aktualizujte na nejnovější verzi** – chyba už může být opravena
3. **Ověřte v dokumentaci** – řešení už může být popsáno

### Jak nahlásit chybu

**Použijte GitHub Issues s následujícími informacemi:**

```markdown
### Popis chyby
Jasný a stručný popis co je špatně.

### Kroky k reprodukci
1. Jděte na '...'
2. Klikněte na '...'
3. Scrollujte dolů na '...'
4. Vidíte chybu

### Očekávané chování
Co jste očekávali že se stane.

### Skutečné chování
Co se skutečně stalo.

### Screenshots
Pokud relevantní, přidejte screenshots.

### Prostředí
- OS: [např. Ubuntu 22.04, Windows 11, macOS 14]
- Python verze: [např. 3.10.12]
- Streamlit verze: [např. 1.32.0]
- LM Studio verze: [např. 0.4.2]
- Model: [např. Qwen2.5-32B-Instruct-Q4_K_M]
- GPU: [např. RTX 4090 24GB, nebo CPU]

### Dodatečný kontext
Cokoliv dalšího relevantního.

### Logy
```
Vložte relevantní části logu zde
```
```

### Označení priorit

- 🔴 **Critical** – Aplikace nefunguje, ztráta dat
- 🟠 **High** – Hlavní funkce nefunguje
- 🟡 **Medium** – Funkce funguje ale špatně
- 🟢 **Low** – Kosmetické problémy

---

## Feature Requests

### Proces

1. **Otevřete Discussion** místo Issue pro návrhy funkcí
2. **Popište use case** – proč je to užitečné?
3. **Navrhněte implementaci** – jak by to mohlo fungovat?
4. **Diskutujte s komunitou** – získejte feedback

### Šablona

```markdown
### Feature Description
Jasný popis co chcete přidat.

### Problem it Solves
Jaký problém to řeší? Proč je to užitečné?

### Proposed Solution
Jak by to mohlo fungovat?

### Alternatives Considered
Jaké jiné přístupy jste uvažovali?

### Additional Context
Screenshots, mockupy, příklady z jiných aplikací.

### Implementation Ideas (optional)
Pokud máte nápady na implementaci.
```

---

## Pull Requests

### Proces

1. **Fork a clone**
2. **Vytvořte feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commitujte změny**
   ```bash
   git commit -m "feat: add amazing feature"
   ```
   
   Používejte [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` – Nová funkce
   - `fix:` – Oprava chyby
   - `docs:` – Dokumentace
   - `style:` – Formátování, CSS
   - `refactor:` – Refaktoring
   - `perf:` – Optimalizace výkonu
   - `test:` – Testy
   - `chore:` – Build, dependencies

4. **Pushněte branch**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Otevřete Pull Request**
   - Jasný popis co PR dělá
   - Odkazy na related issues
   - Screenshots pro UI změny
   - Checklist (viz níže)

### PR Checklist

```markdown
- [ ] Kód dodržuje projekt coding style
- [ ] Přidány/aktualizovány testy
- [ ] Všechny testy procházejí
- [ ] Dokumentace aktualizována
- [ ] CHANGELOG.md aktualizován
- [ ] Commit messages jsou v Conventional Commits formátu
- [ ] PR je proti `main` branchi
- [ ] Změny jsou backwards compatible (nebo dokumentovány)
```

### PR Review Process

1. **Automated checks**
   - Linting (flake8, black)
   - Type checking (mypy)
   - Tests (pytest)

2. **Code review**
   - Minimálně 1 reviewer
   - Komentáře konstruktivní
   - Změny lze requestovat

3. **Merge**
   - Squash & merge (čisté history)
   - Delete branch po merge

---

## Vývojové prostředí

### Setup

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/lm-studio-utility-pro.git
cd lm-studio-utility-pro

# Vytvořte virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Nainstalujte dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Dev dependencies

# Nastavte pre-commit hooks
pre-commit install
```

### Dev dependencies

```txt
# requirements-dev.txt
black==24.3.0          # Code formatter
flake8==7.0.0          # Linter
mypy==1.9.0            # Type checker
pytest==8.1.1          # Testing framework
pytest-cov==5.0.0      # Coverage
pre-commit==3.6.2      # Git hooks
```

### Spuštění aplikace

```bash
# Základní spuštění
streamlit run app_grok.py

# Debug mode
streamlit run app_grok.py --logger.level=debug

# S custom portem
streamlit run app_grok.py --server.port=8502
```

---

## Kódovací standardy

### Python Style Guide

Následujeme [PEP 8](https://pep8.org/) s několika úpravami:

```python
# ✅ Správně
def extract_taxa_from_text(text: str, min_length: int = 2) -> List[str]:
    """
    Extract taxonomic names from text.
    
    Args:
        text: Input text to search
        min_length: Minimum word count for taxon name
        
    Returns:
        List of unique taxonomic names
        
    Example:
        >>> extract_taxa_from_text("Hyolithes communis found in...")
        ['Hyolithes communis']
    """
    taxa = []
    # Implementation...
    return taxa

# ❌ Špatně
def extract(t,m=2):
    r=[]
    # Implementation...
    return r
```

### Naming Conventions

```python
# Funkce a proměnné: snake_case
def validate_taxon_name(taxon: str) -> Dict:
    user_input = st.text_input("Taxon")
    
# Třídy: PascalCase
class TaxonValidator:
    pass
    
# Konstanty: UPPER_CASE
MAX_CONCURRENT_REQUESTS = 4
DEFAULT_TEMPERATURE = 0.1

# Private: _prefix
def _internal_helper(data):
    pass
```

### Type Hints

**Vždy používejte type hints:**

```python
from typing import List, Dict, Optional, Union, Tuple

def chat_completion(
    base_url: str,
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 4000,
    stop: Optional[List[str]] = None
) -> str:
    """Function with proper type hints."""
    # Implementation...
    return "result"
```

### Docstrings

**Google style docstrings:**

```python
def validate_taxon_name(
    taxon: str,
    databases: List[str],
    cache: Dict,
    timeout: int = 10
) -> Dict:
    """
    Validates taxonomic name in selected databases.
    
    This function queries multiple biological databases in parallel
    to verify if a taxonomic name exists and is valid. Results are
    cached to speed up repeated queries.
    
    Args:
        taxon: Taxonomic name to validate (e.g., "Hyolithes communis")
        databases: List of database codes to query
        cache: SQLite cache dictionary (shared between calls)
        timeout: HTTP request timeout in seconds
        
    Returns:
        Dictionary with validation results:
        {
            "taxon": str,
            "summary": {"found": int, "confidence": str, "rank": str},
            "results": {"paleodb": {...}, "gbif": {...}, ...}
        }
        
    Raises:
        ValueError: If taxon is empty or databases list is empty
        ConnectionError: If all database queries fail
        
    Example:
        >>> result = validate_taxon_name(
        ...     "Hyolithes communis",
        ...     ["paleodb", "gbif"],
        ...     cache={}
        ... )
        >>> result["summary"]["found"]
        2
        
    Note:
        Results are cached for 30 days to reduce API load.
        Use clear_validation_cache() to invalidate.
    """
    # Implementation...
```

### Error Handling

```python
# ✅ Správně - specifické exceptions
try:
    result = chat_completion(base_url, model, messages)
except ConnectionError as e:
    st.error(f"Cannot connect to LM Studio: {e}")
    return None
except JSONDecodeError as e:
    st.error(f"Invalid response from LLM: {e}")
    return None
except Exception as e:
    st.error(f"Unexpected error: {e}")
    logger.exception("Unexpected error in chat_completion")
    return None

# ❌ Špatně - broad exception
try:
    result = chat_completion(base_url, model, messages)
except:  # Too broad, silent failure
    return None
```

### Code Organization

```python
# Struktura souboru:
# 1. Imports (stdlib → third-party → local)
import json
import re
from pathlib import Path
from typing import List, Dict

import streamlit as st
import requests
from bs4 import BeautifulSoup

from utils import normalize_text
from config import DATABASE_URLS

# 2. Constants
MAX_WORKERS = 8
DEFAULT_TIMEOUT = 10

# 3. Helper functions (private)
def _parse_response(html: str) -> Dict:
    """Private helper function."""
    pass

# 4. Public API functions
def validate_taxon_name(taxon: str) -> Dict:
    """Public function."""
    pass

# 5. Main execution (if __name__ == "__main__")
if __name__ == "__main__":
    main()
```

---

## Testování

### Spuštění testů

```bash
# Všechny testy
pytest

# S coverage reportem
pytest --cov=app_grok --cov-report=html

# Pouze konkrétní test
pytest tests/test_validation.py::test_paleodb_query

# Verbose mode
pytest -v

# Stop on first failure
pytest -x
```

### Psaní testů

```python
# tests/test_validation.py
import pytest
from app_grok import validate_taxon_name, extract_taxa_from_text

def test_extract_taxa_simple():
    """Test basic taxon extraction."""
    text = "Hyolithes communis and Gompholites were found."
    taxa = extract_taxa_from_text(text)
    assert "Hyolithes communis" in taxa
    assert "Gompholites" in taxa
    assert len(taxa) == 2

def test_extract_taxa_empty():
    """Test extraction from empty text."""
    assert extract_taxa_from_text("") == []
    assert extract_taxa_from_text("   ") == []

def test_validate_taxon_cache():
    """Test cache usage in validation."""
    cache = {}
    
    # First call - cache miss
    result1 = validate_taxon_name("Hyolithes", ["paleodb"], cache)
    assert len(cache) == 1
    
    # Second call - cache hit
    result2 = validate_taxon_name("Hyolithes", ["paleodb"], cache)
    assert result1 == result2
    assert len(cache) == 1  # No new entries

@pytest.mark.parametrize("taxon,expected_found", [
    ("Hyolithes communis", True),
    ("InvalidTaxonXYZ123", False),
    ("Alnus", True),
])
def test_validate_multiple_taxa(taxon, expected_found):
    """Test validation for multiple taxa."""
    result = validate_taxon_name(taxon, ["paleodb", "gbif"], {})
    assert (result["summary"]["found"] > 0) == expected_found
```

### Test Coverage

**Cíl: >80% coverage**

```bash
# Generate coverage report
pytest --cov=app_grok --cov-report=term-missing

# View HTML report
pytest --cov=app_grok --cov-report=html
open htmlcov/index.html
```

---

## Dokumentace

### Co dokumentovat

1. **API funkce** – všechny public funkce musí mít docstrings
2. **Složité algoritmy** – vysvětlete logiku
3. **Neobvyklá rozhodnutí** – proč něco děláte tímto způsobem
4. **Workarounds** – pokud obcházíte bug nebo limitaci

### Formát dokumentace

```python
def complex_algorithm(data: List[str], threshold: float = 0.85) -> List[List[str]]:
    """
    Brief description in one line.
    
    Longer description if needed. Explain what the function does,
    why it exists, and any important context.
    
    Args:
        data: Input data with detailed description
        threshold: Similarity threshold (0.0-1.0)
        
    Returns:
        List of grouped items based on similarity
        
    Raises:
        ValueError: If threshold is out of range
        
    Example:
        >>> data = ["item1", "item2", "item3"]
        >>> groups = complex_algorithm(data, threshold=0.9)
        >>> len(groups)
        2
        
    Note:
        Uses Levenshtein distance with prefix indexing optimization.
        See: https://en.wikipedia.org/wiki/Levenshtein_distance
        
    Warning:
        For large datasets (>10k items), consider using approximate
        matching with locality-sensitive hashing instead.
    """
    # Implementation with comments explaining non-obvious parts
    
    # Prefix indexing optimization - skip 95% of comparisons
    prefix_map = {}
    for item in data:
        prefix = item[:3].lower()
        prefix_map.setdefault(prefix, []).append(item)
    
    # Rest of implementation...
```

### README a návody

- **README.md** – přehled projektu, quick start
- **USER_GUIDE_CZ.md** / **USER_GUIDE_EN.md** – kompletní dokumentace
- **CONTRIBUTING.md** – tento soubor
- **CHANGELOG.md** – seznam změn mezi verzemi

### Aktualizace dokumentace

**Při změně kódu, aktualizujte:**
1. Docstrings
2. Type hints
3. README (pokud je API změna)
4. USER_GUIDE (pokud je user-facing změna)
5. CHANGELOG.md

---

## Licencování

Přispěním do tohoto projektu souhlasíte s tím, že váš kód bude uvolněn pod MIT licencí.

---

## Kontakt

- **GitHub Issues**: https://github.com/martin-valent/lm-studio-utility-pro/issues
- **Discussions**: https://github.com/martin-valent/lm-studio-utility-pro/discussions
- **Email**: martin.valent@nm.cz

---

## Poděkování

Děkujeme všem přispěvatelům! Váš čas a úsilí jsou oceněny. 🙏

---

**Poslední aktualizace:** Duben 2026
