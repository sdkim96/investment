from __future__ import annotations

import typing as t
import pydantic
from typing_extensions import TypedDict

from src.base import BaseModel

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



class Market(BaseModel):
    """Represents a market data structure returned by the Upbit API."""

    market: str
    """Market code.
    [Example: "KRW-BTC"]
    """

    korean_name: str
    """Korean name of the market."""

    english_name: str
    """English name of the market."""

    market_event: MarketEvent
    """Market caution event."""

    @property
    def quote_currency(self) -> str:
        """Represents the head of the market code, indicating the quote currency."""
        return f"{self.market.split('-')[0]}"


class MarketEvent(BaseModel):
    warning: bool
    """Indicates if there is warning for the market.
    The warning flag is true when the market is under caution due to abnormal price movements or other factors.
    """

    caution: Caution
    """Represents the detailed caution information for the market."""


class Caution(BaseModel):

    price_fluctuations: bool = pydantic.Field(alias="PRICE_FLUCTUATIONS")
    """Represents whether there is a price fluctuation caution for the market."""

    trading_volume_soaring: bool = pydantic.Field(alias="TRADING_VOLUME_SOARING")
    """Represents whether there is a trading volume soaring caution for the market."""

    deposit_amount_soaring: bool = pydantic.Field(alias="DEPOSIT_AMOUNT_SOARING")
    """Represents whether there is a deposit amount soaring caution for the market."""

    global_price_differences: bool = pydantic.Field(alias="GLOBAL_PRICE_DIFFERENCES")
    """Represents whether there is a global price differences caution for the market."""

    concentration_of_small_accounts: bool = pydantic.Field(alias="CONCENTRATION_OF_SMALL_ACCOUNTS")
    """Represents whether there is a concentration of small accounts caution for the market."""

from pydantic import BaseModel
from typing_extensions import Literal


class Ticker(BaseModel):
    """Represents ticker data returned by the Upbit API."""

    market: str
    """Trading pair code representing the market.
    [Example] "KRW-BTC"
    """

    trade_date: str
    """Recent trade date in UTC.
    [Format] yyyyMMdd
    """

    trade_time: str
    """Recent trade time in UTC.
    [Format] HHmmss
    """

    trade_date_kst: str
    """Recent trade date in KST.
    [Format] yyyyMMdd
    """

    trade_time_kst: str
    """Recent trade time in KST.
    [Format] HHmmss
    """

    trade_timestamp: int
    """The timestamp (in milliseconds) when the trade was executed."""

    opening_price: float
    """The opening price of the candle,
    representing the first trading price during the candle period.
    """

    high_price: float
    """The highest trading price,
    recorded during the candle period.
    """

    low_price: float
    """The lowest trading price,
    recorded during the candle period.
    """

    trade_price: float
    """The closing price of the candle,
    representing the last trading price during the candle period.
    """

    prev_closing_price: float
    """Previous day's closing price, based on UTC."""

    change: Literal["EVEN", "RISE", "FALL"]
    """Status of price change.

    EVEN: No change
    RISE: Increase
    FALL: Decrease
    """

    change_price: float
    """Absolute value of the price change compared to the previous day's closing price.
    Calculated as "trade_price" - "prev_closing_price".
    """

    change_rate: float
    """Absolute value of the price change rate compared to the previous day's closing price.
    """

    signed_change_price: float
    """Price change compared to the previous day's closing price.

    Positive (+): Current price is higher than previous day's closing price
    Negative (-): Current price is lower than previous day's closing price
    """

    signed_change_rate: float
    """Signed price change rate compared to the previous day's closing price.
    [Example] 0.015 = 1.5% increase.
    """

    trade_volume: float
    """Most recent trade volume for the trading pair."""

    acc_trade_price: float
    """Accumulated trade amount since UTC 00:00."""

    acc_trade_price_24h: float
    """Accumulated trade amount over the past 24 hours."""

    acc_trade_volume: float
    """Accumulated trade volume since UTC 00:00."""

    acc_trade_volume_24h: float
    """Accumulated trade volume over the past 24 hours."""

    highest_52_week_price: float
    """Highest trading price achieved in the past 52 weeks."""

    highest_52_week_date: str
    """Date when the 52-week high price was achieved.
    [Format] yyyy-MM-dd
    """

    lowest_52_week_price: float
    """Lowest trading price achieved in the past 52 weeks."""

    lowest_52_week_date: str
    """Date when the 52-week low price was achieved.
    [Format] yyyy-MM-dd
    """

    timestamp: int
    """The timestamp (in milliseconds) when the ticker was requested."""

    # ----------------------
    # Derived properties
    # ----------------------

    @property
    def quote_currency(self) -> str:
        """Quote currency (e.g. 'KRW' in 'KRW-BTC')."""
        return self.market.split("-")[0]

    @property
    def base_currency(self) -> str:
        """Base asset (e.g. 'BTC' in 'KRW-BTC')."""
        return self.market.split("-")[1]


class Candle(BaseModel):
    market: str
    """Trading pair code representing the market."""

    candle_date_time_utc: str
    """Candle date and time in UTC.
    [Format] yyyy-MM-ddTHH:mm:ssZ
    """

    candle_date_time_kst: str
    """Candle date and time in KST.
    [Format] yyyy-MM-ddTHH:mm:ss+09:00
    """

    opening_price: int
    """The opening price of the candle,
    representing the first trading price during the candle period.
    """

    high_price: int
    """The highest trading price,
    recorded during the candle period.
    """

    low_price: int
    """The lowest trading price,
    recorded during the candle period.
    """

    trade_price: int
    """The closing price of the candle,
    representing the last trading price during the candle period.
    """

    timestamp: int
    """The timestamp (in milliseconds) when the candle was requested."""

    candle_acc_trade_price: float
    """Accumulated trade amount during the candle period."""

    candle_acc_trade_volume: float
    """Accumulated trade volume during the candle period."""

    prev_closing_price: int
    """Previous day's closing price, based on UTC."""

    change_price: int
    """Absolute value of the price change compared to the previous day's closing price.
    Calculated as "trade_price" - "prev_closing_price".
    """

    change_rate: float
    """Absolute value of the price change rate compared to the previous day's closing price.
    """


