"""
Author: Cascade (Claude Sonnet 4)
Date: 2025-11-25
PURPOSE: Analyze test results and generate comprehensive status report.
         Outputs tested/untested puzzle lists and categorized results.
SRP and DRY check: Pass - Standalone analysis script.
"""

import json
from pathlib import Path

# Load all data
BASE = Path(__file__).parent
solutions = json.load(open(BASE / 'data/arc-prize-2025/arc-agi_evaluation_solutions.json'))
challenges = json.load(open(BASE / 'data/arc-prize-2025/arc-agi_evaluation_challenges.json'))
all_ids = sorted(challenges.keys())

# Load submission files
sub1 = json.load(open(BASE / 'output/submission_2025-11-25_11-31-40.json'))
sub2 = json.load(open(BASE / 'output/submission_2025-11-25_15-01-00.json'))
merged = {**sub1, **sub2}

def score_puzzle(preds, gt_outputs):
    """Score a puzzle: fraction of test cases correct."""
    if not gt_outputs or not preds:
        return 0.0
    correct = 0
    for i, gt in enumerate(gt_outputs):
        if i >= len(preds):
            continue
        pack = preds[i] or {}
        a1 = pack.get('attempt_1')
        a2 = pack.get('attempt_2')
        if (a1 is not None and a1 == gt) or (a2 is not None and a2 == gt):
            correct += 1
    return correct / max(len(gt_outputs), 1)

def has_data(preds):
    """Check if predictions contain actual data (not empty/error)."""
    if not preds:
        return False
    return any(p.get('attempt_1') or p.get('attempt_2') for p in preds)

# Categorize results
tested_ids = set(merged.keys())
untested_ids = sorted(set(all_ids) - tested_ids)

results = {
    'PASS': [],      # score = 1.0
    'PARTIAL': [],   # 0 < score < 1.0
    'FAIL': [],      # score = 0 but has data (model couldn't solve)
    'ERROR': [],     # score = 0 and no data (infrastructure error)
}

for pid in sorted(tested_ids):
    preds = merged[pid]
    gt = solutions.get(pid, [])
    score = score_puzzle(preds, gt)
    
    if score == 1.0:
        results['PASS'].append((pid, score))
    elif score > 0:
        results['PARTIAL'].append((pid, score))
    elif has_data(preds):
        results['FAIL'].append((pid, score))
    else:
        results['ERROR'].append((pid, score))

# Print report
print("=" * 70)
print("ARC PRIZE 2025 - PUZZLE STATUS REPORT")
print("=" * 70)
print()
print(f"Total puzzles in dataset: {len(all_ids)}")
print(f"Tested: {len(tested_ids)}")
print(f"Untested: {len(untested_ids)}")
print()

print("-" * 70)
print("RESULTS BY CATEGORY")
print("-" * 70)
print()

print(f"PASS ({len(results['PASS'])} puzzles) - All test cases solved correctly:")
for pid, score in results['PASS']:
    print(f"  {pid}")
print()

print(f"PARTIAL ({len(results['PARTIAL'])} puzzles) - Some test cases solved:")
for pid, score in results['PARTIAL']:
    print(f"  {pid} (score={score:.2f})")
print()

print(f"FAIL ({len(results['FAIL'])} puzzles) - Model attempted but couldn't solve:")
for pid, score in results['FAIL']:
    print(f"  {pid}")
print()

print(f"ERROR ({len(results['ERROR'])} puzzles) - Infrastructure error, no valid attempt:")
for pid, score in results['ERROR']:
    print(f"  {pid}")
print()

print("-" * 70)
print("UNTESTED PUZZLES (94 remaining)")
print("-" * 70)
print()
print("Copy this list into SELECTED_PROBLEMS in main.py:")
print()
print("UNTESTED_IDS = [")
for pid in untested_ids:
    print(f"    '{pid}',")
print("]")
print()

# Summary stats
total_score = sum(s for _, s in results['PASS']) + sum(s for _, s in results['PARTIAL'])
total_attempted = len(results['PASS']) + len(results['PARTIAL']) + len(results['FAIL'])
print("-" * 70)
print("SUMMARY")
print("-" * 70)
print(f"Successfully solved (PASS): {len(results['PASS'])}")
print(f"Partially solved (PARTIAL): {len(results['PARTIAL'])}")
print(f"Failed to solve (FAIL): {len(results['FAIL'])}")
print(f"Errors (ERROR): {len(results['ERROR'])}")
print(f"Total score: {total_score:.2f} / {total_attempted}")
print(f"Accuracy on attempted: {total_score/total_attempted*100:.1f}%" if total_attempted > 0 else "N/A")
