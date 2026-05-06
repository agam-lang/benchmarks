# Agam Cross-Language Benchmark Suite

> Part of the [agam-lang](https://github.com/agam-lang) organization.

## Mission

Provide a standalone, reproducible cross-language benchmark suite for comparing Agam's performance against C, C++, Rust, Go, Python, and GPU/ML frameworks.

## Inventory

### Suite 01: Algorithms (5 × 6 = 30 sources)

| Workload | Agam | C | C++ | Rust | Go | Python |
|----------|------|---|-----|------|----|--------|
| `fibonacci` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `quicksort` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `binary_search` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `prime_sieve` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `edit_distance` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Suite 02: Numerical Computation (5 × 6 = 30 sources)

| Workload | Agam | C | C++ | Rust | Go | Python |
|----------|------|---|-----|------|----|--------|
| `matrix_multiply` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `fft` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `monte_carlo_pi` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `polynomial_eval` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `tensor_operations` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Suite 03: Data Structures (4 × 6 = 24 sources)

| Workload | Agam | C | C++ | Rust | Go | Python |
|----------|------|---|-----|------|----|--------|
| `hashmap_operations` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `btree_operations` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `linked_list` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `ring_buffer` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Suite 05: ML Primitives (4 × 6 = 24 sources)

| Workload | Agam | C | C++ | Rust | Go | Python |
|----------|------|---|-----|------|----|--------|
| `tensor_matmul` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `convolution` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `softmax` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `autodiff` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Suite 06: GPU Compute (17 Python framework benchmarks)

| Workload | PyTorch | CuPy | Numba | TensorFlow | NumPy |
|----------|---------|------|-------|------------|-------|
| `matmul` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `reduction` | ✅ | ✅ | — | ✅ | ✅ |
| `elementwise` | ✅ | ✅ | — | — | ✅ |
| `conv2d` | ✅ | — | — | ✅ | — |
| `softmax` | ✅ | ✅ | — | ✅ | — |

### Suite 09: Compilation Metrics (4 Agam sources)

Programs of varying complexity for measuring compile-time and binary-size:
`tiny_program`, `medium_program`, `large_program`, `complex_generics`

### Suite 10: Compiler Pipeline (29 test programs)

A-to-Z correctness tests covering:

| Category | Tests |
|----------|-------|
| Lexer | keywords, operators, numeric_literals, string_literals |
| Parser | basic_expressions, function_definitions, control_flow, nested_structures, annotations |
| Type System | integer_types, type_inference, function_signatures |
| Control Flow | if_else_chains, while_loops, nested_control, early_return |
| Functions | recursion, mutual_recursion, multiple_functions, function_composition |
| Operators | arithmetic, comparison, precedence |
| Memory | variable_scoping, shadowing, mutability |
| Backends | c_output_verify, llvm_output_verify, jit_execution |

## Layout

```
benchmarks/
├── config/                  # Settings and target definitions
│   ├── benchmark_config.json
│   ├── comparison_targets.json
│   ├── gpu_targets.json
│   └── environments.json
├── infrastructure/          # Discovery, execution, statistics, GPU runner
│   ├── utils.py
│   ├── statistical_analyzer.py
│   ├── benchmark_runner.py
│   ├── gpu_runner.py
│   └── compiler_test_runner.py
├── harness/                 # Language-specific runners
│   ├── base_harness.py
│   ├── agam|c|cpp|rust|go|python_harness.py
├── suites/
│   ├── 01_algorithms/          5 Agam + 25 comparisons
│   ├── 02_numerical_computation/ 5 Agam + 25 comparisons
│   ├── 03_data_structures/     4 Agam + 20 comparisons
│   ├── 05_ml_primitives/       4 Agam + 20 comparisons
│   ├── 06_gpu_compute/         17 Python ML framework benchmarks
│   ├── 09_compilation_metrics/ 4 Agam programs
│   └── 10_compiler_pipeline/   29 Agam tests + expected_outputs.json
├── results/
└── tests/                   5 test modules
```

## Usage

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run GPU Benchmarks (requires frameworks)
```bash
pip install torch cupy-cuda12x numba tensorflow numpy
python suites/06_gpu_compute/matmul_pytorch.py 512
```

### Run Compiler Pipeline Tests (requires agamc)
```python
from infrastructure.compiler_test_runner import run_all_pipeline_tests, print_pipeline_summary
results = run_all_pipeline_tests(backend="llvm")
print_pipeline_summary(results)
```

## License

Dual-licensed under [MIT](LICENSE-MIT) and [Apache 2.0](LICENSE-APACHE).
