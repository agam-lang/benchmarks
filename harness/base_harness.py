"""Base harness contract for all language-specific benchmark runners."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class PreparedBenchmark:
    """A fully resolved benchmark ready for compile + execute."""

    target_id: str
    target_name: str
    language: str
    backend: str | None
    compiler: str | None
    call_cache_enabled: bool
    compile_command: list[str] | None
    run_command: list[str]
    artifact_path: Path | None = None
    runtime_executable: Path | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseHarness:
    """Abstract harness that language-specific runners extend."""

    language = "unknown"
    suffixes: tuple[str, ...] = ()

    def __init__(self, environment: dict[str, Any], targets: dict[str, Any]) -> None:
        self.environment = environment
        self.targets = targets

    def can_handle(self, source: Path) -> bool:
        """Return True if this harness can run the given source file."""
        return source.suffix in self.suffixes

    def compatible_targets(
        self,
        target_filters: set[str] | None = None,
    ) -> list[tuple[str, dict[str, Any]]]:
        """Return targets whose language matches this harness."""
        compatible: list[tuple[str, dict[str, Any]]] = []
        for target_id, target_spec in self.targets["targets"].items():
            if target_spec.get("language") != self.language:
                continue
            if target_filters and target_id not in target_filters:
                continue
            compatible.append((target_id, target_spec))
        return compatible

    def prepare_variants(
        self,
        source: Path,
        build_root: Path,
        target_filters: set[str] | None = None,
    ) -> list[PreparedBenchmark]:
        """Prepare all compatible benchmark variants for a source file."""
        prepared: list[PreparedBenchmark] = []
        for target_id, target_spec in self.compatible_targets(target_filters):
            build_target = build_root / target_id
            build_target.parent.mkdir(parents=True, exist_ok=True)
            prepared.append(self.prepare(source, build_target, target_id, target_spec))
        return prepared

    def prepare(
        self,
        source: Path,
        build_target: Path,
        target_id: str,
        target_spec: dict[str, Any],
    ) -> PreparedBenchmark:
        """Prepare a single benchmark variant. Must be overridden."""
        raise NotImplementedError
