from PySide6.QtWidgets import (
    QMainWindow, QLabel, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

class LineEdit(QLineEdit):

    def __init__(self):
        super().__init__()
        #########################################################################
        #Anything in here is an instance variable as long as it has self keyword#
        #########################################################################
        self.setMaxLength(7)
        # https://doc.qt.io/qt-5/qlineedit.html
        self.setInputMask("9999999")
        self.textEdited.connect(self.text_edited)
        self.entry = "N/A"
        self.setMaximumWidth(80)

    #######################################################################
    #Methods containing self, are instance methods#########################
    #######################################################################
    def text_edited(self, s):
        # s is a string, confirmed wity print(type(s))
        self.entry = s
        # Don't have to pass self again, implied, but weird
        print(self.get_entry())

    def get_entry(self):
        return self.text()

    def set_entry(self, new_entry):
        
        self.entry = new_entry
        self.setText(str(new_entry))

class Label(QLabel):
    def __init__(self, label_name):
        super().__init__()

        self.setText(label_name)
        font = self.font()
        font.setPointSize(12)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft)
        self.setMaximumWidth(80)

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
    