# Benchmark Results

This directory holds all benchmark output from local and CI runs.

## Layout

- `raw/<timestamp>/` — per-run output directories
  - `performance.json` — timing measurements and statistics
  - `metadata.json` — host platform, timestamp, and run context
- `aggregated/` — cross-run summaries (generated)
- `reports/` — human-readable markdown reports (generated)
- `plots/` — visualizations (generated, requires matplotlib)

## Result Status

No benchmark results have been generated yet. This repository is bootstrapping Phase 1 (Algorithm Suite).

### Expected Workloads

| Workload | Suite | Status |
|----------|-------|--------|
| `fibonacci` | 01_algorithms | source-present only |
| `quicksort` | 01_algorithms | source-present only |
| `binary_search` | 01_algorithms | source-present only |
| `prime_sieve` | 01_algorithms | source-present only |
| `edit_distance` | 01_algorithms | source-present only |
