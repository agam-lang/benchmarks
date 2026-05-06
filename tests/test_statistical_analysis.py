"""Tests for the statistical analysis module."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from infrastructure.statistical_analyzer import (
    coefficient_of_variation,
    interquartile_range,
    median,
    percentile,
    std_dev,
    summarize,
)


class MedianTests(unittest.TestCase):
    def test_empty(self) -> None:
        self.assertEqual(median([]), 0.0)

    def test_single(self) -> None:
        self.assertEqual(median([42.0]), 42.0)

    def test_odd_count(self) -> None:
        self.assertEqual(median([1.0, 3.0, 2.0]), 2.0)

    def test_even_count(self) -> None:
        self.assertEqual(median([1.0, 2.0, 3.0, 4.0]), 2.5)


class PercentileTests(unittest.TestCase):
    def test_empty(self) -> None:
        self.assertEqual(percentile([], 50.0), 0.0)

    def test_median_via_percentile(self) -> None:
        self.assertAlmostEqual(percentile([1.0, 2.0, 3.0, 4.0, 5.0], 50.0), 3.0)

    def test_q1(self) -> None:
        result = percentile([1.0, 2.0, 3.0, 4.0, 5.0], 25.0)
        self.assertAlmostEqual(result, 2.0)

    def test_q3(self) -> None:
        result = percentile([1.0, 2.0, 3.0, 4.0, 5.0], 75.0)
        self.assertAlmostEqual(result, 4.0)


class IQRTests(unittest.TestCase):
    def test_simple(self) -> None:
        result = interquartile_range([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertAlmostEqual(result, 2.0)


class StdDevTests(unittest.TestCase):
    def test_single_value(self) -> None:
        self.assertEqual(std_dev([5.0]), 0.0)

    def test_uniform(self) -> None:
        self.assertEqual(std_dev([3.0, 3.0, 3.0]), 0.0)

    def test_known_values(self) -> None:
        result = std_dev([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
        self.assertAlmostEqual(result, 2.0, places=1)


class CVTests(unittest.TestCase):
    def test_empty(self) -> None:
        self.assertEqual(coefficient_of_variation([]), 0.0)

    def test_uniform(self) -> None:
        self.assertEqual(coefficient_of_variation([5.0, 5.0, 5.0]), 0.0)

    def test_nonzero(self) -> None:
        result = coefficient_of_variation([10.0, 20.0, 30.0])
        self.assertGreater(result, 0.0)


class SummarizeTests(unittest.TestCase):
    def test_empty(self) -> None:
        s = summarize([])
        self.assertEqual(s.count, 0)
        self.assertEqual(s.median_ns, 0.0)

    def test_basic(self) -> None:
        s = summarize([100.0, 200.0, 300.0, 400.0, 500.0])
        self.assertEqual(s.count, 5)
        self.assertEqual(s.median_ns, 300.0)
        self.assertEqual(s.mean_ns, 300.0)
        self.assertEqual(s.min_ns, 100.0)
        self.assertEqual(s.max_ns, 500.0)
        self.assertGreater(s.iqr_ns, 0.0)
        self.assertGreater(s.std_dev_ns, 0.0)
        self.assertGreater(s.coefficient_of_variation, 0.0)


if __name__ == "__main__":
    unittest.main()
