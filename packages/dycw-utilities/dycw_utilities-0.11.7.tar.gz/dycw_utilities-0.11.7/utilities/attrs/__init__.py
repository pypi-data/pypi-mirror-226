from typing import Any, cast

from attrs import Factory, define, field, fields
from beartype import beartype
from beartype.door import die_if_unbearable
from beartype.roar import BeartypeDoorHintViolation

from utilities.class_name import get_class_name
from utilities.random import SYSTEM_RANDOM


@define
class AttrsBase:
    """Base class for `attrs` class which applies `beartype` checking."""

    @beartype
    def __attrs_post_init__(self) -> None:
        all_fields = fields(cast(Any, type(self)))
        try:
            field = SYSTEM_RANDOM.choice(all_fields)
        except IndexError:
            pass
        else:
            fname = field.name
            try:
                die_if_unbearable(getattr(self, fname), field.type)
            except BeartypeDoorHintViolation:
                msg = (
                    f"module = {self.__module__}, "
                    f"class = {get_class_name(self)}, field = {fname}"
                )
                raise FieldTypeError(msg) from None


class FieldTypeError(TypeError):
    """Raised when an `attrs` field has the wrong type."""


@beartype
def make_dict_field() -> Any:
    """Create a `__dict__` field."""
    return field(default=Factory(cast(Any, dict)), init=False, repr=False, eq=False)


class DictMixin:
    """Mix-in to support cached properties."""

    __dict__: dict[str, Any] = make_dict_field()
