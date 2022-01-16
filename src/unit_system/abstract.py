from typing import Any, Generic, TypeVar
from dataclasses import dataclass


_T = TypeVar("_T")


@dataclass(frozen=True)
class UnitBase(Generic[_T]):
    name: str

    def to_base(self, value: _T) -> _T:  # pylint: disable=R0201
        return value

    def from_base(self, value: _T) -> _T:  # pylint: disable=R0201
        return value
