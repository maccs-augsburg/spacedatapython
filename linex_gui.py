# from ast import Pass
# import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QLabel,
    QToolBar, QStatusBar, QCheckBox,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QLineEdit, QWidget, QFormLayout
)
# from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
# # Adding this import for layout debugging
# from PySide6.QtGui import QPalette, QColor
from linex_gui_helper import LineEdit, Label, Color

class MainWindow(QMainWindow):

    def __init__(self):
        # Why does tutorial sometimes pass MainWindow, and other times it doesnt
        super(MainWindow, self).__init__()

        self.setWindowTitle("MACCS Stacked Plots")
        self.setWindowIcon(QIcon("maccslogo_870.jpeg"))
        self.setMinimumHeight(600)
        self.setMinimumWidth(1200)
        self.station_code = ""
        
        #main_layout = QHBoxLayout()
        main_layout = QGridLayout()
        # only one????
        print(main_layout.columnCount())
        #entry_layout = QVBoxLayout()
        entry_layout = QFormLayout()
        '''
        Add widgets to entries form
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

        dummy_layout = QVBoxLayout()
        dummy_two_layout = QVBoxLayout()

        dummy_layout.addWidget(Color('green'))
        dummy_two_layout.addWidget(Color('red'))

        main_layout.addLayout(entry_layout, 0, 0, 1, 1)
        main_layout.addLayout(dummy_layout, 0, 2, 2, 2)
        main_layout.addLayout(dummy_two_layout, 0, 4, 2, 2)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        
def main ():

    # use brackets if not using command line
    # app = QApplication(sys.argv)
    app = QApplication([])

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
