import typing as t

from .base import UpbitResourceBase
from ..types import (
    CreateOrderBody,
    Order,
)

class OrdersResource(UpbitResourceBase):
    
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
            .post(
                Order,
                url=url, 
                json=body,
                headers=self._build_headers(body)
            )
        )
        order, error = response
        if error:
            raise error
        if order is None:
            raise ValueError("Failed to create order: No order data returned.")
        return order