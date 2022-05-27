from PySide6.QtWidgets import (
    QMainWindow, QLabel,
    QLineEdit, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class LineEdit(QLineEdit):

    def __init__(self):
        super().__init__()
        #########################################################################
        #Anything in here is an instance variable as long as it has self keyword#
        #########################################################################
        self.setMaxLength(5)
        # https://doc.qt.io/qt-5/qlineedit.html

        # Weird side effect,
        # Turns cursor black, and lets you put cursor in any spot inside the QLineEdit entries
        # It counts empty spaces as part of the limit, so could be annoying deleting blank spaces
        self.setInputMask("99999")
        # self.setFocus()
        self.textEdited.connect(self.text_edited)
        self.setAlignment(Qt.AlignCenter)
        self.entry = "N/A"
        self.setMaximumWidth(80)

    #######################################################################
    #Methods containing self, are instance methods#########################
    #######################################################################
    def text_edited(self, s):
        self.entry = s
        print(self.get_entry())

    # Wrapper around getter for QLineEdit, can also decide not to use and refactor with ide
    # Chose this because method name is more memorable
    def get_entry(self):
        return self.text()

    # Same situation here, want to keep the continuity in naming
    def set_entry(self, new_entry):

        self.entry = new_entry
        self.setText(str(new_entry))


class Label(QLabel):
    def __init__(self, label_name):
        super().__init__()

        self.setText(label_name)
        font = self.font()
        font.setPointSize(13)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft)
        self.setMaximumWidth(80)


class PlotCanvas(FigureCanvasQTAgg):

    def __init__(self, parent = None, width = 5, height = 4, dpi = 100):
        fig = Figure(figsize = (width, height), dpi = dpi)
        self.axes = fig.add_subplot(111)
        super(PlotCanvas, self).__init__(fig)


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

