from PyQt5.QtWidgets import QLabel
from magiqt.interface import IsPlaceable


class Label(QLabel, IsPlaceable):  # pylint: disable=W0223
    def span(self) -> int:
        return 1

    def __repr__(self) -> str:
        return f"{type(self).__name__}(text={self.text()!r})"
