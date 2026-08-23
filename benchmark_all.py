"""Agam Cross-Platform Benchmark Suite Master Script.

Commands:
- `python benchmarks/benchmark_all.py --win-vs-wsl` : Benchmarks Windows 11 vs WSL Ubuntu across @lang.base and @lang.advance
- `python benchmarks/benchmark_all.py --compilers`  : Benchmarks Agam vs Clang++ 21 vs GCC 15 vs Rust vs Python
- `python benchmarks/benchmark_all.py --aot-vs-jit` : Benchmarks Agam LLVM AOT vs Agam JIT
"""

import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    if "--compilers" in sys.argv:
        from scripts.run_live_comparisons import main as run_compilers
        run_compilers()
    elif "--aot-vs-jit" in sys.argv:
        from scripts.benchmark_aot_vs_jit_vs_profiles import main as run_aot
        run_aot()
    else:
        from scripts.benchmark_win11_vs_wsl_profiles import main as run_win_wsl
        run_win_wsl()
