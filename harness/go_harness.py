"""Harness for Go benchmark sources (.go files)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from harness.base_harness import BaseHarness, PreparedBenchmark
from infrastructure.utils import resolve_command_path


class GoHarness(BaseHarness):
    """Prepares compile and run commands for Go benchmarks."""

    language = "go"
    suffixes = (".go",)

    def prepare(
        self,
        source: Path,
        build_target: Path,
        target_id: str,
        target_spec: dict[str, Any],
    ) -> PreparedBenchmark:
        compiler_name = self.environment.get("go_compiler", "go")
        compiler_path = resolve_command_path(compiler_name)
        compiler = str(compiler_path) if compiler_path else compiler_name
        binary = build_target.with_suffix(".exe" if os.name == "nt" else "")

        compile_command = [
            compiler,
            "build",
            "-o",
            str(binary),
            str(source),
        ]

        return PreparedBenchmark(
            target_id=target_id,
            target_name=str(target_spec.get("name", target_id)),
            language=self.language,
            backend=None,
            compiler=compiler,
            call_cache_enabled=False,
            compile_command=compile_command,
            run_command=[str(binary)],
            artifact_path=binary,
            runtime_executable=binary,
        )
