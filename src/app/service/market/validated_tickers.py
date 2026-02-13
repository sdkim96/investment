from src.base import BaseModel
from src.client.upbit.types import Ticker


class ValidatedTickers(BaseModel):
    ticker: Ticker
    """The ticker information."""

    volume: float
    """The calculated volume for validation."""

    change: float
    """The calculated change for validation."""

    volatility: float
    """The calculated volatility for validation."""
