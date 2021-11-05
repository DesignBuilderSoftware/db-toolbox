from enum import Enum
from typing import Callable, Type

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)


class IconSize:
    SMALL = QSize(16, 16)
    MEDIUM = QSize(24, 24)
    LARGE = QSize(48, 48)


class ToolWidget(QWidget):
    """
    Generic widget to be used for all tools.

    It includes description and 'content_layout', tool specific widgets
    can be placed in 'content_layout'.

    Parameters
    ----------
    parent : QWidget
        A parent of this widget.
    layout_cls : Type of QLayout
        Class to be used as main layout ('QHBoxLayout', 'QVBoxLayout', ...)

    Attributes
    ----------------
    description : str
        Brief text to describe tool functionality.

    """

    description = ""

    def __init__(self, parent: QWidget, layout_cls: Type[QLayout] = QHBoxLayout):
        super().__init__(parent)
        self.description_label = QLabel(self.description, self)
        self.content_layout = layout_cls()
        layout = QVBoxLayout(self)
        layout.addWidget(self.description_label, stretch=0)
        layout.addLayout(self.content_layout, stretch=1)


class ErrorLevel(Enum):
    """Define error severity."""

    INFORMATION = 0
    WARNING = 1
    ERROR = 2


class ErrorHandler:
    """
    Context class to handle error reporting.

    Warning dialogs pops up when operation protected by
    'with' statement fails.

    Parameters
    ----------
    parent_widget : QWidget
        Parent widget of information message box.
    level : ErrorLevel
        Severity to set message box icon.

    """

    def __init__(self, parent_widget: QWidget, level: ErrorLevel = ErrorLevel.WARNING):
        self.level = level
        self.parent_widget = parent_widget

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        switch = {
            ErrorLevel.INFORMATION: QMessageBox.information,
            ErrorLevel.WARNING: QMessageBox.warning,
            ErrorLevel.ERROR: QMessageBox.critical,
        }
        if exc_type:
            name = exc_type.__name__
            text = str(exc_val)
            dialog = switch[self.level]
            dialog(self.parent_widget, name, text)
        return True


def cursor_waiting(func: Callable):
    """Show waiting cursor while function executes."""

    def wrapper(*args, **kwargs):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        res = func(*args, **kwargs)
        QApplication.restoreOverrideCursor()
        return res

    return wrapper
