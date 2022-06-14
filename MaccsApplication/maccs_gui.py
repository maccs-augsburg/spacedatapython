'''
linex_gui.py
May 2022 -- Created -- Mark Ortega-Ponce

# to make requirements file
pipenv run pip freeze > requirements.txt

# for someone else to be able to install those dependencies
pipenv install -r path/to/requirements.txt

Usage: python3 maccs_gui.py

Tutorial for PySide6

https://www.pythonguis.com/pyside6-tutorial/

'''
from ast import Pass
import subprocess
import sys
import os
import datetime
from unittest.main import MAIN_EXAMPLES
from PySide6.QtWidgets import (
    QMainWindow, QToolBar,
    QHBoxLayout, QGridLayout, QLabel,
    QWidget, QComboBox, QFileDialog, 
    QMessageBox, QVBoxLayout, QApplication, 
    QCheckBox, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
# FigureCanvasQTAgg wraps matplot image as a widget 
from matplotlib.backends.backend_qt5agg import (
                                    FigureCanvasQTAgg, 
                                    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from numpy import min_scalar_type

#### Importing our own files ####################
from custom_widgets import (
    LineEdit, Label, CheckBox, 
    PushButton, Spinbox, Time, Layout, HLayout,
    Toolbar, VLayout)
import entry_checks
from profiler import profile

# Move back one directory to grab shared files between guis
sys.path.append("../")

import file_naming
import read_raw_to_lists
import read_clean_to_lists
import plot_stacked_graphs

MINIMUM_WINDOW_HEIGHT = 600
MINIMUM_WINDOW_WIDTH = 1200

class MainWindow(QMainWindow):

    ''' Main display for our gui, all additional widgets go in here
    
    Attributes:
        self.file_extension: extension of filename chosen (remove? Check code)
        self.filename: name of file chosen, includes extension
        self.file_path: Stores absolute file path returned in get_file_name
        self.save_filename: Stores last saved filename.
        self.launch_dialog_option: Stores option index from drop down box in gui.
                                   Used to pick what function to extract data with.
        self.figure: Stores plot figure made from plot_graph function.
        self.figure_canvas: Canvas for figure, wraps matplotlib image as a widget.
                            Allows you to embed and hover over values
        self.figure_canvas_flag: Flag for removing old canvas, and plotting new file/values. 
                                 First pass = False, rest = True.
        self.matplotlib_toolbar: Tolbar to save, zoom in/out on plotting figure.
        self.main_layout: QHBoxLayout, add all child layouts to main_layout.
        self.entry_layout: QGridLayout, add user inputs here. 
                           layout.addWidget(row, column).
        self.plotting_layout: QVBoxLayout, add matplotlibar then 
                              figure_canvas to have toolbar on top of plot
        self.someVariableName_label: Labels for the user input boxes.
        self.someVariableName_edit: These variables allow for user to enter input. 
                                    Setters, and getters for these variables.
        self.x_arr: Stores last x values list.
        self.y_arr: Stores last y values list.
        self.z_arr: Stores last z values list.
        self.time_arr: Stores last hour values list.
        self.start_time_stamp: Stores last start time_stamp used.
        self.end_time_stamp: Stores last end time_stamp used.
    '''
    def __init__(self):
        super(MainWindow, self).__init__()

        ######## MAIN WINDOW SETTINGS #################
        self.setWindowTitle("MACCS Graphing Application")
        self.setWindowIcon(QIcon("../maccslogo_nobg.png"))
        self.setMinimumHeight(MINIMUM_WINDOW_HEIGHT)
        self.setMinimumWidth(MINIMUM_WINDOW_WIDTH)
        toolbar = Toolbar()
        toolbar.save_action.triggered.connect(self.save_file)
        toolbar.open_action.triggered.connect(self.launch_dialog)
        self.addToolBar(toolbar)
        ################################################
        # Maccs Logo
        self.mac_label = QLabel()
        pixmap = QPixmap('../maccslogo_nobg.png')
        self.mac_label.setPixmap(pixmap)
        self.mac_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        ################################################
        # Station input label
        # Currently label + line_edit
        self.station_code = ""
        station_label = Label("Station Code: ")
        self.station_edit = LineEdit()
        # Only allow station input to be 2-4 letter chars
        self.station_edit.setInputMask(">AAAA")
        self.error_message = QMessageBox()
        self.error_message.setText("Error Invalid Input")
        ################################################
        
        self.main_layout = QHBoxLayout()
        # Make another layout for toolbar and matplotlib
        # We add this layout onto the gui once user has chosen a file
        # Then it goes into plotting function and adds it at the end 
        self.plotting_layout = VLayout()
        # Parent Layout for entries, single graph button.
        # And other buttons
        self.parent_layout = QGridLayout()
        self.main_layout.addLayout(self.parent_layout, 1)
        entry_layout = Layout()
        xyz_layout = QGridLayout()
        ######## SIDE ENTRIES FOR GUI ##################
        year_day_label = Label("Year Day: ")
        self.year_day_edit = LineEdit()
        start_time_label = Label("Start Time: ")
        self.start_time = Time()
        self.start_time.set_start_time()
        end_time_label = Label("End Time: ")
        self.end_time = Time()
        self.end_time.set_end_time()
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
        # Add common labels and Spinbox
        # to entry_layout
        entry_layout.add_widget(station_label, 0, 0)
        entry_layout.add_widget(self.station_edit, 0, 1)
        entry_layout.add_widget(year_day_label, 1, 0)
        entry_layout.add_widget(self.year_day_edit, 1, 1)
        entry_layout.add_widget(start_time_label, 2, 0)
        entry_layout.add_widget(self.start_time,2, 1)
        entry_layout.add_widget(end_time_label, 3, 0)
        entry_layout.add_widget(self.end_time, 3, 1)
        # Add different labels and Spinbox
        # to xyz_layout
        self.xyz_two_layout = Layout()
        self.xyz_two_layout.add_widget(self.min_x_label, 0, 0)
        self.xyz_two_layout.add_widget(self.min_x_edit, 0, 1)
        self.xyz_two_layout.add_widget(self.max_x_label, 1, 0)
        self.xyz_two_layout.add_widget(self.max_x_edit, 1, 1)
        self.xyz_two_layout.add_widget(self.min_y_label, 2, 0)
        self.xyz_two_layout.add_widget(self.min_y_edit, 2, 1)
        self.xyz_two_layout.add_widget(self.max_y_label, 3, 0)
        self.xyz_two_layout.add_widget(self.max_y_edit, 3, 1)
        self.xyz_two_layout.add_widget(self.min_z_label, 4, 0)
        self.xyz_two_layout.add_widget(self.min_z_edit, 4, 1)
        self.xyz_two_layout.add_widget(self.max_z_label, 5, 0)
        self.xyz_two_layout.add_widget(self.max_z_edit, 5, 1)
        ################################################

        #### DROP DOWN MENU FOR FILE FORMATS ###########
        self.options = ("IAGA2000 - NW",       # Index 0 
                        "IAGA2002 - NW",       # Index 1
                        "Clean File",          # Index 2
                        "Raw 2hz File",        # Index 3
                        "Other -- Not Working")# Index 4

        # Making buttons and connecting to a function
        # with signal events

        self.combo_box = QComboBox()
        # Add items to combo box
        self.combo_box.addItems(self.options)
        # Add combo box to entry layout
        file_button = PushButton("Open File")
        file_button.set_uncheckable()
        file_button.clicked.connect(self.launch_dialog)

        plot_button = PushButton("Plot File")
        plot_button.set_uncheckable()
        plot_button.setMaximumWidth(180)
        plot_button.clicked.connect(self.plot_graph)

        self.zoom_out_button = PushButton("Zoom In", "Zoom Out")
        self.zoom_out_button.set_toggle_status_false()
        self.zoom_out_button.clicked.connect(self.zoom_out)

        save_button = PushButton("Save File")
        save_button.setMaximumWidth(180)
        save_button.set_uncheckable()
        save_button.clicked.connect(self.save_file)

        save_as_button = PushButton("Save As")
        save_as_button.set_uncheckable()
        save_as_button.clicked.connect(self.save_as)

        #horizontal_layout = QHBoxLayout()
        horizontal_layout = HLayout()

        self.one_array_plotted_button = PushButton(
                        "Single Graph (X, Y, Z)", 
                        "Three Graphs (X, Y, Z)")
        self.one_array_plotted_button.clicked.connect(self.update_layout)
        self.x_checkbox = CheckBox('x')
        self.y_checkbox = CheckBox('y')
        self.z_checkbox = CheckBox('z')

        horizontal_layout.add_widget(self.one_array_plotted_button)
        horizontal_layout.add_widget(self.x_checkbox)
        horizontal_layout.add_widget(self.y_checkbox)
        horizontal_layout.add_widget(self.z_checkbox)

        button_layout = Layout()
        button_layout.add_widget(self.combo_box, 0, 0)
        button_layout.add_widget(file_button, 0, 1)
        button_layout.add_widget(plot_button, 1, 0)
        button_layout.add_widget(self.zoom_out_button, 1, 1)
        button_layout.add_widget(save_button, 2, 0)
        button_layout.add_widget(save_as_button, 2, 1)

        self.parent_layout.addWidget(entry_layout,0, 0)
        self.parent_layout.addWidget(self.xyz_two_layout,1, 0)
        self.parent_layout.setRowStretch(0, 24)
        self.parent_layout.setRowStretch(1, 36)
        self.parent_layout.addWidget(horizontal_layout,2, 0)
        self.parent_layout.setRowStretch(2, 6)
        self.parent_layout.addWidget(button_layout, 3, 0)
        self.parent_layout.setRowStretch(3, 18)
        ################################################

        # Add entry layout to the main layout
        #self.main_layout.addLayout(entry_layout)
        #self.main_layout.addLayout(self.parent_layout, 1)
        # Add maccs logo to the main layout
        self.main_layout.addWidget(self.mac_label, 5)
        
        # Set final layout to widget, show in main
        ################################################
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)
        ################################################

        ################################################
        ######### Important Instance Variables #########
        ################################################
        self.filename = ""
        self.one_plot_flag = False
        self.filename_noextension = ""
        self.file_path = ""
        self.launch_dialog_option = 0
        ################################################
        self.figure = None
        self.figure_canvas = None
        self.figure_canvas_flag = False
        self.matplotlib_toolbar = None
        ################################################
        self.save_file_state = 0
        self.save_filename = ""
        self.file_num = 0
        self.new_figure = 0
        ################################################
        self.x_arr = None
        self.y_arr = None
        self.z_arr = None
        self.time_arr = None
        self.start_time_stamp = None
        self.end_time_stamp = None
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.min_z = 0
        self.max_z = 0
        ################################################
        self.plot_x = 0
        self.plot_y = 0
        self.plot_z = 0
    
    def launch_dialog(self):
        '''
        Instance function to select a file filter.
        Filter index assigned to self.launch_dialog_option
        for plotting different file types in plot_graph().
        '''
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
        if len(response[0]) == 0:
            return

        filename, _ = response
        self.file_path = filename
        # splitting up the path and selecting the filename
        filename = filename.split('/')[-1]
        # Ex: CH20097.2hz
        self.filename = filename
        #print(filename)
        self.filename_noextension = filename.split('.')[0]
        #print(self.filename_noextension)

        # setting the station entry box from the filename
        # Ex: CH 20097 .2hz
        self.station_edit.set_entry(filename[0:2])
        self.year_day_edit.set_entry(filename[2:7])
        
        self.reset_entries()

    def checks(self):

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
    
    def same_entries(self):

        start_time_stamp, end_time_stamp = self.time_stamp()

        flag = 0
        
        if start_time_stamp == self.start_time_stamp:
            flag += 1
        if end_time_stamp == self.end_time_stamp:
            flag += 1
        if self.min_x == self.min_x_edit.get_entry():
            flag += 1
        if self.max_x == self.max_x_edit.get_entry():
            flag += 1
        if self.min_y == self.min_y_edit.get_entry():
            flag += 1
        if self.max_y == self.max_y_edit.get_entry():
            flag += 1
        if self.min_z == self.min_z_edit.get_entry():
            flag += 1
        if self.max_z == self.max_z_edit.get_entry():
            flag += 1

        if flag == 8:
            # exact same entries
            print("failed test")
            return False
        else:
            print("passed test")
            return True
    
    def same_entries_one_toggled(self, x, y, z):
        
        start_time_stamp, end_time_stamp = self.time_stamp()

        flag = 0

        if start_time_stamp == self.start_time_stamp:
            flag += 1
        if end_time_stamp == self.end_time_stamp:
            flag += 1

        if self.plot_x == self.x_checkbox.isChecked():
            flag += 1
        
        if self.plot_y == self.y_checkbox.isChecked():
            flag += 1
        
        if self.plot_z == self.z_checkbox.isChecked():
            flag += 1
        

        if flag == 5:
            print("failed test")
            return False
        else:
            print("passed test")
            return True

    def time_stamp(self):

        start_time_stamp = datetime.time(hour = self.start_time.get_hour(),
                                        minute = self.start_time.get_minute(),
                                        second = self.start_time.get_second())
        
        end_time_stamp = datetime.time(hour = self.end_time.get_hour(),
                                    minute = self.end_time.get_minute(),
                                    second = self.end_time.get_second())

        return start_time_stamp, end_time_stamp
    
    
    def plot_graph(self):
        
        self.checks()

        # only check after the first successful plot
        if self.figure_canvas_flag:

            if self.one_array_plotted_button.is_toggled():
                
                if not self.same_entries_one_toggled(self.plot_x, self.plot_y, self.plot_z) and self.one_plot_flag:
                    return
            else:

                if not self.same_entries():
                    return

        start_hour = self.start_time.get_hour()
        start_minute = self.start_time.get_minute()
        start_second = self.start_time.get_second()
        end_hour = self.end_time.get_hour()
        end_minute = self.end_time.get_minute()
        end_second = self.end_time.get_second()

        self.start_time_stamp, self.end_time_stamp = self.time_stamp()
        
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

        min_x, max_x, min_y, max_y, min_z, max_z = entry_checks.axis_entry_checks_old(
            self.x_arr,
            self.y_arr,
            self.z_arr,
            min_x, max_x,
            min_y, max_y,
            min_z, max_z
        )

        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z

        entry_checks.set_axis_entrys(self, min_x, max_x, min_y, max_y, min_z, max_z)

        if self.one_array_plotted_button.is_toggled():
            
            self.plot_x = self.x_checkbox.isChecked()
            self.plot_y = self.y_checkbox.isChecked()
            self.plot_z = self.z_checkbox.isChecked()

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

            self.one_plot_flag = True

        else:

            self.figure = plot_stacked_graphs.plot_arrays(self.x_arr,
                                                self.y_arr,
                                                self.z_arr,
                                                self.time_arr,
                                                self.filename,
                                                self.start_time_stamp,
                                                self.end_time_stamp,
                                                in_min_x=min_x, 
                                                in_max_x=max_x,
                                                in_min_y=min_y, 
                                                in_max_y=max_y,
                                                in_min_z=min_z, 
                                                in_max_z=max_z)
            self.one_plot_flag = False
        
        file.close()
        self.display_figure()

    def display_figure(self):

        if self.figure_canvas_flag:

            self.figure_canvas.setParent(None)
            #self.figure_canvas.deleteLater()
            self.matplotlib_toolbar.setParent(None)
            #self.matplotlib_toolbar.deleteLater()
            self.plotting_layout.setParent(None)
            #self.plotting_layout.deleteLater()

        self.figure_canvas = FigureCanvasQTAgg(self.figure)
        self.matplotlib_toolbar = NavigationToolbar(self.figure_canvas, self)

        self.plotting_layout.add_widget(self.matplotlib_toolbar)
        self.plotting_layout.add_widget(self.figure_canvas)

        self.main_layout.addWidget(self.plotting_layout, 5)
        # Need to set label to hidden, or else it tries to fit logo with graph
        self.mac_label.setHidden(True)

        self.figure_canvas_flag = True
        self.filename_same = True
        #self.new_figure = self.figure + 1
        #self.file_num = self.file_num + 1
        self.show()

    def zoom_out(self):

        is_zoom_out_toggled = self.zoom_out_button.is_toggled()

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


        if is_zoom_out_toggled:

            min_x, max_x = entry_checks.axis_entry_checks_new(self.x_arr, 0, 0)
            min_y, max_y = entry_checks.axis_entry_checks_new(self.y_arr, 0, 0)
            min_z, max_z = entry_checks.axis_entry_checks_new(self.z_arr, 0, 0)
            
        else:
            min_x, max_x, min_y, max_y, min_z, max_z = 0,0,0,0,0,0

            min_x, max_x, min_y, max_y, min_z, max_z = entry_checks.axis_entry_checks_old(
                self.x_arr,
                self.y_arr,
                self.z_arr,
                min_x, max_x,
                min_y, max_y,
                min_z, max_z
            )

        entry_checks.set_axis_entrys(self, min_x, max_x, min_y, max_y, min_z, max_z)

        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z

        self.figure = plot_stacked_graphs.plot_arrays(self.x_arr, 
                                            self.y_arr, 
                                            self.z_arr, 
                                            self.time_arr, 
                                            self.filename, 
                                            self.start_time_stamp, 
                                            self.end_time_stamp,
                                            in_min_x=min_x,in_max_x=max_x,
                                            in_min_y=min_y,in_max_y=max_y,
                                            in_min_z=min_z,in_max_z=max_z)
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
        #print(filename)
        if len(filename) < 5:
            return
        # go to the end (-1) and find last '/', split there
        self.save_filename = filename.split('/')[-1]

        self.figure.savefig(filename, dpi=1200)
        subprocess.Popen(filename, shell=True)
        self.warning_message_dialog("Saved " + self.save_filename)
        #self.save_as_counter = self.save_as_counter + 1


    def warning_message_dialog(self, message):

        self.error_message.setText(message)
        self.error_message.exec()

    def reset_entries(self):

        self.start_time.set_start_time()
        self.end_time.set_end_time()
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
        self.xyz_two_layout.setHidden(bool_value)

        if bool_value:
            self.parent_layout.setRowStretch(0, 27)
            self.parent_layout.setRowStretch(1, 0)
            self.parent_layout.setRowStretch(2, 3)
            self.parent_layout.setRowStretch(3, 9)
        else:
            self.parent_layout.setRowStretch(0, 24)
            self.parent_layout.setRowStretch(1, 36)
            self.parent_layout.setRowStretch(2, 6)
            self.parent_layout.setRowStretch(3, 18)

def main ():

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()