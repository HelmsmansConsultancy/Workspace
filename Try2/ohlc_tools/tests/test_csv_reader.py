"""Tests for ohlc_tools.utils.csv_reader."""

import pytest
import pandas as pd

from ohlc_tools.utils.csv_reader import load_ohlc


class TestLoadOhlc:
    def test_returns_dataframe(self, sample_h1_csv):
        df = load_ohlc(sample_h1_csv)
        assert isinstance(df, pd.DataFrame)

    def test_index_is_datetime(self, sample_h1_csv):
        df = load_ohlc(sample_h1_csv)
        assert isinstance(df.index, pd.DatetimeIndex)

    def test_expected_rows(self, sample_h1_csv):
        df = load_ohlc(sample_h1_csv)
        assert len(df) == 5

    def test_ohlc_columns_present(self, sample_h1_csv):
        df = load_ohlc(sample_h1_csv)
        for col in ("open", "high", "low", "close"):
            assert col in df.columns

    def test_semicolon_delimiter(self, sample_semicolon_csv):
        df = load_ohlc(sample_semicolon_csv)
        assert len(df) == 2

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_ohlc(str(tmp_path / "nonexistent.csv"))
