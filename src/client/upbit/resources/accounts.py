from __future__ import annotations
import typing as t

if t.TYPE_CHECKING:
    from ..client import UpbitClient

from ..types import (
    Account,
)

class AccountsResource:

    def __init__(self, client: "UpbitClient") -> None:
        self._client = client
    
    def get(self) -> t.List[Account]:
        url = "https://api.upbit.com/v1/accounts"
        accounts, error = self._client._get_list(
            Account, 
            url=url, 
            headers=self._client._utils._build_headers() #type: ignore
        )
        if error:
            raise error
        if accounts is None:
            raise ValueError("Failed to fetch accounts: No account data returned.")
        return accounts
        