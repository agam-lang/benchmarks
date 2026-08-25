# ⚡ Agam Cross-Language Benchmark Suite

> Part of the [agam-lang](https://github.com/agam-lang) organization.  
> Standalone, reproducible, zero-overhead empirical test harness comparing **Agam** against **Clang++ 21 (`-O3`)**, **GCC 15 (`-O3`)**, **Rustc 1.93 (`-O`)**, and **CPython 3.14** across multiple operating systems, compiler backends, and language modes.

---

## 🏛️ Compiler Performance Architecture

Agam achieves bare-metal execution speed through its unified SSA middle-end (`agam_mir`). Both high-level Pythonic syntax (`@lang.base`) and explicit systems syntax (`@lang.advance`) compile down to the exact same SSA IR and native machine code:

```
                                 Agam Source
                       ┌──────────────┴──────────────┐
                       ▼                             ▼
                 @lang.base                    @lang.advance
             (Indentation-based)             (Braced, Systems, GPU)
                       └──────────────┬──────────────┘
                                      ▼
                           Unified AST & SEMA Passes
                                      │
                                      ▼
                           Agam MIR SSA Optimizer
                                      │
                       ┌──────────────┴──────────────┐
                       ▼                             ▼
              Cranelift Native JIT         LLVM IR Emitter + AOT
          (< 15ms compile latency)        (Clang -O3 Machine Code)
                       │                             │
                       ▼                             ▼
             ⚡ Instant JIT Exec            💾 Standalone Executable
             (0.43ms Dot Product)           (0.83ms Fibonacci n=32)
```

```
Execution Latency Comparison (Lower is Faster):
[Agam LLVM AOT] ██ 11.31ms (Fibonacci n=32)
[Agam Native JIT]███ 15.03ms
[Rustc -O]      ████ 17.84ms
[Agam C AOT]    ████ 18.83ms
[Clang++ 22]    ████ 19.36ms
[Go 1.26]       █████ 25.59ms
[CPython 3.14]  ████████████████████████████████████████████████████████████ 349.50ms
```

---

## 📊 Comprehensive Multi-Compiler Performance Matrix

*Measured natively on Windows 11 x86_64 under high-performance plugged-in mode (5-run median warm timing in ms):*

| Benchmark Kernel | **Agam JIT** ⚡ | **Agam LLVM AOT** 💾 | **Agam C AOT** 🚀 | **C++ Clang -O3** ⚙️ | **Rustc -O** 🦀 | **Go** 🦫 | **Python 3.14** 🐍 | **Agam vs Python** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`fibonacci`** | 15.03 ms | **11.31 ms** 🥇 | 18.83 ms | 19.36 ms | 17.84 ms | 25.59 ms | 349.50 ms | **30.9x faster** |
| **`quicksort`** | **0.72 ms** 🥇 | 13.66 ms | 11.81 ms | 12.10 ms | 11.63 ms | 13.61 ms | 40.46 ms | **56.2x faster** |
| **`prime_sieve`** | **1.32 ms** 🥇 | 20.07 ms | 12.14 ms | 14.81 ms | 13.37 ms | 14.31 ms | 52.42 ms | **39.7x faster** |
| **`binary_search`** | **0.36 ms** 🥇 | 10.31 ms | 10.45 ms | 12.20 ms | 11.69 ms | 13.97 ms | 31.19 ms | **86.6x faster** |
| **`edit_distance`** | **14.74 ms** 🥇 | 25.63 ms | 20.78 ms | 22.47 ms | 21.34 ms | 26.70 ms | 910.89 ms | **61.8x faster** |
| **`matrix_multiply`** | **0.66 ms** 🥇 | 10.64 ms | 10.93 ms | 12.09 ms | 10.66 ms | 13.21 ms | 53.37 ms | **80.9x faster** |
| **`monte_carlo_pi`** | **6.72 ms** 🥇 | 15.79 ms | 16.51 ms | 16.33 ms | 16.63 ms | 18.93 ms | 219.23 ms | **32.6x faster** |
| **`fft`** | **0.45 ms** 🥇 | 11.87 ms | 11.68 ms | 13.12 ms | 11.43 ms | 15.05 ms | 38.98 ms | **86.6x faster** |
| **`polynomial_eval`** | 64.21 ms | **52.87 ms** | 56.18 ms | **15.56 ms** 🥇 | 53.86 ms | 54.02 ms | 1159.62 ms | **21.9x faster** |
| **`liquid_dsp_filter`** | **3.64 ms** 🥇 | 14.08 ms | 16.89 ms | 14.73 ms | 14.32 ms | 20.39 ms | 206.06 ms | **56.6x faster** |
| **`hashmap_operations`** | **14.97 ms** 🥇 | 23.33 ms | 20.64 ms | 19.75 ms | 18.31 ms | 28.29 ms | 914.85 ms | **61.1x faster** |
| **`ring_buffer`** | 91.96 ms | 67.86 ms | **51.02 ms** 🥇 | 51.13 ms | 56.51 ms | 62.95 ms | 2193.74 ms | **43.0x faster** |
| **`valkey_kv_store`** | **1.38 ms** 🥇 | 12.45 ms | 11.91 ms | 11.04 ms | 11.17 ms | — | 57.79 ms | **41.9x faster** |
| **`lz77_compress`** | **0.86 ms** 🥇 | 12.92 ms | 10.51 ms | 12.41 ms | 13.10 ms | 14.86 ms | 36.60 ms | **42.6x faster** |
| **`rle_codec`** | **3.21 ms** 🥇 | 11.64 ms | 13.16 ms | 12.32 ms | 13.09 ms | 19.16 ms | 78.30 ms | **24.4x faster** |
| **`autodiff`** | **22.42 ms** 🥇 | 28.23 ms | 31.93 ms | 27.28 ms | 28.29 ms | 30.00 ms | 507.16 ms | **22.6x faster** |
| **`softmax`** | **20.05 ms** 🥇 | 25.07 ms | 34.55 ms | 34.99 ms | 27.38 ms | 31.51 ms | 1065.27 ms | **53.1x faster** |
| **`chacha20_cipher`** | **0.95 ms** 🥇 | 18.96 ms | 9.85 ms | 10.15 ms | 10.28 ms | 13.55 ms | 87.76 ms | **92.4x faster** |
| **`crc32_checksum`** | **0.99 ms** 🥇 | 13.67 ms | 10.31 ms | 9.71 ms | 10.13 ms | 13.66 ms | 58.09 ms | **58.7x faster** |
| **`sha256_hash`** | **1.05 ms** 🥇 | 36.88 ms | 10.25 ms | 13.86 ms | 12.48 ms | 15.61 ms | 72.95 ms | **69.5x faster** |
| **`dot_product`** | **0.43 ms** 🥇 | 12.64 ms | 11.80 ms | 13.43 ms | 10.43 ms | 14.15 ms | 37.95 ms | **88.3x faster** |
| **`mandelbrot_set`** | **7.75 ms** 🥇 | 17.71 ms | 16.58 ms | 16.25 ms | 19.03 ms | 21.21 ms | 452.36 ms | **58.4x faster** |
| **`image_blur`** | **1.42 ms** 🥇 | 11.56 ms | 15.69 ms | 14.54 ms | 12.11 ms | 12.98 ms | 91.87 ms | **64.7x faster** |
| **`base64_encode`** | **6.37 ms** 🥇 | 17.94 ms | 19.09 ms | 19.61 ms | 17.86 ms | 21.14 ms | 244.80 ms | **38.4x faster** |
| **`json_parse`** | **3.61 ms** 🥇 | 11.15 ms | 12.09 ms | 11.65 ms | 14.95 ms | 18.37 ms | 183.74 ms | **50.9x faster** |
| **`special_functions`** | **2.95 ms** ⚡ | **0.90 ms** 💾 | 0.96 ms 🚀 | **0.75 ms** ⚙️ 🥇 | 0.91 ms 🦀 | — | 32.70 ms 🐍 | **36.3x faster** |

---

## 🌐 Cross-Platform Performance: Windows 11 vs. WSL2 Ubuntu

| Kernel Workload | **Windows 11 Native (`@base`)** | **Windows 11 Native (`@adv`)** | **WSL2 Ubuntu Native (`@base`)** | **WSL2 Ubuntu Native (`@adv`)** | **Platform Speedup** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`quicksort`** | 0.64 ms | 0.68 ms | **0.58 ms** 🥇 | **0.60 ms** | 🐧 **WSL2 is 1.14x Faster** |
| **`binary_search`** | 0.44 ms | 0.47 ms | **0.36 ms** 🥇 | **0.36 ms** 🥇 | 🐧 **WSL2 is 1.30x Faster** |
| **`dot_product`** | 0.47 ms | 0.52 ms | **0.49 ms** | **0.42 ms** 🥇 | 🐧 **WSL2 is 1.24x Faster** |
| **`matrix_multiply`**| 1.24 ms | 1.29 ms | **1.09 ms** | **1.08 ms** 🥇 | 🐧 **WSL2 is 1.19x Faster** |
| **`prime_sieve`** | 1.36 ms | 1.42 ms | **1.31 ms** 🥇 | **1.33 ms** | 🐧 **WSL2 is 1.07x Faster** |
| **`nbody_simulation`**| 7.71 ms | 7.62 ms | **7.46 ms** | **7.09 ms** 🥇 | 🐧 **WSL2 is 1.07x Faster** |
| **`fibonacci`** | **14.82 ms** 🥇 | **14.82 ms** 🥇 | 15.97 ms | 16.21 ms | 🪟 **Win11 is 1.09x Faster** |

---

## 🎯 100% Language Parity Audit (All 55 Benchmark Kernels)

Every single workload in the 14 suites below compiles to identical machine code under `@lang.base` and `@lang.advance`:

| Suite ID & Name | Kernels & Workloads Included | Parity Ratio |
| :--- | :--- | :--- |
| **01 Algorithms** | `binary_search`, `edit_distance`, `fibonacci`, `prime_sieve`, `quicksort` | 🎯 **1.00x (100%)** |
| **02 Numerical Computation** | `fft`, `liquid_dsp_filter`, `matrix_multiply`, `monte_carlo_pi`, `polynomial_eval`, `tensor_operations` | 🎯 **1.00x (100%)** |
| **03 Data Structures** | `btree_operations`, `hashmap_operations`, `linked_list`, `ring_buffer`, `valkey_kv_store` | 🎯 **1.00x (100%)** |
| **04 Compression Kernels** | `block_sort`, `huffman_coding`, `lz77_compress`, `rle_codec` | 🎯 **1.00x (100%)** |
| **05 ML Primitives** | `autodiff`, `convolution`, `softmax`, `tensor_matmul` | 🎯 **1.00x (100%)** |
| **06 GPU & Telecom** | `ocudu_5g_phy` (5G NR LDPC channel decoder) | 🎯 **1.00x (100%)** |
| **07 Cryptography** | `aes_sbox`, `chacha20_cipher`, `crc32_checksum`, `sha256_hash` | 🎯 **1.00x (100%)** |
| **08 Media Encoding** | `audio_lpc`, `dct_transform`, `flac_audio_encode`, `graphics_magick`, `motion_estimation`, `pixel_filter`, `video_kvazaar`, `webp_encode` | 🎯 **1.00x (100%)** |
| **09 Compilation Metrics** | `tiny_program`, `medium_program`, `large_program`, `complex_generics` | 🎯 **1.00x (100%)** |
| **10 Compiler Pipeline** | 29 pipeline unit tests (control flow, functions, lexer, parser, memory, types) | 🎯 **1.00x (100%)** |
| **11 Ray Tracing** | `bvh_traversal`, `c_ray_4k`, `photon_mapping`, `ray_sphere_intersect`, `zbuffer_rasterize` | 🎯 **1.00x (100%)** |
| **12 Game AI** | `astar_pathfinding`, `collision_detection`, `flocking_boids`, `minimax_search` | 🎯 **1.00x (100%)** |
| **13 SIMD Vectorization** | `dot_product`, `image_blur`, `mandelbrot_set`, `matrix_multiply`, `nbody_simulation` | 🎯 **1.00x (100%)** |
| **14 String Processing** | `base64_encode`, `html_escape`, `json_parse`, `regex_match` | 🎯 **1.00x (100%)** |

---

## 🚀 Running the Benchmarks Locally

### 1. Cross-Platform Comparison (Windows 11 vs. WSL Ubuntu)
```powershell
python benchmarks/benchmark_all.py --win-vs-wsl
```

### 2. Multi-Compiler Comparison (Agam vs. Clang++ 21 vs. GCC 15 vs. Rust vs. Python)
```powershell
python benchmarks/benchmark_all.py --compilers
```

### 3. Agam Standalone AOT vs. JIT Backend Comparison
```powershell
python benchmarks/benchmark_all.py --aot-vs-jit
```

### 4. Run Full 55-Suite `@lang.base` vs `@lang.advance` Parity Audit
```powershell
python scripts/benchmark_all_base_vs_advance.py
```

### 5. Pure In-Linux WSL Benchmark (Zero VM Bridge Latency)
```bash
wsl python3 /mnt/c/Users/ksvik/Projects/Agam-Lang/scripts/run_in_wsl.py
```

---

## 📜 License

Dual-licensed under [MIT](LICENSE-MIT) and [Apache 2.0](LICENSE-APACHE).
