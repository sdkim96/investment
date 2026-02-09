from __future__ import annotations
import typing as t

if t.TYPE_CHECKING:
    from ..client import UpbitClient


from ..types import (
    Ticker,
)

class TickerResource:

    def __init__(self, client: "UpbitClient") -> None:
        self._client = client
    
    def get_all(self, markets_joined_by_comma: str) -> t.List[Ticker]:
        url = "https://api.upbit.com/v1/ticker"
        response = self._client._get_list(
            Ticker, 
            params={"markets": markets_joined_by_comma},
            url=url, 
            headers=self._client._utils._build_headers() #type: ignore
        )
        tickers, error = response
        if error:
            raise error
        if tickers is None:
            raise ValueError("Failed to fetch tickers: No ticker data returned.")
        return tickers
        