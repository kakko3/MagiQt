from dataclasses import dataclass

from unit_system.abstract import UnitBase


@dataclass(frozen=True)
class Unit(UnitBase[float]):
    convert_to_base_multiplier: float = 1
    convert_to_base_add: float = 0

    def to_base(self, value: float) -> float:
        return self.convert_to_base_multiplier * value + self.convert_to_base_add

    def from_base(self, value: float) -> float:
        return (value - self.convert_to_base_add) / self.convert_to_base_multiplier
