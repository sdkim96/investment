import datetime as dt
import collections

from .artifact import (
    SentimentArtifact, 
    FearAndGreedClassification
)
from ..market import MarketData
from ...config import AppConfig

class SentimentAnalyzer: 


    def __init__(self, config: AppConfig) -> None:
        self.config = config
        
        fng_map: dict[int, FearAndGreedClassification] = collections.defaultdict(dict) # type: ignore
        
        for score in range(self.config.thresholds.sentiment.extreme_greed):
            if score < self.config.thresholds.sentiment.extreme_fear:
                fng_map[score] = FearAndGreedClassification(
                    state="Extreme Fear",
                    interpretation="The market is in extreme fear. Caution is advised.",
                    strategy_hint="Consider buying opportunities with caution."
                )
            elif score < self.config.thresholds.sentiment.fear:
                fng_map[score] = FearAndGreedClassification(
                    state="Fear",
                    interpretation="The market is fearful. Be cautious.",
                    strategy_hint="Consider defensive strategies."
                )
            elif score < self.config.thresholds.sentiment.greed:
                fng_map[score] = FearAndGreedClassification(
                    state="Greed",
                    interpretation="The market is greedy.",
                    strategy_hint="Enjoy the gains but stay vigilant. Get ready for profit-taking."
                )
            else:
                fng_map[score] = FearAndGreedClassification(
                    state="Extreme Greed",
                    interpretation="The market is in extreme greed. Caution is advised.",
                    strategy_hint="Consider taking profits or hedging."
                )
        
        self.fng_map = fng_map
        

    def analyze(self, data: MarketData) -> SentimentArtifact:

        if not data.fear_and_greed.entries:
            return SentimentArtifact.failed()
        
        today_index = data.fear_and_greed.get_entry(dt.datetime.today().strftime("%Y%m%d"))
        if today_index is None:
            today_index = data.fear_and_greed.entries[-1]
        
        sentiment_level = self.fng_map.get(today_index.value, FearAndGreedClassification(state="N/A", interpretation="N/A", strategy_hint="N/A"))
        return SentimentArtifact(
            sentiment_index=today_index.value,
            original_classfication=str(today_index.value),
            state=sentiment_level["state"],
            interpretation=sentiment_level["interpretation"],
            hint=sentiment_level["strategy_hint"],
        )