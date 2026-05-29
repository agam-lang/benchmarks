"""Tests for the harness layer."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from harness.agam_harness import AgamHarness
from harness.base_harness import BaseHarness, PreparedBenchmark
from harness.python_harness import PythonHarness
from infrastructure.utils import load_environments, load_targets


class PreparedBenchmarkTests(unittest.TestCase):
    """Verify PreparedBenchmark construction."""

    def test_minimal_construction(self) -> None:
        pb = PreparedBenchmark(
            target_id="test_target",
            target_name="Test Target",
            language="agam",
            backend="llvm",
            compiler="agamc",
            call_cache_enabled=False,
            compile_command=["agamc", "build", "test.agam"],
            run_command=["./test"],
        )
        self.assertEqual(pb.target_id, "test_target")
        self.assertEqual(pb.language, "agam")
        self.assertIsNone(pb.artifact_path)
        self.assertIsNone(pb.skip_reason)
        self.assertEqual(pb.metadata, {})

    def test_with_metadata(self) -> None:
        pb = PreparedBenchmark(
            target_id="t",
            target_name="T",
            language="c",
            backend=None,
            compiler="clang",
            call_cache_enabled=False,
            compile_command=None,
            run_command=["./t"],
            metadata={"optimization_level": 3},
        )
        self.assertEqual(pb.metadata["optimization_level"], 3)


class BaseHarnessTests(unittest.TestCase):
    """Verify BaseHarness target filtering."""

    def _make_harness(self, language: str) -> BaseHarness:
        targets = load_targets()
        envs = load_environments()
        env = envs["environments"]["local_windows_win11"]
        h = BaseHarness(env, targets)
        h.language = language
        return h

    def test_compatible_targets_agam(self) -> None:
        h = self._make_harness("agam")
        targets = h.compatible_targets()
        self.assertGreaterEqual(len(targets), 6)

    def test_compatible_targets_rust(self) -> None:
        h = self._make_harness("rust")
        targets = h.compatible_targets()
        self.assertEqual(len(targets), 1)

    def test_compatible_targets_with_filter(self) -> None:
        h = self._make_harness("agam")
        targets = h.compatible_targets(target_filters={"agam_llvm_o3_call_cache_off"})
        self.assertEqual(len(targets), 1)
        self.assertEqual(targets[0][0], "agam_llvm_o3_call_cache_off")

    def test_can_handle_checks_suffix(self) -> None:
        h = self._make_harness("agam")
        h.suffixes = (".agam",)
        self.assertTrue(h.can_handle(Path("test.agam")))
        self.assertFalse(h.can_handle(Path("test.py")))


class AgamHarnessTests(unittest.TestCase):
    """Verify Agam harness driver resolution behavior."""

    @patch("harness.agam_harness.resolve_agam_driver")
    def test_prepare_uses_resolved_driver_path(self, mock_resolve) -> None:
        resolved_driver = Path("C:/toolchain/agamc.exe")
        mock_resolve.return_value = resolved_driver

        targets = load_targets()
        envs = load_environments()
        env = envs["environments"]["local_windows_win11"]
        harness = AgamHarness(env, targets)
        target_spec = targets["targets"]["agam_llvm_o3_call_cache_off"]

        prepared = harness.prepare(
            Path("sample.agam"),
            Path("build/sample"),
            "agam_llvm_o3_call_cache_off",
            target_spec,
        )

        self.assertEqual(prepared.compiler, str(resolved_driver))
        self.assertEqual(prepared.compile_command[0], str(resolved_driver))
        binary = "build/sample.exe" if os.name == "nt" else "build/sample"
        self.assertEqual(prepared.run_command, [str(Path(binary))])

    @patch("harness.agam_harness.resolve_command_path")
    @patch("harness.agam_harness.resolve_agam_driver")
    def test_c_backend_uses_two_stage_compile(self, mock_resolve_driver, mock_resolve_command) -> None:
        resolved_driver = Path("C:/toolchain/agamc.exe")
        resolved_clang = Path("C:/toolchain/clang.exe")
        mock_resolve_driver.return_value = resolved_driver
        mock_resolve_command.return_value = resolved_clang

        targets = load_targets()
        envs = load_environments()
        env = envs["environments"]["local_windows_win11"]
        harness = AgamHarness(env, targets)
        target_spec = targets["targets"]["agam_c_o3_call_cache_off"]

        prepared = harness.prepare(
            Path("sample.agam"),
            Path("build/sample"),
            "agam_c_o3_call_cache_off",
            target_spec,
        )

        self.assertIsInstance(prepared.compile_command[0], list)
        self.assertIn(prepared.compile_command[0][0], {str(resolved_driver), "pwsh"})
        self.assertEqual(prepared.compile_command[1][0], str(resolved_clang))
        if os.name == "nt":
            self.assertIn("-D_CRT_SECURE_NO_WARNINGS", prepared.compile_command[1])
        else:
            self.assertIn("-lm", prepared.compile_command[1])
        binary = "build/sample.exe" if os.name == "nt" else "build/sample"
        self.assertEqual(prepared.run_command, [str(Path(binary))])


class PythonHarnessTests(unittest.TestCase):
    """Verify Python harness dependency skip detection."""

    @patch("harness.python_harness.importlib.util.find_spec")
    def test_prepare_marks_missing_optional_modules(self, mock_find_spec) -> None:
        def fake_find_spec(name: str):
            return object() if name == "numpy" else None

        mock_find_spec.side_effect = fake_find_spec

        targets = load_targets()
        envs = load_environments()
        env = envs["environments"]["local_windows_win11"]
        harness = PythonHarness(env, targets)
        source = REPO_ROOT / "suites" / "06_gpu_compute" / "matmul_cupy.py"
        target_spec = targets["targets"]["python_cpython"]

        prepared = harness.prepare(source, Path("build/matmul"), "python_cpython", target_spec)

        self.assertEqual(prepared.skip_reason, "missing Python modules: cupy")


if __name__ == "__main__":
    unittest.main()
