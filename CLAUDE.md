# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
## ✍️ Coding Standards

Ideally, every file should start with a basic header like this:

 * Author: {Your Model Name}
 * Date: {timestamp}  
 * PURPOSE: Verbose details about functionality, integration points, dependencies
## Project Overview

This repository reproduces Poetiq's record-breaking ARC-AGI solver using iterative LLM-based code generation. The system solves abstract reasoning tasks by having LLMs write Python transformation functions, execute them in sandboxes, score the results, and refine solutions through feedback loops.

## Development Commands

### Setup
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Solver
```bash
python main.py
```

Configure API keys in `.env`:
```
GEMINI_API_KEY=...
OPENAI_API_KEY=...
```

## Core Architecture

### Solving Pipeline (Entry Point → Execution)

1. **main.py**: Entry point that loads ARC-AGI challenge datasets, runs tasks in parallel via `asyncio.as_completed()`, scores results against solutions if available, and writes incremental Kaggle-format submissions to `output/submission_<timestamp>.json`

2. **solve.py → solve_parallel_coding.py**: Orchestrates multiple expert solvers running concurrently. Each expert is a separate `solve_coding()` instance with its own config. Results are aggregated using a voting system that:
   - Groups solutions by identical test outputs
   - Ranks by vote count (majority consensus)
   - Applies tie-breaking via iteration count or soft scores
   - Returns diversity-first ordering (one per group, then remainders)

3. **solve_coding.py**: Implements the iterative refinement loop for a single expert:
   - Sends problem + past solutions to LLM via prompts (see `prompts.py`)
   - Parses generated Python code from markdown code blocks
   - Evaluates code on training examples in sandboxed subprocess
   - Builds feedback showing what failed (shape mismatches, value diffs)
   - Maintains solution pool with scores, feeds best examples back to LLM
   - Returns early if all training examples pass, otherwise returns best result after max iterations

4. **sandbox.py**: Executes user-generated code in isolated subprocess:
   - Writes code to temporary file with wrapper that calls `transform(np.ndarray) -> np.ndarray`
   - Passes input grid via stdin as JSON
   - Enforces timeout (default 1.5s per execution)
   - Returns success/failure and either the JSON output or error message
   - Code has access to numpy and scipy only

5. **llm.py**: Manages LLM API calls via litellm with:
   - Per-model rate limiters (e.g., 1 req/s for most models)
   - Model-specific parameters (reasoning_effort for OpenAI, thinking budget for Anthropic/Gemini)
   - Retry logic with exponential backoff for rate limits
   - Timeout tracking to respect max_total_time and max_total_timeouts per problem
   - Automatic handling of transient errors (rate limits, server errors)

### Configuration System (arc_agi/config.py)

The solver uses `CONFIG_LIST` (list of `ExpertConfig` dicts) to control behavior. Key parameters:

- **LLM settings**: `llm_id`, `solver_temperature`, `request_timeout`, `max_total_timeouts`, `max_total_time`
- **Iteration control**: `max_iterations` (refinement loops), `max_solutions` (feedback examples), `selection_probability` (solution sampling)
- **Voting strategy**: `use_new_voting`, `count_failed_matches`, `iters_tiebreak`, `low_to_high_iters`
- **Prompts**: `solver_prompt`, `feedback_prompt` (from `prompts.py`)
- **Behavior flags**: `shuffle_examples`, `improving_order`, `return_best_result`

Three preset configs are mentioned in comments: Poetiq(Gemini-3-a/b/c) varying `NUM_EXPERTS` from 1 to 8.

### Data Flow

```
Challenge JSON → main.py loads tasks → solve() creates N experts (CONFIG_LIST)
  → Each expert: LLM generates code → sandbox executes → feedback → LLM refines
  → solve_parallel_coding aggregates expert results via voting
  → io.build_kaggle_two_attempts formats top 2 diverse solutions per test
  → main.py writes submission JSON + scores against solutions if available
```

### Key Type Definitions (arc_agi/types.py)

- **ExpertConfig**: Full solver configuration (prompts, LLM, iteration params, voting)
- **ARCAGIResult**: Contains `train_results`, `results` (test), `iteration` number
- **RunResult**: Single execution outcome with `success`, `output`, `soft_score`, `error`, `code`
- **ARCAGISolution**: Stores `code`, `feedback`, `score` for solution pool

### Scoring (arc_agi/scoring.py)

- Kaggle format: up to 2 attempts per test input
- Task score = fraction of test inputs where attempt_1 or attempt_2 matches ground truth exactly
- Training uses soft scoring (pixel-level accuracy) for partial credit during feedback

## Important Implementation Notes

### Modifying Configurations

When changing solver behavior, edit `CONFIG_LIST` in `arc_agi/config.py`. Each config dict is copied per expert, so you can have heterogeneous expert pools by manually constructing the list with different prompts/models/temperatures.

### Running Subsets of Problems

In `main.py`, configure:
- `NUM_PROBLEMS = 5` to run first N problems
- `SELECTED_PROBLEMS = ['b7999b51', 'abc123']` to run specific task IDs
- `DATA_CHALLENGES` and `DATA_SOLUTIONS` paths to switch between arc-prize-2024/2025 or train/eval/test sets

### Prompt Engineering

Prompts are defined in `arc_agi/prompts.py` as template strings with `$$placeholders$$`:
- `$$problem$$` is replaced with formatted training/test examples
- `$$feedback$$` is replaced with past solution attempts + scores
- The solver expects LLM to output code in markdown fence: ` ```python\n...\n``` `

### Sandbox Security

Code executes in subprocess with:
- `PYTHONHASHSEED=0` for reproducibility
- Temporary directory as working dir (deleted after execution)
- Only numpy/scipy imports available
- No network, file system access beyond temp dir
- Process killed if timeout exceeded

### Parallel Execution

The system runs all problems concurrently (`asyncio.create_task` for each) and uses `asyncio.as_completed` to process results as they finish. File handle limits are raised to 65536 in main.py to support large-scale parallelism.

### Output Directory

Results are written to `output/`:
- `submission_<timestamp>.json`: Kaggle submission format
- `config_<timestamp>.json`: Copy of CONFIG_LIST used for reproducibility

## Models Supported

See `arc_agi/types.py` Models literal for current list. Includes:
- OpenAI: gpt-5, gpt-5.1
- Anthropic: claude-sonnet-4-5, claude-haiku-4-5
- Google: gemini-2.5-pro, gemini-3-pro-preview
- xAI: grok-4, grok-4-fast
- Groq: gpt-oss-120b

Model routing is handled by litellm. API keys must be set in `.env` as `<PROVIDER>_API_KEY`.
