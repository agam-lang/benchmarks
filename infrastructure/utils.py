"""Shared utilities for the Agam cross-language benchmark suite."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover - optional dependency
    yaml = None


REPO_ROOT = Path(__file__).resolve().parents[1]
SUITE_ROOT = REPO_ROOT / "suites"
RESULT_ROOT = REPO_ROOT / "results"
CONFIG_ROOT = REPO_ROOT / "config"

SOURCE_SUFFIX_TO_LANGUAGE: dict[str, str] = {
    ".agam": "agam",
    ".py": "python",
    ".rs": "rust",
    ".c": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".go": "go",
}

COMPLEXITY_HINTS: dict[str, dict[str, str]] = {
    "fibonacci": {
        "time_complexity": "O(phi^n)",
        "space_complexity": "O(n)",
        "complexity_notes": "Naive recursive benchmark.",
    },
    "quicksort": {
        "time_complexity": "O(n log n)",
        "space_complexity": "O(log n)",
        "complexity_notes": "Synthetic partition-cost recursion shaped like quicksort.",
    },
    "binary_search": {
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "complexity_notes": "Scalar search over an implicit sorted range.",
    },
    "prime_sieve": {
        "time_complexity": "O(n*sqrt(n))",
        "space_complexity": "O(1)",
        "complexity_notes": "Direct primality scans, not a dense sieve array.",
    },
    "edit_distance": {
        "time_complexity": "O(rows*cols)",
        "space_complexity": "O(1)",
        "complexity_notes": "Edit-distance lattice scaffold without materializing the full DP matrix.",
    },
}


def ensure_directory(path: Path) -> Path:
    """Create directory and all parents if needed, return the path."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(path: Path) -> Any:
    """Load a JSON config file."""
    return json.loads(path.read_text(encoding="utf-8"))


def load_config() -> dict[str, Any]:
    """Load the default benchmark configuration."""
    return load_json(CONFIG_ROOT / "benchmark_config.json")


def load_targets() -> dict[str, Any]:
    """Load the comparison target definitions."""
    return load_json(CONFIG_ROOT / "comparison_targets.json")


def load_environments() -> dict[str, Any]:
    """Load the environment profiles."""
    return load_json(CONFIG_ROOT / "environments.json")


def timestamp_label() -> str:
    """Return a UTC timestamp string suitable for directory naming."""
    return datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")


def benchmark_name_for(path: Path) -> str:
    """Derive a flat benchmark name from a suite-relative source path."""
    relative = path.relative_to(SUITE_ROOT)
    return relative.as_posix().replace("/", "__").replace(".", "_")


def discover_benchmarks(
    suite_filters: list[str] | None = None,
    include_comparisons: bool = False,
    language_filters: set[str] | None = None,
    match_filters: list[str] | None = None,
) -> list[Path]:
    """Discover benchmark source files under SUITE_ROOT.

    Args:
        suite_filters: Only include sources from these suite directories.
        include_comparisons: If True, include sources under ``comparisons/`` subdirs.
        language_filters: Only include sources whose suffix maps to one of these languages.
        match_filters: Only include sources whose relative path contains one of these substrings (case-insensitive).

    Returns:
        Sorted list of absolute source Paths.
    """
    paths: list[Path] = []
    suite_filter_set = set(suite_filters or [])
    match_values = [value.lower() for value in (match_filters or [])]

    if not SUITE_ROOT.is_dir():
        return paths

    for path in sorted(SUITE_ROOT.rglob("*")):
        if not path.is_file():
            continue
        language = SOURCE_SUFFIX_TO_LANGUAGE.get(path.suffix)
        if language is None:
            continue
        if not include_comparisons and "comparisons" in path.parts:
            continue
        suite_name = path.relative_to(SUITE_ROOT).parts[0]
        if suite_filter_set and suite_name not in suite_filter_set:
            continue
        if language_filters and language not in language_filters:
            continue
        relative_text = path.relative_to(SUITE_ROOT).as_posix().lower()
        if match_values and not any(value in relative_text for value in match_values):
            continue
        paths.append(path)
    return paths


def sha256_text(value: str) -> str:
    """Return the hex SHA-256 digest of a UTF-8 string."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sanitize_preview(value: str, limit: int = 240) -> str:
    """Collapse whitespace and truncate a string for log previews."""
    compact = re.sub(r"\s+", " ", value).strip()
    return compact[:limit]


def current_environment_name() -> str:
    """Auto-detect the current benchmark environment name."""
    system = platform.system().lower()
    if os.environ.get("GITHUB_ACTIONS") == "true":
        if system == "windows":
            return "github_actions_windows"
        return "github_actions_linux"
    if os.environ.get("WSL_DISTRO_NAME"):
        return "wsl_ubuntu_24_04"
    if system == "windows":
        return "local_windows_win11"
    return "local_linux_native"


def host_metadata() -> dict[str, Any]:
    """Collect host platform metadata for result recording."""
    return {
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "processor": platform.processor(),
    }


def complexity_hint_for(path: Path) -> dict[str, str | None]:
    """Return time/space complexity hints for a benchmark source file."""
    return COMPLEXITY_HINTS.get(
        path.stem,
        {
            "time_complexity": None,
            "space_complexity": None,
            "complexity_notes": None,
        },
    )


def file_size_bytes(path: Path | None) -> int | None:
    """Return file size in bytes, or None if the path is missing."""
    if path is None or not path.exists() or not path.is_file():
        return None
    return path.stat().st_size


def resolve_command_path(command: str | None) -> Path | None:
    """Resolve a command name to an absolute path on this system."""
    if not command:
        return None
    resolved = shutil.which(command)
    if resolved:
        return Path(resolved)
    fallback = _resolve_windows_vs_llvm_tool(command)
    return fallback


def _resolve_windows_vs_llvm_tool(command: str) -> Path | None:
    """Try to find clang/clang++ via Visual Studio's bundled LLVM on Windows."""
    if os.name != "nt":
        return None
    if command not in {"clang", "clang++", "clang.exe", "clang++.exe"}:
        return None

    program_files_x86 = os.environ.get("ProgramFiles(x86)")
    if not program_files_x86:
        return None
    vswhere = (
        Path(program_files_x86)
        / "Microsoft Visual Studio"
        / "Installer"
        / "vswhere.exe"
    )
    if not vswhere.exists():
        return None

    try:
        completed = subprocess.run(
            [str(vswhere), "-latest", "-products", "*", "-property", "installationPath"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None

    install_root = Path(completed.stdout.strip())
    executable = "clang++.exe" if "++" in command else "clang.exe"
    candidate = install_root / "VC" / "Tools" / "Llvm" / "x64" / "bin" / executable
    return candidate if candidate.exists() else None
