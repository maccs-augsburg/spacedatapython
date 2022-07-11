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

        # self.three_axis_style.setContentsMargins(0,0,0,0)
        # self.stacked_axis_style.setContentsMargins(0,0,0,0)
        # button_layout.setContentsMargins(0,0,0,0)

        self.setLayout(button_layout)

        self.three_axis_style.clicked.connect(self.button_clicked)
        self.stacked_axis_style.clicked.connect(self.button_clicked)

        self.three_axis_style.clicked.connect(self.three_axis_checked)
        self.stacked_axis_style.clicked.connect(self.stacked_axis_checked)

    def three_axis_checked(self):
        print("Three axis clicked uncheck stacked ")
        self.stacked_axis_style.setChecked(False)
        self.three_axis_style.setChecked(True)
        return True
        
    def stacked_axis_checked(self):
        print("Stacked axis clicked uncheck Three axis ")
        self.three_axis_style.setChecked(False)
        self.stacked_axis_style.setChecked(True)
        return False

    #make same button toggle function for these buttons 
    #and if one button is toggled we want to untoggle the other button
    def button_clicked(self, checked):
        color = QColor(Qt.cyan)
        self.button_is_checked = checked
        if self.three_axis_style.isChecked():
            self.stacked_axis_style.setChecked(False)
        elif self.stacked_axis_style.isChecked():
            self.three_axis_style.setChecked(False)

def main():
    app = QApplication(sys.argv)
    window = SwitchButtonWidget()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
