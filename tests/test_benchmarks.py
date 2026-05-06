"""Workspace shape, benchmark discovery, and cross-language coverage tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from infrastructure.utils import (
    SUITE_ROOT,
    discover_benchmarks,
    load_config,
    load_environments,
    load_targets,
)


class WorkspaceShapeTests(unittest.TestCase):
    """Verify benchmark workspace has expected directory structure."""

    def test_readme_exists(self) -> None:
        self.assertTrue((REPO_ROOT / "README.md").is_file())

    def test_results_readme_exists(self) -> None:
        self.assertTrue((REPO_ROOT / "results" / "README.md").is_file())

    def test_suite_directory_exists(self) -> None:
        self.assertTrue(SUITE_ROOT.is_dir())

    EXPECTED_SUITES = [
        "01_algorithms",
        "02_numerical_computation",
        "03_data_structures",
        "05_ml_primitives",
        "06_gpu_compute",
        "09_compilation_metrics",
        "10_compiler_pipeline",
    ]

    def test_all_suite_directories_exist(self) -> None:
        for suite in self.EXPECTED_SUITES:
            self.assertTrue(
                (SUITE_ROOT / suite).is_dir(),
                msg=f"Missing suite directory: {suite}",
            )

    def test_comparisons_directories_exist(self) -> None:
        for suite in ["01_algorithms", "02_numerical_computation",
                       "03_data_structures", "05_ml_primitives"]:
            self.assertTrue(
                (SUITE_ROOT / suite / "comparisons").is_dir(),
                msg=f"Missing comparisons dir in {suite}",
            )


class BenchmarkDiscoveryTests(unittest.TestCase):
    """Verify discover_benchmarks returns expected sources."""

    def test_discovers_agam_sources(self) -> None:
        agam_sources = discover_benchmarks(language_filters={"agam"})
        # 5 algorithms + 5 numerical + 4 data_structures + 4 ml_primitives + 4 compilation = 22+
        self.assertGreaterEqual(len(agam_sources), 22)

    def test_discovers_comparison_sources(self) -> None:
        comparison_sources = [
            p for p in discover_benchmarks(include_comparisons=True)
            if "comparisons" in p.parts
        ]
        # 25 + 25 + 20 + 20 = 90+
        self.assertGreaterEqual(len(comparison_sources), 90)

    def test_discovers_all_sources(self) -> None:
        all_sources = discover_benchmarks(include_comparisons=True)
        self.assertGreaterEqual(len(all_sources), 110)

    def test_suite_filter_works(self) -> None:
        sources = discover_benchmarks(
            suite_filters=["02_numerical_computation"],
            language_filters={"agam"},
        )
        self.assertGreaterEqual(len(sources), 5)

    def test_match_filter_works(self) -> None:
        sources = discover_benchmarks(
            match_filters=["fibonacci"],
            include_comparisons=True,
        )
        self.assertGreaterEqual(len(sources), 6)

    def test_excludes_comparisons_by_default(self) -> None:
        sources = discover_benchmarks()
        for path in sources:
            self.assertNotIn("comparisons", path.parts)


class CrossLanguageCoverageTests(unittest.TestCase):
    """Verify each workload has all 5 comparison languages."""

    EXPECTED_SUFFIXES = {".c", ".cpp", ".go", ".py", ".rs"}

    def _check_workloads(self, suite: str, workloads: list[str]) -> None:
        comparison_dir = SUITE_ROOT / suite / "comparisons"
        for workload in workloads:
            # Agam source
            self.assertTrue(
                (SUITE_ROOT / suite / f"{workload}.agam").is_file(),
                msg=f"Missing Agam: {suite}/{workload}.agam",
            )
            # Comparisons
            present = {
                p.suffix for p in comparison_dir.iterdir()
                if p.is_file() and p.stem == workload
            }
            self.assertEqual(
                present, self.EXPECTED_SUFFIXES,
                msg=f"{suite}/{workload} missing: {self.EXPECTED_SUFFIXES - present}",
            )

    def test_algorithm_coverage(self) -> None:
        self._check_workloads("01_algorithms", [
            "fibonacci", "quicksort", "binary_search", "prime_sieve", "edit_distance",
        ])

    def test_numerical_coverage(self) -> None:
        self._check_workloads("02_numerical_computation", [
            "matrix_multiply", "fft", "monte_carlo_pi", "polynomial_eval", "tensor_operations",
        ])

    def test_data_structures_coverage(self) -> None:
        self._check_workloads("03_data_structures", [
            "hashmap_operations", "btree_operations", "linked_list", "ring_buffer",
        ])

    def test_ml_primitives_coverage(self) -> None:
        self._check_workloads("05_ml_primitives", [
            "tensor_matmul", "convolution", "softmax", "autodiff",
        ])


class ConfigTests(unittest.TestCase):
    """Verify config files parse correctly."""

    def test_benchmark_config_loads(self) -> None:
        config = load_config()
        self.assertIn("defaults", config)
        self.assertIn("warmup_runs", config["defaults"])

    def test_targets_config_loads(self) -> None:
        targets = load_targets()
        self.assertIn("targets", targets)
        self.assertEqual(len(targets["targets"]), 11)

    def test_environments_config_loads(self) -> None:
        envs = load_environments()
        self.assertIn("environments", envs)

    def test_gpu_targets_config_loads(self) -> None:
        import json
        with open(REPO_ROOT / "config" / "gpu_targets.json") as f:
            data = json.load(f)
        self.assertIn("targets", data)
        self.assertIn("gpu_defaults", data)
        self.assertEqual(len(data["targets"]), 8)


class CompilationMetricsTests(unittest.TestCase):
    """Verify compilation metrics sources exist."""

    EXPECTED = ["tiny_program.agam", "medium_program.agam",
                "large_program.agam", "complex_generics.agam"]

    def test_all_compilation_sources_exist(self) -> None:
        suite_dir = SUITE_ROOT / "09_compilation_metrics"
        for name in self.EXPECTED:
            self.assertTrue(
                (suite_dir / name).is_file(),
                msg=f"Missing: {name}",
            )


if __name__ == "__main__":
    unittest.main()
