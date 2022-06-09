from PySide6.QtWidgets import (QMainWindow, QApplication, 
                                QLabel, QLineEdit, 
                                QWidget, QHBoxLayout, 
                                QGridLayout,QPushButton, 
                                QToolBar,QVBoxLayout,
                                QFileDialog, QRadioButton,
                                QCheckBox,QMessageBox, QButtonGroup, QTimeEdit, 
                                )
from PySide6.QtGui import QIcon, QAction, QPixmap, Qt
from PySide6.QtCore import  QSize, QTime, QRect
from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore
# path for file open 
from pathlib import Path

#imports from python 
import sys
import datetime



class MinMaxTime(QtWidgets.QWidget):
    
    def __init__(self, *args,**kwargs):

        super(MinMaxTime,self).__init__(*args,**kwargs)

        main_layout = QtWidgets.QHBoxLayout()
        button_layout = QtWidgets.QVBoxLayout()

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum,
            QtWidgets.QSizePolicy.Maximum
        )

        self.time_widget = QTimeEdit()
        self.time_widget.setTimeRange(QTime(00,00,00), QTime(24,00,00))
        self.time_widget.setDisplayFormat('hh:mm:ss')
        
        self.time_widget.setFixedWidth(75)

        self.label_one = QPushButton("Min?")
        self.label_two = QPushButton("Max?")

        self.label_two.clicked.connect(self.set_max_time)
        self.label_one.clicked.connect(self.set_min_time)

        main_layout.addWidget(self.time_widget)
        button_layout.addWidget(self.label_one)
        button_layout.addWidget(self.label_two)
        main_layout.addLayout(button_layout)


        self.setLayout(main_layout)        


    #set Qtime() to max 23 59 59 
    def set_max_time(self):
        self.time_widget.setTime(QTime(23,59,59))

    #sets QTime() to min 00 00 00
    def set_min_time(self):
        self.time_widget.setTime(QTime(00,00,00))


    # # MAX SIZE OF WIDget
    # def sizeHint(self):
    #     return QtCore.QSize(20,20)
    
    # # background paint of widget
    # def paintEvent(self, e):
    #     painter = QtGui.QPainter(self)
    #     brush = QtGui.QBrush()
    #     brush.setColor(QtGui.QColor('blue'))
    #     brush.setStyle(Qt.SolidPattern)
    #     rect = QRect(0,0, painter.device().width(), painter.device().height())
    #     painter.fillRect(rect,brush)

def main():
    app = QApplication(sys.argv)
    window = MinMaxTime()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
