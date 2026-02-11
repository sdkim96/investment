from src.client import UpbitClient, AlternativeClient

from .data import FearAndGreedData, MarketData
from ...config import AppConfig
from ...types import CurrencyType

class MarketService: 


    def __init__(
        self,
        config: AppConfig,
        upbit: UpbitClient,
        alternative: AlternativeClient,
    ) -> None:
        self.config = config
        self.upbit = upbit
        self.alternative = alternative


    def get_data(self, currency: CurrencyType) -> MarketData:

        tickers = self.upbit.v1.ticker.get_all(
            ",".join(
                market.market 
                for market in self.upbit.v1.market.get_all() 
                if market.quote_currency == currency
            )
        )
        candles = self.upbit.v1.candles.get_by_days(
            market="KRW-BTC",
            count=200,
        )
        fng_entries = self.alternative.fng.get()
        return MarketData(
            currency=currency,
            tickers=tickers,
            candles=candles,
            fear_and_greed=FearAndGreedData(entries=fng_entries.data),
        )
        
