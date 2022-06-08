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
    QFileDialog, QMessageBox, QVBoxLayout, 
    QApplication, QCheckBox, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
#import matplotlib
# FigureCanvasQTAgg wraps matplot image as a widget 
# for it to be able to be added to layouts in QT
# Navigation is used for matplotlib functionalities, 
# zooming in, zooming out, saving, etc...
from matplotlib.backends.backend_qt5agg import (
                                    FigureCanvasQTAgg, 
                                    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

#### Importing our own files ####################
from custom_widgets import LineEdit, Label, CheckBox, PushButton, Spinbox
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
        self.main_layout = QHBoxLayout()
        self.mac_label = QLabel()
        pixmap = QPixmap('../maccslogo_nobg.png')
        self.mac_label.setPixmap(pixmap)
        self.mac_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #self.mac_label.setScaledContents(True)
        ################################################
        
        #######################
        self.filename = ""
        self.filename_noextension = ""
        self.file_path = ""
        self.launch_dialog_option = 0
        #######################
        self.figure = None
        self.figure_canvas = None
        self.figure_canvas_flag = False
        self.matplotlib_toolbar = None
        #######################
        self.save_file_state = 0
        self.save_filename = ""
        self.file_num = 0
        self.new_figure = 0
        #######################
        self.x_arr = None
        self.y_arr = None
        self.z_arr = None
        self.time_arr = None
        self.start_time_stamp = None
        self.end_time_stamp = None
        self.min_x = 0
        self.max_z = 0
        self.min_y = 0
        self.max_y = 0
        self.min_z = 0
        self.max_z = 0

        # Make another layout for toolbar and matplotlib
        # We add this layout onto the gui once user has chosen a file
        # Then it goes into plotting function and adds it at the end 
        self.plotting_layout = QVBoxLayout()

        ######## SIDE ENTRIES FOR GUI ##################
        parent_layout = QGridLayout()
        entry_layout = QGridLayout()
        xyz_layout = QGridLayout()
        year_day_label = Label("Year Day: ")
        self.year_day_edit = LineEdit()
        start_hour_label = Label("Start Hour: ")
        self.start_hour_edit = Spinbox(0, 23, 1)
        start_minute_label = Label("Start Minute: ")
        self.start_minute_edit = Spinbox(0, 59, 1)
        start_second_label = Label("Start Second: ")
        self.start_second_edit = Spinbox(0, 59, 1)
        end_hour_label = Label("End Hour: ")
        self.end_hour_edit = Spinbox(0, 23, 1)
        end_minute_label = Label("End Minute: ")
        self.end_minute_edit = Spinbox(0, 59, 1)
        end_second_label = Label("End Second: ")
        self.end_second_edit = Spinbox(0, 59, 1)
        self.min_x_label = Label("Plot Min X: ")
        self.min_x_edit = Spinbox(0, 99999, 10)
        self.max_x_label = Label("Plot Max X: ")
        self.max_x_edit = Spinbox(0, 99999, 10)
        self.min_y_label = Label("Plot Min Y: ")
        self.min_y_edit = Spinbox(0, 99999, 10)
        self.max_y_label = Label("Plot Max Y: ")
        self.max_y_edit = Spinbox(0, 99999, 10)
        self.min_z_label = Label("Plot Min Z: ")
        self.min_z_edit = Spinbox(0, 99999, 10)
        self.max_z_label = Label("Plot Max Z: ")
        self.max_z_edit = Spinbox(0, 99999, 10)
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
        xyz_layout.addWidget(self.min_x_label, 0, 0)
        xyz_layout.addWidget(self.min_x_edit, 0, 1)
        xyz_layout.addWidget(self.max_x_label, 1, 0)
        xyz_layout.addWidget(self.max_x_edit, 1, 1)
        xyz_layout.addWidget(self.min_y_label, 2, 0)
        xyz_layout.addWidget(self.min_y_edit, 2, 1)
        xyz_layout.addWidget(self.max_y_label, 3, 0)
        xyz_layout.addWidget(self.max_y_edit, 3, 1)
        xyz_layout.addWidget(self.min_z_label, 4, 0)
        xyz_layout.addWidget(self.min_z_edit, 4, 1)
        xyz_layout.addWidget(self.max_z_label, 5, 0)
        xyz_layout.addWidget(self.max_z_edit, 5, 1)
        parent_layout.addLayout(entry_layout,0, 0)
        parent_layout.addLayout(xyz_layout,1, 0)
        parent_layout.setRowStretch(0, 48)
        parent_layout.setRowStretch(1, 36)

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
        file_button = QPushButton("Open File")
        file_button.clicked.connect(self.launch_dialog)
        plot_button = QPushButton("Plot File")
        plot_button.clicked.connect(self.plot_graph)
        self.zoom_out_button = PushButton("Zoom Out", "Zoom In")
        self.zoom_out_button.set_toggle_status_false()
        self.zoom_out_button.clicked.connect(self.zoom_out)
        save_button = QPushButton("Save File")
        save_button.clicked.connect(self.save_file)
        save_as_button = QPushButton("Save As")
        save_as_button.clicked.connect(self.save_as)
        horizontal_layout = QHBoxLayout()

        self.one_array_plotted_button = PushButton(
                        "Single Graph (X, Y, Z)", 
                        "Three Graphs (X, Y, Z)")
        self.x_checkbox = CheckBox('x')
        self.y_checkbox = CheckBox('y')
        self.z_checkbox = CheckBox('z')
        horizontal_layout.addWidget(self.one_array_plotted_button)
        horizontal_layout.addWidget(self.x_checkbox)
        horizontal_layout.addWidget(self.y_checkbox)
        horizontal_layout.addWidget(self.z_checkbox)
        self.one_array_plotted_button.clicked.connect(self.update_layout)
        button_layout = QGridLayout()
        button_layout.addWidget(self.combo_box, 0, 0)
        button_layout.addWidget(file_button, 0, 1)
        button_layout.addWidget(plot_button, 1, 0)
        button_layout.addWidget(self.zoom_out_button, 1, 1)
        button_layout.addWidget(save_button, 2, 0)
        button_layout.addWidget(save_as_button, 2, 1)
        parent_layout.addLayout(horizontal_layout,2, 0)
        parent_layout.setRowStretch(2, 6)
        parent_layout.addLayout(button_layout, 3, 0)
        parent_layout.setRowStretch(3, 18)
        ################################################

        # Add entry layout to the main layout
        #self.main_layout.addLayout(entry_layout)
        self.main_layout.addLayout(parent_layout)
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
        file_filter = f_filter
        # guis will be in the same folder, so go back one 
        # directory for shared files 
        current_directory = os.getcwd()
        # go back one directory, similar to ls command
        os.chdir('..')
        move_up_current_directory = os.getcwd()

        response = QFileDialog.getOpenFileName(
            parent = self,
            caption = "Select a file",
            dir = move_up_current_directory,
            filter = file_filter
        )
        # after picking file, move back to original location
        os.chdir(current_directory)

        # if user cancels button, dont want to execute function
        if len(response) == 0:
            return

        filename, _ = response
        self.file_path = filename
        # splitting up the path and selecting the filename
        filename = filename.split('/')[-1]
        # Ex: CH20097.2hz
        self.filename = filename
        print(filename)
        self.filename_noextension = filename.split('.')[0]
        print(self.filename_noextension)

        # setting the station entry box from the filename
        # Ex: CH 20097 .2hz
        self.station_edit.set_entry(filename[0:2])
        self.year_day_edit.set_entry(filename[2:7])
        
        self.reset_entries()

    def plot_graph(self):
        
        print("inside plotting")
        if len(self.filename) == 0:
            self.warning_message_dialog(
                "No file to work with. Open a file with open file button.")
            return

        station_code = self.station_edit.get_entry()
        if not entry_checks.station_code_entry_check(station_code):

            self.warning_message_dialog(
            "Error invalid station code. Needs to be 2-4 characters")

            return

        year_day = self.year_day_edit.get_entry()
        if not entry_checks.year_day_entry_check(self):

            self.warning_message_dialog(
            "There was no input for the year day entry box")

            return

        x_state = self.x_checkbox.isChecked()
        y_state = self.y_checkbox.isChecked()
        z_state = self.z_checkbox.isChecked()

        any_state = x_state or y_state or z_state

        if self.one_array_plotted_button.is_toggled():
            if not any_state:
                self.warning_message_dialog("Choose Axis to plot (X, Y, Z)")
                return

        start_hour = self.start_hour_edit.get_entry()
        start_minute = self.start_minute_edit.get_entry()
        start_second = self.start_second_edit.get_entry()
        end_hour = self.end_hour_edit.get_entry()
        end_minute = self.end_minute_edit.get_entry()
        end_second = self.end_second_edit.get_entry()

        self.start_time_stamp = datetime.time(hour = start_hour,
                                            minute = start_minute, 
                                            second = start_second)
        self.end_time_stamp = datetime.time(hour = end_hour, 
                                            minute = end_minute, 
                                            second = end_second)
        
        # TODO: Do I even need this? I think I just copied it over from old line_x file
        time_interval_string = file_naming.create_time_interval_string_hms(
                                                                start_hour, 
                                                                start_minute, 
                                                                start_second, 
                                                                end_hour, 
                                                                end_minute, 
                                                                end_second)

        ####################################
        ######### Making the plot ##########
        ####################################

        try:
            # Open file object, read, binary
            file = open(self.file_path, 'rb')
        except:
            self.warning_message_dialog("File Open Error, couldn't open file")
            return
        
        '''
        Once future file types are supported, add here.
        Launch Dialog Option assigned when you open a file
        '''
        if self.launch_dialog_option == 2:
            # Doing short names to stay around 80-85 chars per row
            x,y,z,t,f = read_clean_to_lists.create_datetime_lists_from_clean(
                                                            file, 
                                                            self.start_time_stamp, 
                                                            self.end_time_stamp, 
                                                            self.filename)
            # easy to glance over, might be used for new feature?
            flag_arr = f

        elif self.launch_dialog_option == 3:
            # Doing short names to stay around 80-85 chars per row
            x,y,z,t = read_raw_to_lists.create_datetime_lists_from_raw(
                                                            file, 
                                                            self.start_time_stamp,
                                                            self.end_time_stamp, 
                                                            self.filename)
        # Assign those short names here
        self.x_arr = x
        self.y_arr = y
        self.z_arr = z
        self.time_arr = t

        min_x = self.min_x_edit.get_entry()
        max_x = self.max_x_edit.get_entry()
        min_y = self.min_y_edit.get_entry()
        max_y = self.max_y_edit.get_entry()
        min_z = self.min_z_edit.get_entry()
        max_z = self.max_z_edit.get_entry()

        min_x, max_x = entry_checks.axis_entry_checks_new(
                                                        self.x_arr, min_x, max_x)
        min_y, max_y = entry_checks.axis_entry_checks_new(
                                                        self.y_arr, min_y, max_y)
        min_z, max_z = entry_checks.axis_entry_checks_new(
                                                        self.z_arr, min_z, max_z)


        entry_checks.set_axis_entrys(self, min_x, max_x, min_y, max_y, min_z, max_z)
        
        if self.one_array_plotted_button.is_toggled():

            self.figure = entry_checks.graph_from_plotter_entry_check( 
                                                        self.x_arr, 
                                                        self.y_arr, 
                                                        self.z_arr,
                                                        self.x_checkbox.isChecked(),
                                                        self.y_checkbox.isChecked(),
                                                        self.z_checkbox.isChecked(), 
                                                        self.time_arr,
                                                        self.filename, 
                                                        self.start_time_stamp,
                                                        self.end_time_stamp)
            # Wont need this here since im hiding other plotting now
            #self.reset_entries()

        else:

            self.figure = raw_to_plot.plot_arrays(self.x_arr, 
                                                self.y_arr, 
                                                self.z_arr, 
                                                self.time_arr, 
                                                self.filename, 
                                                self.start_time_stamp, 
                                                self.end_time_stamp, 
                                                in_min_x=min_x, in_max_x=max_x,
                                                in_min_y=min_y, in_max_y=max_y,
                                                in_min_z=min_z, in_max_z=max_z)


        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z

        self.display_figure()


    def display_figure(self):

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
        #self.new_figure = self.figure + 1
        #self.file_num = self.file_num + 1
        self.show()


    def zoom_out(self):

        print(self.zoom_out_button.is_toggled())
        if self.figure == None:
            self.zoom_out_button.set_toggle_status_false()
            self.zoom_out_button.change_text()
            self.warning_message_dialog("No figure to work with")
            return

        if self.one_array_plotted_button.is_toggled():
            self.zoom_out_button.set_toggle_status_false()
            self.zoom_out_button.change_text()
            self.warning_message_dialog(
                "This feature only available for Three Graph Plotting right now")
            return

        if self.zoom_out_button.is_toggled():
            self.figure = raw_to_plot.plot_arrays(self.x_arr, 
                                                self.y_arr, 
                                                self.z_arr, 
                                                self.time_arr, 
                                                self.filename, 
                                                self.start_time_stamp, 
                                                self.end_time_stamp,
                                                in_min_x=0,in_max_x=0,
                                                in_min_y=0,in_max_y=0,
                                                in_min_z=0,in_max_z=0)
        else:
            self.figure = raw_to_plot.plot_arrays(self.x_arr,
                                                self.y_arr,
                                                self.z_arr,
                                                self.time_arr,
                                                self.filename,
                                                self.start_time_stamp,
                                                self.end_time_stamp,
                                                in_min_x=self.min_x, 
                                                in_max_x=self.max_x,
                                                in_min_y=self.min_y, 
                                                in_max_y=self.max_y,
                                                in_min_z=self.min_z, 
                                                in_max_z=self.max_z)
           #self.plot_counter = self.plot_counter + 1

        self.display_figure()

    def save_file(self):
        
        if self.figure == None:
            self.warning_message_dialog("No figure to be saved")
            return

        cwd = os.getcwd()
        
        if self.save_filename == None:
            filename = self.filename_noextension + '.pdf'
        else:
            filename = self.save_filename
        
        file_list = os.listdir(cwd)

        flag = False
        for file in file_list:
            if filename == file:
                flag = True
        
        if not flag:
            self.save_as()
            return


        self.figure.savefig(filename, format='pdf', dpi=1200)
        subprocess.Popen(filename, shell=True)
        self.warning_message_dialog("Saved " + filename + " in: " + os.getcwd())
        self.save_file_state = 1



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
        self.save_filename = filename

        self.figure.savefig(filename, dpi=1200)
        subprocess.Popen(filename, shell=True)
        self.warning_message_dialog("Saved " + filename + " in: " + os.getcwd())
        #self.save_as_counter = self.save_as_counter + 1
    
    # TODO: Use regular expressions for filter? Prevent bad input by accident
    def warning_message_dialog(self, message):

        self.error_message.setText(message)
        self.error_message.exec()

    def reset_entries(self):
        # reset the start times and end times
        self.start_hour_edit.set_entry(0)
        self.start_minute_edit.set_entry(0)
        self.start_second_edit.set_entry(0)
        self.end_hour_edit.set_entry(23)
        self.end_minute_edit.set_entry(59)
        self.end_second_edit.set_entry(59)
        self.min_x_edit.set_entry(0)
        self.max_x_edit.set_entry(0)
        self.min_y_edit.set_entry(0)
        self.max_y_edit.set_entry(0)
        self.min_z_edit.set_entry(0)
        self.max_z_edit.set_entry(0)

    def update_layout(self):

        bool_value = self.one_array_plotted_button.is_toggled()

        self.zoom_out_button.set_toggle_status_false()
        self.zoom_out_button.change_text()

        self.min_x_edit.setHidden(bool_value)
        self.max_x_edit.setHidden(bool_value)
        self.min_x_label.setHidden(bool_value)
        self.max_x_label.setHidden(bool_value)

        self.min_y_label.setHidden(bool_value)
        self.max_y_label.setHidden(bool_value)
        self.min_y_edit.setHidden(bool_value)
        self.max_y_edit.setHidden(bool_value)

        self.min_z_label.setHidden(bool_value)
        self.max_z_label.setHidden(bool_value)
        self.min_z_edit.setHidden(bool_value)
        self.max_z_edit.setHidden(bool_value)

def main ():

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()