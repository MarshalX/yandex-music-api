import dataclasses
from typing import Type, TypeVar

from typing_extensions import dataclass_transform

_T = TypeVar('_T')


@dataclass_transform(
    field_specifiers=(dataclasses.Field, dataclasses.field),
)
def model(cls: Type[_T]) -> Type[_T]:
    return dataclasses.dataclass(eq=False, repr=False)(cls)
