# Contributing to SciNexus

Thank you for your interest in contributing to SciNexus. This document contains guidelines and best practices for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)
- [Pull Requests](#pull-requests)
- [Development Environment](#development-environment)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct. By participating, you agree to uphold these standards. Please report unacceptable behavior to martin.valent@nm.cz.

**Principles:**

- Be friendly and respectful
- Welcome diverse perspectives and experiences
- Accept constructive criticism
- Focus on what is best for the community

## How to Contribute

### Areas for Contribution

- **Code**
  - New features
  - Bug fixes
  - Performance optimization
  - Refactoring
- **Documentation**
  - User guides
  - API documentation
  - Tutorials and examples
  - Translations
- **Testing**
  - Unit tests
  - Integration tests
  - Testing different models
  - Benchmarks
- **Design**
  - UI/UX improvements
  - CSS/styling
  - Icons and graphics

### First Steps

- **Fork the repository**

```bash
# Click the "Fork" button on GitHub
# Then clone your fork:
git clone https://github.com/YOUR_USERNAME/lm-studio-utility-pro.git
cd lm-studio-utility-pro
```

- **Create a branch**

```bash
git checkout -b feature/amazing-feature
# or
git checkout -b fix/bug-description
```

- **Set up upstream**

```bash
git remote add upstream https://github.com/martin-valent/lm-studio-utility-pro.git
```

## Reporting Bugs

### Before Reporting

- **Check existing issues** – your problem may already have been reported
- **Update to the latest version** – the bug may already be fixed
- **Check the documentation** – the solution may already be described

### How to Report a Bug

**Use GitHub Issues with the following information:**

```markdown
### Bug Description
A clear and concise description of what is wrong.

### Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See the error

### Expected Behavior
What you expected to happen.

### Actual Behavior
What actually happened.

### Screenshots
If relevant, add screenshots.

### Environment
- OS: [e.g. Ubuntu 22.04, Windows 11, macOS 14]
- Python version: [e.g. 3.10.12]
- Streamlit version: [e.g. 1.32.0]
- LM Studio version: [e.g. 0.4.2]
- Model: [e.g. Qwen2.5-32B-Instruct-Q4_K_M]
- GPU: [e.g. RTX 4090 24GB, or CPU]

### Additional Context
Anything else that is relevant.

### Logs
Paste the relevant parts of the log here.
```

### Priority Labels

- 🔴 **Critical** – Application does not work, data loss
- 🟠 **High** – A major feature does not work
- 🟡 **Medium** – A feature works, but incorrectly
- 🟢 **Low** – Cosmetic issues

## Feature Requests

### Process

- **Open a Discussion** instead of an Issue for feature proposals
- **Describe the use case** – why is it useful?
- **Propose an implementation** – how could it work?
- **Discuss with the community** – get feedback

### Template

```markdown
### Feature Description
A clear description of what you want to add.

### Problem it Solves
What problem does it solve? Why is it useful?

### Proposed Solution
How could it work?

### Alternatives Considered
What other approaches did you consider?

### Additional Context
Screenshots, mockups, examples from other applications.

### Implementation Ideas (optional)
If you have ideas for implementation.
```

## Pull Requests

### Process

- **Fork and clone**
- **Create a feature branch**

```bash
git checkout -b feature/your-feature-name
```

- **Commit your changes**

```bash
git commit -m "feat: add amazing feature"
```

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` – New feature
- `fix:` – Bug fix
- `docs:` – Documentation
- `style:` – Formatting, CSS
- `refactor:` – Refactoring
- `perf:` – Performance optimization
- `test:` – Tests
- `chore:` – Build, dependencies

- **Push the branch**

```bash
git push origin feature/your-feature-name
```

- **Open a Pull Request**
  - Clear description of what the PR does
  - Links to related issues
  - Screenshots for UI changes
  - Checklist (see below)

### PR Checklist

- [ ] Code follows the project coding style
- [ ] Tests have been added/updated
- [ ] All tests pass
- [ ] Documentation has been updated
- [ ] CHANGELOG.md has been updated
- [ ] Commit messages are in Conventional Commits format
- [ ] PR targets the `main` branch
- [ ] Changes are backward compatible (or documented)

### PR Review Process

- **Automated checks**
  - Linting (flake8, black)
  - Type checking (mypy)
  - Tests (pytest)
- **Code review**
  - At least 1 reviewer
  - Constructive comments
  - Changes may be requested
- **Merge**
  - Squash & merge (clean history)
  - Delete the branch after merge

## Development Environment

### Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/lm-studio-utility-pro.git
cd lm-studio-utility-pro

# Create a virtual environment
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt # Dev dependencies

# Set up pre-commit hooks
pre-commit install
```

### Dev Dependencies

```txt
# requirements-dev.txt
black==24.3.0 # Code formatter
flake8==7.0.0 # Linter
mypy==1.9.0 # Type checker
pytest==8.1.1 # Testing framework
pytest-cov==5.0.0 # Coverage
pre-commit==3.6.2 # Git hooks
```

### Running the Application

```bash
# Basic run
streamlit run app_grok.py

# Debug mode
streamlit run app_grok.py --logger.level=debug

# With a custom port
streamlit run app_grok.py --server.port=8502
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with a few adjustments:

```python
# ✅ Correct
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

# ❌ Incorrect
def extract(t, m=2):
    r = []
    # Implementation...
    return r
```

### Naming Conventions

```python
# Functions and variables: snake_case
def validate_taxon_name(taxon: str) -> Dict:
    user_input = st.text_input("Taxon")

# Classes: PascalCase
class TaxonValidator:
    pass

# Constants: UPPER_CASE
MAX_CONCURRENT_REQUESTS = 4
DEFAULT_TEMPERATURE = 0.1

# Private: _prefix
def _internal_helper(data):
    pass
```

### Type Hints

**Always use type hints:**

```python
from typing import List, Dict, Optional, Union, Tuple

def chat_completion(
    base_url: str,
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 4000,
    stop: Optional[List[str]] = None,
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
    timeout: int = 10,
) -> Dict:
    """
    Validates a taxonomic name in selected databases.

    This function queries multiple biological databases in parallel
    to verify whether a taxonomic name exists and is valid. Results are
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
            "results": {"paleodb": {...}, "gbif": {...}, ...},
        }

    Raises:
        ValueError: If taxon is empty or the databases list is empty
        ConnectionError: If all database queries fail

    Example:
        >>> result = validate_taxon_name(
        ...     "Hyolithes communis",
        ...     ["paleodb", "gbif"],
        ...     cache={},
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
# ✅ Correct - specific exceptions
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

# ❌ Incorrect - broad exception
try:
    result = chat_completion(base_url, model, messages)
except:  # Too broad, silent failure
    return None
```

### Code Organization

```python
# File structure:
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

## Testing

### Running Tests

```bash
# All tests
pytest

# With coverage report
pytest --cov=app_grok --cov-report=html

# Only a specific test
pytest tests/test_validation.py::test_paleodb_query

# Verbose mode
pytest -v

# Stop on first failure
pytest -x
```

### Writing Tests

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
    assert extract_taxa_from_text(" ") == []


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

**Goal: >80% coverage**

```bash
# Generate coverage report
pytest --cov=app_grok --cov-report=term-missing

# View HTML report
pytest --cov=app_grok --cov-report=html
open htmlcov/index.html
```

## Documentation

### What to Document

- **API functions** – all public functions must have docstrings
- **Complex algorithms** – explain the logic
- **Unusual decisions** – explain why you do something this way
- **Workarounds** – if you are working around a bug or limitation

### Documentation Format

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

### README and Guides

- **README.md** – project overview, quick start
- **USER_GUIDE_CZ.md** / **USER_GUIDE_EN.md** – complete documentation
- **CONTRIBUTING.md** – this file
- **CHANGELOG.md** – list of changes between versions

### Updating Documentation

**When changing code, update:**

- Docstrings
- Type hints
- README (if the API changes)
- USER_GUIDE (if there is a user-facing change)
- CHANGELOG.md

## Licensing

By contributing to this project, you agree that your code will be released under the MIT license.

## Contact

- **GitHub Issues**: [https://github.com/martin-valent/lm-studio-utility-pro/issues](https://github.com/martin-valent/lm-studio-utility-pro/issues)
- **Discussions**: [https://github.com/martin-valent/lm-studio-utility-pro/discussions](https://github.com/martin-valent/lm-studio-utility-pro/discussions)
- **Email**: martin.valent@nm.cz

## Acknowledgments

Thank you to all contributors! Your time and effort are appreciated. 🙏

**Last updated:** April 2026
