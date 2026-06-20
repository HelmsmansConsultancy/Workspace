"""
tabular.utils.display
=========================

Terminal display helpers (formatting, units).
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd


def human_size(num_bytes: int) -> str:
    """Return a human-readable file size string."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes //= 1024
    return f"{num_bytes:.1f} PB"


def format_datetime(dt: datetime | pd.Timestamp | None) -> str:
    """Format a datetime for display, including timezone when available."""
    if dt is None:
        return "N/A"
    ts = pd.Timestamp(dt)
    base = ts.strftime("%Y-%m-%d %H:%M:%S " + str(ts.microsecond)[:-3])
    if ts.tzinfo is not None:
        tz = str(ts.tzinfo)
        return f"{base}  [{tz}]"
    return base
