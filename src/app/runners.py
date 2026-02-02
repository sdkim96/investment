from src.upbit.client import UpbitClient

from .config import AppConfig
from .service.market import MarketService
from .service.sentiment import SentimentAnalyzer
from .service.technical import TechnicalAnalyzer
from .service.strategy import StrategyExecutor
from .service.executor import ExecutorService


class Runner: 

    def __init__(
        self,
        config: AppConfig,
        client: UpbitClient,
    ) -> None:
        self.market_service = MarketService(config, client)
        self.sentiment_analyzer = SentimentAnalyzer(config)
        self.technical_analyzer = TechnicalAnalyzer(config)
        self.strategy_executor = StrategyExecutor(config)
        self.executor_service = ExecutorService(config)


    
    def run(self) -> None:
        data = self.market_service.get_data()
        
        sentiment_artifact = self.sentiment_analyzer.analyze(data)
        technical_artifact = self.technical_analyzer.analyze(data)
        strategy_artifact = self.strategy_executor.execute(
            sentiment_artifact, 
            technical_artifact
        )
        
        self.executor_service.act_on_strategy(strategy_artifact)
