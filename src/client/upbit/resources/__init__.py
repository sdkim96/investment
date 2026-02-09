from __future__ import annotations
import typing as t

if t.TYPE_CHECKING:
    from ..client import UpbitClient

from functools import cached_property

from .accounts import AccountsResource as Accounts
from .orders import OrdersResource as Orders
from .market import MarketResource as Market
from .ticker import TickerResource as Ticker

class V1:
    def __init__(self, client: "UpbitClient"):
        self._client = client


    @cached_property
    def accounts(self) -> Accounts:
        return Accounts(self._client)
    
    @cached_property
    def orders(self) -> Orders:
        return Orders(self._client)
    
    @cached_property
    def market(self) -> Market:
        return Market(self._client)
        
    @cached_property
    def ticker(self) -> Ticker:
        return Ticker(self._client)

__all__ = [
    "V1",
]