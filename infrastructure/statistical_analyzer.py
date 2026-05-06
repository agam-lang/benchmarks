"""Statistical analysis utilities for benchmark results."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(slots=True)
class StatisticalSummary:
    """Summary statistics for a set of timing measurements."""

    count: int
    median_ns: float
    mean_ns: float
    min_ns: float
    max_ns: float
    iqr_ns: float
    std_dev_ns: float
    coefficient_of_variation: float


def median(values: list[float]) -> float:
    """Return the median of a sorted-copy of *values*."""
    if not values:
        return 0.0
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2 == 0:
        return (s[mid - 1] + s[mid]) / 2.0
    return s[mid]


def percentile(values: list[float], p: float) -> float:
    """Return the *p*-th percentile (0–100) using linear interpolation."""
    if not values:
        return 0.0
    s = sorted(values)
    k = (p / 100.0) * (len(s) - 1)
    lo = int(math.floor(k))
    hi = int(math.ceil(k))
    if lo == hi:
        return s[lo]
    frac = k - lo
    return s[lo] * (1.0 - frac) + s[hi] * frac


def interquartile_range(values: list[float]) -> float:
    """Return Q3 − Q1."""
    return percentile(values, 75.0) - percentile(values, 25.0)


def std_dev(values: list[float]) -> float:
    """Population standard deviation."""
    if len(values) < 2:
        return 0.0
    m = sum(values) / len(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / len(values))


def coefficient_of_variation(values: list[float]) -> float:
    """CV = std_dev / mean, as a percentage. Returns 0 if mean is zero."""
    if not values:
        return 0.0
    m = sum(values) / len(values)
    if m == 0.0:
        return 0.0
    return (std_dev(values) / m) * 100.0


def summarize(timing_ns: list[float]) -> StatisticalSummary:
    """Produce a full statistical summary from a list of timing values in nanoseconds."""
    if not timing_ns:
        return StatisticalSummary(
            count=0,
            median_ns=0.0,
            mean_ns=0.0,
            min_ns=0.0,
            max_ns=0.0,
            iqr_ns=0.0,
            std_dev_ns=0.0,
            coefficient_of_variation=0.0,
        )
    return StatisticalSummary(
        count=len(timing_ns),
        median_ns=median(timing_ns),
        mean_ns=sum(timing_ns) / len(timing_ns),
        min_ns=min(timing_ns),
        max_ns=max(timing_ns),
        iqr_ns=interquartile_range(timing_ns),
        std_dev_ns=std_dev(timing_ns),
        coefficient_of_variation=coefficient_of_variation(timing_ns),
    )
