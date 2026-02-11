from __future__ import annotations

import datetime as dt
import typing as t

from src.base import BaseModel

from .ohlcv import OHLCVData


class SMAFn(t.Protocol):
    def __call__(
        self, 
        ohlcv_data: OHLCVData,
        *,
        period: int = 20
    ) -> SMA: ...


class SMA(BaseModel):

    values: t.Dict[dt.datetime, float | None]

    @property
    def slope(self) -> dict[dt.datetime, float | None]:
        sorted_dates = sorted(self.values.keys())
        slopes: dict[dt.datetime, float | None] = {}

        for i in range(1, len(sorted_dates)):
            date = sorted_dates[i]
            prev_date = sorted_dates[i - 1]

            v = self.values[date]
            pv = self.values[prev_date]

            if v is None or pv is None:
                slopes[date] = None
            else:
                slopes[date] = v - pv

        return slopes
    

def default_sma_fn(
    ohlcv_data: OHLCVData,
    *,
    period: int = 20
) -> SMA:
    dates = sorted(ohlcv_data.keys())
    values: dict[dt.datetime, float | None] = {}

    closes = [ohlcv_data[d].close for d in dates]

    for i, d in enumerate(dates):
        if i + 1 < period:
            values[d] = None
            continue

        window = closes[i + 1 - period : i + 1]
        values[d] = sum(window) / period

    return SMA(values=values)