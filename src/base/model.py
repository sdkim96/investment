import typing as t
from collections.abc import Mapping

import pydantic

from .types import JSONValue

class BaseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
        use_attribute_docstrings=True,
    )

    def to_dict(self) -> dict[str, JSONValue]:
        return t.cast(dict[str, JSONValue], self.model_dump(mode="json"))

    @classmethod
    def from_dict(cls, data: Mapping[str, JSONValue]) -> t.Self:
        return cls.model_validate(data)