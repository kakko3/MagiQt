from __future__ import annotations
from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Generic,
    TypeVar,
    Sequence,
    Dict,
    Optional,
    Type,
    Union,
    overload,
    Any,
)

from PyQt5.QtWidgets import QWidget, QLayout

_Value = TypeVar("_Value")
_Converted = TypeVar("_Converted")
_Self = TypeVar("_Self")
_ReturnType = TypeVar("_ReturnType")
_Widgets = TypeVar("_Widgets", bound="Sequence[IsPlaceable]")
_Declaration = TypeVar("_Declaration", bound="Declaration[Any]")


class AbstractWithClassRepr(ABCMeta):
    def __repr__(cls) -> str:
        return cls.__name__


@dataclass
class ValidatorResult(Generic[_Converted]):
    class State(Enum):
        VALID = auto()
        INTERMEDIATE = auto()
        INVALID = auto()

    converted: Optional[_Converted]
    corrected: str
    state: State = State.VALID

    def get_valid_value(self) -> _Converted:
        if self.converted is None:
            raise ValueError("Invalid value")
        return self.converted


@dataclass(init=False)  # type: ignore
class Validator(Generic[_Value, _Converted], metaclass=AbstractWithClassRepr):
    range_: Range[_Value, _Converted]

    def __init__(self, range_: Range[_Value, _Converted]) -> None:
        self.range = range_

    @abstractmethod
    def validated(self, value: str) -> Optional[_Value]:
        pass

    @abstractmethod
    def mapped_to_range(self, value: _Value) -> _Converted:
        pass

    def converted(self, value: str) -> Optional[_Converted]:
        validated = self.validated(value)
        if validated is None:
            return None
        return self.mapped_to_range(validated)

    def validate(self, value: str) -> ValidatorResult[_Value]:
        validated = self.validated(value)
        if validated is None:
            return ValidatorResult(None, value, ValidatorResult.State.INTERMEDIATE)
        if validated not in self.range:
            return ValidatorResult(None, value, ValidatorResult.State.INTERMEDIATE)
        return ValidatorResult(validated, value)


@dataclass  # type: ignore
class Range(Generic[_Value, _Converted]):
    @abstractmethod
    def __contains__(self, item: _Value) -> bool:
        return True

    @abstractmethod
    def to_range_item(self, item: _Value) -> _Converted:
        pass

    @abstractmethod
    def is_mapping(self) -> bool:
        pass

    @abstractmethod
    def gui_items(self) -> Sequence[str]:
        pass


class Declaration(ABC, Generic[_ReturnType]):
    attribute_name: str

    @overload
    def __get__(self: _Self, instance: None, owner: Type[DeclaredContainer]) -> _Self:
        ...

    @overload
    def __get__(self: _Self, instance: DeclaredContainer, owner: Type[DeclaredContainer]) -> Optional[_ReturnType]:
        ...

    @abstractmethod
    def __get__(
        self: _Self,
        instance: Optional[DeclaredContainer],
        owner: Type[DeclaredContainer],
    ) -> Union[_Self, Optional[_ReturnType]]:
        pass

    @abstractmethod
    def __set__(self, instance: DeclaredContainer, value: _ReturnType) -> None:
        pass

    def __set_name__(self, owner: Declaration[_ReturnType], name: str) -> None:
        self.attribute_name = name

    @abstractmethod
    def create_widgets(self, this_node: DeclarationItem) -> Sequence[QWidget]:
        pass

    def associated_widgets(self, instance: DeclaredContainer) -> Sequence[QWidget]:
        pass


class DeclaredContainer(Declaration["DeclaredContainer"], ABC):
    node: DeclarationItem

    def _on_change(self, attr: str, this_item: DeclarationItem) -> None:
        if not self.on_change_pre_validate(attr, this_item):
            return None
        if not self.is_valid(this_item):
            return None
        if self.on_change(attr, this_item):
            parent = this_item.parent
            if parent is None:
                return None
            widget = parent.widgets[0]
            widget.changed.emit(attr)
        return None

    def widget(self) -> QWidget:
        raise NotImplementedError

    def on_change(self, attr: str, this_item: DeclarationItem) -> bool:
        """Hook after validation. Return True to propagate"""
        return True

    def on_change_pre_validate(self, attr: str, this_item: DeclarationItem) -> bool:
        """Hook before validation. Return True to propagate"""
        return True

    def is_valid(self, this_item: DeclarationItem) -> bool:
        return True


class IsPlaceable:
    def span(self) -> int:
        raise NotImplementedError()

    def layout(self) -> QLayout:
        raise NotImplementedError()


class IsEditable(Generic[_Converted], IsPlaceable):
    def converted(self) -> Optional[_Converted]:
        raise NotImplementedError


@dataclass
class DeclarationItem:
    declaration: Declaration[Any]
    widgets: Sequence[QWidget] = tuple()
    parent: Optional[DeclarationItem] = None
    children: Dict[str, DeclarationItem] = field(default_factory=dict)

    def add_child(self, attribute: str, item: DeclarationItem) -> None:
        item.parent = self
        self.children[attribute] = item
