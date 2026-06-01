"""
conftest.py — shared pytest fixtures.
"""

from __future__ import annotations

import io
import textwrap

import pandas as pd
import pytest


@pytest.fixture
def sample_h1_csv(tmp_path) -> str:
    """Write a tiny H1 OHLC CSV to a temp file and return its path."""
    content = textwrap.dedent("""\
        datetime,open,high,low,close,volume
        2024-01-02 00:00:00,1.10500,1.10620,1.10480,1.10590,1234
        2024-01-02 01:00:00,1.10590,1.10700,1.10550,1.10650,2100
        2024-01-02 02:00:00,1.10650,1.10800,1.10600,1.10750,1875
        2024-01-02 03:00:00,1.10750,1.10900,1.10700,1.10800,2300
        2024-01-02 04:00:00,1.10800,1.10950,1.10760,1.10870,1990
    """)
    p = tmp_path / "eurusd_h1.csv"
    p.write_text(content, encoding="utf-8")
    return str(p)


@pytest.fixture
def sample_semicolon_csv(tmp_path) -> str:
    """OHLC CSV with semicolon delimiter."""
    content = textwrap.dedent("""\
        date;open;high;low;close
        2024-01-02;1.10500;1.10620;1.10480;1.10590
        2024-01-03;1.10590;1.10700;1.10550;1.10650
    """)
    p = tmp_path / "eurusd_semi.csv"
    p.write_text(content, encoding="utf-8")
    return str(p)
