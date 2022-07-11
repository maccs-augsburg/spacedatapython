#Chris Hance July 2022

#imports from python 
from hmac import new
import sys

from PySide6.QtWidgets import (
    QLabel,QLineEdit, 
    QWidget,QPushButton,QApplication)

from PySide6.QtGui import  (
    QColor, QBrush, 
    QPaintEvent, QPen, 
    QPainter, QIcon, 
    QAction, QPalette)

from PySide6.QtCore import (
        Qt, QSize, QPoint)

from PySide6 import QtWidgets, QtGui

from custom_widgets import PushButton

class SwitchButtonWidget(QtWidgets.QWidget):
    """
    Custom button widget to switch between the two graph styles we have
    the two buttons should be right next to each other touching, and when one is checked the other is unchecked
    """
    def __init__(self, *args,**kwargs):
        super(SwitchButtonWidget,self).__init__(*args,**kwargs)
        button_layout = QtWidgets.QHBoxLayout()
        # Using our already created pushbutton widget to create our buttons here
        # We can still customize it as needed or scrap it and use our own for this widget
        self.three_axis_style = PushButton("Three Axis Style")
        self.stacked_axis_style = PushButton("Stacked Axis Style")

        button_layout.addWidget(self.three_axis_style)
        button_layout.addWidget(self.stacked_axis_style)

        self.setLayout(button_layout)

        self.three_axis_style.clicked.connect(self.three_axis_checked)
        self.stacked_axis_style.clicked.connect(self.stacked_axis_checked)

    def three_axis_checked(self):
        self.stacked_axis_style.setChecked(False)
        self.three_axis_style.setChecked(True)
        
    def stacked_axis_checked(self):
        self.three_axis_style.setChecked(False)
        self.stacked_axis_style.setChecked(True)

def main():
    app = QApplication(sys.argv)
    window = SwitchButtonWidget()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
