import abc
import typing as t

import pydantic
from pydantic_core import core_schema


JSONValue: t.TypeAlias = (
    str
    | int
    | float
    | bool
    | None
    | t.Dict[str, t.Any]
    | t.List[t.Any]
)


class SerdeCapable(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def _validate(cls, value: t.Any) -> "SerdeCapable":
        ...

    @classmethod
    @abc.abstractmethod
    def _serialize(cls, value: t.Any) -> t.Any:
        ...

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: t.Any, handler: pydantic.GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls._validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize
            )
        )

