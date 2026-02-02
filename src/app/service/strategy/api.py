from .artifact import StrategyArtifact
from ..sentiment import SentimentArtifact
from ..technical import TechnicalArtifact
from ...config import AppConfig

class StrategyExecutor: 

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        

    def execute(
        self, 
        sentiment_artifact: SentimentArtifact, 
        technical_artifact: TechnicalArtifact
    ) -> StrategyArtifact:
        # Implement strategy execution logic here
        pass