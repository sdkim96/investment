import typing as t

from src.base import BaseModel
from src.upbit.types import Ticker

from ...types import CurrencyType


class ValidatedTickers(BaseModel):
    ticker: Ticker
    """The ticker information."""

    volume: float
    """The calculated volume for validation."""

    change: float
    """The calculated change for validation."""

    volatility: float
    """The calculated volatility for validation."""


def _default_volume_calculation(ticker: Ticker) -> float:
    return ticker.acc_trade_volume_24h

def _default_change_calculation(ticker: Ticker) -> float:
    return ticker.signed_change_rate * 100    

def _default_volatility_calculation(ticker: Ticker) -> float:
    return ((ticker.high_price - ticker.low_price) / ticker.trade_price) * 100 if ticker.trade_price > 0 else 0
    
def _default_sort_by(validated_ticker: ValidatedTickers) -> float:
    return validated_ticker.change * validated_ticker.volume


class MarketData(BaseModel): 

    currency: CurrencyType
    """The currency type for the market data."""

    tickers: t.List[Ticker]
    """List of tickers for the specified currency."""


    def calculate_validated_tickers(
        self,
        custom_volume_fn: t.Callable[[Ticker], float] = _default_volume_calculation,
        custom_change_fn: t.Callable[[Ticker], float] = _default_change_calculation,
        custom_volatility_fn: t.Callable[[Ticker], float] = _default_volatility_calculation,
        sort_by_fn: t.Callable[[ValidatedTickers], float] = _default_sort_by,
        *,
        sort_reverse: bool = True,
        top_n: t.Optional[int] = None,
    ) -> t.List[ValidatedTickers]:
        """Calculate and return validated tickers based on custom criteria."""
        
        validated_tickers: t.List[ValidatedTickers] = []
        for ticker in self.tickers:
            volume = custom_volume_fn(ticker)
            change = custom_change_fn(ticker)
            volatility = custom_volatility_fn(ticker)

            validated_tickers.append(
                ValidatedTickers(
                    ticker=ticker,
                    volume=volume,
                    change=change,
                    volatility=volatility,
                )
            )
        
        validated_tickers.sort(key=sort_by_fn, reverse=sort_reverse)
        if top_n is not None:
            validated_tickers = validated_tickers[:top_n]
        return validated_tickers


