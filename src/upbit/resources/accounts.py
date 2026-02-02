import typing as t

from .base import UpbitResourceBase
from ..types import (
    Account,
)

class AccountsResource(UpbitResourceBase):
    
    def get(self) -> t.List[Account]:
        url = "https://api.upbit.com/v1/accounts"
        response = self.get_list(Account, url=url, headers=self._build_headers())
        accounts, error = response
        if error:
            raise error
        if accounts is None:
            raise ValueError("Failed to fetch accounts: No account data returned.")
        return accounts
        