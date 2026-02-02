from src.upbit.client import UpbitClient

from .data import MarketData
from ...config import AppConfig

class MarketService: 


    def __init__(
        self,
        config: AppConfig,
        client: UpbitClient,
    ) -> None:
        self.config = config
        self.client = client



    def get_data(self) -> MarketData: ...