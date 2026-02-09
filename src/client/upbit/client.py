import os

from .resources import V1
from .types import UpbitConfig
from .utils import UpbitUtils

from src.base import HTTPClientBase

class UpbitClient(HTTPClientBase):

    def __init__(
        self,
        *,
        access_key: str | None = None,
        secret_key: str | None = None,
    ) -> None:
        
        super().__init__()

        access_key = access_key or os.getenv("UPBIT_ACCESS_KEY")
        secret_key = secret_key or os.getenv("UPBIT_SECRET_KEY")
        if access_key is None or secret_key is None:
            raise ValueError("Both access_key and secret_key must be provided.")
        
        self._utils = UpbitUtils(
            UpbitConfig(
                access_key=access_key,
                secret_key=secret_key,
            )
        )
        self.v1 = V1(self)
        