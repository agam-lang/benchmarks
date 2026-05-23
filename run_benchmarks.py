#!/usr/bin/env python3
"""Top-level CLI for running the Agam benchmark suite."""

import argparse
import sys
from pathlib import Path
from typing import Any

# Ensure project root is in path
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from infrastructure.utils import (
    load_config,
    load_targets,
    load_environments,
    discover_benchmarks,
    current_environment_name,
    benchmark_name_for,
    ensure_directory,
    file_size_bytes,
    resolve_command_path,
)
from infrastructure.benchmark_runner import compile_benchmark, run_benchmark, write_results
from harness.agam_harness import AgamHarness
from harness.c_harness import CHarness
from harness.cpp_harness import CppHarness
from harness.rust_harness import RustHarness
from harness.go_harness import GoHarness
from harness.python_harness import PythonHarness


def required_tools_for(prepared) -> list[str]:
    """Return the invocable commands required for this benchmark variant."""
    if prepared.compile_command:
        if isinstance(prepared.compile_command[0], list):
            return [command[0] for command in prepared.compile_command]
        return [prepared.compile_command[0]]
    return [prepared.run_command[0]]


def tool_available(command: str) -> bool:
    """Return True when a command can be executed on this host."""
    return resolve_command_path(command) is not None


def skip_entry_for(prepared, command: str) -> dict[str, Any]:
    """Return a stable skip summary record for later aggregation/reporting."""
    return {
        "target_id": prepared.target_id,
        "name": prepared.target_name,
        "command": command,
        "count": 0,
    }


def main():
    parser = argparse.ArgumentParser(description="Run Agam benchmark suite")
    parser.add_argument("--suites", nargs="+", help="Filter by suite directories")
    parser.add_argument("--matches", nargs="+", help="Filter by workload names")
    parser.add_argument("--targets", nargs="+", help="Filter by target IDs")
    parser.add_argument("--no-comparisons", action="store_true", help="Skip comparison languages")
    parser.add_argument("--warmup", type=int, help="Override warmup runs")
    parser.add_argument("--measured", type=int, help="Override measured runs")
    
    args = parser.parse_args()
    
    config = load_config()
    targets = load_targets()
    envs = load_environments()
    
    env_name = current_environment_name()
    env_spec = envs["environments"].get(env_name, {})
    
    harnesses = [
        AgamHarness(env_spec, targets),
        CHarness(env_spec, targets),
        CppHarness(env_spec, targets),
        RustHarness(env_spec, targets),
        GoHarness(env_spec, targets),
        PythonHarness(env_spec, targets),
    ]
    
    include_comparisons = not args.no_comparisons
    sources = discover_benchmarks(
        suite_filters=args.suites,
        match_filters=args.matches,
        include_comparisons=include_comparisons
    )
    
    if not sources:
        print("No benchmarks discovered with current filters.")
        return

    target_filters = set(args.targets) if args.targets else set(config["defaults"]["default_targets"])
    warmup_runs = args.warmup if args.warmup is not None else config["defaults"]["warmup_runs"]
    measured_runs = args.measured if args.measured is not None else config["defaults"]["measured_runs"]
    
    all_results = []
    skipped_targets: dict[str, dict[str, Any]] = {}
    tool_availability: dict[str, bool] = {}
    build_root = REPO_ROOT / "build"
    ensure_directory(build_root)
    
    print(f"Running {len(sources)} benchmark sources on {env_name}...")
    
    for source in sources:
        bench_name = benchmark_name_for(source)
        print(f"\nWorkload: {source.relative_to(REPO_ROOT / 'suites')}")
        
        for harness in harnesses:
            if not harness.can_handle(source):
                continue
            
            prepared_variants = harness.prepare_variants(source, build_root / bench_name, target_filters)
            
            for prepared in prepared_variants:
                print(f"  Target: {prepared.target_name} ({prepared.target_id})")
                if prepared.skip_reason:
                    skip_key = f"{prepared.target_id}::{prepared.skip_reason}"
                    skipped = skipped_targets.setdefault(
                        skip_key,
                        skip_entry_for(prepared, prepared.skip_reason),
                    )
                    skipped["count"] += 1
                    if skipped["count"] == 1:
                        print(f"    [-] Skipping target: {prepared.skip_reason}")
                    continue
                missing_tool = None
                for required_tool in required_tools_for(prepared):
                    available = tool_availability.get(required_tool)
                    if available is None:
                        available = tool_available(required_tool)
                        tool_availability[required_tool] = available
                    if not available:
                        missing_tool = required_tool
                        break

                if missing_tool is not None:
                    skipped = skipped_targets.setdefault(
                        prepared.target_id,
                        skip_entry_for(prepared, missing_tool),
                    )
                    skipped["count"] += 1
                    if skipped["count"] == 1:
                        print(f"    [-] Skipping target: missing tool '{missing_tool}'")
                    continue
                
                # Compilation
                compile_meta = compile_benchmark(prepared.compile_command)
                if compile_meta and not compile_meta["success"]:
                    print(f"    [!] Compilation failed: {compile_meta['stderr_preview']}")
                    continue
                
                # Execution
                run_res = run_benchmark(
                    prepared.run_command,
                    warmup_runs=warmup_runs,
                    measured_runs=measured_runs
                )
                
                if not run_res["success"]:
                    print(f"    [!] Execution failed: {run_res.get('error', 'unknown error')}")
                    continue
                
                # Collect result
                result = {
                    "workload": str(source.relative_to(REPO_ROOT / 'suites')),
                    "benchmark_name": bench_name,
                    "target_id": prepared.target_id,
                    "target_name": prepared.target_name,
                    "language": prepared.language,
                    "backend": prepared.backend,
                    "compiler": prepared.compiler,
                    "compilation": compile_meta,
                    "execution": run_res,
                    "binary_size_bytes": file_size_bytes(prepared.artifact_path),
                }
                all_results.append(result)
                
                stats = run_res["statistics"]
                median_ms = stats['median_ns'] / 1_000_000.0
                stddev_ms = stats['std_dev_ns'] / 1_000_000.0
                print(f"    Result: {median_ms:.3f} ms (+/-{stddev_ms:.3f})")

    if all_results:
        output_dir = write_results(all_results)
        print(f"\nResults written to: {output_dir}")
    else:
        print("\nNo results collected.")

    if skipped_targets:
        print("\nSkipped targets:")
        for _, skipped in sorted(skipped_targets.items(), key=lambda item: (item[1]["target_id"], item[1]["command"])):
            print(
                f"  {skipped['name']} ({skipped['target_id']}): "
                f"{skipped['count']} workload(s), missing {skipped['command']}"
            )

if __name__ == "__main__":
    main()
