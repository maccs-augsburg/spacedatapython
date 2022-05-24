# from ast import Pass
import sys
import os
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QLabel,
    QToolBar, QStatusBar, QCheckBox,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QLineEdit, QWidget, QFormLayout, QComboBox, QPushButton, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
# # Adding this import for layout debugging
# from PySide6.QtGui import QPalette, QColor
from linex_gui_helper import LineEdit, Label, Color

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000

class MainWindow(QMainWindow):

    def __init__(self):
        # Why does tutorial sometimes pass MainWindow, and other times it doesnt
        super(MainWindow, self).__init__()

        ######## MAIN WINDOW SETTINGS #################
        self.setWindowTitle("MACCS Stacked Plots")
        # self.setWindowIcon(QIcon("/Users/markortega-ponce/Desktop/ZMACCS/spacedatapython/maccslogo_nobg.png"))
        self.setMinimumHeight(WINDOW_HEIGHT)
        self.setMinimumWidth(WINDOW_WIDTH)
        self.station_code = ""
        station_label = Label("Station Code: ")
        self.station_edit = LineEdit()
        # only allow station edit to take 2 uppercase characters
        self.station_edit.setInputMask(">AA")

        main_layout = QHBoxLayout()
        mac_label = QLabel()
        # TODO: use sys import so it doesnt use my path
        pixmap = QPixmap('/Users/markortega-ponce/Desktop/ZMACCS/spacedatapython/maccslogo_nobg.png')
        mac_label.setPixmap(pixmap)
        mac_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #print(main_layout.columnCount())
        ################################################

        ######## SIDE ENTRIES FOR GUI ##################
        entry_layout = QGridLayout()
        year_day_label = Label("Year Day: ")
        self.year_day_edit = LineEdit()
        start_hour_label = Label("Start Hour: ")
        self.start_hour_edit = LineEdit()
        start_minute_label = Label("Start Minute: ")
        self.start_minute_edit = LineEdit()
        start_second_label = Label("Start Second: ")
        self.start_second_edit = LineEdit()
        end_hour_label = Label("End Hour: ")
        self.end_hour_edit = LineEdit()
        end_minute_label = Label("End Minute: ")
        self.end_minute_edit = LineEdit()
        end_second_label = Label("End Second: ")
        self.end_second_edit = LineEdit()
        min_x_label = Label("Plot Min X: ")
        self.min_x_edit = LineEdit()
        max_x_label = Label("Plot Max X: ")
        self.max_x_edit = LineEdit()
        min_y_label = Label("Plot Min Y: ")
        self.min_y_edit = LineEdit()
        max_y_label = Label("Plot Max Y: ")
        self.max_y_edit = LineEdit()
        min_z_label = Label("Plot Min Z: ")
        self.min_z_edit = LineEdit()
        max_z_label = Label("Plot Max Z: ")
        self.max_z_edit = LineEdit()
        entry_layout.addWidget(station_label, 0, 0)
        entry_layout.addWidget(self.station_edit, 0, 1)
        entry_layout.addWidget(year_day_label, 1, 0)
        entry_layout.addWidget(self.year_day_edit, 1, 1)
        entry_layout.addWidget(start_hour_label, 2, 0)
        entry_layout.addWidget(self.start_hour_edit,2, 1)
        entry_layout.addWidget(start_minute_label, 3, 0)
        entry_layout.addWidget(self.start_minute_edit, 3, 1)
        entry_layout.addWidget(start_second_label, 4, 0)
        entry_layout.addWidget(self.start_second_edit, 4, 1)
        entry_layout.addWidget(end_hour_label, 5, 0)
        entry_layout.addWidget(self.end_hour_edit, 5, 1)
        entry_layout.addWidget(end_minute_label, 6, 0)
        entry_layout.addWidget(self.end_minute_edit, 6, 1)
        entry_layout.addWidget(end_second_label, 7, 0)
        entry_layout.addWidget(self.end_second_edit, 7, 1)
        entry_layout.addWidget(min_x_label, 8, 0)
        entry_layout.addWidget(self.min_x_edit, 8, 1)
        entry_layout.addWidget(min_y_label, 9, 0)
        entry_layout.addWidget(self.min_y_edit, 9, 1)
        entry_layout.addWidget(max_y_label, 10, 0)
        entry_layout.addWidget(self.max_y_edit, 10, 1)
        entry_layout.addWidget(min_z_label, 11, 0)
        entry_layout.addWidget(self.min_z_edit, 11, 1)
        entry_layout.addWidget(max_z_label, 12, 0)
        entry_layout.addWidget(self.max_z_edit, 12, 1)
        ################################################

        #### DROP DOWN MENU FOR FILE FORMATS ###########
        self.options = ("IAGA2000 - NW",       # Index 0 
                        "IAGA2002 - NW",       # Index 1
                        "Clean File",          # Index 2
                        "Raw 2hz File",        # Index 3
                        "Other -- Not Working")# Index 4

        self.combo_box = QComboBox()
        # Add items to combo box
        self.combo_box.addItems(self.options)
        # Add combo box to entry layout
        entry_layout.addWidget(self.combo_box)
        file_button = QPushButton("Open File")
        file_button.clicked.connect(self.launch_dialog)
        entry_layout.addWidget(file_button)
        ################################################

        # Add entry layout to the main layout
        main_layout.addLayout(entry_layout)
        # Add maccs logo to the main layout
        main_layout.addWidget(mac_label)

        ################################################
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        ################################################

    def launch_dialog(self):

        option = self.options.index(self.combo_box.currentText())

        if option == 0:
            # TODO: IAGA2000
            print("Option not available yet")
            pass
        elif option == 1:
            # TODO: IAGA2002
            print("Option not available yet")
        elif option == 2:
            # TODO: CLEAN FILE (.s2)
            file_filter = "Clean File (*.s2)"
            response = self.get_file_name(file_filter)
        
        elif option == 3:
            # TODO: RAW FILE (.2HZ)
            file_filter = "Raw File (*.2hz)"
            response = self.get_file_name(file_filter)
        elif option == 4:
            print("Option not available yet")
        else:
            print("Got nothing")

        
    def get_file_name(self, f_filter):
        # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QFileDialog.html#PySide2.QtWidgets.PySide2.QtWidgets.QFileDialog.getOpenFileName

        file_filter = f_filter

        response = QFileDialog.getOpenFileName(
            parent = self,
            caption = "Select a file",
            dir = os.getcwd(),
            filter = file_filter
            #initialFilter = 'Clean File (*.s2)'
        )
        # Documentation says QFileDialog.getOpenFileName returns
        # (fileNames, filter used)
        # Example output to terminal
        # ('/Users/markortega-ponce/Desktop/ZMACCS/spacedatapython/CH20097.s2', 'Clean File (*.s2)')
        print(response)

        # getting file path from tuple returned in response
        filename = response[0]
        print(filename)

        # splitting up the path and selecting the filename
        filename = filename.split('/')[-1]
        print(filename)

        # setting the station entry box from the filename
        self.station_edit.set_entry(filename[0:2])
        self.year_day_edit.set_entry(filename[2:7])
        
        # reset the start times and end times
        self.start_hour_edit.set_entry(0)
        self.start_minute_edit.set_entry(0)
        self.start_second_edit.set_entry(0)
        self.end_hour_edit.set_entry(24)
        self.end_minute_edit.set_entry(0)
        self.end_second_edit.set_entry(0)

    def plot_graph(self):

        station_code_value = self.station_edit.get_entry()

def main ():

    # use brackets if not using command line
    # app = QApplication(sys.argv)
    app = QApplication([])

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()