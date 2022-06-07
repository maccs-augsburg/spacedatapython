'''
custom_widgets.py

May 2022 -- Created -- Mark Ortega-Ponce
'''

from PySide6.QtWidgets import (
    QMainWindow, QLabel,
    QLineEdit, QWidget, QCheckBox, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

FONT_SIZE = 12

class LineEdit(QLineEdit):
    '''
    '''

    def __init__(self):
        super().__init__()
        self.setMaxLength(5)
        # https://doc.qt.io/qt-5/qlineedit.html
        # Weird side effect,
        # Turns cursor black, and lets you put cursor in any spot inside the QLineEdit entries
        # It counts empty spaces as part of the limit, so could be annoying deleting blank spaces
        self.setInputMask("99999")
        self.textEdited.connect(self.text_edited)
        self.setAlignment(Qt.AlignCenter)
        #self.setAlignment(Qt.AlignLeft)
        self.entry = "N/A"
        self.setMaximumWidth(95)

    def text_edited(self, s):
        self.entry = s
        print(self.get_entry())

    # Wrapper around getter for QLineEdit, can also decide not to use and refactor with ide
    # Chose this because method name is more memorable
    def get_entry(self):
        return self.text()

    # Same situation here, want to keep the continuity in naming
    def set_entry(self, new_entry):

        self.entry = str(new_entry)
        self.setText(str(new_entry))


class Label(QLabel):
    def __init__(self, label_name):
        super().__init__()

        self.setText(label_name)
        font = self.font()
        font.setPointSize(FONT_SIZE)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft)
        self.setMaximumWidth(85)

class CheckBox(QCheckBox):
    def __init__(self, label_name):
        super().__init__()

        self.setText(label_name)
        font = self.font()
        font.setPointSize(FONT_SIZE)
        self.setFont(font)
        self.setMaximumWidth(30)


class PushButton(QPushButton):
    def __init__(self, label_name):
        super().__init__()

        self.setText(label_name)
        font = self.font()
        self.setFont(font)
        font.setPointSize(FONT_SIZE)
        self.setCheckable(True)
        self.button_is_checked = False
        self.clicked.connect(self.button_toggle)
        self.setChecked(self.button_is_checked)
        self.setMaximumWidth(145)

    def button_toggle(self, checked):
        self.button_is_checked = checked
        # if checked:
        #     self.setText("Stacked (X, Y, Z)")
        # else:
        #     pass
        #     self.setText("Single Plot (X, Y, Z)")
        print(self.button_is_checked)
    
    def is_toggled(self):
        return self.button_is_checked


# class ToggleButton (QCheckBox):
#     def __init__(self, width = 60, bg_color = '#777', circle_color = "#DDD", active_color = "#00Bcff"):
#         super().__init__()

#         self.bg_color = bg_color
#         self.circle_color = circle_color
#         self.active_color = active_color

#         self.stateChanged.connect(self.state_change)

#     def state_change(self, pos: QPoint):
#         print("Status ", self.isChecked())

#     def hitButton(self, pos: QPoint):
#         return self.contentsRect().contains(pos)

#     def paintEvent(self, e):
#         p = QPainter(self)
#         p.setRenderHint(QPainter.AntiAliasing)
#         # Set as no pen
#         p.setPen(Qt.NoPen)

#         rect = QRect(0,0,self.width(), self.height())

#         if not self.is_checked():

#             p.setBrush(QColor(self.bg_color))
#             p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height()/2, self.width() / 2)
#             p.setBrush(QColor(self.circle_color))
#             p.drawEllipse(3, 3, 22, 22)
    
#         else:
#             p.setBrush(QColor(self.bg_color))
#             p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height()/2, self.width() / 2)
#             p.setBrush(QColor(self.active_color))
#             p.drawEllipse(3, 3, 22, 22)
            
#         # Close Q painter pen, else error
#         p.end()


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
