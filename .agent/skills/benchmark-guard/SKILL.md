---
name: benchmark-guard
description: Use when changes claim performance wins or affect benchmark infrastructure.
---

# Benchmark Guard

Use this skill when modifying benchmark suites or interpreting results.

## Workflow

1. Verify all comparison targets use equivalent optimization levels.
2. Run warmup before measurement.
3. Use median timing over at least 5 runs.
4. Document any anomalies or outliers.
5. Reject results from shared CI runners for cross-language performance claims.

## Success Criteria

- Results are reproducible on the same hardware
- Methodology is documented alongside results
- No cherry-picked or misleading comparisons
