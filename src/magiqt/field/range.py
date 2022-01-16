from dataclasses import dataclass
from typing import Sequence, Dict

from magiqt.interface import Range, _Converted


class AnyRange(Range[str, str]):
    def is_mapping(self) -> bool:
        return False

    def gui_items(self) -> Sequence[str]:
        return ("",)

    def to_range_item(self, item: str) -> str:
        return item

    def __contains__(self, item: str) -> bool:
        return True


@dataclass
class FloatRange(Range[float, float]):
    low: float = float("-inf")
    high: float = float("inf")
    low_inclusive: bool = True
    high_inclusive: bool = True

    def is_mapping(self) -> bool:
        return False

    def gui_items(self) -> Sequence[str]:
        return ("",)

    def to_range_item(self, item: float) -> float:
        return item

    def __contains__(self, item: float) -> bool:
        if self.low < item < self.high:
            return True
        if self.low_inclusive and item == self.low:
            return True
        if self.high_inclusive and item == self.high_inclusive:
            return True
        return False


@dataclass
class IntRange(Range[int, int]):
    low: float = float("-inf")
    high: float = float("inf")
    low_inclusive: bool = True
    high_inclusive: bool = True

    def is_mapping(self) -> bool:
        return False

    def gui_items(self) -> Sequence[str]:
        return ("",)

    def to_range_item(self, item: int) -> int:
        return item

    def __contains__(self, item: int) -> bool:
        if self.low < item < self.high:
            return True
        if self.low_inclusive and item == self.low:
            return True
        if self.high_inclusive and item == self.high_inclusive:
            return True
        return False


@dataclass
class ListRange(Range[str, str]):
    _items: Sequence[str]

    def __contains__(self, item: str) -> bool:
        return item in self._items

    def to_range_item(self, item: str) -> str:
        return item

    def is_mapping(self) -> bool:
        return True

    def gui_items(self) -> Sequence[str]:
        return self._items


@dataclass
class MappedRange(Range[str, _Converted]):
    _items: Dict[str, _Converted]

    def __contains__(self, item: str) -> bool:
        return item in self._items

    def to_range_item(self, item: str) -> _Converted:
        return self._items[item]

    def is_mapping(self) -> bool:
        return True

    def gui_items(self) -> Sequence[str]:
        return list(self._items.keys())
