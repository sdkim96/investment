from __future__ import annotations

from src.base import BaseModel

from .sma import (
    SMA,
)
from .volatile import (
    Volatility,
)


class Metrix(BaseModel):

    sma: SMA
    """The Simple Moving Average (SMA) data."""

    volatility: Volatility
    """The Volatility data."""


class TechnicalArtifact(BaseModel): 

    metrix: Metrix
    """The computed technical metrix."""
