from __future__ import annotations
from typing import Optional, Generic, TYPE_CHECKING, Union

from PyQt5.QtCore import QModelIndex, QAbstractListModel, Qt
from PyQt5.QtWidgets import QComboBox, QWidget

from magiqt.interface import _Converted, _Value, Validator
from magiqt.widgets.input.abstract import InputWidget
from magiqt.field.range import ItemRange
from magiqt.widgets.input.wrappers import QtValidatorWrapper

if TYPE_CHECKING:
    from magiqt.field.fields import FieldBase


class QtModelWrapper(QAbstractListModel, Generic[_Converted]):
    def __init__(self, range_: ItemRange[_Converted], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._range = range_

    def data(self, index: QModelIndex, role: int = -1) -> Union[str, _Converted, None]:
        return self._range.display_role(index.row()) if role == Qt.DisplayRole else None

    def rowCount(self, parent: Optional[QModelIndex] = None) -> int:  # pylint: disable=W0613, C0103
        return len(self._range)


class ComboBox(QComboBox, InputWidget[_Value, _Converted]):
    _validator: Validator[_Value, _Converted]

    def __init__(self, field: FieldBase[_Value, _Converted], parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.set_field(field)

    def set_validator(self, field: FieldBase[_Value, _Converted]) -> None:
        self._validator = field.validator(field.range)

    def set_range(self, range_: ItemRange[_Converted]) -> None:  # type: ignore
        self.setModel(QtModelWrapper(range_))

    def set_readonly(self, state: bool) -> None:
        self.setEnabled(not state)

    def validator(self) -> QtValidatorWrapper[_Value, _Converted]:
        return QtValidatorWrapper(self, self._validator)

    def text(self) -> str:
        return self.currentText()

    def widget(self) -> ComboBox[_Value, _Converted]:
        return self

    def span(self) -> int:
        return 1

    def model(self) -> QtModelWrapper[_Converted]:
        return self.model()

    def converted(self) -> Optional[_Converted]:
        validator: Validator[_Value, _Converted] = self.validator().wrapped
        return validator.converted(self.text())

    def __repr__(self) -> str:
        return f"{type(self).__name__}(text={self.text()!r})"
