'''
linex_gui.py
May 2022 -- Created -- Mark Ortega-Ponce

If your on Mac system that don't use intel anymore
https://phoenixnap.com/kb/install-pip-mac
https://codingpub.dev/python-pip3-pipenv/
https://codingpub.dev/python-install-virtualenv-and-virtualenvwrapper/

Summary: I found installing libraries to be the most difficult
         I recommend using pipenv environments

make sure your using pip3 install matplotlib, numpy .... and so on

I was using pip, but I guess that one installs the old architecture?
Will throw errors, and lead you down a long goose chase for finding the solution

I think another viable solution is anaconda environments

But im pretty sure i've broken my python paths and have not done a clean reset
'''
from ast import Pass
import sys
import os
import datetime
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QToolBar, QStatusBar, QCheckBox,
    QHBoxLayout, QGridLayout, QLabel,
    QWidget, QComboBox, QPushButton, QFileDialog, QMessageBox,
    QVBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap

from linex_gui_helper import LineEdit, Label, Color, PlotCanvas
import file_naming
import read_raw_to_lists
import read_clean_to_lists
import raw_to_plot
# forgot this wasn't being used anymore
#import clean_to_plot

import matplotlib
# FigureCanvasQTAgg wraps matplot image as a widget for it to be able to be added to layouts in QT
# Navigation is used for matplotlib functionalities, zooming in, zooming out, saving, etc...
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1200

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
        self.error_message = QMessageBox()
        self.error_message.setText("Error Invalid Input")
        
        #######################
        self.file_extension = ""
        self.filename = ""
        self.launch_dialog_option = 0
        self.figure = None
        #######################

        self.main_layout = QHBoxLayout()
        self.mac_label = QLabel()
        # TODO: use sys import so it doesnt use my path
        pixmap = QPixmap('/Users/markortega-ponce/Desktop/ZMACCS/spacedatapython/maccslogo_nobg.png')
        self.mac_label.setPixmap(pixmap)
        self.mac_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
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
        entry_layout.addWidget(max_x_label, 9, 0)
        entry_layout.addWidget(self.max_x_edit, 9, 1)
        entry_layout.addWidget(min_y_label, 10, 0)
        entry_layout.addWidget(self.min_y_edit, 10, 1)
        entry_layout.addWidget(max_y_label, 11, 0)
        entry_layout.addWidget(self.max_y_edit, 11, 1)
        entry_layout.addWidget(min_z_label, 12, 0)
        entry_layout.addWidget(self.min_z_edit, 12, 1)
        entry_layout.addWidget(max_z_label, 13, 0)
        entry_layout.addWidget(self.max_z_edit, 13, 1)
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
        plot_button = QPushButton("Plot File")
        plot_button.clicked.connect(self.plot_graph)
        entry_layout.addWidget(plot_button)
        ################################################

        # Add entry layout to the main layout
        self.main_layout.addLayout(entry_layout)
        # Add maccs logo to the main layout
        self.main_layout.addWidget(self.mac_label)

        # Make another layout for toolbar and matplotlib 
        self.plotting_layout = QVBoxLayout()
        ################################################
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)
        ################################################

    def launch_dialog(self):

        option = self.options.index(self.combo_box.currentText())
        self.launch_dialog_option = option

        if option == 0:
            # TODO: IAGA2000
            print("Option not available yet")
            self.error_message.setText("Option Not Available Yet")
            self.error_message.exec()
        elif option == 1:
            # TODO: IAGA2002
            print("Option not available yet")
            self.error_message.setText("Option Not Available Yet")
            self.error_message.exec()
        elif option == 2:
            # TODO: CLEAN FILE (.s2)
            self.file_extension = ".s2"
            file_filter = "Clean File (*.s2)"
            response = self.get_file_name(file_filter)
        
        elif option == 3:
            # TODO: RAW FILE (.2HZ)
            self.file_extension = ".2hz"
            file_filter = "Raw File (*.2hz)"
            response = self.get_file_name(file_filter)
        elif option == 4:
            print("Option not available yet")
            self.error_message.setText("Option Not Available Yet")
            self.error_message.exec()
            # it does, starts from where it left off
            #print("Does it ever reach this line? Or where does it go after dialog?")

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
        self.min_x_edit.set_entry(0)
        self.max_x_edit.set_entry(0)
        self.min_y_edit.set_entry(0)
        self.max_y_edit.set_entry(0)
        self.min_z_edit.set_entry(0)
        self.max_z_edit.set_entry(0)

    def plot_graph(self):

        print("Entered plot_graph callback function")
        station_code = self.station_edit.get_entry()
        if not self.station_code_entry_check():
            print(len(self.station_edit.get_entry()))
            print("Failed station entry check, user entered: " + self.station_edit.get_entry())
            return        
        year_day = self.year_day_edit.get_entry()
        if not self.year_day_entry_check():
            print("Failed year day entry check, user entered: " + self.year_day_edit.get_entry())
            return
        
        print("Passed year day, and station code checks")
        start_hour = self.hour_entry_check(self.start_hour_edit.get_entry(), 1)
        start_minute = self.minute_entry_check(self.start_minute_edit.get_entry(), 1)
        start_second = self.second_entry_check(self.start_second_edit.get_entry(), 1)
        end_hour = self.hour_entry_check(self.end_hour_edit.get_entry(), 0)
        end_minute = self.minute_entry_check(self.end_minute_edit.get_entry(), 0)
        end_second = self.second_entry_check(self.end_second_edit.get_entry(), 0)

        print("passed initial checks")
        min_x = int(self.min_x_edit.get_entry())
        print(min_x)
        max_x = int(self.max_x_edit.get_entry())
        print(max_x)
        min_y = int(self.min_y_edit.get_entry())
        print(min_y)
        max_y = int(self.max_y_edit.get_entry())
        print(max_y)
        min_z = int(self.min_z_edit.get_entry())
        print(min_z)
        max_z = int(self.max_z_edit.get_entry())
        print(max_z)

        start_time_stamp = datetime.time(hour = start_hour, minute = start_minute, second = start_second)

        if end_hour >= 24:
            self.end_hour_edit.set_entry(23)
            self.end_minute_edit.set_entry(59)
            self.end_second_edit.set_entry(59)
            end_time_stamp = datetime.time(23, 59, 59)
        else:
            end_time_stamp = datetime.time(hour = end_hour, minute = end_minute, second = end_second)

        time_interval_string = file_naming.create_time_interval_string_hms(start_hour, 
                                                                           start_minute, 
                                                                           start_second, 
                                                                           end_hour, 
                                                                           end_minute, 
                                                                           end_second)
        ####################################
        ######### Making the plot ##########
        ####################################
        
        # If file has been selected, and user chose plotting
        # I am assuming file_extension has at least been set by the most recent file
        # Means no checks needed, unless my loop invariant is incorrect
        file_name_full = station_code + year_day + self.file_extension
        self.filename = file_name_full

        try:
            #https://www.w3schools.com/python/ref_func_open.asp#:~:text=The%20open()%20function%20opens,our%20chapters%20about%20File%20Handling.
            file = open(file_name_full, 'rb')
        except:
            print(file_name_full)
            self.error_message.setText("File Open Error, couldn't open file")
            self.error_message.exec()
            #print("Where does program go after dialog window closes")
            #keeps going I guess
        
        print(file)
        print(self.launch_dialog_option)

        if self.launch_dialog_option == 2:

            x_arr, y_arr, z_arr, time_arr = read_clean_to_lists.create_datetime_lists_from_clean(file, start_time_stamp, end_time_stamp, file_name_full)

        elif self.launch_dialog_option == 3:

            x_arr, y_arr, z_arr, time_arr = read_raw_to_lists.create_datetime_lists_from_raw(file, start_time_stamp, end_time_stamp, file_name_full)


        self.figure = raw_to_plot.plot_arrays(x_arr, y_arr, z_arr, time_arr, self.filename, start_time_stamp, end_time_stamp, 
            in_min_x=min_x, in_max_x=max_x,
            in_min_y=min_y, in_max_y=max_y,
            in_min_z=min_z, in_max_z=max_z
        )
        
        #print("making the canvas now")
        #sc = PlotCanvas(self, width = 5, height = 4, dpi = 100)
        #sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        sc = FigureCanvasQTAgg(self.figure)
        matplotlib_toolbar = NavigationToolbar(sc, self)
        self.plotting_layout.addWidget(matplotlib_toolbar)
        self.plotting_layout.addWidget(sc)
        self.main_layout.addLayout(self.plotting_layout)
        #self.main_layout.setCentralWidget(sc)
        # Need to set label to hidden, or else it tries to fit logo with graph
        self.mac_label.setHidden(True)
        self.show()


    def station_code_entry_check (self):

        if len(self.station_edit.get_entry()) <= 1:
            print("Failed statio code entry check")
            self.error_message.setText("Error invalid station code, needs to be 2 uppercase characters")
            self.error_message.exec()
        
        # If it passed check return True
        return True
    
    def year_day_entry_check(self):

        if (len(self.year_day_edit.get_entry()) == 0):
            self.error_message.setText("There was no input for the year day entry box")
            self.error_message.exec()
        # If it passed check return True
        return True

    def hour_entry_check(self, hour_entry, end_or_start):
         
        hour = int(hour_entry)

        if hour > 24 or hour < 0:
            self.error_message.setText("Hour Entry Error. Valid input (0 - 23)")
            self.error_message.exec()
        else:
            return hour

        if end_or_start:
            self.start_hour_edit.set_entry(0)
            return 0
        else:
            self.end_hour_edit.set_entry(24)
            return 24

    def minute_entry_check(self, minute_entry, end_or_start):
        
        minute = int(minute_entry)

        if minute > 59 or minute < 0:
            self.error_message.setText("Minute Entry Error. Valid input (0 - 59)")
            self.error_message.exec()
        else:
            return minute
        
        if end_or_start:
            self.start_minute_edit.set_entry(0)
            return 0
        else:
            self.end_minute_edit.set_entry(59)
            return 59

    def second_entry_check(self, second_entry, end_or_start):

        second = int(second_entry)

        if second > 59 or second < 0:
            self.error_message.setText("Second Entry Error. Valid input (0- 59)")
            self.error_message.exec()
        else:
            return second
        
        if end_or_start:
            self.start_second_edit.set_entry(0)
            return 0
        else:
            self.end_second_edit.set_entry(59)
            return 59

def main ():

    # use brackets if not using command line
    # app = QApplication(sys.argv)
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()