
import typing as t

from .base import UpbitResourceBase
from ..types import (
    Market,
)

class MarketResource(UpbitResourceBase):
    
    def get_all(self) -> t.List[Market]:
        url = "https://api.upbit.com/v1/market/all"
        response = self._get_list(
            Market, 
            params={"is_details": True},
            url=url, 
            headers=self._build_headers()
        )
        markets, error = response
        if error:
            raise error
        if markets is None:
            raise ValueError("Failed to fetch markets: No market data returned.")
        return markets
        