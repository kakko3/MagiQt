from __future__ import annotations

import sys
import traceback
from types import TracebackType
from typing import Optional, List, Type

from PyQt5.QtWidgets import QApplication


class Application(QApplication):
    def __init__(self, argv: Optional[List[str]] = None, use_sys_argv: bool = True):
        argv = argv if argv is not None else []
        if use_sys_argv:
            argv = sys.argv + argv
        super().__init__(argv)


def excepthook(exc_type: Type[BaseException], exc_value: BaseException, exc_tb: Optional[TracebackType]) -> None:
    trace = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(trace)


sys.excepthook = excepthook
