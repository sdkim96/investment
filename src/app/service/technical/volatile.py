from __future__ import annotations

import datetime as dt
import typing as t

from src.base import BaseModel

from .ohlcv import OHLCVData


class VolatilityFn(t.Protocol):
    def __call__(
        self,
        ohlcv_data: OHLCVData,
        *,
        period: int = ...
    ) -> Volatility: ...

    
class Volatility(BaseModel):

    values: t.Dict[dt.datetime, float | None]


def default_volatility_fn(
    ohlcv_data: OHLCVData,
    *,
    period: int = 14
) -> Volatility:
    dates = sorted(ohlcv_data.keys())
    values: dict[dt.datetime, float | None] = {}

    trs: list[float] = []

    for i, d in enumerate(dates):
        o = ohlcv_data[d]

        if i == 0:
            tr = o.high - o.low
        else:
            prev_close = ohlcv_data[dates[i - 1]].close
            tr = max(
                o.high - o.low,
                abs(o.high - prev_close),
                abs(o.low - prev_close),
            )

        trs.append(tr)

        if i + 1 < period:
            values[d] = None
        else:
            values[d] = sum(trs[i + 1 - period : i + 1]) / period

    return Volatility(values=values)