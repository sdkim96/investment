from __future__ import annotations
import typing as t

if t.TYPE_CHECKING:
    from ..client import AlternativeClient

from ..types import (
    FNGResponse,
)

class FNGResource:

    def __init__(self, client: "AlternativeClient") -> None:
        self._client = client


    def get(self) -> FNGResponse:
        url = "https://api.alternative.me/fng/"
        response = self._client._get_one(
            FNGResponse, 
            url=url, 
            params={"limit": 10}
        )
        fng_index, error = response
        if error:
            raise error
        if fng_index is None:
            raise ValueError("Failed to fetch Fear and Greed Index: No data returned.")
        return fng_index