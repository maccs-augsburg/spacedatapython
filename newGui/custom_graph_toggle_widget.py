#Chris Hance July 2022

#imports from python 
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

        self.three_axis_style.clicked.connect(self.button_toggle)
        self.stacked_axis_style.clicked.connect(self.button_toggle)

    #make same button toggle function for these buttons 
    #and if one button is toggled we want to untoggle the other button
    def button_toggle(self, checked):
        self.button_is_checked = checked
        if self.three_axis_style.isChecked():
            self.three_axis_style.setPalette(QColor('black'))
            self.stacked_axis_style.setPalette(QColor("grey"))
        else:
            self.three_axis_style.setPalette(QPalette.Inactive)


def main():
    app = QApplication(sys.argv)
    window = SwitchButtonWidget()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
