/**
 * Author: Cascade (Claude Opus 4.5)
 * Date: 2025-11-25T16:52:00-05:00
 * PURPOSE: Comprehensive status report of all 120 ARC Prize 2025 puzzles.
 *          Documents which puzzles have been tested, their results, and
 *          which remain untested for future runs.
 * SRP and DRY check: Pass - Standalone documentation file.
 */

# ARC Prize 2025 - Puzzle Status Report
## Date: 2025-11-25

---

## Overview

| Metric | Count |
|--------|-------|
| Total puzzles in dataset | 120 |
| Tested | 26 |
| Untested | 94 |

---

## Scoring Definitions

The scoring system works as follows:

- **Each puzzle** may have 1 or more test cases
- **Each test case** gets 2 attempts (attempt_1, attempt_2)
- **A test case is correct** if either attempt matches the ground truth exactly
- **Score** = (correct test cases) / (total test cases)

### Result Categories

| Category | Definition |
|----------|------------|
| **PASS** | Score = 1.0 — All test cases solved correctly |
| **PARTIAL** | 0 < Score < 1.0 — Some but not all test cases solved |
| **FAIL** | Score = 0.0 with valid attempts — Model tried but couldn't solve |
| **ERROR** | No valid attempts recorded — Infrastructure/API error prevented attempt |

---

## Tested Puzzles (26)

### PASS (9 puzzles)

These puzzles were completely solved correctly.

| Puzzle ID | Score | Run |
|-----------|-------|-----|
| 136b0064 | 1.00 | Run 1 |
| 16de56c4 | 1.00 | Run 1 |
| 1818057f | 1.00 | Run 1 |
| d8e07eb2 | 1.00 | Run 2 |
| db0c5428 | 1.00 | Run 2 |
| e3721c99 | 1.00 | Run 2 |
| e376de54 | 1.00 | Run 2 |
| e8686506 | 1.00 | Run 2 |
| f931b4a8 | 1.00 | Run 2 |

### PARTIAL (2 puzzles)

These puzzles had some test cases solved correctly.

| Puzzle ID | Score | Notes |
|-----------|-------|-------|
| 1ae2feb7 | 0.67 | 2 of 3 test cases correct |
| dd6b8c4b | 0.50 | 1 of 2 test cases correct |

### FAIL (14 puzzles)

Model made valid attempts but could not solve any test cases.

| Puzzle ID | Run | Known Issues |
|-----------|-----|--------------|
| 0934a4d8 | Run 1 | Multiple timeouts during solve |
| 135a2760 | Run 1 | Multiple timeouts during solve |
| 13e47133 | Run 1 | **500 Internal Server Errors** from Gemini API |
| 142ca369 | Run 1 | Exhausted all 6 timeouts, early exit |
| 16b78196 | Run 1 | — |
| 195c6913 | Run 1 | Multiple timeouts during solve |
| db695cfb | Run 2 | — |
| dbff022c | Run 2 | — |
| dfadab01 | Run 2 | — |
| e12f9a14 | Run 2 | — |
| edb79dae | Run 2 | — |
| eee78d87 | Run 2 | — |
| faa9f03d | Run 2 | — |
| fc7cae8d | Run 2 | — |

### ERROR (1 puzzle)

Infrastructure error prevented valid attempt.

| Puzzle ID | Error Type | Details |
|-----------|------------|---------|
| de809cff | Windows PermissionError | Temp file cleanup failed; `sandbox.py` issue (now fixed) |

---

## Untested Puzzles (94)

These puzzles have not been attempted yet.

