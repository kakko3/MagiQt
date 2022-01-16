from __future__ import annotations

from typing import (
    Optional,
    TYPE_CHECKING,
    Generic,
)

from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QWidget, QCompleter

from magiqt.interface import (
    Validator,
    _Value,
    _Converted,
    Range,
    IsEditable,
)
from magiqt.widgets.input.wrappers import QtCompleterWrapper, QtValidatorWrapper

if TYPE_CHECKING:
    from magiqt.field.fields import FieldBase


class LineEdit(QLineEdit, IsEditable[_Converted], Generic[_Value, _Converted]):  # pylint: disable=W0223
    def __init__(self, field: FieldBase[_Value, _Converted], parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.set_field(field)

    def widget(self) -> LineEdit[_Value, _Converted]:
        return self

    def set_field(self, field: FieldBase[_Value, _Converted]) -> None:
        self.set_validator(field)
        self.set_completer(field.range)
        self.set_readonly(field.read_only)

    def set_validator(self, field: FieldBase[_Value, _Converted]) -> None:
        validator = field.validator(field.range)
        self.setValidator(QtValidatorWrapper(self, validator))

    def set_completer(self, range_: Range[_Value, _Converted]) -> None:
        self.setCompleter(QtCompleterWrapper(self, range_))

    def set_readonly(self, state: bool) -> None:
        self.setReadOnly(state)

    def keyPressEvent(self, key_event: QKeyEvent) -> None:  # pylint: disable=C0103
        super().keyPressEvent(key_event)
        if key_event.key() == Qt.Key_Down:
            if self.text() == "":
                self.completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
            self.completer().complete()
            self.completer().setCompletionMode(QCompleter.PopupCompletion)

    def validator(self) -> QtValidatorWrapper[_Value, _Converted]:
        return super().validator()  # type: ignore

    def converted(self) -> Optional[_Converted]:
        validator: Validator[_Value, _Converted] = self.validator().wrapped
        return validator.converted(self.text())

    def span(self) -> int:
        return 1

    def __repr__(self) -> str:
        return f"{type(self).__name__}(text={self.text()!r})"
