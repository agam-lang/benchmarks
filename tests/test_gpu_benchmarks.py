"""Tests for GPU benchmark suite — source existence and framework detection."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

GPU_SUITE = REPO_ROOT / "suites" / "06_gpu_compute"
GPU_CONFIG = REPO_ROOT / "config" / "gpu_targets.json"


class GPUSuiteShapeTests(unittest.TestCase):
    """Verify GPU suite directory structure."""

    def test_gpu_suite_exists(self) -> None:
        self.assertTrue(GPU_SUITE.is_dir())

    def test_gpu_targets_config_exists(self) -> None:
        self.assertTrue(GPU_CONFIG.is_file())

    def test_matmul_benchmarks_exist(self) -> None:
        expected = [
            "matmul_pytorch.py", "matmul_cupy.py", "matmul_numba.py",
            "matmul_tensorflow.py", "matmul_numpy.py",
        ]
        for name in expected:
            self.assertTrue(
                (GPU_SUITE / name).is_file(),
                msg=f"Missing GPU benchmark: {name}",
            )

    def test_reduction_benchmarks_exist(self) -> None:
        expected = ["reduction_pytorch.py", "reduction_cupy.py", "reduction_numpy.py",
                     "reduction_tensorflow.py"]
        for name in expected:
            self.assertTrue(
                (GPU_SUITE / name).is_file(),
                msg=f"Missing GPU benchmark: {name}",
            )

    def test_elementwise_benchmarks_exist(self) -> None:
        expected = ["elementwise_pytorch.py", "elementwise_cupy.py", "elementwise_numpy.py"]
        for name in expected:
            self.assertTrue(
                (GPU_SUITE / name).is_file(),
                msg=f"Missing GPU benchmark: {name}",
            )

    def test_conv2d_benchmarks_exist(self) -> None:
        expected = ["conv2d_pytorch.py", "conv2d_tensorflow.py"]
        for name in expected:
            self.assertTrue(
                (GPU_SUITE / name).is_file(),
                msg=f"Missing GPU benchmark: {name}",
            )

    def test_softmax_benchmarks_exist(self) -> None:
        expected = ["softmax_pytorch.py", "softmax_tensorflow.py", "softmax_cupy.py"]
        for name in expected:
            self.assertTrue(
                (GPU_SUITE / name).is_file(),
                msg=f"Missing GPU benchmark: {name}",
            )


class GPUConfigTests(unittest.TestCase):
    """Verify GPU config loads correctly."""

    def test_gpu_targets_loads(self) -> None:
        import json
        with open(GPU_CONFIG) as f:
            data = json.load(f)
        self.assertIn("targets", data)
        self.assertIn("pytorch_cuda", data["targets"])
        self.assertIn("cupy_gpu", data["targets"])
        self.assertIn("numba_cuda", data["targets"])
        self.assertIn("tensorflow_gpu", data["targets"])
        self.assertIn("numpy_cpu", data["targets"])

    def test_gpu_defaults_present(self) -> None:
        import json
        with open(GPU_CONFIG) as f:
            data = json.load(f)
        self.assertIn("gpu_defaults", data)
        defaults = data["gpu_defaults"]
        self.assertIn("matrix_sizes", defaults)
        self.assertIn("vector_sizes", defaults)
        self.assertEqual(len(defaults["matrix_sizes"]), 4)


class FrameworkDetectionTests(unittest.TestCase):
    """Verify framework detection infrastructure works."""

    def test_detect_frameworks_returns_dict(self) -> None:
        from infrastructure.gpu_runner import detect_frameworks
        frameworks = detect_frameworks()
        self.assertIsInstance(frameworks, dict)
        # Should always have entries even if not installed
        self.assertIn("pytorch", frameworks)
        self.assertIn("numpy", frameworks)

    def test_detect_gpu_returns_info(self) -> None:
        from infrastructure.gpu_runner import GPUDeviceInfo, detect_gpu
        info = detect_gpu()
        self.assertIsInstance(info, GPUDeviceInfo)

    def test_collect_environment_metadata(self) -> None:
        from infrastructure.gpu_runner import collect_environment_metadata
        meta = collect_environment_metadata()
        self.assertIn("platform", meta)
        self.assertIn("python_version", meta)
        self.assertIn("gpu", meta)
        self.assertIn("frameworks", meta)


if __name__ == "__main__":
    unittest.main()
