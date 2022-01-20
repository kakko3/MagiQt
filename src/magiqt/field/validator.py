import locale
from typing import Optional

from magiqt.field.range import ItemRange
from magiqt.interface import Validator, _Converted, _Value

SYSTEM_SEPARATOR = str(locale.localeconv()["decimal_point"])
INVALID_SEPARATOR = "," if SYSTEM_SEPARATOR == "." else "."


class AnyValidator(Validator[str, str]):
    def mapped_to_range(self, value: str) -> str:
        return value

    def validated(self, value: str) -> Optional[str]:
        return value


class FloatValidator(Validator[float, float]):
    def validated(self, value: str) -> Optional[float]:
        if INVALID_SEPARATOR in value:
            return None
        value = value.replace(SYSTEM_SEPARATOR, ".")
        try:
            converted = float(value)
        except ValueError:
            return None
        return converted

    def mapped_to_range(self, value: float) -> float:
        return value


class IntValidator(Validator[int, int]):
    def validated(self, value: str) -> Optional[int]:
        if SYSTEM_SEPARATOR in value or INVALID_SEPARATOR in value:
            return None
        try:
            converted = int(value)
        except ValueError:
            return None
        return converted

    def mapped_to_range(self, value: int) -> int:
        return value


class ItemRangeValidator(Validator[str, _Converted]):
    range: ItemRange[_Converted]

    def validated(self, value: str) -> Optional[_Value]:
        if value in self.range:
            return value  # type: ignore
        return None

    def mapped_to_range(self, value: str) -> _Converted:
        return self.range.to_range_item(value)
