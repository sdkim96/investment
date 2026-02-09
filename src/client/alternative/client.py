from src.base import HTTPClientBase

from .resources.fng import FNGResource

class AlternativeClient(HTTPClientBase):

    def __init__(
        self
    ):
        super().__init__()
        
        self.fng = FNGResource(self)