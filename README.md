# Agam Cross-Language Benchmark Suite

> Part of the [agam-lang](https://github.com/agam-lang) organization.

## Mission

Provide a standalone, reproducible cross-language benchmark suite for comparing Agam's performance against C, C++, Rust, Go, Python, and GPU/ML frameworks.

## Inventory

### Suite 01: Algorithms (5 × 6 = 30 sources)
`fibonacci`, `quicksort`, `binary_search`, `prime_sieve`, `edit_distance`

### Suite 02: Numerical Computation (5 × 6 = 30 sources)
`matrix_multiply`, `fft`, `monte_carlo_pi`, `polynomial_eval`, `tensor_operations`

### Suite 03: Data Structures (4 × 6 = 24 sources)
`hashmap_operations`, `btree_operations`, `linked_list`, `ring_buffer`

### Suite 04: Compression Kernels (4 × 6 = 24 sources)
`huffman_encoding`, `lzw_compression`, `rle_encoding`, `deflate_block`

### Suite 05: ML Primitives (4 × 6 = 24 sources)
`tensor_matmul`, `convolution`, `softmax`, `autodiff`

### Suite 06: GPU Compute (17 Python framework benchmarks)
`matmul`, `reduction`, `elementwise`, `conv2d`, `softmax`

### Suite 07: Cryptography Kernels (4 × 6 = 24 sources)
`aes_encrypt`, `sha256_hash`, `crc32_checksum`, `rsa_modular_exp`

### Suite 08: Media Encoding Kernels (4 × 6 = 24 sources)
`dct_transform`, `motion_estimation`, `yuv_to_rgb`, `audio_resample`

### Suite 09: Compilation Metrics (4 Agam sources)
`tiny_program`, `medium_program`, `large_program`, `complex_generics`

### Suite 10: Compiler Pipeline (29 test programs)
A-to-Z correctness tests covering Lexer, Parser, Type System, Control Flow, etc.

### Suite 11: Ray Tracing (4 × 6 = 24 sources)
`sphere_intersection`, `phong_reflection`, `bounding_box_hit`, `camera_ray_gen`

### Suite 12: Game AI (4 × 6 = 24 sources)
`astar_pathfinding`, `collision_detection`, `flocking_boids`, `minimax_search`

### Suite 13: SIMD & Vectorization (5 × 6 = 30 sources)
`matrix_multiply`, `nbody_simulation`, `mandelbrot_set`, `dot_product`, `image_blur`

### Suite 14: String & Text Processing (4 × 6 = 24 sources)
`regex_match`, `json_parse`, `html_escape`, `base64_encode`

## Usage

### Run All Benchmarks
```bash
python run_benchmarks.py
```

### Run Specific Workload
```bash
python run_benchmarks.py --matches fibonacci
```

### Run Tests
```bash
python -m pytest tests/ -v
```

## License

Dual-licensed under [MIT](LICENSE-MIT) and [Apache 2.0](LICENSE-APACHE).
