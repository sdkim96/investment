import os
import httpx

from .resources import (
    V1,
)
from .types import UpbitConfig

class UpbitClient:

    def __init__(
        self,
        client: httpx.Client | None = None,
        *,
        access_key: str | None = None,
        secret_key: str | None = None,
    ) -> None:
        access_key = access_key or os.getenv("UPBIT_ACCESS_KEY")
        secret_key = secret_key or os.getenv("UPBIT_SECRET_KEY")
        if access_key is None or secret_key is None:
            raise ValueError("Both access_key and secret_key must be provided.")
         
        self._client = client or httpx.Client()
        self._upbit_config = UpbitConfig(
            access_key=access_key,
            secret_key=secret_key,
        )
        self.v1 = V1(
            self._client, 
            self._upbit_config,
        )