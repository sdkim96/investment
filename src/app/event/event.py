from src.base import BaseModel, JSONValue

class Event(BaseModel): 
    id: str
    """The unique identifier for the event."""
    
    type: str
    """The type/category of the event."""

    run_id: str
    """The ID of the run that generated this event."""

    data: JSONValue | None = None

    @classmethod
    def Start(cls, run_id: str) -> "Event":
        return cls(
            id="start",
            type="system",
            run_id=run_id,
        )
    
    @classmethod
    def MarketDataFetched(cls, data: JSONValue) -> "Event":
        return cls(
            id="market_data_fetched",
            type="market",
            run_id="default_run",
            data=data,
        )
    

    @classmethod
    def SentimentAnalyzed(cls, artifact: JSONValue) -> "Event":
        return cls(
            id="sentiment_analyzed",
            type="sentiment",
            run_id="default_run",
            data=artifact,
        )