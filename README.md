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

*Measured natively in Linux under high-performance plugged-in mode:*

| Benchmark Kernel | **Agam Native JIT** ⚡ | **Agam LLVM AOT** 💾 | **GCC 15 (`-O3`)** 🐧 | **Clang++ 21 (`-O3`)** ⚙️ | **Rustc 1.93 (`-O`)** 🦀 | **CPython 3.14** 🐍 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`fibonacci` ($n=32$)** | 16.00 ms | **0.73 ms** 🥇 | 3.88 ms | 7.52 ms | 6.16 ms | 209.51 ms (287x) |
| **`binary_search`** (Logarithmic) | **0.36 ms** 🥇 | 0.74 ms | 0.62 ms | 1.37 ms | 0.78 ms | 28.67 ms (79.6x) |
| **`quicksort`** (Partitioning) | **0.61 ms** 🥇 | 3.10 ms | 0.67 ms | 1.36 ms | 0.91 ms | 31.38 ms (51.4x) |
| **`dot_product`** (SIMD Vector) | **0.43 ms** 🥇 | 0.86 ms | 0.69 ms | 1.13 ms | 0.90 ms | 34.11 ms (79.3x) |
| **`prime_sieve`** (Bit Sieve) | **1.32 ms** 🥇 | 7.38 ms | 1.67 ms | 2.37 ms | 1.56 ms | 38.07 ms (28.8x) |
| **`ocudu_5g_phy`** (5G LDPC) | 0.92 ms | **0.66 ms** 🥇 | 1.10 ms | 1.14 ms | 0.83 ms | 34.55 ms (52.3x) |
| **`c_ray_4k`** (Ray Tracing) | 0.90 ms | **0.71 ms** 🥇 | 1.16 ms | 1.25 ms | 0.75 ms | 109.24 ms (153.8x) |
| **`video_kvazaar`** (HEVC Intra)| **0.57 ms** 🥇 | 0.80 ms | 1.40 ms | 1.53 ms | 3.81 ms | 905.13 ms (1,588x) |
| **`valkey_kv_store`** (In-Memory KV)| 1.15 ms | **0.89 ms** 🥇 | 1.27 ms | 1.25 ms | 0.98 ms | 41.08 ms (46.1x) |
| **`matrix_multiply`** (GEMM Tile) | 1.11 ms | 0.99 ms | **0.71 ms** 🥇 | 1.23 ms | 0.92 ms | 55.02 ms (49.5x) |
| **`flac_audio_encode`** (LPC) | **0.73 ms** 🥇 | 1.02 ms | 1.43 ms | 1.43 ms | 1.05 ms | 46.76 ms (64.0x) |
| **`image_blur`** (2D Convolution) | 1.53 ms | 1.13 ms | **0.86 ms** 🥇 | 1.33 ms | 0.97 ms | 63.18 ms (41.2x) |
| **`graphics_magick`** (Filter) | 2.27 ms | 1.57 ms | 1.98 ms | 2.04 ms | **1.06 ms** 🥇 | 49.71 ms (21.9x) |
| **`webp_encode`** (Paeth) | 2.13 ms | 41.86 ms | 1.97 ms | 1.79 ms | **0.95 ms** 🥇 | 48.35 ms (22.7x) |
| **`nbody_simulation`** (Physics)| 7.26 ms | 4.09 ms | **3.94 ms** 🥇 | 4.47 ms | **3.94 ms** 🥇 | 212.62 ms (29.2x) |
| **`mandelbrot_set`** (Fractal) | 7.78 ms | 6.66 ms | **6.58 ms** 🥇 | 7.10 ms | 6.76 ms | 244.79 ms (31.4x) |
| **`edit_distance`** (DP) | 14.03 ms | 12.68 ms | **10.26 ms** 🥇 | 11.99 ms | 10.25 ms | 636.60 ms (45.3x) |
| **`liquid_dsp_filter`** (FIR 32) | 25.92 ms | 29.03 ms | **2.52 ms** 🥇 | 3.26 ms | 6.31 ms | 453.43 ms (17.5x) |

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
