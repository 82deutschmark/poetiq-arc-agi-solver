"""ARC-2 evaluation runner for a fixed subset of problems.

Author: Cascade
Date: 2025-11-24
PURPOSE: Run a fixed subset of ARC-2 evaluation problems using the existing
Poetiq/ARC solver stack and default Gemini-based configuration. Reads the
ARC-2 2025 evaluation JSONs, invokes `solve` for each selected problem ID,
computes scores with `score_task`, and writes Kaggle-style predictions via
`build_kaggle_two_attempts` into `output/arc2_eval_subset`.
"""

import asyncio
import json
import os
import time
from datetime import datetime

from dotenv import load_dotenv

from arc_agi.io import build_kaggle_two_attempts
from arc_agi.scoring import score_task
from arc_agi.solve import solve


HERE = os.path.dirname(__file__)

DATA_CHALLENGES_2025_EVAL = os.path.join(
    HERE,
    "data",
    "arc-prize-2025",
    "arc-agi_evaluation_challenges.json",
)
DATA_SOLUTIONS_2025_EVAL = os.path.join(
    HERE,
    "data",
    "arc-prize-2025",
    "arc-agi_evaluation_solutions.json",
)

TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_DIR = os.path.join(HERE, "output", "arc2_eval_subset")

PREDICTIONS_PATH = os.path.join(OUTPUT_DIR, f"submission_{TIMESTAMP}.json")
LOG_PATH = os.path.join(OUTPUT_DIR, f"log_{TIMESTAMP}.txt")

# The specific ARC-2 evaluation task IDs to run
SELECTED_PROBLEMS: list[str] = [
    "65b59efc",
    "e3721c99",
    "dd6b8c4b",
    "2ba387bc",
    "14754a24",
    "b457fec5",
    "891232d6",
    "7b5033c1",
    "981571dc",
    "136b0064",
]


async def run() -> None:
    """Run the solver on a fixed subset of ARC-2 evaluation tasks."""
    load_dotenv()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(DATA_CHALLENGES_2025_EVAL, "r", encoding="utf-8") as f:
        challenges_blob: dict[str, dict] = json.load(f)

    solutions_blob: dict[str, list] | None = None
    if os.path.exists(DATA_SOLUTIONS_2025_EVAL):
        with open(DATA_SOLUTIONS_2025_EVAL, "r", encoding="utf-8") as f:
            solutions_blob = json.load(f)

    submission: dict[str, list[dict]] = {}

    for task_id in SELECTED_PROBLEMS:
        task = challenges_blob.get(task_id)
        if task is None:
            print(f"! {task_id}: not found in evaluation challenges")
            continue

        train = task.get("train", [])
        test = task.get("test", [])
        train_in = [ex["input"] for ex in train]
        train_out = [ex["output"] for ex in train]
        test_in = [ex["input"] for ex in test]

        print(f"\n=== {task_id} (eval subset) ===")
        start = time.time()
        try:
            results = await solve(train_in, train_out, test_in, problem_id=task_id)
        except asyncio.CancelledError as exc:
            print(
                f"{task_id}: LLM request was cancelled "
                f"(network timeout, cancellation, or interrupt): {exc}"
            )
            return
        except Exception as exc:
            print(f"{task_id}: ERROR while solving task: {exc}")
            return

        elapsed = time.time() - start

        preds = build_kaggle_two_attempts(results, test_in)
        submission[task_id] = preds

        if solutions_blob is not None:
            gt_outputs = solutions_blob.get(task_id)
        else:
            gt_outputs = None

        if gt_outputs is not None:
            task_score = score_task(preds, gt_outputs)
            print(f"Score: {task_score:.3f}")
        else:
            task_score = None
            print("Score: N/A (no ground truth solutions)")

        print(f"Time: {elapsed:.1f}s")

        try:
            with open(LOG_PATH, "a", encoding="utf-8") as log_f:
                if task_score is None:
                    score_str = "NA"
                else:
                    score_str = f"{task_score:.6f}"
                log_f.write(
                    f"{task_id}\tscore={score_str}\ttime={elapsed:.3f}s\n"
                )
        except Exception as e:
            print(f"WARNING: Failed to write log entry for {task_id}: {e}")

    try:
        with open(PREDICTIONS_PATH, "w", encoding="utf-8") as f:
            json.dump(submission, f)
        print(f"\nWrote predictions to {PREDICTIONS_PATH}")
        print(f"Wrote log to {LOG_PATH}")
    except Exception as e:
        print(f"ERROR: Failed to write predictions to {PREDICTIONS_PATH}: {e}")


if __name__ == "__main__":
    asyncio.run(run())
