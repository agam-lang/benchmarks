# Benchmark Results Summary

This directory holds the performance data from benchmark runs.

## Latest Result: 2026-05-14 (All-Suite Same-Host Baseline)

**Environment:** `local_windows_win11` on Windows 11  
**Raw result root:** `results/raw/2026-05-14_14-26-15`

This measured run used the repo defaults:
- Warmup runs: `2`
- Measured runs: `7`

Coverage in this result:
- `760` timed result rows
- `47` cross-language comparable workload families
- all suites `01` through `14` exercised

Available timed targets in this run:
- Agam LLVM `-O3` with call cache on/off
- Agam C backend `-O3` with call cache on/off
- Agam JIT `-O2` with call cache on/off
- Clang C `-O3`
- Clang++ `-O3`
- Clang 22 C `-O3`
- Clang 22 C++ `-O3`
- Rust release
- CPython

Unavailable or skipped on this host:
- GCC 16 targets: `gcc` / `g++` not installed
- Go target: `go` not installed
- Suite 06 Python GPU/ML variants requiring `cupy`, `numba`, `tensorflow`, or `torch`

Remaining non-host limitation:
- Agam C backend still misses `10_compiler_pipeline/memory/shadowing.agam` because the current generated-C path does not handle lexical shadowing correctly

## Cross-Language Rollup

Geometric mean of per-workload medians across the `47` comparable workload families:

| Target | Comparable workloads | Geometric mean median (ms) |
|--------|----------------------|----------------------------|
| Agam LLVM O3 | 47 | 18.309 |
| Agam C O3 | 47 | 14.756 |
| Rust release | 47 | 15.288 |
| Clang C O3 | 47 | 14.652 |
| Clang++ O3 | 47 | 14.519 |
| Clang 22 C O3 | 47 | 14.216 |
| Clang 22 C++ O3 | 47 | 14.097 |
| CPython | 47 | 140.984 |

Workload-family win counts in this same comparable set:

| Target | Best median count |
|--------|-------------------|
| Agam LLVM O3 | 7 |
| Agam C O3 | 8 |
| Rust release | 1 |
| Clang C O3 | 7 |
| Clang++ O3 | 5 |
| Clang 22 C O3 | 11 |
| Clang 22 C++ O3 | 8 |
| CPython | 0 |

> [!NOTE]
> Agam C now sits inside the native-performance cluster across the comparable suite set. Agam LLVM remains competitive overall but is still held back by slower suite-level behavior in workloads such as media encoding and game AI.

## Suite Highlights

Geometric mean medians for representative targets by suite:

| Suite | Agam LLVM O3 | Agam C O3 | Rust | Clang C | Python |
|------|---------------|------------|------|---------|--------|
| `01_algorithms` | 13.513 | 14.818 | 13.908 | 13.447 | 98.900 |
| `02_numerical_computation` | 15.285 | 15.208 | 15.774 | 15.034 | 97.897 |
| `03_data_structures` | 26.885 | 23.126 | 23.467 | 23.306 | 402.808 |
| `04_compression_kernels` | 10.863 | 10.926 | 11.640 | 11.822 | 36.293 |
| `05_ml_primitives` | 17.282 | 17.131 | 17.549 | 17.432 | 197.445 |
| `07_cryptography_kernels` | 16.782 | 10.989 | 11.575 | 10.875 | 46.322 |
| `08_media_encoding_kernels` | 33.054 | 11.735 | 12.178 | 11.451 | 159.445 |
| `09_compilation_metrics` | 11.546 | 11.161 | — | — | — |
| `10_compiler_pipeline` | 11.040 | 10.899 | — | — | — |
| `11_ray_tracing` | 18.251 | 16.955 | 19.346 | 16.576 | 223.272 |
| `12_game_ai` | 54.503 | 21.106 | 22.160 | 20.402 | 639.112 |
| `13_simd_vectorization` | 12.627 | 12.631 | 12.916 | 12.670 | 113.237 |
| `14_string_processing` | 13.211 | 13.095 | 13.766 | 13.573 | 165.812 |

## Suite Completion Status

| Suite | Name | Status | Notes |
|-------|------|--------|-------|
| 01 | Algorithms | ✅ | full same-host baseline measured |
| 02 | Numerical | ✅ | full same-host baseline measured |
| 03 | Data Structures | ✅ | full same-host baseline measured |
| 04 | Compression | ✅ | full same-host baseline measured |
| 05 | ML Primitives | ✅ | full same-host baseline measured |
| 06 | GPU Compute | ✅ | NumPy timed, GPU/ML module variants skipped by environment |
| 07 | Cryptography | ✅ | full same-host baseline measured |
| 08 | Media | ✅ | full same-host baseline measured |
| 09 | Compilation | ✅ | Agam-only baseline measured |
| 10 | Pipeline | ✅ | one Agam C backend shadowing limitation remains |
| 11 | Ray Tracing | ✅ | BVH sources normalized across languages |
| 12 | Game AI | ✅ | minimax source normalized across Agam backends |
| 13 | SIMD/Vectorization | ✅ | full same-host baseline measured |
| 14 | String Processing | ✅ | full same-host baseline measured |

## Next Steps

1. Fix the current `agam_mir` source build break so the matrix can run from a fresh compiler binary instead of the last built debug `agamc`.
2. Add automated report generation so rollups like the tables above come directly from `performance.json`.
3. Re-run the same matrix when `gcc`, `g++`, and `go` are available to fill the missing host toolchain lanes.
