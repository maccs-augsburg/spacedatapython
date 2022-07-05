from PySide6.QtWidgets import (
    QApplication,
    QPushButton, 
    QTimeEdit,
    QSizePolicy
)
from PySide6.QtCore import  QTime
from PySide6 import QtWidgets

#imports from python 
import sys

class MinMaxTime(QtWidgets.QWidget,):
    
    def __init__(self,text, *args,**kwargs,):

        super(MinMaxTime,self).__init__(*args,**kwargs)

        main_layout = QtWidgets.QHBoxLayout()
        button_layout = QtWidgets.QVBoxLayout()

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )
        
        self.time_widget = QTimeEdit()
        self.time_widget.setTimeRange(QTime(00,00,00), QTime(23,59,59))
        self.time_widget.setDisplayFormat('hh:mm:ss')
        self.time_widget.timeChanged.connect(self.time_changed)
        self.time_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.time_widget.setMaximumHeight(25)
        
        self.time_widget.setMaximumWidth(95)

        self.label_one = QPushButton(text)
        self.label_one.setMaximumSize(35,35)

        self.label_one.setContentsMargins(0,0,0,0)
        
        if text == 'Min':
            self.label_one.clicked.connect(self.set_min_time)
        else:
            self.label_one.clicked.connect(self.set_max_time)

        main_layout.addWidget(self.time_widget)
        button_layout.addWidget(self.label_one)
        button_layout.setContentsMargins(0,0,0,0)
        main_layout.addLayout(button_layout)
        main_layout.setContentsMargins(0,0,0,0)

        self.setLayout(main_layout)        
        
        self.hour = 0
        self.minute = 0
        self.second = 0

    #set Qtime() to max 23 59 59 
    def set_max_time(self):
        self.time_widget.setTime(QTime(23,59,59))

    #sets QTime() to min 00 00 00
    def set_min_time(self):
        self.time_widget.setTime(QTime(00,00,00))

    def time_changed(self, time):
        self.time = time
        # inherited function from QDateTimeEdit
        self.hour = self.time.hour()
        self.minute = self.time.minute()
        self.second = self.time.second()
        
    def get_hour(self):
        return self.hour
    def get_minute(self):
        return self.minute
    def get_second(self):
        return self.second

    def set_own_time(self, hour, minute, second):
        self.time_widget.setTime(QTime(hour, minute, second))
        
def main():
    app = QApplication(sys.argv)
    window = MinMaxTime()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
