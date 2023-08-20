from dataclasses import dataclass
from typing import List
from ezpyqt.constants import MessageBoxConstants as mbc

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QMessageBox,
    QTableWidget,
    QGroupBox,
    QTableWidgetItem,
    QComboBox,
    QFormLayout,
    QLineEdit,
    QCheckBox,
    QRadioButton,
    QTextEdit
)
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QColor, QFont


@dataclass
class Button(QPushButton):
    def __init__(
            self,
            title: str,
            height: int = None,
            width: int = None,
            object_name: str = None,
            clicked_slot: object = None,
            _style: str = None,
            _margin_top: int = None,
            _margin_bottom: int = None,
            _margin_right: int = None,
            _margin_left: int = None,
            _alignment: str = None,
    ):
        super().__init__()
        self.title = title
        self.height = height
        self.width = width
        self.object_name = object_name
        self.clicked_slot = clicked_slot
        self._style = _style
        self._margin_top = _margin_top
        self._margin_bottom = _margin_bottom
        self._margin_right = _margin_right
        self._margin_left = _margin_left
        self._alignment = _alignment

        self.setText(self.title)

        if self.clicked_slot is not None:
            self.clicked.connect(self.clicked_slot)

        if self.height is not None:
            self.setFixedHeight(self.height)

        if self.width is not None:
            self.setFixedWidth(self.width)

        if self._style is not None:
            self.setStyleSheet(self._style)

        if self._margin_top is not None:
            self.setContentsMargins(0, self._margin_top, 0, 0)

        if self._margin_bottom is not None:
            self.setContentsMargins(0, 0, 0, self._margin_bottom)

        if self._margin_right is not None:
            self.setContentsMargins(0, 0, self._margin_right, 0)

        if self._margin_left is not None:
            self.setContentsMargins(self._margin_left, 0, 0, 0)

        if self._alignment is not None:
            self.setAlignment(_alignment)

        if self.object_name is not None:
            self.setObjectName(self.object_name)

    def __repr__(self):
        return (f"Buttons(title={self.title}, height={self.height}, "
                f"width={self.width}, _slot={self._slot}, _style={self._style})")


class LineEdit(QLineEdit):
    def __init__(self, place_holder: str = None, tool_tip: str = None):
        super().__init__()
        self.place_holder = place_holder
        self.tool_tip = tool_tip

        if self.place_holder is not None:
            self.setPlaceholderText(self.place_holder)

        if self.tool_tip is not None:
            self.setToolTip(self.tool_tip)


class ComboBox(QComboBox):
    def __init__(
            self,
            items: List = None,
            height: int = None,
            width: int = None,
    ):
        super().__init__()
        self.items = items
        self.height = height
        self.width = width

        if self.items is not None:
            for item in self.items:
                self.addItem(str(item))

        if self.width is not None:
            self.setFixedWidth(self.width)

        if self.height is not None:
            self.setFixedHeight(self.height)


class RadioButton(QRadioButton):
    def __init__(self, title: str, set_disabled: bool = False, _slot: object = None):
        super().__init__()
        self.title = title
        self.set_disabled = set_disabled
        self._slot = _slot

        self.setText(title)

        if set_disabled:
            self.setDisabled(set_disabled)

        if self._slot is not None:
            self.toggled.connect(self._slot)


class MessageBox(QMessageBox):
    def __init__(self, err_type: str, message: str):
        super().__init__()
        self.err_type = err_type
        self.message = message

        if self.err_type == mbc.info:
            QMessageBox.information(
                self,
                "Merged!",
                self.message,
                QMessageBox.Ok,
            )

        elif self.err_type == mbc.error:
            QMessageBox.critical(
                self,
                "Error!",
                self.message,
                QMessageBox.Ok,
            )

        elif self.err_type == mbc.warning:
            QMessageBox.warning(
                self,
                "Warning!",
                self.message,
                QMessageBox.Ok,
            )

        else:
            raise Exception("Invalid choice of err_type arg!")
