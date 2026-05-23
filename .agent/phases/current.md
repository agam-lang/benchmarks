# Current Development

## Active Workstreams

1. **All-Suite Same-Host Comparison Baseline**
   - Status: complete
   - Goal: run the measured Windows same-host matrix across suites `01` through `14`
   - Progress:
     - ✅ Benchmark discovery cleaned up (`.agam_cache` excluded, Agam driver auto-discovery added)
     - ✅ Agam C backend benchmark flow fixed on Windows (`agamc -> generated C -> clang`)
     - ✅ Missing toolchains and Python ML stacks now skip cleanly instead of crashing the runner
     - ✅ Agam suite sources normalized for current parser/backend constraints
     - ✅ `bvh_traversal` divide-by-zero bug fixed across Agam, C, C++, Rust, Python, and Go sources
     - ✅ `minimax_search` source reshaped to avoid current LLVM/C temp-allocation failures
     - ✅ `if_else_chains` reshaped so the JIT target now executes successfully
     - ✅ Full measured result set captured at `results/raw/2026-05-14_14-26-15`

2. **Known Environment / Compiler Limits**
   - Status: active
   - Notes:
     - Host toolchains missing: `gcc`, `g++`, `go`
     - Host Python modules missing for suite 06: `cupy`, `numba`, `tensorflow`, `torch`
     - Fresh `agamc` rebuild from `agam/` is still blocked by current `agam_mir` source errors, so benchmarking uses the last built `agam/target/debug/agamc.exe`
     - One benchmark/backend gap remains: `10_compiler_pipeline/memory/shadowing.agam` still fails on the Agam C backend due to shadowing codegen limitations

3. **Next Benchmarking Work**
   - Status: planned
   - Goal: move from baseline generation to automated reporting and fresh-compiler reruns
   - Candidates:
     - Generate suite/target summary reports automatically from `performance.json`
     - Re-run the same matrix once GCC 16 and Go are available on the host
     - Re-run the same matrix from a freshly rebuilt `agamc` once `agam_mir` is fixed

## Decision Rules

- Align all work with the Agam language vision and ecosystem policies.
- Follow the quality rules defined in `.agent/rules/`.
- Update this file when the measured same-host baseline changes materially.
