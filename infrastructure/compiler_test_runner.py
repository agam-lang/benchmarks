"""Compiler pipeline test runner — runs Agam programs and checks expected output."""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PIPELINE_ROOT = Path(__file__).resolve().parents[1] / "suites" / "10_compiler_pipeline"
EXPECTED_OUTPUTS_FILE = PIPELINE_ROOT / "expected_outputs.json"


@dataclass(slots=True)
class PipelineTestResult:
    """Result of a single compiler pipeline test."""

    test_path: str
    status: str  # "pass", "fail", "skip", "error"
    expected: str = ""
    actual: str = ""
    error_message: str = ""
    backend: str = "llvm"
    compile_time_ms: float = 0.0
    run_time_ms: float = 0.0


def load_expected_outputs() -> dict[str, str]:
    """Load expected outputs from JSON file."""
    if not EXPECTED_OUTPUTS_FILE.is_file():
        return {}
    with open(EXPECTED_OUTPUTS_FILE) as f:
        data = json.load(f)
    # Remove comments
    return {k: v for k, v in data.items() if not k.startswith("_")}


def discover_pipeline_tests() -> list[Path]:
    """Find all .agam files under the pipeline test directory."""
    if not PIPELINE_ROOT.is_dir():
        return []
    return sorted(PIPELINE_ROOT.rglob("*.agam"))


def resolve_agamc() -> str | None:
    """Find agamc on PATH."""
    return shutil.which("agamc")


def run_pipeline_test(
    source: Path,
    backend: str = "llvm",
    agamc_path: str | None = None,
    timeout: int = 30,
) -> PipelineTestResult:
    """Compile and run a single pipeline test, comparing stdout to expected."""
    import time

    rel_path = source.relative_to(PIPELINE_ROOT).as_posix()
    expected_outputs = load_expected_outputs()
    expected = expected_outputs.get(rel_path, "")

    driver = agamc_path or resolve_agamc()
    if not driver:
        return PipelineTestResult(
            test_path=rel_path, status="skip",
            error_message="agamc not found on PATH",
            backend=backend,
        )

    # Run via agamc run (interpret mode)
    try:
        t0 = time.perf_counter()
        result = subprocess.run(
            [driver, "run", str(source), "--backend", backend],
            capture_output=True, text=True, timeout=timeout,
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
    except subprocess.TimeoutExpired:
        return PipelineTestResult(
            test_path=rel_path, status="error",
            error_message=f"Timeout after {timeout}s",
            backend=backend,
        )
    except OSError as e:
        return PipelineTestResult(
            test_path=rel_path, status="error",
            error_message=str(e), backend=backend,
        )

    if result.returncode != 0:
        return PipelineTestResult(
            test_path=rel_path, status="error",
            expected=expected, actual=result.stdout,
            error_message=result.stderr.strip(),
            backend=backend, run_time_ms=elapsed_ms,
        )

    actual = result.stdout
    if expected and actual == expected:
        status = "pass"
    elif expected and actual != expected:
        status = "fail"
    else:
        # No expected output defined — just check it ran
        status = "pass"

    return PipelineTestResult(
        test_path=rel_path, status=status,
        expected=expected, actual=actual,
        backend=backend, run_time_ms=elapsed_ms,
    )


def run_all_pipeline_tests(
    backend: str = "llvm",
    agamc_path: str | None = None,
) -> list[PipelineTestResult]:
    """Run all discovered pipeline tests and return results."""
    tests = discover_pipeline_tests()
    results: list[PipelineTestResult] = []
    for test_source in tests:
        results.append(run_pipeline_test(test_source, backend, agamc_path))
    return results


def print_pipeline_summary(results: list[PipelineTestResult]) -> None:
    """Print a summary table of pipeline test results."""
    passed = sum(1 for r in results if r.status == "pass")
    failed = sum(1 for r in results if r.status == "fail")
    skipped = sum(1 for r in results if r.status == "skip")
    errors = sum(1 for r in results if r.status == "error")

    print(f"\nPipeline Test Summary: {passed} passed, {failed} failed, "
          f"{skipped} skipped, {errors} errors, {len(results)} total\n")

    for r in results:
        icon = {"pass": "✅", "fail": "❌", "skip": "⏭️", "error": "💥"}.get(r.status, "?")
        line = f"  {icon} {r.test_path}"
        if r.status == "fail":
            line += f"  (expected={r.expected!r}, got={r.actual!r})"
        elif r.status == "error":
            line += f"  ({r.error_message})"
        print(line)
