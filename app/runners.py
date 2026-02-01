class Runner: 

    def __init__(
        self,
        market_service: MarketService,
        sentiment_analyzer: SentimentAnalyzer,
        technical_analyzer: TechnicalAnalyzer,
        strategy_executor: StrategyExecutor,
    ) -> None:
        self.market_service = market_service
        self.semtiment_analyzer = sentiment_analyzer
        self.technical_analyzer = technical_analyzer
        self.strategy_executor = strategy_executor


    
    def run(self) -> None:
        self.market_service.fetch_data()
        self.semtiment_analyzer.analyze()
        self.technical_analyzer.analyze()
        self.strategy_executor.execute()