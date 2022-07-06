#Chris Hance July 2022

from PySide6.QtWidgets import (
    QLabel,QLineEdit, 
    QWidget,QPushButton)

from PySide6.QtGui import  (
    QColor, QBrush, 
    QPaintEvent, QPen, 
    QPainter, QIcon, 
    QAction)

from PySide6.QtCore import (
        Qt, QSize, QPoint)

from PySide6 import QtWidgets

from custom_widgets import PushButton

class SwitchButtonWidget(QtWidgets.QWidget):
    """
    Custom button widget to switch between the two graph styles we have
    the two buttons should be right next to each other touching, and when one is checked the other is unchecked
    """
    def __init__(self,text, *args,**kwargs):
        super(SwitchButtonWidget,self).__init__(*args,**kwargs)

        # Using our already created pushbutton widget to create our buttons here
        # We can still customize it as needed or scrap it and use our own for this widget
        self.three_axis_style = PushButton("Three Axis Style")
        self.stacked_axis_style = PushButton("Stacked Axis Style")
        
