import httpx
import jwt
import uuid
import hashlib
import typing as t
from urllib.parse import urlencode

from pydantic import BaseModel

from ..types import (
    UpbitConfig, 
    UpbitHeaders
)
from ..errors import (
    UpbitError,
    UpbitHTTPError,
    UpbitNetworkError,
    UpbitAPIErrorPayload,
    UpbitDecodeError,
    UpbitUsageError,
    UpbitValidationError,
)

ModelT = t.TypeVar("ModelT", bound=BaseModel)

class UpbitResourceBase:
    
    def __init__(
        self,
        client: httpx.Client,
        upbit_config: UpbitConfig,
    ) -> None:
        self._client = client
        self._upbit_config = upbit_config

    
    def _get_one(
        self,
        fmt: t.Type[ModelT],
        *,
        url: str,
        params: dict[str, t.Any] | None = None,
        headers: UpbitHeaders | None = None,
    ) -> t.Tuple[ModelT | None, UpbitError | None]:
        try:
            response = self._client.get(
                url,
                params=params,
                headers=headers, # type: ignore
            ) 
        except Exception as e:
            return None, UpbitNetworkError(str(e))
        try:
            response.raise_for_status()
        except Exception as e:
            return None, UpbitHTTPError.from_response(response)
    
        try:
            return fmt.model_validate(response.json()), None
        except Exception as e:
            return None, UpbitDecodeError(str(e))
        

    def _get_list(
        self,
        fmt: t.Type[ModelT],
        *,
        url: str,
        params: dict[str, t.Any] | None = None,
        headers: UpbitHeaders | None = None,
    ) -> t.Tuple[t.List[ModelT] | None, UpbitError | None]:
        try:
            response = self._client.get(
                url,
                params=params,
                headers=headers, # type: ignore
            ) 
        except Exception as e:
            return None, UpbitNetworkError(str(e))
        try:
            response.raise_for_status()
        except Exception as e:
            return None, UpbitHTTPError.from_response(response)
    
        try:
            return [fmt.model_validate(item) for item in response.json()], None
        except Exception as e:
            return None, UpbitDecodeError(str(e))
        
    
    def _post(
        self,
        fmt: t.Type[ModelT],
        *,
        url: str,
        json: dict[str, t.Any] | None = None,
        headers: UpbitHeaders | None = None,
    ) -> t.Tuple[ModelT | None, UpbitError | None]:
        try:
            response = self._client.post(
                url,
                json=json,
                headers=headers, # type: ignore
            ) 
        except Exception as e:
            return None, UpbitNetworkError(str(e))
        try:
            response.raise_for_status()
        except Exception as e:
            return None, UpbitHTTPError.from_response(response)
        
        try:
            return fmt.model_validate(response.json()), None
        except Exception as e:
            return None, UpbitDecodeError(str(e))
        

    def _delete(
        self,
        fmt: t.Type[ModelT],
        *,
        url: str,
        headers: UpbitHeaders | None = None,
    ) -> t.Tuple[ModelT | None, UpbitError | None]:
        try:
            response = self._client.delete(
                url,
                headers=headers, # type: ignore
            ) 
        except Exception as e:
            return None, UpbitNetworkError(str(e))
        try:
            response.raise_for_status()
        except Exception as e:
            return None, UpbitHTTPError.from_response(response)
        
        try:
            return fmt.model_validate(response.json()), None
        except Exception as e:
            return None, UpbitDecodeError(str(e))


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
    

