"""Benchmark execution engine — compile, warm up, measure, collect."""

from __future__ import annotations

import json
import subprocess
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from infrastructure.statistical_analyzer import summarize
from infrastructure.utils import (
    RESULT_ROOT,
    ensure_directory,
    host_metadata,
    sanitize_preview,
    sha256_text,
    timestamp_label,
)


def _run_subprocess(
    command: list[str],
    *,
    timeout: float = 120.0,
) -> tuple[int, str, str, float]:
    """Run a subprocess and return (returncode, stdout, stderr, elapsed_ns)."""
    start = time.perf_counter_ns()
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter_ns() - start
        return -1, "", f"TIMEOUT after {timeout}s", float(elapsed)
    except FileNotFoundError as exc:
        elapsed = time.perf_counter_ns() - start
        return -1, "", str(exc), float(elapsed)
    elapsed = time.perf_counter_ns() - start
    return result.returncode, result.stdout, result.stderr, float(elapsed)


def compile_benchmark(
    compile_command: list[str] | None,
    *,
    timeout: float = 60.0,
) -> dict[str, Any] | None:
    """Compile a benchmark source. Returns compile metadata or None if no compile step."""
    if not compile_command:
        return None
    rc, stdout, stderr, elapsed_ns = _run_subprocess(compile_command, timeout=timeout)
    return {
        "command": compile_command,
        "returncode": rc,
        "elapsed_ns": elapsed_ns,
        "stdout_preview": sanitize_preview(stdout),
        "stderr_preview": sanitize_preview(stderr),
        "success": rc == 0,
    }


def run_benchmark(
    run_command: list[str],
    *,
    warmup_runs: int = 2,
    measured_runs: int = 7,
    timeout: float = 120.0,
) -> dict[str, Any]:
    """Execute a benchmark with warmup and measurement passes.

    Returns a dict with timing_ns list, stdout hash, and per-run metadata.
    """
    # Warmup
    for _ in range(warmup_runs):
        _run_subprocess(run_command, timeout=timeout)

    # Measurement
    timing_ns: list[float] = []
    stdout_hash: str | None = None
    stdout_preview: str = ""
    stderr_preview: str = ""

    for _ in range(measured_runs):
        rc, stdout, stderr, elapsed_ns = _run_subprocess(run_command, timeout=timeout)
        if rc != 0:
            return {
                "timing_ns": timing_ns,
                "stdout_hash": None,
                "stdout_preview": sanitize_preview(stdout),
                "stderr_preview": sanitize_preview(stderr),
                "success": False,
                "error": f"Non-zero exit code: {rc}",
            }
        timing_ns.append(elapsed_ns)
        current_hash = sha256_text(stdout)
        if stdout_hash is None:
            stdout_hash = current_hash
            stdout_preview = sanitize_preview(stdout)
            stderr_preview = sanitize_preview(stderr)
        elif current_hash != stdout_hash:
            return {
                "timing_ns": timing_ns,
                "stdout_hash": stdout_hash,
                "stdout_preview": stdout_preview,
                "stderr_preview": stderr_preview,
                "success": False,
                "error": "Non-deterministic output across runs",
            }

    stats = summarize(timing_ns)
    return {
        "timing_ns": timing_ns,
        "statistics": asdict(stats),
        "stdout_hash": stdout_hash,
        "stdout_preview": stdout_preview,
        "stderr_preview": stderr_preview,
        "success": True,
    }


def write_results(
    results: list[dict[str, Any]],
    *,
    label: str | None = None,
) -> Path:
    """Write benchmark results to a timestamped directory under results/raw/.

    Returns the output directory path.
    """
    ts = label or timestamp_label()
    output_dir = ensure_directory(RESULT_ROOT / "raw" / ts)

    metadata = {
        "timestamp": ts,
        "host": host_metadata(),
        "result_count": len(results),
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    (output_dir / "performance.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    return output_dir
