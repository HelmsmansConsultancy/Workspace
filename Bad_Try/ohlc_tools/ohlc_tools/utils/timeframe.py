"""
ohlc_tools.utils.timeframe
===========================

Helpers for detecting and labelling OHLC timeframes.
"""

from __future__ import annotations

from collections import Counter

import pandas as pd


# Human-readable labels keyed by interval in seconds
_TIMEFRAME_LABELS: dict[int, str] = {
    60:       "1 minute  (M1)",
    300:      "5 minutes (M5)",
    600:      "10 minutes (M10)",
    900:      "15 minutes (M15)",
    1800:     "30 minutes (M30)",
    3600:     "1 hour  (H1)",
    7200:     "2 hours (H2)",
    14400:    "4 hours (H4)",
    28800:    "8 hours (H8)",
    86400:    "1 day  (D1)",
    604800:   "1 week (W1)",
    2592000:  "1 month (MN)",
}

# Pandas offset aliases for resampling, keyed by user-friendly label
PANDAS_FREQ_ALIASES: dict[str, str] = {
    "M1":  "1min",
    "M5":  "5min",
    "M15": "15min",
    "M30": "30min",
    "H1":  "1h",
    "H2":  "2h",
    "H4":  "4h",
    "H8":  "8h",
    "D":   "1D",
    "W":   "1W",
    "M":   "1ME",
}


def detect_timeframe(index: pd.DatetimeIndex) -> str:
    """Infer the dominant bar interval from a sorted DatetimeIndex.

    Weekend / holiday gaps are excluded by capping at 4× the median delta.

    Parameters
    ----------
    index : pd.DatetimeIndex
        Sorted index of bar timestamps.

    Returns
    -------
    str
        Human-readable timeframe label (e.g. ``"1 hour  (H1)"``).
    """
    if len(index) < 2:
        return "Unknown (too few bars)"

    sorted_idx = index.sort_values()
    deltas = (
        sorted_idx[1:].asi8 - sorted_idx[:-1].asi8
    ) // 1_000_000_000          # nanoseconds → seconds

    # Filter obvious gaps (weekends, holidays)
    positive = [d for d in deltas if d > 0]
    if not positive:
        return "Unknown (no positive gaps)"

    sorted_d = sorted(positive)
    median   = sorted_d[len(sorted_d) // 2]
    filtered = [d for d in positive if d <= median * 4]

    most_common_seconds, _ = Counter(filtered).most_common(1)[0]
    return _TIMEFRAME_LABELS.get(
        most_common_seconds,
        f"{most_common_seconds} seconds",
    )
