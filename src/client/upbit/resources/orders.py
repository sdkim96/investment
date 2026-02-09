from __future__ import annotations
import typing as t

if t.TYPE_CHECKING:
    from ..client import UpbitClient

from ..types import (
    CreateOrderBody,
    Order,
)

class OrdersResource():
    
    def __init__(self, client: "UpbitClient") -> None:
        self._client = client

    def create(
        self,
        market: str = "KRW-BTC",
        price: int = 1000,
    ) -> Order:
        url = "https://api.upbit.com/v1/orders"
        body = CreateOrderBody(
            market=market,
            side="bid",
            ord_type="price",
            price=str(price),
        ).model_dump(mode="json", exclude_none=True)
        
        response = (
            self
            ._client
            ._post(
                Order,
                url=url, 
                json=body,
                headers=self._client._utils._build_headers(body) #type: ignore
            )
        )
        order, error = response
        if error:
            raise error
        if order is None:
            raise ValueError("Failed to create order: No order data returned.")
        return order