import typing as t
from typing_extensions import TypedDict

from pydantic import BaseModel

class UpbitConfig(TypedDict):
    """Represents the required configuration for Upbit API access."""
    
    access_key: str
    """The access key for Upbit API authentication."""
    
    secret_key: str
    """The secret key for Upbit API authentication."""


class UpbitHeaders(TypedDict):
    """Represents the headers required for Upbit API requests."""
    
    Authorization: str
    """The authorization header containing the JWT token."""


class Account(BaseModel):
    """Represents the account data structure returned by Upbit API."""

    currency: str
    """The currency code to be queried."""

    balance: str
    """Available amount or volume for orders.
    For digital assets, this represents the available quantity. 
    For fiat currency, this represents the available amount.
    """

    locked: str
    """Amount or quantity locked by pending orders or withdrawals."""

    avg_buy_price: str
    """Average purchase price of the asset."""

    avg_buy_price_modified: bool
    """Indicates if the average buy price has been modified."""

    unit_currency: str
    """The unit currency for the account.
    [Example: "KRW", "BTC", "USDT"]
    """


class CreateOrderBody(BaseModel):
    """Represents the request body for creating an order via the Upbit API."""

    market: str
    """Trading pair code for which the order will be created.
    [Example: "KRW-BTC"]
    """

    side: t.Literal["ask", "bid"]
    """Order side.
    - bid: Buy order
    - ask: Sell order
    """

    volume: str | None = None
    """Order quantity (numeric string).

    Required for:
    - Limit buy/sell (ord_type = "limit")
    - Market sell (ord_type = "market")
    - Best limit sell (side = "ask" and ord_type = "best")
    """

    price: str | None = None
    """Order unit price or total purchase amount (numeric string).

    Required for:
    - Limit buy/sell (ord_type = "limit")
    - Market buy (ord_type = "price")
    - Best limit buy (side = "bid" and ord_type = "best")

    Usage depends on order type:
    - Limit order: unit price
    - Market buy / Best buy: total purchase amount
    """

    ord_type: t.Literal["limit", "price", "market", "best"] = "limit"
    """Order type.
    - limit: Limit buy/sell order (default)
    - price: Market buy order
    - market: Market sell order
    - best: Best limit buy/sell order (time_in_force required)
    """

    identifier: str | None = None
    """Client-specified unique order identifier.
    Once used, an identifier cannot be reused.
    """

    time_in_force: t.Literal["fok", "ioc", "post_only"] | None = None
    """Order execution policy.

    - ioc: Immediate or Cancel
    - fok: Fill or Kill
    - post_only: Post Only

    Notes:
    - Optional for limit orders
    - Required (ioc or fok) for best limit orders (ord_type = "best")
    """

    smp_type: t.Literal["cancel_maker", "cancel_taker", "reduce"] | None = None
    """Self-Match Prevention (SMP) mode.
    - cancel_maker: Cancel existing maker order
    - cancel_taker: Cancel new taker order
    - reduce: Reduce both order quantities to prevent self-trading
    """


class Order(BaseModel):
    """Represents an order data structure returned by the Upbit API."""

    market: str
    """Trading pair code representing the market.
    [Example: "KRW-BTC"]
    """

    uuid: str
    """Unique identifier (UUID) for the order."""

    side: t.Literal["ask", "bid"]
    """Order side.
    - ask: Sell
    - bid: Buy
    """

    ord_type: t.Literal["limit", "price", "market", "best"]
    """Order type.
    - limit: Limit order
    - price: Market buy (amount-based)
    - market: Market sell
    - best: Best order
    """

    price: str | None = None
    """Order unit price or total amount.
    - For limit orders: unit price
    - For market buy orders: total purchase amount
    """

    state: t.Literal["wait", "watch", "done", "cancel"]
    """Order status.
    - wait: Waiting for execution
    - watch: Scheduled order
    - done: Execution completed
    - cancel: Order cancelled
    """

    created_at: str
    """Order creation time in KST.
    [Format: yyyy-MM-ddTHH:mm:ss+09:00]
    """

    volume: str | None = None
    """Order request amount or quantity."""

    remaining_volume: str
    """Remaining order quantity after execution."""

    executed_volume: str
    """Executed order quantity."""

    reserved_fee: str
    """Fee amount reserved for the order."""

    remaining_fee: str
    """Remaining fee amount."""

    paid_fee: str
    """Fee amount paid at the time of execution."""

    locked: str
    """Amount or quantity locked by pending orders or trades."""

    trades_count: int
    """Number of trades executed for the order."""

    time_in_force: t.Literal["fok", "ioc", "post_only"] | None = None
    """Order execution policy applied in the response.
    - fok: Fill or Kill
    - ioc: Immediate or Cancel
    - post_only: Post Only
    """

    identifier: str | None = None
    """Order identifier specified by the client at order creation.
    This field is only provided for orders created on or after October 18, 2024.
    """

    smp_type: t.Literal["reduce", "cancel_maker", "cancel_taker"] | None = None
    """Self-Match Prevention (SMP) mode applied in the response."""

    prevented_volume: str
    """Quantity cancelled due to self-match prevention (SMP)."""

    prevented_locked: str
    """Assets released due to self-match prevention (SMP).
    - For buy orders: Cancelled amount
    - For sell orders: Cancelled quantity
    """
