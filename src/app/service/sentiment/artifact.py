from __future__ import annotations

import typing as t
from typing_extensions import TypedDict

from src.base import BaseModel

class FearAndGreedClassification(TypedDict):

    state: t.Literal["Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed"]
    """The sentiment classification based on the Fear and Greed index."""

    interpretation: str
    """The interpretation of the sentiment classification."""

    strategy_hint: str
    """The strategy hint based on the sentiment classification."""



class SentimentArtifact(BaseModel): 

    sentiment_index: float | None = None

    original_classfication: str

    state: str

    interpretation: str

    hint: str

    @classmethod
    def failed(cls) -> SentimentArtifact:
        return cls(
            sentiment_index=None,
            original_classfication="N/A",
            state="N/A",
            interpretation="N/A",
            hint="No data available to analyze sentiment."
        )