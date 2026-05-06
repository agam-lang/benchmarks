"""Tests for the compiler pipeline test suite — source existence and runner infrastructure."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

PIPELINE_ROOT = REPO_ROOT / "suites" / "10_compiler_pipeline"
EXPECTED_FILE = PIPELINE_ROOT / "expected_outputs.json"


class PipelineShapeTests(unittest.TestCase):
    """Verify compiler pipeline test directory structure."""

    def test_pipeline_root_exists(self) -> None:
        self.assertTrue(PIPELINE_ROOT.is_dir())

    def test_expected_outputs_exists(self) -> None:
        self.assertTrue(EXPECTED_FILE.is_file())

    EXPECTED_SUBDIRS = [
        "lexer", "parser", "type_system", "control_flow",
        "functions", "operators", "memory", "backends",
    ]

    def test_all_category_dirs_exist(self) -> None:
        for subdir in self.EXPECTED_SUBDIRS:
            self.assertTrue(
                (PIPELINE_ROOT / subdir).is_dir(),
                msg=f"Missing pipeline category: {subdir}",
            )

    def test_lexer_tests_exist(self) -> None:
        expected = ["keywords.agam", "operators.agam", "numeric_literals.agam",
                     "string_literals.agam"]
        for f in expected:
            self.assertTrue((PIPELINE_ROOT / "lexer" / f).is_file(), msg=f"Missing: {f}")

    def test_parser_tests_exist(self) -> None:
        expected = ["basic_expressions.agam", "function_definitions.agam",
                     "control_flow.agam", "nested_structures.agam", "annotations.agam"]
        for f in expected:
            self.assertTrue((PIPELINE_ROOT / "parser" / f).is_file(), msg=f"Missing: {f}")

    def test_type_system_tests_exist(self) -> None:
        expected = ["integer_types.agam", "type_inference.agam", "function_signatures.agam"]
        for f in expected:
            self.assertTrue((PIPELINE_ROOT / "type_system" / f).is_file(), msg=f"Missing: {f}")

    def test_control_flow_tests_exist(self) -> None:
        expected = ["if_else_chains.agam", "while_loops.agam", "nested_control.agam",
                     "early_return.agam"]
        for f in expected:
            self.assertTrue((PIPELINE_ROOT / "control_flow" / f).is_file(), msg=f"Missing: {f}")

    def test_functions_tests_exist(self) -> None:
        expected = ["recursion.agam", "mutual_recursion.agam",
                     "multiple_functions.agam", "function_composition.agam"]
        for f in expected:
            self.assertTrue((PIPELINE_ROOT / "functions" / f).is_file(), msg=f"Missing: {f}")

    def test_operators_tests_exist(self) -> None:
        expected = ["arithmetic.agam", "comparison.agam", "precedence.agam"]
        for f in expected:
            self.assertTrue((PIPELINE_ROOT / "operators" / f).is_file(), msg=f"Missing: {f}")

    def test_memory_tests_exist(self) -> None:
        expected = ["variable_scoping.agam", "shadowing.agam", "mutability.agam"]
        for f in expected:
            self.assertTrue((PIPELINE_ROOT / "memory" / f).is_file(), msg=f"Missing: {f}")

    def test_backend_tests_exist(self) -> None:
        expected = ["c_output_verify.agam", "llvm_output_verify.agam", "jit_execution.agam"]
        for f in expected:
            self.assertTrue((PIPELINE_ROOT / "backends" / f).is_file(), msg=f"Missing: {f}")


class ExpectedOutputsTests(unittest.TestCase):
    """Verify expected_outputs.json is consistent with test files."""

    def test_expected_outputs_valid_json(self) -> None:
        with open(EXPECTED_FILE) as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)

    def test_all_test_files_have_expected_output(self) -> None:
        with open(EXPECTED_FILE) as f:
            expected = json.load(f)
        # Remove comment keys
        expected = {k: v for k, v in expected.items() if not k.startswith("_")}

        all_tests = sorted(PIPELINE_ROOT.rglob("*.agam"))
        for test_path in all_tests:
            rel = test_path.relative_to(PIPELINE_ROOT).as_posix()
            self.assertIn(
                rel, expected,
                msg=f"Test file {rel} missing from expected_outputs.json",
            )

    def test_expected_count_matches_test_count(self) -> None:
        with open(EXPECTED_FILE) as f:
            expected = json.load(f)
        expected = {k: v for k, v in expected.items() if not k.startswith("_")}
        all_tests = list(PIPELINE_ROOT.rglob("*.agam"))
        self.assertEqual(len(expected), len(all_tests))


class CompilerTestRunnerTests(unittest.TestCase):
    """Verify the compiler test runner infrastructure."""

    def test_discover_pipeline_tests(self) -> None:
        from infrastructure.compiler_test_runner import discover_pipeline_tests
        tests = discover_pipeline_tests()
        self.assertGreaterEqual(len(tests), 29)

    def test_load_expected_outputs(self) -> None:
        from infrastructure.compiler_test_runner import load_expected_outputs
        outputs = load_expected_outputs()
        self.assertGreaterEqual(len(outputs), 29)
        self.assertIn("functions/recursion.agam", outputs)
        self.assertEqual(outputs["functions/recursion.agam"], "55\n")


if __name__ == "__main__":
    unittest.main()
