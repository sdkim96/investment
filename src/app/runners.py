import typing as t

from src.client import (
    UpbitClient, 
    AlternativeClient,
)

from .config import AppConfig
from .event import Event
from .service.market import MarketService
from .service.sentiment import SentimentAnalyzer
from .service.technical import TechnicalAnalyzer
from .service.strategy import StrategyExecutor
from .service.executor import ExecutorService


class Runner: 

    def __init__(
        self,
        config: AppConfig,
        upbit_client: UpbitClient,
        alternative_client: AlternativeClient,
    ) -> None:
        self.market_service = MarketService(config, upbit_client, alternative_client)
        self.sentiment_analyzer = SentimentAnalyzer(config)
        self.technical_analyzer = TechnicalAnalyzer(config)
        self.strategy_executor = StrategyExecutor(config)
        self.executor_service = ExecutorService(config)


    
    def run(
        self, 
        run_id: str = "default_run"
    ) -> t.Iterable[Event]:
        
        yield Event.Start(run_id=run_id)
        data = self.market_service.get_data("KRW")
        
        yield Event.MarketDataFetched(data=data.to_dict())
        
        sentiment_artifact = self.sentiment_analyzer.analyze(data)
        technical_artifact = self.technical_analyzer.analyze(data)
        strategy_artifact = self.strategy_executor.execute(
            sentiment_artifact, 
            technical_artifact
        )
        
        self.executor_service.act_on_strategy(strategy_artifact)
    