from __future__ import annotations

import typing as t

from src.base import BaseModel

from .ohlcv import (
    OHLCVData,
)
from .sma import (
    SMA,
)
from .volatile import (
    Volatility,
)
from ..sentiment import SentimentArtifact


class SignalFn(t.Protocol):
    def __call__(
        self, 
        *,
        ohlcv_data: OHLCVData,
        sma_data: SMA,
        volatility_data: Volatility,
        sentiment_data: SentimentArtifact,
        **kwargs
    ) -> Signal: ...


class Signal(BaseModel):

    name: t.Literal['RED', 'YELLOW', 'GREEN']
    """The name of the signal."""

    reason: str
    """The reason for the signal."""

    action: str
    """The recommended action for the signal."""


class Metrix(BaseModel):

    sma: SMA
    """The Simple Moving Average (SMA) data."""

    volatility: Volatility
    """The Volatility data."""


class TechnicalArtifact(BaseModel): 

    signal: Signal
    """The generated technical signal."""

    metrix: Metrix
    """The computed technical metrix."""


def default_signal_fn(
    *,
    ohlcv_data: OHLCVData,
    sma_data: SMA,
    volatility_data: Volatility,
    sentiment_data: SentimentArtifact,
    **kwargs
) -> Signal:
    return Signal(
        name="GREEN",
        reason="Market sentiment indicates extreme greed.",
        action="Consider buying opportunities."
    )
    match sentiment_data.state:

        case "Extreme Greed":
            return Signal(
                name="GREEN",
                reason="Market sentiment indicates extreme greed.",
                action="Consider buying opportunities."
            )
    
    if sentiment_data.state in ["Extreme Fear", "Fear"]:
        return Signal(
            name="RED",
            reason="Market sentiment indicates extreme fear.",
            action="Avoid trading or consider selling positions."
        )