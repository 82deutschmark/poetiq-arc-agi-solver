/**
 * Author: Cascade (Claude Sonnet 4)
 * Date: 2025-11-25T13:58:00-05:00
 * PURPOSE: Extrapolation analysis from 10-puzzle test run to full 120-puzzle dataset.
 *          Raw findings and projected metrics for ARC Prize 2025 evaluation set.
 * SRP and DRY check: Pass - Standalone documentation file.
 */

# Gemini 3 Pro Preview – 10-Puzzle Test Run
## ARC Prize 2025 Evaluation Set

---

## Key Finding: Gemini 500 Internal Server Errors

- During this 10-puzzle run, the Gemini 3 Pro Preview API returned **multiple 500 Internal Server Errors**.
- Puzzle `13e47133` in particular triggered repeated 500s and exhausted the configured retry logic.
- These failures are **infrastructure / API reliability issues**, not necessarily modeling errors.
- Any interpretation of model performance from this run must be viewed in light of these repeated 500 errors.

---

## Raw Test Data (10 Puzzles)

### Individual Results

| # | Puzzle ID | Result | Time (s) | Time (min) | Score |
|---|-----------|--------|----------|------------|-------|
| 1 | 1818057f | PASS | 120 | 2.0 | 1.00 |
| 2 | 1ae2feb7 | PARTIAL | 226 | 3.8 | 0.67 |
| 3 | 16de56c4 | PASS | 933 | 15.6 | 1.00 |
| 4 | 136b0064 | PASS | 1,965 | 32.8 | 1.00 |
| 5 | 13e47133 | FAIL | 1,993 | 33.2 | 0.00 |
| 6 | 16b78196 | FAIL | 2,180 | 36.3 | 0.00 |
| 7 | 0934a4d8 | FAIL | 3,880 | 64.7 | 0.00 |
| 8 | 135a2760 | FAIL | 5,454 | 90.9 | 0.00 |
| 9 | 195c6913 | FAIL | 7,173 | 119.6 | 0.00 |
| 10 | 142ca369 | FAIL | 7,217 | 120.3 | 0.00 |

### Aggregate Metrics

| Metric | Value |
|--------|-------|
| Total Puzzles | 10 |
| Correct (full) | 3 |
| Partial Credit | 0.67 |
| Total Score | 3.67 |
| Failed | 6 |
| Accuracy | 36.67% |
| Total Time | 7,217 seconds |
| Total Time | 120.3 minutes |
| Total Time | 2.0 hours |

### Time Distribution

| Metric | Value |
|--------|-------|
| Mean time per puzzle | 721.7 seconds (12.0 min) |
| Median time | 2,086.5 seconds (34.8 min) |
| Min time | 120 seconds (2.0 min) |
| Max time | 7,217 seconds (120.3 min) |
| Std deviation | ~2,500 seconds |

---

## Issues Observed During Test

### API Errors
- Puzzle `13e47133`: Multiple Gemini 500 Internal Server Errors
- Retry limits reached, solver continued with degraded performance

### Timeout Events
| Puzzle | Timeouts Used |
|--------|---------------|
| 0934a4d8 | 2 of 6 |
| 136b0064 | 1 of 6 |
| 135a2760 | 2 of 6 |
| 142ca369 | 6 of 6 (early exit) |
| 195c6913 | 3 of 6 |

### Resource Warning
- Unclosed aiohttp client session at exit
- May indicate memory leak in long runs

---

*This document reports only observed behavior from a single 10-puzzle run and does not attempt to project results to the full dataset.*
