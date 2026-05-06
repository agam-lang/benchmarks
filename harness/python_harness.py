"""Harness for Python benchmark sources (.py files)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from harness.base_harness import BaseHarness, PreparedBenchmark
from infrastructure.utils import resolve_command_path


class PythonHarness(BaseHarness):
    """Prepares run commands for Python benchmarks (no compile step)."""

    language = "python"
    suffixes = (".py",)

    def prepare(
        self,
        source: Path,
        build_target: Path,
        target_id: str,
        target_spec: dict[str, Any],
    ) -> PreparedBenchmark:
        interpreter_key = target_spec.get("interpreter_key", "cpython")
        interpreter_name = self.environment.get(interpreter_key, sys.executable)
        interpreter_path = resolve_command_path(interpreter_name)
        interpreter = str(interpreter_path) if interpreter_path else interpreter_name

        return PreparedBenchmark(
            target_id=target_id,
            target_name=str(target_spec.get("name", target_id)),
            language=self.language,
            backend=None,
            compiler=interpreter,
            call_cache_enabled=False,
            compile_command=None,
            run_command=[interpreter, str(source)],
            artifact_path=None,
            runtime_executable=Path(interpreter),
        )
