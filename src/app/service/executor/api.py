from ..strategy import StrategyArtifact
from ...config import AppConfig

class ExecutorService: 

    def __init__(
        self,
        config: AppConfig,
    ) -> None:
        self.config = config



    def act_on_strategy(self, strategy_artifact: StrategyArtifact) -> None: ...