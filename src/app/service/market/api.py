from src.upbit.client import UpbitClient

from .data import MarketData
from ...config import AppConfig
from ...types import CurrencyType

class MarketService: 


    def __init__(
        self,
        config: AppConfig,
        client: UpbitClient,
    ) -> None:
        self.config = config
        self.client = client


    def get_data(self, currency: CurrencyType) -> MarketData:

        tickers = self.client.v1.ticker.get_all(
            ",".join(
                market.market 
                for market in self.client.v1.market.get_all() 
                if market.quote_currency == currency
            )
        )
        return MarketData(
            currency=currency,
            tickers=tickers,
        )
        
