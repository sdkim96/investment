import typing as t

import httpx
import pydantic

ModelT = t.TypeVar("ModelT", bound=pydantic.BaseModel)

class HTTPClientBase:

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
    ) -> None:
        self._http_client = client or httpx.Client()


    def _get_one(
        self,
        fmt: t.Type[ModelT],
        *,
        url: str,
        params: dict[str, t.Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> t.Tuple[ModelT | None, Exception | None]:
        try:
            response = self._http_client.get(
                url,
                params=params,
                headers=headers,
            )
        except Exception as e:
            return None, e
        
        try:
            response.raise_for_status()
        except Exception as e:
            return None, e
        
        try:
            return fmt.model_validate(response.json()), None
        except Exception as e:
            return None, e
        

    def _get_list(
        self,
        fmt: t.Type[ModelT],
        *,
        url: str,
        params: dict[str, t.Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> t.Tuple[t.List[ModelT] | None, Exception | None]:
        try:
            response = self._http_client.get(
                url,
                params=params,
                headers=headers,
            )
        except Exception as e:
            return None, e
        
        try:
            response.raise_for_status()
        except Exception as e:
            return None, e
        
        try:
            data = response.json()
            return [fmt.model_validate(item) for item in data], None
        except Exception as e:
            return None, e
    

    def _post(
        self,
        fmt: t.Type[ModelT],
        *,
        url: str,
        json: dict[str, t.Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> t.Tuple[ModelT | None, Exception | None]:
        try:
            response = self._http_client.post(
                url,
                json=json,
                headers=headers,
            )
        except Exception as e:
            return None, e
        
        try:
            response.raise_for_status()
        except Exception as e:
            return None, e
        
        try:
            return fmt.model_validate(response.json()), None
        except Exception as e:
            return None, e
    

    def _delete(
        self,
        fmt: t.Type[ModelT],
        *,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> t.Tuple[ModelT | None, Exception | None]:
        try:
            response = self._http_client.delete(
                url,
                headers=headers,
            )
        except Exception as e:
            return None, e
        
        try:
            response.raise_for_status()
        except Exception as e:
            return None, e
        
        try:
            return fmt.model_validate(response.json()), None
        except Exception as e:
            return None, e

    
    