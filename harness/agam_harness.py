"""Harness for Agam benchmark sources (.agam files)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from harness.base_harness import BaseHarness, PreparedBenchmark
from infrastructure.utils import resolve_agam_driver, resolve_command_path


class AgamHarness(BaseHarness):
    """Prepares compile and run commands for Agam benchmarks."""

    language = "agam"
    suffixes = (".agam",)

    def prepare(
        self,
        source: Path,
        build_target: Path,
        target_id: str,
        target_spec: dict[str, Any],
    ) -> PreparedBenchmark:
        driver = self._resolve_driver()
        backend = str(target_spec["backend"])
        opt_level = int(target_spec.get("optimization_level", 2))
        call_cache_enabled = bool(target_spec.get("call_cache", False))
        build_then_run = bool(target_spec.get("build_then_run", True))
        binary = build_target.with_suffix(".exe" if os.name == "nt" else "")

        compile_command: list[str] | None
        run_command: list[str]
        artifact_path: Path | None

        if build_then_run:
            if backend == "c":
                generated_c = build_target.with_suffix(".c")
                c_compiler_name = self.environment.get("clang_c_compiler", "clang")
                c_compiler_path = resolve_command_path(c_compiler_name)
                c_compiler = str(c_compiler_path) if c_compiler_path else c_compiler_name

                raw_agam_build_command = [
                    *driver,
                    "build",
                    str(source),
                    "--backend",
                    backend,
                    "-O",
                    str(opt_level),
                    "--output",
                    str(generated_c),
                ]
                if call_cache_enabled:
                    raw_agam_build_command.append("--call-cache")

                if os.name == "nt":
                    quoted_args = " ".join([f"'{part}'" for part in raw_agam_build_command])
                    output_path = str(generated_c).replace("'", "''")
                    agam_build_command = [
                        "pwsh",
                        "-NoLogo",
                        "-NoProfile",
                        "-Command",
                        (
                            f"& {quoted_args}; "
                            f"if (Test-Path '{output_path}') {{ exit 0 }} "
                            f"else {{ exit $LASTEXITCODE }}"
                        ),
                    ]
                else:
                    agam_build_command = raw_agam_build_command

                native_build_command = [
                    c_compiler,
                ]
                if os.name == "nt":
                    native_build_command.extend(
                        [
                            "-include",
                            "sys/stat.h",
                            "-include",
                            "direct.h",
                            "-D_CRT_SECURE_NO_WARNINGS",
                            "-DS_ISREG(m)=(((m)&_S_IFMT)==_S_IFREG)",
                            "-DS_ISDIR(m)=(((m)&_S_IFMT)==_S_IFDIR)",
                        ]
                    )
                native_build_command.extend(
                    [
                        str(generated_c),
                        "-O3",
                        "-o",
                        str(binary),
                    ]
                )
                if os.name != "nt":
                    native_build_command.append("-lm")

                compile_command = [agam_build_command, native_build_command]
                run_command = [str(binary)]
                artifact_path = binary
                runtime_executable = binary
            else:
                compile_command = [
                    *driver,
                    "build",
                    str(source),
                    "--backend",
                    backend,
                    "-O",
                    str(opt_level),
                    "--output",
                    str(binary),
                ]
                if call_cache_enabled:
                    compile_command.append("--call-cache")
                run_command = [str(binary)]
                artifact_path = binary
                runtime_executable = binary
        else:
            compile_command = None
            run_command = [
                *driver,
                "run",
                str(source),
                "--backend",
                backend,
                "-O",
                str(opt_level),
            ]
            if call_cache_enabled:
                run_command.append("--call-cache")
            artifact_path = None
            runtime_executable = resolve_command_path(str(driver[0]))

        return PreparedBenchmark(
            target_id=target_id,
            target_name=str(target_spec.get("name", target_id)),
            language=self.language,
            backend=backend,
            compiler=self._compiler_label(driver[0], backend),
            call_cache_enabled=call_cache_enabled,
            compile_command=compile_command,
            run_command=run_command,
            artifact_path=artifact_path,
            runtime_executable=runtime_executable,
            metadata={"optimization_level": opt_level},
        )

    def _resolve_driver(self) -> list[str]:
        """Resolve the agamc driver command."""
        configured = self.environment.get("agam_driver", ["agamc"])
        resolved = resolve_agam_driver(str(configured[0]))
        if resolved:
            return [str(resolved), *configured[1:]]
        return configured

    def _compiler_label(self, driver: str, backend: str) -> str:
        """Return a readable compiler label for result rows."""
        if backend != "c":
            return str(driver)
        c_compiler_name = self.environment.get("clang_c_compiler", "clang")
        c_compiler_path = resolve_command_path(c_compiler_name)
        c_compiler = str(c_compiler_path) if c_compiler_path else c_compiler_name
        return f"{driver} + {c_compiler}"
