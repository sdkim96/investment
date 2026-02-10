from __future__ import annotations

from src.base import BaseModel


class AppConfig(BaseModel):
    name: str
    """The name of the application."""

    thresholds: Thresholds
    """The threshold configurations.
    This could include sentiment and technical parameters.
    """
    

class Thresholds(BaseModel):
    sentiment: SentimentThresholds
    """Represents the sentiment threshold configurations."""

    technical: TechnicalThresholds
    """Represents the technical threshold configurations."""


class SentimentThresholds(BaseModel):
    extreme_fear: int
    """Threshold for extreme fear sentiment.
    if fng(Fear and Greed) index is below this value, 
    the market is considered to be in extreme fear.
    """

    fear: int
    """Threshold for fear sentiment.
    if fng(Fear and Greed) index is below this value,
    the market is considered to be in fear.
    """

    greed: int
    """Threshold for greed sentiment.
    if fng(Fear and Greed) index is above this value,
    the market is considered to be in greed.
    """

    extreme_greed: int
    """Threshold for extreme greed sentiment.
    if fng(Fear and Greed) index is above this value,
    the market is considered to be in extreme greed.
    """


class TechnicalThresholds(BaseModel):
    ma_period: int
    """The moving average period for technical analysis.
    This period is used to determine market trends.
    """