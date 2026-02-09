from __future__ import annotations

import typing as t

from src.base import BaseModel


class FNGResponse(BaseModel):
    name: str
    """The name of the index."""

    data: t.List[FearAndGreedEntry]
    """A list of Fear and Greed Index entries."""

    metadata: dict[str, t.Any]
    """Additional metadata about the response."""


class FearAndGreedEntry(BaseModel):
    value: str
    """The numeric value of the Fear and Greed Index."""

    value_classification: str
    """The classification of the index value (e.g., 'Fear', 'Greed')."""

    timestamp: int
    """The timestamp of the index entry."""

    time_until_update: str | None = None
    """Time remaining until the next update of the index."""