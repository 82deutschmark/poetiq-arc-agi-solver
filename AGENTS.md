# Repository Guidelines
## ✍️ Coding Standards

Ideally, every file should start with a basic header like this:

 * Author: {Your Model Name}
 * Date: {timestamp}  
 * PURPOSE: Verbose details about functionality, integration points, dependencies
## Project Structure & Module Organization
- `main.py`: Entry point. Adjust `NUM_PROBLEMS`, `SELECTED_PROBLEMS`, and data file paths to switch between `data/arc-prize-2024` and `data/arc-prize-2025`.
- `arc_agi/`: Core library
  - `config.py` (LLM/solver parameters), `solve.py`/`solve_parallel_coding.py` (orchestration), `solve_coding.py` (experts), `llm.py` (LiteLLM wrapper), `sandbox.py` (safe code exec), `io.py` (Kaggle formatting), `scoring.py` (metrics), `prompts.py` (prompt text), `types.py` (TypedDicts).
- `data/arc-prize-20xx/`: Challenge/solution JSONs (read-only).
- `requirements.txt`: Python deps. `output/` is generated and git‑ignored.

## Build, Test, and Development Commands
- Create venv and install deps:
  - Unix: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
  - Windows: `python -m venv .venv; .\.venv\Scripts\activate; pip install -r requirements.txt`
- Configure API keys in `.env` (never commit):
  - `GEMINI_API_KEY=...`, `OPENAI_API_KEY=...`
- Run locally: `python main.py` (writes `output/config_*.json` and `output/submission_*.json`).

## Coding Style & Naming Conventions
- Python 3.11+, follow PEP 8, 4‑space indents, wrap ~100 cols.
- Use type hints and docstrings. Functions/modules: `snake_case`; classes: `PascalCase`; constants: `UPPER_SNAKE_CASE`.
- Keep changes focused; prefer small, pure functions; avoid global side‑effects beyond `config.py`.

## Testing Guidelines
- No test suite exists yet. If adding tests, use `pytest`, place under `tests/`, and name files `test_*.py`.
- Target deterministic units first (`io.py`, `scoring.py`, `utils.py`).
- Example: `pip install pytest && pytest -q`. Aim to cover changed code paths.

## Commit & Pull Request Guidelines
- Commits: imperative, present tense; concise subject (≤72 chars). Include context in body; reference issues with `#123`.
- Pull Requests: summary of what/why, linked issues, steps to reproduce (command used), and a snippet/path to produced artifacts (e.g., `output/submission_YYYY-MM-DD_HH-MM-SS.json`). Note any `config.py` or `.env` changes.

## Security & Configuration Tips
- Never commit secrets or `output/`. Data files are large—avoid editing them.
- Model IDs are LiteLLM‑style (e.g., `gemini/gemini-3-pro-preview`). Tune solver/LLM settings in `arc_agi/config.py`; avoid changing global rate limits in `arc_agi/llm.py` without justification.
