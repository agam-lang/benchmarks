"""Tests for the harness layer."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from harness.base_harness import BaseHarness, PreparedBenchmark
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


if __name__ == "__main__":
    unittest.main()
