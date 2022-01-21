from __future__ import annotations
from typing import Generic, Optional, TYPE_CHECKING

from magiqt.interface import IsEditable, _Converted, _Value, Range
from magiqt.widgets.input.wrappers import QtValidatorWrapper


if TYPE_CHECKING:
    from magiqt.field.fields import FieldBase


class InputWidget(IsEditable[_Converted], Generic[_Value, _Converted]):
    def widget(self) -> InputWidget[_Value, _Converted]:
        return self

    def set_field(self, field: FieldBase[_Value, _Converted]) -> None:
        self.set_validator(field)
        self.set_range(field.range)
        self.set_readonly(field.read_only)

    def set_validator(self, field: FieldBase[_Value, _Converted]) -> None:
        raise NotImplementedError

    def set_range(self, range_: Range[_Value, _Converted]) -> None:
        raise NotImplementedError

    def set_readonly(self, state: bool) -> None:
        raise NotImplementedError

    def text(self) -> str:
        raise NotImplementedError

    def validator(self) -> QtValidatorWrapper[_Value, _Converted]:
        raise NotImplementedError

    def converted(self) -> Optional[_Converted]:
        raise NotImplementedError

    def span(self) -> int:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{type(self).__name__}(text={self.text()!r})"
