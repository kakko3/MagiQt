from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Type, overload, Tuple, Any, Optional, Union, TypeVar, Callable

from magiqt.field.range import IntRange, AnyRange, FloatRange, ItemRange, ListRange
from magiqt.field.validator import IntValidator, AnyValidator, FloatValidator, ItemRangeValidator
from magiqt.interface import (
    Validator,
    Range,
    DeclaredContainer,
    _Value,
    Declaration,
    _Converted,
    DeclarationItem,
)
from magiqt.widgets.input.abstract import InputWidget
from magiqt.widgets.input.combo_box import ComboBox
from magiqt.widgets.label import Label
from magiqt.widgets.input.line_edit import LineEdit
from magiqt.widgets.group_box import GroupBox


_Field = TypeVar("_Field", bound="FieldBase[Any, Any]")


@dataclass
class FieldBase(Declaration[_Converted], Generic[_Value, _Converted]):
    name: str
    validator: Type[Validator[_Value, _Converted]]
    range: Range[_Value, _Converted]
    read_only: bool = False

    def create_widgets(self, this_node: DeclarationItem) -> Tuple[Label, LineEdit[_Value, _Converted]]:
        if this_node.parent is None:
            raise ValueError(f"Cannot add to a node without parent {this_node}")
        parent: GroupBox = this_node.parent.widgets[0]  # type: ignore
        label = Label(f"{self.name}:", parent)
        line_edit = LineEdit(self, parent)
        line_edit.textEdited.connect(self._changed(parent))
        return label, line_edit

    def _changed(self, parent: GroupBox) -> Callable[[str], None]:
        attr = self.attribute_name

        def _inner(text: str) -> None:
            parent.changed.emit(attr)

        return _inner

    def associated_widgets(self, instance: DeclaredContainer) -> Tuple[Label, LineEdit[_Value, _Converted]]:
        node = instance.node
        return node.children[self.attribute_name].widgets  # type: ignore

    @overload  # type: ignore
    def __get__(
        self: FieldBase[_Value, _Converted], instance: None, owner: Type[DeclaredContainer]
    ) -> FieldBase[_Value, _Converted]:
        ...

    @overload
    def __get__(self: _Field, instance: DeclaredContainer, owner: Type[DeclaredContainer]) -> Optional[_Converted]:
        ...

    def __get__(
        self: _Field,
        instance: Optional[DeclaredContainer],
        owner: Type[DeclaredContainer],
    ) -> Union[FieldBase[_Value, _Converted], Optional[_Converted]]:
        if instance is None:
            return self
        widgets = self.associated_widgets(instance)
        line_edit = widgets[1]
        return line_edit.converted()

    def __set__(self, instance: DeclaredContainer, value: Any) -> None:
        widgets = self.associated_widgets(instance)
        line_edit = widgets[1]
        return line_edit.setText(str(value))


@dataclass
class StringField(FieldBase[str, str]):
    validator: Type[AnyValidator] = AnyValidator
    range: Range[str, str] = AnyRange()


@dataclass
class IntegerField(FieldBase[int, int]):
    validator: Type[IntValidator] = IntValidator
    range: IntRange = IntRange()


@dataclass
class FloatField(FieldBase[float, float]):
    validator: Type[Validator[float, float]] = FloatValidator
    range: FloatRange = FloatRange()


@dataclass
class DropDown(FieldBase[str, _Converted]):
    validator: ItemRangeValidator[_Converted] = ItemRangeValidator  # type: ignore
    range: ItemRange[_Converted] = ListRange(("",))  # type: ignore

    def create_widgets(self, this_node: DeclarationItem) -> Tuple[Label, ComboBox[str, _Converted]]:  # type: ignore
        if this_node.parent is None:
            raise ValueError(f"Cannot add to a node without parent {this_node}")
        parent: GroupBox = this_node.parent.widgets[0]  # type: ignore
        label = Label(f"{self.name}:", parent)
        combo = ComboBox(self, parent)
        combo.currentIndexChanged.connect(self._changed(parent))
        return label, combo