```python
UNTESTED_PUZZLES = [
    '20270e3b', '20a9e565', '21897d95', '221dfab4', '247ef758',
    '269e22fb', '271d71e2', '28a6681f', '291dc1e1', '2b83f449',
    '2ba387bc', '2c181942', '2d0172a1', '31f7f899', '332f06d7',
    '35ab12c3', '36a08778', '38007db0', '3a25b0d8', '3dc255db',
    '3e6067c3', '409aa875', '446ef5d2', '45a5af55', '4a21e3da',
    '4c3d4a41', '4c416de3', '4c7dc4dd', '4e34c42c', '53fb4810',
    '5545f144', '581f7754', '58490d8a', '58f5dbd5', '5961cc34',
    '5dbc8537', '62593bfd', '64efde09', '65b59efc', '67e490f4',
    '6e453dd6', '6e4f6532', '6ffbe589', '71e489b6', '7491f3cf',
    '7666fa5d', '78332cb0', '7b0280bc', '7b3084d4', '7b5033c1',
    '7b80bb43', '7c66cb00', '7ed72f31', '800d221b', '80a900e0',
    '8698868d', '88bcf3b4', '88e364bc', '89565ca0', '898e7135',
    '8b7bacbf', '8b9c3697', '8e5c0c38', '8f215267', '8f3a5a89',
    '9385bd28', '97d7923e', '981571dc', '9aaea919', '9bbf930d',
    'a251c730', 'a25697e4', 'a32d8b75', 'a395ee82', 'a47bf94d',
    'a6f40cea', 'aa4ec2a5', 'abc82100', 'b0039139', 'b10624e5',
    'b5ca7ac4', 'b6f77b65', 'b99e7126', 'b9e38dc0', 'bf45cf4b',
    'c4d067a0', 'c7f57c3e', 'cb2d8a2c', 'cbebaa4b', 'd35bdbdc',
    'd59b0160', 'da515329', 'e87109e9', 'f560132c',
]
```

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total tested | 26 |
| PASS | 9 (34.6% of tested) |
| PARTIAL | 2 (7.7% of tested) |
| FAIL | 14 (53.8% of tested) |
| ERROR | 1 (3.8% of tested) |
| **Total score** | **10.17 / 25** |
| **Accuracy** | **40.7%** (on 25 valid attempts) |

---

## Known Issues and Fixes

### 1. Gemini 500 Internal Server Errors

- **Affected**: Puzzle 13e47133 (Run 1)
- **Cause**: Gemini API returned HTTP 500 errors
- **Behavior**: Upstream code retries without counting against retry budget
- **Status**: Not fixable on our end; API stability issue

### 2. Gemini 429 Quota Exhaustion

- **Affected**: Run 2 (puzzles after #10 never completed)
- **Cause**: Daily API quota exceeded
- **Behavior**: Upstream code retries indefinitely; run never terminates
- **Status**: Requires new API key or waiting for quota reset

### 3. Windows PermissionError in sandbox.py

- **Affected**: Puzzle de809cff
- **Cause**: `tempfile.TemporaryDirectory()` cleanup fails when subprocess holds file handles
- **Fix Applied**: Added `ignore_cleanup_errors=True` to `sandbox.py` line 15
- **Status**: FIXED

---

## Instructions for Next Run

### Step 1: Update main.py

Set `SELECTED_PROBLEMS` to the untested puzzle list:

```python
# In main.py, replace SELECTED_PROBLEMS with:
SELECTED_PROBLEMS = [
    '20270e3b', '20a9e565', '21897d95', '221dfab4', '247ef758',
    '269e22fb', '271d71e2', '28a6681f', '291dc1e1', '2b83f449',
    '2ba387bc', '2c181942', '2d0172a1', '31f7f899', '332f06d7',
    '35ab12c3', '36a08778', '38007db0', '3a25b0d8', '3dc255db',
    '3e6067c3', '409aa875', '446ef5d2', '45a5af55', '4a21e3da',
    '4c3d4a41', '4c416de3', '4c7dc4dd', '4e34c42c', '53fb4810',
    '5545f144', '581f7754', '58490d8a', '58f5dbd5', '5961cc34',
    '5dbc8537', '62593bfd', '64efde09', '65b59efc', '67e490f4',
    '6e453dd6', '6e4f6532', '6ffbe589', '71e489b6', '7491f3cf',
    '7666fa5d', '78332cb0', '7b0280bc', '7b3084d4', '7b5033c1',
    '7b80bb43', '7c66cb00', '7ed72f31', '800d221b', '80a900e0',
    '8698868d', '88bcf3b4', '88e364bc', '89565ca0', '898e7135',
    '8b7bacbf', '8b9c3697', '8e5c0c38', '8f215267', '8f3a5a89',
    '9385bd28', '97d7923e', '981571dc', '9aaea919', '9bbf930d',
    'a251c730', 'a25697e4', 'a32d8b75', 'a395ee82', 'a47bf94d',
    'a6f40cea', 'aa4ec2a5', 'abc82100', 'b0039139', 'b10624e5',
    'b5ca7ac4', 'b6f77b65', 'b99e7126', 'b9e38dc0', 'bf45cf4b',
    'c4d067a0', 'c7f57c3e', 'cb2d8a2c', 'cbebaa4b', 'd35bdbdc',
    'd59b0160', 'da515329', 'e87109e9', 'f560132c',
]

# Set NUM_PROBLEMS to limit how many to run (or None for all 94)
NUM_PROBLEMS = None  # or set to 20, 30, etc. based on quota
```

### Step 2: Ensure new API key is configured

Update `.env` with the new Gemini API key.

### Step 3: Run

```bash
python main.py
```

### Step 4: After run completes

Run `python analyze_results.py` to generate updated status report.

---

*Report generated by analyze_results.py*
