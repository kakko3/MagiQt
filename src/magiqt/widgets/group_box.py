from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Union

from PyQt5.QtWidgets import QGroupBox, QWidget
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal

from magiqt.interface import IsPlaceable


@dataclass
class GroupBox(QGroupBox, IsPlaceable):  # pylint: disable=W0223
    changed: Union[pyqtSignal, pyqtBoundSignal] = pyqtSignal(str)

    def __init__(self, title: str = "", parent: Optional[QWidget] = None) -> None:
        if title:
            super().__init__(title, parent)
        else:
            super().__init__(parent)

    def widget(self) -> GroupBox:
        return self

    def span(self) -> int:
        return 3
