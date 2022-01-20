from dataclasses import dataclass
from typing import Sequence, Dict, Generic, Union

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


class ItemRange(Range[str, _Converted], Generic[_Converted]):
    def __contains__(self, item: str) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def to_range_item(self, item: str) -> _Converted:
        raise NotImplementedError

    def is_mapping(self) -> bool:
        raise NotImplementedError

    def gui_items(self) -> Sequence[str]:
        raise NotImplementedError

    def display_role(self, index: int) -> str:
        raise NotImplementedError

    def item(self, index: int) -> _Converted:
        raise NotImplementedError


@dataclass
class ListRange(ItemRange[str]):
    _items: Sequence[str]

    def __contains__(self, item: str) -> bool:
        return item in self._items

    def __len__(self) -> int:
        return len(self._items)

    def to_range_item(self, item: str) -> str:
        return item

    def is_mapping(self) -> bool:
        return True

    def gui_items(self) -> Sequence[str]:
        return self._items

    def display_role(self, index: int) -> str:
        return self._items[index]

    def item(self, index: int) -> str:
        return self.display_role(index)


@dataclass
class MappedRange(ItemRange[_Converted]):
    _items: Dict[str, _Converted]

    def __contains__(self, item: str) -> bool:
        return item in self._items

    def __len__(self) -> int:
        return len(self._items)

    def to_range_item(self, item: str) -> _Converted:
        return self._items[item]

    def is_mapping(self) -> bool:
        return True

    def gui_items(self) -> Sequence[str]:
        return list(self._items.keys())

    def _get_key(self, index: int) -> str:
        listed = list(self._items.keys())
        return listed[index]

    def display_role(self, index: int) -> str:
        return self._get_key(index)

    def item(self, index: int) -> str:
        return self._items[self._get_key(index)]
