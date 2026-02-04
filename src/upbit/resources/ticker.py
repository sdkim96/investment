
import typing as t

from .base import UpbitResourceBase
from ..types import (
    Ticker,
)

class TickerResource(UpbitResourceBase):
    
    def get_all(self, markets_joined_by_comma: str) -> t.List[Ticker]:
        url = "https://api.upbit.com/v1/ticker"
        response = self._get_list(
            Ticker, 
            params={"markets": markets_joined_by_comma},
            url=url, 
            headers=self._build_headers()
        )
        tickers, error = response
        if error:
            raise error
        if tickers is None:
            raise ValueError("Failed to fetch tickers: No ticker data returned.")
        return tickers
        