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
Hello this is a change to see if source control is working
'''
import subprocess
import sys
import os
import datetime
from PySide6.QtWidgets import (
    QMainWindow,QHBoxLayout, 
    QGridLayout, QLabel,
    QWidget, QComboBox, QFileDialog, 
    QMessageBox, QApplication 
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QAction, QKeySequence
# FigureCanvasQTAgg wraps matplot image as a widget 
from matplotlib.backends.backend_qt5agg import (
                                    FigureCanvasQTAgg, 
                                    NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#### Importing our own files ####################
from custom_widgets import (
    LineEdit, Label, CheckBox, 
    PushButton, Spinbox, Time, 
    Layout, HLayout,
    Toolbar, VLayout)
import entry_checks
# Move back one directory to grab shared files between guis
sys.path.append("../")
import file_naming
import read_raw_to_lists
import read_clean_to_lists
import plot_stacked_graphs

MINIMUM_WINDOW_HEIGHT = 700
MINIMUM_WINDOW_WIDTH = 1400

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
        self.toolbar = Toolbar()
        self.toolbar.home_action.triggered.connect(self.home)
        self.toolbar.save_action.triggered.connect(self.save_file)
        self.toolbar.open_action.triggered.connect(self.toolbar_open)
        self.toolbar.hide_entry_action.triggered.connect(self.hide_entry_layout)
        self.toolbar.zoom_action.triggered.connect(self.time_zoom)
        self.addToolBar(self.toolbar)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        tool_menu = menu.addMenu("&Tools")
        help_menu = menu.addMenu("&Help")
    
        zoom_in_action = QAction("Zoom In       ", self)
        zoom_in_action.triggered.connect(self.time_zoom)
        zoom_in_action.setStatusTip("Pick two points on the x-axis to zoom in")
        tool_menu.addAction(zoom_in_action)

        help_zoom_action = QAction("Zoom in help ", self)
        help_zoom_action.triggered.connect(self.help_menu_zoom_button)
        help_menu.addAction(help_zoom_action)

        help_time_action = QAction("Why is time set to 23:00:00 and not 23:59:59?", self)
        help_time_action.triggered.connect(self.help_menu_time_button)
        help_menu.addAction(help_time_action)

        #file_menu = menu.addMenu("&Open...                   ")
        open_action = QAction("Open...       ", self)
        open_action.triggered.connect(self.toolbar_open)
        # https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2#bkmk_frequentwin
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        file_menu.addSeparator()
        file_menu.addAction(open_action)
        file_submenu = file_menu.addMenu("Open Recent")
        open_recent_action = QAction("Open Recent (In Development)", self)
        #open_recent_action.triggered.connect(self.open_recent)
        file_submenu.addAction(open_recent_action)

        # f = open("open_recent/recent.txt", "r")
        # self.file_list = f.readlines()
        # f.close()
        # open_one = QAction(self.file_list[0], self)
        # open_one.triggered.connect(self.open_recent)
        # file_submenu.addAction(open_one)
        # file_submenu.addAction(open_one)
        # open_two = QAction(self.file_list[1], self)
        # file_submenu.addAction(open_two)
        # open_two.triggered.connect(self.open_recent)
        # open_three = QAction(self.file_list[2], self)
        # file_submenu.addAction(open_three)
        # open_three.triggered.connect(self.open_recent)
        # open_four = QAction(self.file_list[3], self)
        # file_submenu.addAction(open_four)
        # open_four.triggered.connect(self.open_recent)
        # open_five = QAction(self.file_list[4], self)
        # open_five.triggered.connect(self.open_recent)
        # file_submenu.addAction(open_five)

        '''
        https://www.w3schools.com/python/python_sets.asp
        https://www.w3schools.com/python/python_dictionaries.asp
        lets say we have a set of file_paths, meaning we only take distinct paths
        we add it to our set, so now we can access by index.
        We could do a quick search through the set/list, maybe hashmap?
        once we found name, we access our QAction by index, we get the name by index
        we split it, and get the filename, we assign to our instance variables
        plot right away?
        '''
        file_menu.addSeparator()
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        file_menu.addAction(save_action)
        save_as_action = QAction("Save As...", self)
        save_as_action.triggered.connect(self.save_as)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        file_menu.addAction(save_as_action)
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
        self.parent_layout = Layout()
        self.main_layout.addWidget(self.parent_layout, 1)
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
        self.combo_box.setCurrentIndex(3)
        # Add combo box to entry layout
        file_button = PushButton("Open File")
        file_button.set_uncheckable()
        file_button.clicked.connect(self.launch_dialog)

        plot_button = PushButton("Plot File")
        plot_button.set_uncheckable()
        plot_button.setMaximumWidth(180)
        plot_button.clicked.connect(self.plot_graph)

        self.zoom_out_button = PushButton("Zoom In", "Zoom In")
        self.zoom_out_button.set_toggle_status_false()
        #self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_out_button.clicked.connect(self.time_zoom)

        save_button = PushButton("Save File")
        save_button.setMaximumWidth(180)
        save_button.set_uncheckable()
        save_button.clicked.connect(self.save_file)

        save_as_button = PushButton("Save As")
        save_as_button.set_uncheckable()
        save_as_button.clicked.connect(self.save_as)

        self.one_array_plotted_button = PushButton(
                        "Single Graph (X, Y, Z)", 
                        "Three Graphs (X, Y, Z)")
        self.one_array_plotted_button.clicked.connect(self.update_layout)
        self.x_checkbox = CheckBox('x')
        self.y_checkbox = CheckBox('y')
        self.z_checkbox = CheckBox('z')

        horizontal_layout = HLayout()
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

        self.parent_layout.add_widget(entry_layout,0, 0)
        self.parent_layout.add_widget(self.xyz_two_layout,1, 0)
        self.parent_layout.set_row_stretch(0, 24)
        self.parent_layout.set_row_stretch(1, 36)
        self.parent_layout.add_widget(horizontal_layout,2, 0)
        self.parent_layout.set_row_stretch(2, 6)
        self.parent_layout.add_widget(button_layout, 3, 0)
        self.parent_layout.set_row_stretch(3, 18)
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
        self.file_paths = []
        self.one_plot_flag = False
        self.stacked_plot_flag = False
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
        ################################################
        self.time_flag = False
        self.datetime_object_one = None
        self.y_coord_one = None
        self.datetime_object_two = None
        self.y_coord_two = None
    
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
            return False

        filename, _ = response
        self.file_path = filename
        self.file_paths.append(self.file_path)

        # splitting up the path and selecting the filename
        filename = filename.split('/')[-1]
        #https://www.w3schools.com/python/python_file_write.asp
        #https://thispointer.com/python-how-to-insert-lines-at-the-top-of-a-file/
        # f = open("open_recent/recent.txt", "a")
        # f.write(self.file_path + "\n")
        # #f.write(filename + "\n")
        # f.close()
        # Ex: CH20097.2hz
        self.filename = filename
        self.filename_noextension = filename.split('.')[0]
        # setting the station entry box from the filename
        # Ex: CH 20097 .2hz
        self.station_edit.set_entry(filename[0:2])
        self.year_day_edit.set_entry(filename[2:7])
        
        self.reset_entries()
        return True

    def toolbar_open(self):

        if not self.get_file_name("Raw File (*.2hz);;Clean File (*.s2)"):
            return
        # breaks up into [filename][extension]
        extension = self.filename.split('.')[1]
        print(extension)

        if extension == "s2":
            self.combo_box.setCurrentIndex(2)
        
        if extension == "2hz":
            self.combo_box.setCurrentIndex(3)

        self.launch_dialog_option = self.options.index(self.combo_box.currentText())

    def open_recent(self):
        pass

    def checks(self):

        if len(self.filename) == 0:
            self.warning_message_dialog(
                "No file to work with. Open a file with open file button.")
            return False

        station_code = self.station_edit.get_entry()
        if not entry_checks.station_code_entry_check(station_code):

            self.warning_message_dialog(
            "Error invalid station code. Needs to be 2-4 characters")

            return False

        year_day = self.year_day_edit.get_entry()
        if not entry_checks.year_day_entry_check(self):

            self.warning_message_dialog(
            "There was no input for the year day entry box")

            return False

        x_state = self.x_checkbox.isChecked()
        y_state = self.y_checkbox.isChecked()
        z_state = self.z_checkbox.isChecked()

        any_state = x_state or y_state or z_state

        if self.one_array_plotted_button.is_toggled():
            if not any_state:
                self.warning_message_dialog("Choose Axis to plot (X, Y, Z)")
                return False

        return True
    
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
    
    def same_entries_one_toggled(self):
        
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
        #https://doc.qt.io/qt-6/qdatetimeedit.html#maximumTime-prop
        e_hour = self.end_time.get_hour()
        e_minute = self.end_time.get_minute()
        e_second = self.end_time.get_second()

        start_time_stamp = datetime.time(hour = self.start_time.get_hour(),
                                        minute = self.start_time.get_minute(),
                                        second = self.start_time.get_second())
        
        if e_hour == 23 and e_minute == 0 and e_second == 0:
            end_time_stamp = datetime.time(hour = 23, minute = 59, second = 59)
            print("Time stamp, default value")
        else:
            print("Time stamp, custom value")
            print(self.end_time.get_hour())
            end_time_stamp = datetime.time(hour = self.end_time.get_hour(),
                                            minute = self.end_time.get_minute(),
                                            second = self.end_time.get_second())


        return start_time_stamp, end_time_stamp
    
    
    def plot_graph(self):
    
        # if checks test return false, don't plot
        if not self.checks():
            return

        # only check after the first successful plot
        # gets set at the end of this function and remains True

        if self.figure_canvas_flag:
            # if this is toggled, do following test
            if self.one_array_plotted_button.is_toggled():
                # if !(test failed) and we have plotted one_plot already
                # means no new info to plot
                if not self.same_entries_one_toggled() and self.one_plot_flag:
                    return
                else:
                    self.delete_figure()

            else:  
                # if !(test failed) and we have plotted stacked already
                # means no new info to plot
                if not self.same_entries() and self.stacked_plot_flag:
                    return
                else:
                    self.delete_figure()

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
        Adding a coupe more else if checks to get datetime lists
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

        # get current stacked plot entries
        min_x = self.min_x_edit.get_entry()
        max_x = self.max_x_edit.get_entry()
        min_y = self.min_y_edit.get_entry()
        max_y = self.max_y_edit.get_entry()
        min_z = self.min_z_edit.get_entry()
        max_z = self.max_z_edit.get_entry()

        # normalize the data to display even ticks
        min_x, max_x, min_y, max_y, min_z, max_z = entry_checks.axis_entry_checks_old(
            self.x_arr,
            self.y_arr,
            self.z_arr,
            min_x, max_x,
            min_y, max_y,
            min_z, max_z
        )
        # assign these to self to keep track of what's been plotted
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z

        entry_checks.set_axis_entrys(self, min_x, max_x, min_y, max_y, min_z, max_z)
        # if one plot button is toggled
        # call necessary functions for one plot
        if self.one_array_plotted_button.is_toggled():
            
            # keeping track of whats been plotted already
            self.plot_x = self.x_checkbox.isChecked()
            self.plot_y = self.y_checkbox.isChecked()
            self.plot_z = self.z_checkbox.isChecked()

            self.figure = entry_checks.graph_from_plotter_entry_check( 
                                                        self.x_arr, 
                                                        self.y_arr, 
                                                        self.z_arr,
                                                        self.plot_x,
                                                        self.plot_y,
                                                        self.plot_z, 
                                                        self.time_arr,
                                                        self.filename, 
                                                        self.start_time_stamp,
                                                        self.end_time_stamp)
            # set one plot flag to true, meaning we have plotted at least once
            self.one_plot_flag = True
            # set stacked flag to false, meaning next time we plot it
            # it will be the first time again
            self.stacked_plot_flag = False

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
            # set one plot flag to false, meaning next time we plot it
            # it will be the first time again
            self.one_plot_flag = False
            # set staacked flag to true, meaninig we have plotted at least once
            self.stacked_plot_flag = True
        
        # close opened file
        file.close()
        self.display_figure()

    def __call__(self, event):

        datetime_object = mdates.num2date(event.xdata)

        if not self.time_flag:
            self.datetime_object_one = datetime_object
            self.y_coord_one = event.ydata
            print(self.datetime_object_one, self.y_coord_one)
            self.time_flag = True
        else:
            self.datetime_object_two = datetime_object
            self.y_coord_two = event.ydata
            print(self.datetime_object_two, self.y_coord_two)
            self.time_zoom()

        print("-----------------------------------------")

    def time_zoom(self):
        # connect figure to mpl_in...
        # https://matplotlib.org/stable/users/explain/event_handling.html

        if self.figure is None:
            # soft warning, no dialog
            self.zoom_out_button.set_toggle_status_false()
            return

        # if we went through menu, still want to set zoom button to blue
        # on first pass self.time_flag is false, set to true when we pick first point
        # so we only go through this once
        if not self.zoom_out_button.is_toggled() and not self.time_flag:
            self.zoom_out_button.set_toggle_status_true()

        self.cid = self.figure_canvas.mpl_connect("button_press_event", self)

        if self.time_flag:
            self.figure_canvas.mpl_disconnect(self.cid)
            self.zoom_out_button.set_toggle_status_false()
            self.time_flag = False
            if not self.check_datetimes():
                return
            hour, minute, second, e_hour, e_minute, e_second = self.get_times(
                self.datetime_object_one,
                self.datetime_object_two
            )
            self.start_time.set_own_time(hour, minute, second)
            self.end_time.set_own_time(e_hour, e_minute, e_second)
            self.plot_graph()

    def get_times(self, datetime_object, datetime_object_two):

        start_h = int(datetime_object.strftime("%H"))
        start_min = int(datetime_object.strftime("%M"))
        start_sec = int(datetime_object.strftime("%S"))
        end_h = int(datetime_object_two.strftime("%H"))
        end_min = int(datetime_object_two.strftime("%M"))
        end_sec = int(datetime_object_two.strftime("%S"))

        # if same hour, then dont want to set min to 0
        if start_h == end_h:

            return start_h, start_min, 0, end_h, end_min, 0
        
        # want to graph by integer hour values, can change based on feedback
        if end_h - start_h > 1:

            if start_min > 30:
                start_h += 1
            
            if end_min > 30:
                end_h += 1

        return start_h, 0, 0, end_h, 0, 0
        
    def check_datetimes(self):
        if self.datetime_object_one > self.datetime_object_two:
            print("Failed Datetime Test in Zoom In function.")
            self.warning_message_dialog("Second time cannot be greater than the first, please try again")
            return False
        else:
            return True

    def display_figure(self):

        self.plotting_layout.setHidden(False)

        if self.figure_canvas_flag:

            self.figure_canvas.setParent(None)
            self.matplotlib_toolbar.setParent(None)

        self.figure_canvas = FigureCanvasQTAgg(self.figure)
        self.matplotlib_toolbar = NavigationToolbar(self.figure_canvas, self)

        self.plotting_layout.add_widget(self.matplotlib_toolbar)
        self.plotting_layout.add_widget(self.figure_canvas)
        self.main_layout.addWidget(self.plotting_layout, 5)

        self.mac_label.setHidden(True)

        self.figure_canvas_flag = True
        self.show()

    def delete_figure(self):
        '''Deletes widgets, setting parent to none on widgets
        leaves them hanging in the background process.
        Not garbage collected, so have to delete'''
        self.figure_canvas.deleteLater()
        plt.close(self.figure)
        self.matplotlib_toolbar.deleteLater()

    def save_file(self):
        
        if self.figure is None:
            self.warning_message_dialog("No figure to be saved")
            return

        cwd = os.getcwd()
        
        if self.save_filename is None:
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

        #self.figure.set_size_inches(12, 7)
        self.figure.savefig(filename, format='pdf', dpi=1200)
        subprocess.Popen(filename, shell=True)
        self.warning_message_dialog("Saved " + filename + " in: " + os.getcwd())

    def save_as(self):

        if self.figure is None:
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
        #self.figure.set_size_inches(12, 7)
        self.figure.savefig(filename, dpi=1200)
        subprocess.Popen(filename, shell=True)
        self.warning_message_dialog("Saved " + self.save_filename)

    def home(self):

        self.plotting_layout.setHidden(True)
        self.mac_label.setHidden(False)
        self.one_plot_flag = False
        self.stacked_plot_flag = False
        self.reset_entries()

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
            self.parent_layout.set_row_stretch(0, 27)
            self.parent_layout.set_row_stretch(1, 0)
            self.parent_layout.set_row_stretch(2, 3)
            self.parent_layout.set_row_stretch(3, 9)
        else:
            self.parent_layout.set_row_stretch(0, 24)
            self.parent_layout.set_row_stretch(1, 36)
            self.parent_layout.set_row_stretch(2, 6)
            self.parent_layout.set_row_stretch(3, 18)

    def hide_entry_layout(self):
        
        bool_value = self.toolbar.hide_entry_action.isChecked()
        
        self.parent_layout.setHidden(bool_value)

    def help_menu_zoom_button(self):
        self.warning_message_dialog("Zoom In Button: Pick two points on the plot.\nFirst point picked should be smaller than the second point to avoid error.")

    def help_menu_time_button(self):
        self.warning_message_dialog(
            "Default time is set to 23:00:00 for convenience.\nAllows user to change hour values faster without having to adjust MM:SS.\nStill graphs as 23:59:59 (whole day).")

def main ():

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()