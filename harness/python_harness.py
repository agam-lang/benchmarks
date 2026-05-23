"""Harness for Python benchmark sources (.py files)."""

from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path
from typing import Any

from harness.base_harness import BaseHarness, PreparedBenchmark
from infrastructure.utils import resolve_command_path


class PythonHarness(BaseHarness):
    """Prepares run commands for Python benchmarks (no compile step)."""

    language = "python"
    suffixes = (".py",)
    STDLIB_MODULES = set(sys.stdlib_module_names)

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
        skip_reason = self._skip_reason_for(source)

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
            skip_reason=skip_reason,
        )

    def _skip_reason_for(self, source: Path) -> str | None:
        try:
            tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        except (OSError, SyntaxError):
            return None

        missing: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            else:
                continue

            for name in names:
                module_name = name.split(".")[0]
                if module_name in self.STDLIB_MODULES:
                    continue
                if importlib.util.find_spec(module_name) is None and module_name not in missing:
                    missing.append(module_name)

        if missing:
            return "missing Python modules: " + ", ".join(sorted(missing))
        return None
