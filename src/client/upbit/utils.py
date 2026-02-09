import uuid
import hashlib
import jwt
import typing as t
from urllib.parse import urlencode

from ..upbit.types import (
    UpbitConfig, 
    UpbitHeaders
)


class UpbitUtils:


    def __init__(self, config: UpbitConfig) -> None:
        self._upbit_config = config

    def _build_headers(self, data: t.Any | None = None) -> UpbitHeaders:
        payload = {
            "access_key": self._upbit_config['access_key'],
            "nonce": str(uuid.uuid4())
        }

        if data:
            m = hashlib.sha512()
            m.update(urlencode(data, doseq=True).replace("%5B%5D=", "[]=").encode())
            query_hash = m.hexdigest()
            payload['query_hash'] = query_hash
            payload['query_hash_alg'] = "SHA512"

        jwt_token = jwt.encode(payload, self._upbit_config['secret_key'], algorithm="HS256")
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = UpbitHeaders(
            Authorization=authorization_token
        )
        return headers