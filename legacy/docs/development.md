# Development Guide

Welcome to the AntiRickRoll development team! This guide will help you set up your environment and understand the codebase.

## Repository Structure
- `source/antirickroll/`: The main Python package.
- `tests/`: Unit and integration tests.
- `scripts/`: Build and utility scripts.
- `assets/`: Icons, sounds, and other static resources.
- `docs/`: Technical documentation.

## Setup Instructions

1.  **Clone the Repo:**
    ```bash
    git clone https://github.com/NotZenith/AntiRickRoll.git
    cd AntiRickRoll
    ```

2.  **Environment:**
    We recommend using Python 3.9 or 3.10.
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Dependencies:**
    Install in editable mode with development tools:
    ```bash
    pip install -e .[dev]
    ```

## Coding Standards
We use the following tools to ensure code quality:
- **Ruff:** Linting and sorting imports.
- **Black:** Code formatting.
- **MyPy:** Static type checking.
- **Pytest:** Testing framework.

### Running Quality Checks
```bash
ruff check .
black --check .
mypy source/antirickroll
pytest
```

## Running the App
```bash
# Set PYTHONPATH if necessary, or just run from root if installed as editable
python -m antirickroll.app.main
```
