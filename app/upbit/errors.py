from __future__ import annotations

import typing as t
from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class UpbitAPIErrorPayload:
    name: str
    message: str


class UpbitError(Exception):
    """Base exception for all Upbit SDK errors."""


class UpbitHTTPError(UpbitError):
    """HTTP error (non-2xx) returned from Upbit API."""

    def __init__(
        self,
        status_code: int,
        *,
        payload: UpbitAPIErrorPayload | None = None,
        response_text: str | None = None,
        request_url: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.payload = payload
        self.response_text = response_text
        self.request_url = request_url
        super().__init__(self.__str__())

    @classmethod
    def from_response(cls, resp: httpx.Response) -> "UpbitHTTPError":
        payload: UpbitAPIErrorPayload | None = None
        text: str | None = None
        try:
            text = resp.text
        except Exception:
            text = None

        try:
            data = resp.json()
            err = data.get("error")
            if isinstance(err, dict):
                name = err.get("name")
                message = err.get("message")
                if isinstance(name, str) and isinstance(message, str):
                    payload = UpbitAPIErrorPayload(name=name, message=message)
        except Exception:
            pass

        return cls(
            resp.status_code,
            payload=payload,
            response_text=text,
            request_url=str(resp.request.url) if resp.request else None,
        )

    def __str__(self) -> str:
        if self.payload:
            return f"[UpbitHTTPError {self.status_code}] {self.payload.name}: {self.payload.message}"
        return f"[UpbitHTTPError {self.status_code}] {self.response_text or 'HTTP error'}"


class UpbitNetworkError(UpbitError):
    """Network/transport error (DNS, timeout, connection, etc.)."""


class UpbitDecodeError(UpbitError):
    """Response could not be decoded as JSON."""


class UpbitValidationError(UpbitError):
    """Response JSON could not be validated into a Pydantic model."""


class UpbitUsageError(UpbitError):
    """Client-side misuse, e.g., invalid order body before hitting API."""