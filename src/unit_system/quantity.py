from dataclasses import dataclass
from typing import Union, Sequence, Generic

from unit_system.unit import Unit
from unit_system.abstract import UnitBase, _T


@dataclass(init=False)
class QuantityType(Generic[_T]):
    name: str
    units: Sequence[UnitBase[_T]]

    def __init__(self, name: str, *units: UnitBase[_T]):
        self.name = name
        self.units = tuple(units)

    def __hash__(self) -> int:
        return id(self.name) | id(self.units)

    def convert(
        self,
        value: _T,
        from_unit: Union[str, UnitBase[_T]],
        to_unit: Union[str, UnitBase[_T]],
    ) -> _T:
        start_unit = self[from_unit]
        end_unit = self[to_unit]
        base = start_unit.to_base(value)
        return end_unit.from_base(base)

    def __getitem__(self, index: Union[str, UnitBase[_T]]) -> UnitBase[_T]:
        try:
            if isinstance(index, str):
                return next(u for u in self.units if u.name == index)
            self.units.index(index)
            return index
        except (IndexError, StopIteration):
            raise ValueError(f"{index} is not a valid unit") from None

    def __contains__(self, item: Union[str, UnitBase[_T]]) -> bool:
        try:
            _ = self.__getitem__(item)
            return True
        except ValueError:
            return False

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, *units={self.units})"


Unitless = QuantityType(
    "Unitless",
    Unit("-"),
)
Fraction = QuantityType("Fraction", Unit("-"), Unit("%", 0.01), Unit("ppm", 1e-6), Unit("ppt", 1e-9))
Pressure = QuantityType("Pressure", Unit("Pa"), Unit("bar(a)", 100000), Unit("bar(g)", 100000, 100000))
Temperature = QuantityType(
    "Temperature",
    Unit("K"),
    Unit("\u2103", 1, 273.15),
)
Area = QuantityType(
    "Area",
    Unit("m\u00B2"),
    Unit("mm\u00B2", 1000 ** -2),
    Unit("cm\u00B2", 100 ** -2),
)
Force = QuantityType("Force", Unit("N"), Unit("kN", 1000))


if __name__ == "__main__":
    print(Unitless.units)
