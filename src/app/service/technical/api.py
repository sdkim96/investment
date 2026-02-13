from .artifact import (
    Metrix,
    TechnicalArtifact,
)
from .sma import (
    SMAFn, 
    default_sma_fn
)
from .volatile import (
    VolatilityFn,
    default_volatility_fn
)
from ..market import MarketData
from ...config import AppConfig

class TechnicalAnalyzer: 


    def __init__(
        self, 
        config: AppConfig,
        *,
        sma_fn: SMAFn | None = None,
        volatility_fn: VolatilityFn | None = None,
    ) -> None:
        self.config = config
        self.sma_fn: SMAFn = sma_fn or default_sma_fn
        self.volatility_fn: VolatilityFn = volatility_fn or default_volatility_fn


    def analyze(
        self, 
        data: MarketData,
    ) -> TechnicalArtifact:
        ohlcv_data = data.get_ohlcv_data()

        sma = self.sma_fn(ohlcv_data)
        volatility = self.volatility_fn(ohlcv_data)
        
        return TechnicalArtifact(
            metrix=Metrix(
                sma=sma,
                volatility=volatility
            ),
        )
