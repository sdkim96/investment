from pydantic import BaseModel

class AppConfig(BaseModel):
    name: str
    """The name of the application."""

    