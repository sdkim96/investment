from __future__ import annotations
import datetime as dt
import typing as t

if t.TYPE_CHECKING:
    from ..client import UpbitClient

from ..types import (
    Candle,
)

class CandlesResource:
    
    def __init__(self, client: "UpbitClient") -> None:
        self._client = client

    def get_by_days(self, *, market: str | None = None, count: int | None = None) -> t.List[Candle]:
        url = "https://api.upbit.com/v1/candles/days"
        candles, error = self._client._get_list(
            Candle, 
            params={
                'market': market or "KRW-BTC", 
                'to': dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                'count': count or 200,
            },
            url=url, 
        )
        if error:
            raise error
        if candles is None:
            raise ValueError("Failed to fetch candles: No candle data returned.")
        return candles
        