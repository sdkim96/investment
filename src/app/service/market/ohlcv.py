from __future__ import annotations

import datetime as dt

from src.base import BaseModel

OHLCVData = dict[dt.datetime, 'OHLCV']

class OHLCV(BaseModel):

    open: int
    """Opening price."""

    high: int
    """Highest price."""

    low: int
    """Lowest price."""

    close: int
    """Closing price."""

    volume: float
    """Trading volume."""

    value: float
    """Trading value."""
