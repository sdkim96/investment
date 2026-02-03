from src.base import BaseModel

class Event(BaseModel): 
    id: str
    """The unique identifier for the event."""
    
    type: str
    """The type/category of the event."""

    run_id: str
    """The ID of the run that generated this event."""


    @classmethod
    def Start(cls, run_id: str) -> "Event":
        return cls(
            id="start",
            type="system",
            run_id=run_id,
        )