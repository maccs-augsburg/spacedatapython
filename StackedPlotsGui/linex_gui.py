'''
linex_gui.py
May 2022 -- Created -- Mark Ortega-Ponce

# to make requirements file
pipenv run pip freeze > requirements.txt

# for someone else to be able to install those dependencies
pipenv install -r path/to/requirements.txt

'''
from ast import Pass
import subprocess
import sys
import os
import datetime
from PySide6.QtWidgets import (
    QMainWindow, QToolBar,
    QHBoxLayout, QGridLayout, QLabel,
    QWidget, QComboBox, QPushButton, 
    QFileDialog, QMessageBox, QVBoxLayout, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap

#import matplotlib
# FigureCanvasQTAgg wraps matplot image as a widget for it to be able to be added to layouts in QT
# Navigation is used for matplotlib functionalities, zooming in, zooming out, saving, etc...
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

#### Importing our own files ####################
from custom_widgets import LineEdit, Label, Color
import entry_checks

# Move back one directory to grab shared files between guis
sys.path.append("../")

import file_naming
import read_raw_to_lists
import read_clean_to_lists
import raw_to_plot

MINIMUM_WINDOW_HEIGHT = 600
MINIMUM_WINDOW_WIDTH = 1200

class MainWindow(QMainWindow):

    ''' Main display for our gui, all additional widgets go in here
    
    Attributes:
        self.file_extension: 
        self.filename: 
        self.file_path: Stores absolute file path returned in get_file_name function, String
        self.launch_dialog_option: Stores option index from drop down box in gui, distinguishes how we should plot
        self.figure: Stores figure made from plot_graph function. Uses: Save, display to user
        self.figure_canvas: canvas for figure, wraps matplotlib image as a widget. Allows you to embed and hover over values
        self.figure_canvas_flag: flag for removing old canvas, and plotting new file/values. First pass = False, rest = True
        self.matplotlib_toolbar:
        self.main_layout: QHBoxLayout, add other layouts/widgets on top of main layout in horizontal direction
        self.entry_layout: QGridLayout, add user inputs here. layout.addWidget(row, column)
        self.plotting_layout: QVBoxLayout, add matplotlibar then figure_canvas to have toolbar on top of plot
        self.someVariableName_label: Labels for the user input boxes
        self.someVariableName_edit: These variables allow for user to enter input, setters, and getters for these variables
    '''
    def __init__(self):
        super(MainWindow, self).__init__()

        ######## MAIN WINDOW SETTINGS #################
        self.setWindowTitle("MACCS Stacked Plots")
        self.setWindowIcon(QIcon("../maccslogo_nobg.png"))
        self.setMinimumHeight(MINIMUM_WINDOW_HEIGHT)
        self.setMinimumWidth(MINIMUM_WINDOW_WIDTH)
        self.station_code = ""
        station_label = Label("Station Code: ")
        self.station_edit = LineEdit()
        # Only allow station input to be 2-4 letter chars
        self.station_edit.setInputMask(">AAAA")
        self.error_message = QMessageBox()
        self.error_message.setText("Error Invalid Input")
        
        #######################
        self.file_extension = ""
        self.filename = ""
        self.filename_noextension = ""
        self.file_path = ""
        self.launch_dialog_option = 0
        self.figure = None
        self.figure_canvas = None
        self.figure_canvas_flag = False
        self.matplotlib_toolbar = None
        # Make another layout for toolbar and matplotlib
        # We add this layout onto the gui once user has chosen a file
        # Then it goes into plotting function and adds it at the end 
        self.plotting_layout = QVBoxLayout()
        #######################

        self.main_layout = QHBoxLayout()
        self.mac_label = QLabel()
        pixmap = QPixmap('../maccslogo_nobg.png')
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
        entry_layout.addWidget(self.combo_box, 14, 0)
        file_button = QPushButton("Open File")
        file_button.clicked.connect(self.launch_dialog)
        entry_layout.addWidget(file_button, 14, 1)
        plot_button = QPushButton("Plot File")
        plot_button.clicked.connect(self.plot_graph)
        entry_layout.addWidget(plot_button, 15, 0, 1, 2)
        save_button = QPushButton("Save File")
        save_button.clicked.connect(self.save_file)
        entry_layout.addWidget(save_button, 16, 0)
        save_as_button = QPushButton("Save As")
        save_as_button.clicked.connect(self.save_as)
        entry_layout.addWidget(save_as_button, 16, 1)
        ################################################

        # Add entry layout to the main layout
        self.main_layout.addLayout(entry_layout)
        # Add maccs logo to the main layout
        self.main_layout.addWidget(self.mac_label)

        ################################################
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)
        ################################################

    def launch_dialog(self):

        option = self.options.index(self.combo_box.currentText())
        self.launch_dialog_option = option

        if option == 0:
            self.warning_message_dialog("IAGA2000 Option Not Available Yet")

        elif option == 1:
            self.warning_message_dialog("IAGA2002 Option Not Available Yet")

        elif option == 2:

            self.file_extension = ".s2"
            file_filter = "Clean File (*.s2)"
            response = self.get_file_name(file_filter)
        
        elif option == 3:

            self.file_extension = ".2hz"
            file_filter = "Raw File (*.2hz)"
            response = self.get_file_name(file_filter)

        elif option == 4:

            self.warning_message_dialog("Option Not Available Yet")

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
        )
        # getting file path from tuple returned in response, ignoring second return param
        # https://www.datacamp.com/tutorial/role-underscore-python
        filename, _ = response
        self.file_path = filename
        #print(filename)

        # splitting up the path and selecting the filename
        filename = filename.split('/')[-1]
        #print(filename)

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

        station_code = self.station_edit.get_entry()
        if not entry_checks.station_code_entry_check(self):
            return

        year_day = self.year_day_edit.get_entry()
        if not entry_checks.year_day_entry_check(self):
            return
        
        start_hour = entry_checks.hour_entry_check(self, int(self.start_hour_edit.get_entry()), 1)
        start_minute = entry_checks.minute_entry_check(self, int(self.start_minute_edit.get_entry()), 1)
        start_second = entry_checks.second_entry_check(self, int(self.start_second_edit.get_entry()), 1)
        end_hour = entry_checks.hour_entry_check(self, int(self.end_hour_edit.get_entry()), 0)
        end_minute = entry_checks.minute_entry_check(self, int(self.end_minute_edit.get_entry()), 0)
        end_second = entry_checks.second_entry_check(self, int(self.end_second_edit.get_entry()), 0)

        start_time_stamp = datetime.time(hour = start_hour, minute = start_minute, second = start_second)

        if end_hour >= 24:
            self.end_hour_edit.set_entry(23)
            self.end_minute_edit.set_entry(59)
            self.end_second_edit.set_entry(59)
            end_time_stamp = datetime.time(23, 59, 59)
        else:
            end_time_stamp = datetime.time(hour = end_hour, minute = end_minute, second = end_second)

        time_interval_string = file_naming.create_time_interval_string_hms(start_hour, start_minute, start_second, 
                                                                           end_hour, end_minute, end_second)

        ####################################
        ######### Making the plot ##########
        ####################################
        self.filename_noextension = station_code + year_day
        file_name_full = station_code + year_day + self.file_extension
        self.filename = file_name_full

        try:
            # Open file object, read, binary
            file = open(self.file_path, 'rb')
        except:
            self.warning_message_dialog("File Open Error, couldn't open file")
        

        if self.launch_dialog_option == 2:

            x_arr, y_arr, z_arr, time_arr, flag_arr = read_clean_to_lists.create_datetime_lists_from_clean(file, 
                                                                                                            start_time_stamp, 
                                                                                                            end_time_stamp, 
                                                                                                            file_name_full)

        elif self.launch_dialog_option == 3:

            x_arr, y_arr, z_arr, time_arr = read_raw_to_lists.create_datetime_lists_from_raw(file, 
                                                                                            start_time_stamp, 
                                                                                            end_time_stamp, 
                                                                                            file_name_full)

        
        #min_x, max_x, min_y, max_y, min_z, max_z = entry_checks.axis_entry_checks_old(
        #     x_arr, y_arr, z_arr, min_x, max_x, min_y, max_y, min_z, max_z
        # )

        min_x = int(self.min_x_edit.get_entry())
        max_x = int(self.max_x_edit.get_entry())
        min_y = int(self.min_y_edit.get_entry())
        max_y = int(self.max_y_edit.get_entry())
        min_z = int(self.min_z_edit.get_entry())
        max_z = int(self.max_z_edit.get_entry())

        min_x, max_x = entry_checks.axis_entry_checks_new(x_arr, min_x, max_x)
        min_y, max_y = entry_checks.axis_entry_checks_new(y_arr, min_y, max_y)
        min_z, max_z = entry_checks.axis_entry_checks_new(z_arr, min_z, max_z)

        entry_checks.set_axis_entrys(self, min_x, max_x, min_y, max_y, min_z, max_z)

        self.figure = raw_to_plot.plot_arrays(x_arr, y_arr, z_arr, time_arr, 
                                                self.filename, start_time_stamp, end_time_stamp, 
                                                in_min_x=min_x, in_max_x=max_x,
                                                in_min_y=min_y, in_max_y=max_y,
                                                in_min_z=min_z, in_max_z=max_z)

        if self.figure_canvas_flag:

            self.figure_canvas.setParent(None)
            self.matplotlib_toolbar.setParent(None)
            self.plotting_layout.setParent(None)

        self.figure_canvas = FigureCanvasQTAgg(self.figure)
        self.matplotlib_toolbar = NavigationToolbar(self.figure_canvas, self)

        self.plotting_layout.addWidget(self.matplotlib_toolbar)
        self.plotting_layout.addWidget(self.figure_canvas)

        self.main_layout.addLayout(self.plotting_layout)
        # Need to set label to hidden, or else it tries to fit logo with graph
        self.mac_label.setHidden(True)
        self.figure_canvas_flag = True
        self.show()

    def save_file(self):
        
        if self.figure == None:
            self.warning_message_dialog("No figure to be saved")
            return

        filename = self.filename_noextension + '.pdf'

        self.figure.savefig(filename, format='pdf', dpi=1200)
        subprocess.Popen(filename, shell=True)
        self.warning_message_dialog("Saved " + filename + " in: " + os.getcwd())

    def save_as(self):

        if self.figure == None:
            self.warning_message_dialog("No figure to be saved")
            return
            
        response = QFileDialog.getSaveFileName(
            dir = os.getcwd(),
            filter = "PDF (*.pdf);;PNG (*.png)"
        )
        # response returns tuple
        # gets filename you put and returns as absolute path, along with filter
        #filename = response[0]
        # only grab filename, ignore file filter
        filename, _ = response
        # .pdf = 4
        if len(filename) < 5:
            return
        # go to the end (-1) and find last '/', split there
        filename = filename.split('/')[-1]

        self.figure.savefig(filename, dpi=1200)
        subprocess.Popen(filename, shell=True)
        self.warning_message_dialog("Saved " + filename + " in: " + os.getcwd())

    
    def warning_message_dialog(self, message):

        self.error_message.setText(message)
        self.error_message.exec()


def main ():

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()