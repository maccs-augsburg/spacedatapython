from ast import Pass
import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QLabel,
    QToolBar, QStatusBar, QCheckBox,
    QHBoxLayout, QVBoxLayout,
    QLineEdit, QWidget, QFormLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
# Adding this import for layout debugging
from PySide6.QtGui import QPalette, QColor

class MainWindow(QMainWindow):

    def __init__(self):
        # Why does tutorial sometimes pass MainWindow, and other times it doesnt
        super(MainWindow, self).__init__()

        self.setWindowTitle("MACCS Stacked Plots")
        self.setWindowIcon(QIcon("maccslogo_870.jpeg"))
        self.setMinimumHeight(600)
        self.setMinimumWidth(1100)
        self.station_code = ""
        
        main_layout = QHBoxLayout()
        #entry_layout = QVBoxLayout()
        entry_layout = QFormLayout()
        '''
        Add widgets to entry_layout
        '''
        station_label = Label("Station Code: ")
        station_edit = LineEdit()
        year_day_label = Label("Year Day: ")
        year_day_edit = LineEdit()
        start_hour_label = Label("Start Hour: ")
        start_hour_edit = LineEdit()
        start_minute_label = Label("Start Minute: ")
        start_minute_edit = LineEdit()
        start_second_label = Label("Start Second: ")
        start_second_edit = LineEdit()
        end_hour_label = Label("End Hour: ")
        end_hour_edit = LineEdit()
        end_minute_label = Label("End Minute: ")
        end_minute_edit = LineEdit()
        end_second_label = Label("End Second: ")
        end_second_edit = LineEdit()
        min_x_label = Label("Plot Min X: ")
        min_x_edit = LineEdit()
        max_x_label = Label("Plot Max X: ")
        max_x_edit = LineEdit()
        min_y_label = Label("Plot Min Y: ")
        min_y_edit = LineEdit()
        max_y_label = Label("Plot Max Y: ")
        max_y_edit = LineEdit()
        min_z_label = Label("Plot Min Z: ")
        min_z_edit = LineEdit()
        max_z_label = Label("Plot Max Z: ")
        max_z_edit = LineEdit()
        entry_layout.addRow(station_label, station_edit)
        entry_layout.addRow(year_day_label, year_day_edit)
        entry_layout.addRow(start_hour_label, start_hour_edit)
        entry_layout.addRow(start_minute_label, start_minute_edit)
        entry_layout.addRow(start_second_label, start_second_edit)
        entry_layout.addRow(end_hour_label, end_hour_edit)
        entry_layout.addRow(end_minute_label, end_minute_edit)
        entry_layout.addRow(end_second_label, end_second_edit)
        entry_layout.addRow(min_x_label, min_x_edit)
        entry_layout.addRow(max_x_label, max_x_edit)
        entry_layout.addRow(min_y_label, min_y_edit)
        entry_layout.addRow(max_y_label, max_y_edit)
        entry_layout.addRow(min_z_label, min_z_edit)
        entry_layout.addRow(max_z_label, max_z_edit)


        main_layout.addLayout(entry_layout)
        main_layout.addWidget(Color('green'))

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        
# class attributes are before init, they are like static variables?
# instance attributes are after init, they are unique to each one, more of what I want

class LineEdit(QLineEdit):
    ###########################################
    #Anything in here is a static variable#####
    ###########################################
    # this explains the super() keyword and various variations you might see used in tutorials
    #https://stackoverflow.com/questions/1607612/python-how-do-i-make-a-subclass-from-a-superclass
    def __init__(self):
        super().__init__()
        #########################################################################
        #Anything in here is an instance variable as long as it has self keyword#
        #########################################################################
        self.setMaxLength(7)
        self.textEdited.connect(self.text_edited)
        self.entry = "N/A"
    #######################################################################
    #Methods containing self, are instance methods#########################
    #######################################################################
    def text_edited(self, s):
        # s is a string, confirmed wity print(type(s))
        self.entry = s
        # Don't have to pass self again, implied, but weird
        print(self.get_entry())

    def get_entry(self):
        return self.entry

class Label(QLabel):
    def __init__(self, label_name):
        super().__init__()

        self.setText(label_name)
        font = self.font()
        font.setPointSize(12)
        self.setFont(font)

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
    
# class EntryBox(LineEdit, Label):

#     def __init__(self, label_name):
#         super().__init__()

#         self.line_edit = LineEdit()
#         self.label = Label(label_name)

#         self.label.setBuddy(self.line_edit)

def main ():

    # use brackets if not using command line
    # app = QApplication(sys.argv)
    app = QApplication([])

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()