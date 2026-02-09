from __future__ import annotations
import typing as t

if t.TYPE_CHECKING:
    from ..client import UpbitClient

from ..types import (
    Market,
)

class MarketResource():
    
    def __init__(self, client: "UpbitClient") -> None:
        self._client = client

    def get_all(self) -> t.List[Market]:
        url = "https://api.upbit.com/v1/market/all"
        response = self._client._get_list(
            Market, 
            params={"is_details": True},
            url=url, 
            headers=self._client._utils._build_headers() #type: ignore
        )
        markets, error = response
        if error:
            raise error
        if markets is None:
            raise ValueError("Failed to fetch markets: No market data returned.")
        return markets
        