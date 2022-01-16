from __future__ import annotations
from contextlib import contextmanager
from typing import Optional, Iterator, Generic, Dict, Tuple, TYPE_CHECKING

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QValidator, QPalette, QColor
from PyQt5.QtWidgets import QCompleter, QLineEdit

from magiqt.interface import Range, _Value, _Converted, ValidatorResult, Validator

if TYPE_CHECKING:
    from magiqt.widgets.input.line_edit import LineEdit


class QtCompleterWrapper(QCompleter):
    def __init__(self, parent: QLineEdit, range_: Range[_Value, _Converted]):
        self.range = range_
        self.connected_to = parent
        super().__init__(range_.gui_items(), parent)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)

    def complete(self, rect: Optional[QRect] = None) -> None:
        if not self.range.is_mapping():
            return None
        with self._handle_empty_textbox():
            if rect is None:
                super().complete()
            else:
                super().complete(rect)
        return None

    @contextmanager
    def _handle_empty_textbox(self) -> Iterator[None]:
        if self.connected_to.text() != "":
            yield None
            return
        self.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        try:
            yield None
        finally:
            self.setCompletionMode(QCompleter.PopupCompletion)
        return


class QtValidatorWrapper(QValidator, Generic[_Value, _Converted]):
    _state_mapping: Dict[ValidatorResult.State, QValidator.State] = {
        ValidatorResult.State.VALID: QValidator.Acceptable,
        ValidatorResult.State.INTERMEDIATE: QValidator.Intermediate,
        ValidatorResult.State.INVALID: QValidator.Invalid,
    }

    def __init__(
        self,
        parent: LineEdit[_Value, _Converted],
        validator: Validator[_Value, _Converted],
    ):
        super().__init__(parent)
        self.wrapped = validator
        self.connected_to = parent

    def validate(self, value: str, position: int) -> Tuple["QValidator.State", str, int]:
        validated = self.wrapped.validate(value)
        palette = self.connected_to.palette()
        if validated.state is ValidatorResult.State.VALID:
            palette.setColor(QPalette.Text, QColor("black"))
        else:
            palette.setColor(QPalette.Text, QColor("red"))
        self.connected_to.setPalette(palette)
        state, value = self.parse_result(validated)
        return state, value, position

    def parse_result(self, result: ValidatorResult[_Value]) -> Tuple["QValidator.State", str]:
        return self._state_mapping[result.state], str(result.corrected)
