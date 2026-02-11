import datetime as dt
import typing as t

from src.client.upbit.types import Candle

from .artifact import (
    Signal,
    Metrix,
    SignalFn,
    TechnicalArtifact,
    default_signal_fn
)
from .ohlcv import (
    OHLCV, 
    OHLCVData
)
from .sma import (
    SMA, 
    SMAFn, 
    default_sma_fn
)
from .volatile import (
    Volatility,
    VolatilityFn,
    default_volatility_fn
)
from ..sentiment import SentimentArtifact
from ..market import MarketData
from ...config import AppConfig

class TechnicalAnalyzer: 


    def __init__(
        self, 
        config: AppConfig,
        *,
        sma_fn: SMAFn | None = None,
        volatility_fn: VolatilityFn | None = None,
        signal_fn: SignalFn | None = None,
    ) -> None:
        self.config = config
        self.sma_fn: SMAFn = sma_fn or default_sma_fn
        self.volatility_fn: VolatilityFn = volatility_fn or default_volatility_fn
        self.signal_fn: SignalFn = signal_fn or default_signal_fn


    def _convert_candles_to_ohlcv(
        self, 
        candles: t.List[Candle]
    ) -> OHLCVData:
        ohlcv_data: OHLCVData = {}
        
        for candle in candles:
            ohlcv = OHLCV(
                open=candle.opening_price,
                high=candle.high_price,
                low=candle.low_price,
                close=candle.trade_price,
                volume=candle.candle_acc_trade_volume,
                value=candle.candle_acc_trade_price,
            )
            ohlcv_data[dt.datetime.fromisoformat(candle.candle_date_time_utc)] = ohlcv
        
        return ohlcv_data


    def analyze(
        self, 
        market_data: MarketData,
        sentiment_artifact: SentimentArtifact,
    ) -> TechnicalArtifact:
        ohlcv_data = self._convert_candles_to_ohlcv(market_data.candles)

        sma = self.sma_fn(ohlcv_data)
        volatility = self.volatility_fn(ohlcv_data)
        signal = self.signal_fn(
            ohlcv_data=ohlcv_data,
            sma_data=sma,
            volatility_data=volatility,
            sentiment_data=sentiment_artifact
        )
        return TechnicalArtifact(
            metrix=Metrix(
                sma=sma,
                volatility=volatility
            ),
            signal=signal
        )
