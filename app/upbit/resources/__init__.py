
from functools import cached_property

from .accounts import AccountsResource as Accounts
from .orders import OrdersResource as Orders


class V1:
    def __init__(self, client, upbit_config):
        self._client = client
        self._upbit_config = upbit_config

    @cached_property
    def accounts(self) -> Accounts:
        return Accounts(self._client, self._upbit_config)
    
    @cached_property
    def orders(self) -> Orders:
        return Orders(self._client, self._upbit_config)
        

__all__ = [
    "V1",
]