#Chris Hance July 2022
# custom superator line 
"""
Custom line to seperate differnet parts of the layout 
for our gui to make groups of widgets easier to read and understand what goes with what 

"""

from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtCore import QLine, QRect
from PySide6.QtCore import Qt
import sys
class LineSeperator(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawLine(0,0,25,0)
        # brush = QBrush()
        # brush.setColor(QColor('black'))
        # brush.setStyle(Qt.SolidPattern)
        # rect = QtCore.QRect(0, 0, 100, 10)
        # painter.fillRect(rect, brush)
        #painter.end()
        