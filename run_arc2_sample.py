"""ARC-2 training runner using the default Poetiq/Gemini solver.

Author: Cascade
Date: 2025-11-22
PURPOSE: Run a small subset of ARC-2 training problems using the existing
Poetiq/ARC solver stack and default Gemini-based configuration. Reads ARC-2
training JSONs, invokes `solve`, scores predictions with `score_task`, and
writes Kaggle-style predictions via `build_kaggle_two_attempts` into the
`output/arc2_gemini` directory.
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
DATA_CHALLENGES_2025 = os.path.join(
    HERE,
    "data",
    "arc-prize-2025",
    "arc-agi_training_challenges.json",
)
DATA_SOLUTIONS_2025 = os.path.join(
    HERE,
    "data",
    "arc-prize-2025",
    "arc-agi_training_solutions.json",
)

TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_DIR = os.path.join(HERE, "output", "arc2_gemini")

PREDICTIONS_PATH = os.path.join(OUTPUT_DIR, f"submission_{TIMESTAMP}.json")
LOG_PATH = os.path.join(OUTPUT_DIR, f"log_{TIMESTAMP}.txt")

# The specific ARC-2 training task IDs to run
SELECTED_PROBLEMS: list[str] = [
    "dc2e9a9d",
    "8b28cd80",
    "7d419a02",
    "4ff4c9da",
    "477d2879",
]


async def run() -> None:
    load_dotenv()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    gemini_key = os.getenv('GEMINI_API_KEY')
    if not gemini_key:
        print(
            'ERROR: GEMINI_API_KEY is not set. '
            'Please configure it in your environment or .env before running this script.'
        )
        return

    with open(DATA_CHALLENGES_2025, "r", encoding="utf-8") as f:
        challenges_blob: dict[str, dict] = json.load(f)

    with open(DATA_SOLUTIONS_2025, "r", encoding="utf-8") as f:
        solutions_blob: dict[str, list] = json.load(f)
    submission: dict[str, list[dict]] = {}

    for task_id in SELECTED_PROBLEMS:
        task = challenges_blob.get(task_id)
        if task is None:
            print(f"! {task_id}: not found in training challenges")
            continue

        train = task.get("train", [])
        test = task.get("test", [])
        train_in = [ex["input"] for ex in train]
        train_out = [ex["output"] for ex in train]
        test_in = [ex["input"] for ex in test]

        print(f"\n=== {task_id} ===")
        start = time.time()
        try:
            results = await solve(train_in, train_out, test_in, problem_id=task_id)
        except asyncio.CancelledError as exc:
            print(
                f'{task_id}: LLM request was cancelled '
                f'(network timeout, cancellation, or interrupt): {exc}'
            )
            return
        except Exception as exc:
            print(f'{task_id}: ERROR while calling Gemini model: {exc}')
            return
        elapsed = time.time() - start

        preds = build_kaggle_two_attempts(results, test_in)
        submission[task_id] = preds

        gt_outputs = solutions_blob.get(task_id)
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
