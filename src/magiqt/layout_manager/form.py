from __future__ import annotations

from dataclasses import dataclass, field
from typing import (
    Optional,
    Dict,
    Any,
    TypeVar,
    Tuple,
    NoReturn,
    Type,
    cast,
)

from PyQt5.QtWidgets import QGridLayout, QWidget

from magiqt.interface import (
    DeclaredContainer,
    DeclarationItem,
    Declaration,
    IsEditable,
)
from magiqt.widgets.group_box import GroupBox


_Form = TypeVar("_Form", bound="Form")


@dataclass
class Form(DeclaredContainer):
    title: str
    node: DeclarationItem = field(init=False, repr=False)

    @classmethod
    def new_tree(cls: Type[_Form], title: str) -> _Form:
        instance = cls(title)
        instance.node = DeclarationItem(instance)
        instance.create_widgets(instance.node)
        return instance

    def create_widgets(self, this_node: DeclarationItem) -> Tuple[GroupBox]:
        parent_widget: Optional[QWidget]
        parent_widget = this_node.parent.widgets[0] if this_node.parent else None
        widget = GroupBox(self.title, parent_widget)
        QGridLayout(widget)  # To bing this to widget
        this_node.widgets = (widget,)
        self._build_children(this_node)
        return (widget,)

    def widget(self) -> GroupBox:
        return self.node.widgets[0]  # type: ignore

    def _build_children(self, this_node: DeclarationItem) -> None:
        fields = (f for f in type(self).__dict__.values() if isinstance(f, Declaration))
        layout = cast(QGridLayout, this_node.widgets[0].layout())
        for line, user_field in enumerate(fields):
            item = DeclarationItem(user_field)
            this_node.add_child(user_field.attribute_name, item)
            item.widgets = user_field.create_widgets(item)
            column = 0
            for widget in item.widgets:
                layout.addWidget(widget, line, column, 1, widget.span())
                column += 1

    def on_change(self, attr: str, parent: DeclaredContainer) -> bool:
        """Hook after validation. Return True to propagate"""
        return True

    def on_change_pre_validate(self, attr: str, parent: DeclaredContainer) -> bool:
        """Hook before validation. Return True to propagate"""
        return True

    def is_valid(self, parent: Optional[DeclaredContainer]) -> bool:
        return True

    def associated_widgets(self, instance: DeclaredContainer) -> Tuple[GroupBox]:
        node = instance.node
        return node.children[self.attribute_name].widgets  # type: ignore

    def show(self) -> None:
        self.node.widgets[0].show()

    def _as_dict(self, declaration_item: DeclarationItem) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for key, declaration in declaration_item.children.items():
            label_or_group, *edit_and_unit = declaration.widgets
            if isinstance(label_or_group, GroupBox):
                result[key] = self._as_dict(declaration)
                continue
            edit, *unit = edit_and_unit
            if isinstance(edit, IsEditable):
                result[key] = edit.converted()
            if unit:
                continue
        return result

    def as_dict(self) -> Dict[str, Any]:
        return self._as_dict(self.node)

    def __get__(self: _Form, instance: Optional[DeclaredContainer], owner: Type[DeclaredContainer]) -> _Form:
        if instance is None:
            return self
        new = type(self)(self.title)
        new.node = instance.node.children[self.attribute_name]
        return new

    def __set__(self, instance: Any, value: Any) -> NoReturn:
        raise ValueError("Cannot set form. Use set_from_dict instead")