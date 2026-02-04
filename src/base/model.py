import typing as t
from collections.abc import Mapping

import pydantic

from .types import JSONValue

class BaseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
        use_attribute_docstrings=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    def to_dict(self) -> dict[str, t.Any]:
        return t.cast(dict[str, JSONValue], self.model_dump(mode="json"))

    @classmethod
    def from_dict(cls, data: Mapping[str, t.Any]) -> t.Self:
        return cls.model_validate(data)