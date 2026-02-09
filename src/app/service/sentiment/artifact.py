from src.base import BaseModel


class SentimentArtifact(BaseModel): 

    sentiment_index: float

    original_classfication: str

    state: str

    interpretation: str

    hint: str