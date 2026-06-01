"""Tests for ohlc_tools.utils.timeframe."""

import pandas as pd
import pytest

from ohlc_tools.utils.timeframe import detect_timeframe


def _make_index(freq: str, periods: int, tz=None) -> pd.DatetimeIndex:
    return pd.date_range("2024-01-01", periods=periods, freq=freq, tz=tz)


class TestDetectTimeframe:
    def test_h1(self):
        idx = _make_index("1h", 100)
        assert "H1" in detect_timeframe(idx)

    def test_h4(self):
        idx = _make_index("4h", 100)
        assert "H4" in detect_timeframe(idx)

    def test_d1(self):
        idx = _make_index("1D", 30)
        assert "D1" in detect_timeframe(idx)

    def test_m1(self):
        idx = _make_index("1min", 500)
        assert "M1" in detect_timeframe(idx)

    def test_single_bar_returns_unknown(self):
        idx = pd.DatetimeIndex(["2024-01-01"])
        result = detect_timeframe(idx)
        assert "Unknown" in result
