"""GPU-aware benchmark runner with framework detection and device metadata."""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class GPUDeviceInfo:
    """Metadata about the GPU device used for benchmarking."""

    name: str = "unknown"
    vram_mb: int = 0
    cuda_version: str = "unknown"
    driver_version: str = "unknown"
    compute_capability: str = "unknown"


@dataclass(slots=True)
class FrameworkInfo:
    """Version info for a GPU/compute framework."""

    name: str
    version: str
    available: bool
    gpu_available: bool = False


def detect_gpu() -> GPUDeviceInfo:
    """Detect NVIDIA GPU via nvidia-smi or torch/cupy."""
    info = GPUDeviceInfo()

    # Try nvidia-smi first
    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi:
        try:
            result = subprocess.run(
                [nvidia_smi, "--query-gpu=name,memory.total,driver_version",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0:
                parts = result.stdout.strip().split(",")
                if len(parts) >= 3:
                    info.name = parts[0].strip()
                    info.vram_mb = int(float(parts[1].strip()))
                    info.driver_version = parts[2].strip()
        except (subprocess.TimeoutExpired, ValueError, OSError):
            pass

    # Try CUDA version from nvcc
    nvcc = shutil.which("nvcc")
    if nvcc:
        try:
            result = subprocess.run(
                [nvcc, "--version"], capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "release" in line.lower():
                        # e.g. "Cuda compilation tools, release 12.3, V12.3.107"
                        parts = line.split("release")
                        if len(parts) > 1:
                            info.cuda_version = parts[1].strip().rstrip(",").strip()
                        break
        except (subprocess.TimeoutExpired, OSError):
            pass

    return info


def detect_frameworks() -> dict[str, FrameworkInfo]:
    """Detect availability and versions of GPU/compute frameworks."""
    frameworks: dict[str, FrameworkInfo] = {}

    # PyTorch
    try:
        import torch
        frameworks["pytorch"] = FrameworkInfo(
            name="pytorch", version=torch.__version__,
            available=True, gpu_available=torch.cuda.is_available(),
        )
    except ImportError:
        frameworks["pytorch"] = FrameworkInfo(name="pytorch", version="", available=False)

    # CuPy
    try:
        import cupy
        gpu_ok = False
        try:
            cupy.cuda.Device(0).compute_capability
            gpu_ok = True
        except Exception:
            pass
        frameworks["cupy"] = FrameworkInfo(
            name="cupy", version=cupy.__version__, available=True, gpu_available=gpu_ok,
        )
    except ImportError:
        frameworks["cupy"] = FrameworkInfo(name="cupy", version="", available=False)

    # Numba
    try:
        import numba
        gpu_ok = False
        try:
            from numba import cuda
            gpu_ok = cuda.is_available()
        except Exception:
            pass
        frameworks["numba"] = FrameworkInfo(
            name="numba", version=numba.__version__, available=True, gpu_available=gpu_ok,
        )
    except ImportError:
        frameworks["numba"] = FrameworkInfo(name="numba", version="", available=False)

    # TensorFlow
    try:
        import tensorflow as tf
        gpu_ok = bool(tf.config.list_physical_devices("GPU"))
        frameworks["tensorflow"] = FrameworkInfo(
            name="tensorflow", version=tf.__version__,
            available=True, gpu_available=gpu_ok,
        )
    except ImportError:
        frameworks["tensorflow"] = FrameworkInfo(
            name="tensorflow", version="", available=False,
        )

    # NumPy (always CPU)
    try:
        import numpy
        frameworks["numpy"] = FrameworkInfo(
            name="numpy", version=numpy.__version__, available=True, gpu_available=False,
        )
    except ImportError:
        frameworks["numpy"] = FrameworkInfo(name="numpy", version="", available=False)

    return frameworks


@dataclass(slots=True)
class GPUBenchmarkResult:
    """Result from a GPU benchmark run."""

    workload: str
    framework: str
    device: str
    size: int | str
    timings_ns: list[int] = field(default_factory=list)
    median_ns: int = 0
    checksum: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


def run_gpu_benchmark_script(
    script_path: Path,
    args: list[str] | None = None,
    timeout: int = 120,
) -> list[dict[str, Any]]:
    """Run a GPU benchmark Python script and parse its JSON output."""
    import sys

    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)

    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout,
        cwd=str(script_path.parent),
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"GPU benchmark {script_path.name} failed:\n{result.stderr}"
        )

    return json.loads(result.stdout)


def collect_environment_metadata() -> dict[str, Any]:
    """Collect full environment metadata for reproducibility."""
    gpu_info = detect_gpu()
    frameworks = detect_frameworks()

    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "processor": platform.processor(),
        "gpu": asdict(gpu_info),
        "frameworks": {k: asdict(v) for k, v in frameworks.items()},
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
