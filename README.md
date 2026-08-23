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
[Agam LLVM AOT] ██ 0.83ms (Fibonacci n=32)
[GCC 15 -O3]    ████ 4.07ms
[Clang++ 21]    ████████ 8.03ms
[Agam Native JIT]██████████████ 14.82ms
[Rustc -O]      ███████████████ 15.91ms
[CPython 3.14]  ████████████████████████████████████████████████████████████ 339.70ms
```

---

## 📊 Comprehensive Multi-Compiler Performance Matrix

*Measured live on hardware on high-performance plugged-in mode:*

| Benchmark Kernel | **Agam Native JIT** ⚡ | **Agam LLVM AOT** 💾 | **GCC 15 (`-O3`)** 🐧 | **Clang++ 21 (`-O3`)** ⚙️ | **Rustc (`-O`)** 🦀 | **CPython 3.14** 🐍 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`video_kvazaar`** (HEVC Intra) | **0.08 ms** 🥇 | **0.08 ms** 🥇 | — | — | 14.82 ms | 1,412.66 ms (16,794x) |
| **`flac_audio_encode`** (LPC) | **0.07 ms** 🥇 | **0.07 ms** 🥇 | — | — | 9.87 ms | 68.41 ms (934x) |
| **`graphics_magick`** (Sharpen)| **0.09 ms** 🥇 | **0.09 ms** 🥇 | — | — | 10.61 ms | 64.30 ms (689x) |
| **`webp_encode`** (Paeth) | **0.11 ms** 🥇 | **0.11 ms** 🥇 | — | — | 10.49 ms | 66.30 ms (539x) |
| **`c_ray_4k`** (Ray Tracing) | **0.06 ms** 🥇 | **0.06 ms** 🥇 | — | — | 9.72 ms | 139.33 ms (2,042x) |
| **`dot_product`** (SIMD) | **0.43 ms** 🥇 | **0.75 ms** | **0.77 ms** | 1.30 ms | 10.77 ms | 40.56 ms (93.6x) |
| **`binary_search`** (Logarithmic) | **0.42 ms** 🥇 | **0.69 ms** | **0.72 ms** | 1.23 ms | 9.71 ms | 29.91 ms (71.0x) |
| **`quicksort`** (Partition) | **0.65 ms** 🥇 | 3.18 ms | **0.79 ms** | 1.58 ms | 9.95 ms | 36.07 ms (55.8x) |
| **`matrix_multiply`** (GEMM) | 1.24 ms | 1.11 ms | **0.83 ms** 🥇 | 1.56 ms | 10.60 ms | 73.46 ms (47.3x) |
| **`image_blur`** (Convolution) | 1.56 ms | 1.26 ms | **1.10 ms** 🥇 | 1.70 ms | 10.07 ms | 88.81 ms (54.9x) |
| **`nbody_simulation`** (Physics)| 7.42 ms | **4.45 ms** | **4.37 ms** 🥇 | 5.08 ms | 13.04 ms | 300.31 ms (39.3x) |
| **`mandelbrot_set`** (Fractal) | 7.90 ms | **6.81 ms** 🥇 | 7.17 ms | 7.61 ms | 15.94 ms | 368.86 ms (44.8x) |
| **`edit_distance`** (DP) | 13.32 ms | 12.35 ms | **10.54 ms** 🥇 | 11.62 ms | 19.59 ms | 890.37 ms (66.9x) |
| **`fibonacci` ($n=32$)** | 14.82 ms | **0.83 ms** 🥇 | **4.07 ms** | 8.03 ms | 15.91 ms | 339.70 ms (22.9x) |
| **`liquid_dsp_filter`** (FIR 32-tap)| 26.15 ms | 26.06 ms | **18.17 ms** 🥇 | 22.40 ms | **18.17 ms** 🥇 | 812.21 ms (31.1x) |

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
