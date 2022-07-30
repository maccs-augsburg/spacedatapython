'''
new_gui.py

PySide6 Gui interface for Augsburg Physics Department

Usage: python3 new_gui.py

Created - Mark Ortega-Ponce & Chris Hance
June 2022
'''
# Imports from PySide6 // QT
from PySide6.QtWidgets import (QMainWindow, QApplication, 
                                QLabel, QWidget, QHBoxLayout, 
                                QToolBar,QFileDialog,
                                QMessageBox,QComboBox,
                                QGroupBox,QSizePolicy
                                )
from PySide6.QtGui import QIcon, QAction, QPalette, QPixmap, Qt,QKeySequence
from PySide6.QtCore import  QSize, QTime, QSettings

# Imports from matplotlib
import matplotlib
matplotlib.use('qtagg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

# Imports from python 
import sys
import datetime
import os


#Custom Widget Imports
from gui.custom_widgets import (
    LineEdit, Label, CheckBox, 
    PushButton, Spinbox, 
    GridLayout, HLayout,
    VLayout)

# Imports from subpackages
import gui.entry_check
from gui.custom_graph_toggle_widget import SwitchButtonWidget
from gui.custom_time_widget import MinMaxTime
from gui.custom_seperator_line import LineSeperator
from util.file_naming import create_2hz_plot_file_name
import model.read_clean_to_lists
import model.read_raw_to_lists
import model.read_IAGA2002_to_lists
import plot.plot_stacked_graphs
import plot.plot_three_axis_graphs
import plot.test_figure

# Packaging stuff
# Holds full path of the current Python File
# Use this to build relative paths for icons using os.path.join()
basedir = os.path.dirname(__file__)

MINIMUM_WINDOW_HEIGHT = 1000
MINIMUM_WINDOW_WIDTH = 1600

class MainWindow(QMainWindow):
    """
    MainWindow class that uses the PySide6 library. Creates a 
    graphical user interface to visualize data collected from
    MACCS magnetometer stations. Current file types supported 
    are .2hz and .s2 format.
    """
    
    def __init__(self):
        """
        Initializes the application including setting the window size
        and setting all the widgets into the window and actions into the
        application.
        """
        
        super().__init__()
        self.setWindowTitle("MACCS Plotting Program")

        self.setMinimumHeight(MINIMUM_WINDOW_HEIGHT)
        self.setMinimumWidth(MINIMUM_WINDOW_WIDTH)
        self.prev_time = []

        ###########################
        ### Place Holder Values ###
        ###########################
        self.selection_file_value = ''
        self.temp_var = 0
        
        ##################
        ### Maccs Logo ###
        ##################

        # Maccs Logo
        self.mac_label = QLabel()
        pixmap = QPixmap(os.path.join(basedir, "images", "maccslogo_nobg.png") )
        self.mac_label.setPixmap(pixmap)
        self.mac_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        ###############
        ### Toolbar ###
        ###############

        toolbar = QToolBar("Main Toolbar")    
        toolbar.setIconSize(QSize(16,16))
        action_home = QAction(QIcon(os.path.join(basedir, "images","home.png")), "Home", self)
        action_openfile = QAction(QIcon(os.path.join(basedir, "images", "folder-open.png")),"Open...       ", self)
        action_savefile = QAction(QIcon(os.path.join(basedir, "images", "disk.png")),"Save Plot", self)
        action_saveasfile = QAction(QIcon(os.path.join(basedir, "images", "disk.png")), "Save Plot As...", self)
        self.action_zoom = QAction(QIcon(os.path.join(basedir, "images", "magnifier-zoom-in.png")),"Zoom in", self)
        action_help = QAction(QIcon(os.path.join(basedir, "images", "question-frame.png")),"Help", self)
        action_help_plot = QAction(QIcon(os.path.join(basedir, "images", "question-frame.png")),"Why is the plot button not working?", self)
        self.action_hide_entries = QAction(QIcon(os.path.join(basedir, "images", "inactive_eye.png")), "Hide Entries", self)
        self.action_hide_entries.setCheckable(True)
        self.action_hide_entries.setStatusTip("Hide Entries")

        toolbar.addAction(action_home)
        toolbar.addAction(action_openfile)
        toolbar.addAction(action_savefile)
        toolbar.addAction(self.action_zoom)
        toolbar.addAction(self.action_hide_entries)
        toolbar.addSeparator()

        self.addToolBar(toolbar)

        action_openfile.setShortcut(QKeySequence("Ctrl+O"))
        action_savefile.setShortcut(QKeySequence("Ctrl+S"))
        action_saveasfile.setShortcut(QKeySequence("Ctrl+Shift+S"))

        ############
        ### Menu ###
        ############

        menu = self.menuBar()
        menu_file = menu.addMenu("&File")
        menu_file.addAction(action_openfile)
        menu_file.addAction(action_savefile)
        menu_file.addAction(action_saveasfile)
        menu_edit = menu.addMenu("&Edit")
        menu_tool = menu.addMenu("&Tools")
        menu_tool.addAction(self.action_zoom)
        menu_help = menu.addMenu("&Help")
        menu_help.addAction(action_help_plot)
        menu_help.addAction(action_help)

        ###############
        ### Layouts ###
        ###############

        # layout for buttons and checkboxs
        self.main_layout = QHBoxLayout()

        self.parent_label_layout = GridLayout()
        self.parent_label_layout.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        color = QPalette()#dbdbdb
        color.setColor(QPalette.Window,"#e1e1e1")
        self.parent_label_layout.setPalette(color)
        self.parent_label_layout.setAutoFillBackground(True)

        self.labels_and_text_fields_layout = GridLayout()
        self.min_max_xyz_layout = GridLayout()
        self.checkbox_layout = VLayout()
        self.button_layout = GridLayout()

        self.graph_layout = HLayout()


        # left, top, right, bottom
        # align time_widget with rest of widgets
        #  offset of about 14 + any offset from other layouts
        self.labels_and_text_fields_layout.layout.setContentsMargins(10, 0, 0, 0)
        self.min_max_xyz_layout.layout.setContentsMargins(10, 0, 0, 0)
        self.checkbox_layout.layout.setContentsMargins(10, 0, 0, 0)
        self.button_layout.layout.setContentsMargins(10, 0, 0, 0)

        self.labels_and_text_fields_layout.layout.setAlignment(Qt.AlignLeft)

        ###############
        ### Labels ####
        ###############

        self.label_year_day = Label("Year Day: ")
        self.label_start_time = Label("Start Time: ")
        self.label_end_time = Label("End Time: ")
        self.label_station = Label("Station Code:")
        self.label_station.setMaximumWidth(120)
        self.label_min_x = Label("Plot min x: ")
        self.label_max_x = Label("Plot max x: ")
        self.label_min_y = Label("Plot min y: ")
        self.label_max_y = Label("Plot max y: ")
        self.label_min_z = Label("Plot min z: ")
        self.label_max_z = Label("Plot max z: ")

        ################
        ### Spinbox ####
        ################
        self.spinbox_max_x = Spinbox(0, 99999, 10)
        self.spinbox_min_x = Spinbox(0, 99999, 10)
        self.spinbox_max_y = Spinbox(0, 99999, 10)
        self.spinbox_min_y = Spinbox(0, 99999, 10)
        self.spinbox_max_z = Spinbox(0, 99999, 10)
        self.spinbox_min_z = Spinbox(0, 99999, 10)

        ###################
        ### Text Fields ###
        ###################
        self.input_station_code = LineEdit()
        self.input_station_code.setInputMask(">AAAA")
        # Read Only Because User Shouldnt change the station code it should already be set
        # With proper file selection 
        self.input_station_code.setReadOnly(True)
        self.input_year = LineEdit()

        #####################
        ### QTime Widgets ###
        #####################
        self.start_time = MinMaxTime('Min')
        self.end_time = MinMaxTime('Max')
        self.start_time.time_widget.setTime(QTime(00,00,00))
        self.end_time.time_widget.setTime(QTime(23,59,59))
        self.start_time.setMaximumWidth(165)
        self.end_time.setMaximumWidth(165)

        #################
        ### Combo Box ###
        #################

        #### DROP DOWN MENU FOR FILE FORMATS ###########
        self.file_options = (
                        "All",                 # Index 0
                        "IAGA2000 - NW",       # Index 1 
                        "IAGA2002",       # Index 2
                        "Clean File",          # Index 3
                        "Raw 2hz File",        # Index 4
                        "Other -- Not Working")# Index 5

        self.combo_box_files = QComboBox()
        self.combo_box_files.setMaximumWidth(150)
        # Add items to combo box
        self.combo_box_files.addItems(self.file_options)
        self.combo_box_files.setCurrentIndex(0)

        #######################
        ### Checkbox Select ###
        #######################
        
        self.checkbox_x = CheckBox("X Axis")
        self.checkbox_y = CheckBox("Y Axis")
        self.checkbox_z = CheckBox("Z Axis")

        ###############
        ### Buttons ###
        ###############
        self.button_open_file = PushButton("Open...")
        self.button_open_file.set_uncheckable()
        self.button_save = PushButton('Save Plot')
        self.button_save.set_uncheckable()
        self.button_save_as = PushButton('Save Plot As...')
        self.button_save_as.set_uncheckable()
        self.button_plot = PushButton("Plot File")
        self.button_plot.set_uncheckable()
        self.button_zoom = PushButton("Zoom in")
        self.button_clear_plot = PushButton('Clear Plot')
        self.button_clear_plot.set_uncheckable()
        self.button_quit = PushButton('Quit')
        self.button_quit.set_uncheckable()
        self.button_zoom_out = PushButton('Zoom out')
        #####################
        ### Custom Widget ###
        #####################
        self.button_graph_switch = SwitchButtonWidget()
        self.line_sep = LineSeperator()
        self.second_line_sep = LineSeperator()
        
        ########################
        ### Signals / Events ###
        ########################

        action_openfile.triggered.connect(self.toolbar_open)
        action_savefile.triggered.connect(self.save)
        action_saveasfile.triggered.connect(self.save_as)
        action_help_plot.triggered.connect(self.help_plot)
        self.action_zoom.triggered.connect(self.zoom_in_listener)
        action_home.triggered.connect(self.clear_plot)
        self.action_hide_entries.triggered.connect(self.hide_entry_layout)

        self.button_quit.clicked.connect(self.close)
        self.button_open_file.clicked.connect(self.launch_dialog)
        self.button_save.clicked.connect(self.save)
        self.button_save_as.clicked.connect(self.save_as)

        self.button_graph_switch.three_axis_style.clicked.connect(self.update_layout)
        self.button_graph_switch.stacked_axis_style.clicked.connect(self.update_layout)
        self.button_graph_switch.stacked_axis_style.clicked.connect(self.is_plottable)
        self.button_graph_switch.three_axis_style.clicked.connect(self.is_plottable)
        self.button_graph_switch.stacked_axis_style.setChecked(True)
        self.button_plot.clicked.connect(self.plot_graph)
        # set the plot button disabled until all entry checks go through 
        self.button_plot.setDisabled(True)
        self.button_zoom.clicked.connect(self.zoom_in_listener)
        self.button_clear_plot.clicked.connect(self.clear_plot)
        
        self.button_zoom_out.setDisabled(True)
        self.button_zoom_out.clicked.connect(self.zoom_out)
        # Since we have a entry check that checks for the state of
        # what axis is being plotted when we 3 axis display so we 
        # dont enable the plot button until atleast one checkbox is displayed 
        self.checkbox_x.clicked.connect(self.is_plottable)
        self.checkbox_y.clicked.connect(self.is_plottable)
        self.checkbox_z.clicked.connect(self.is_plottable)

        # Every time we update or change a time in we want to check to see if 
        # Start time is greater than end time
        self.start_time.time_widget.timeChanged.connect(self.is_plottable)
        self.end_time.time_widget.timeChanged.connect(self.is_plottable)
        
        ################
        ### Groupbox ###
        ################
        self.group_file_info = QGroupBox()
        self.test = QHBoxLayout()
        self.label = QLabel('asdkas')
        self.test.addWidget(self.label)
        self.group_file_info.setLayout(self.test)
        self.group_graph_values = QGroupBox()
        self.group_buttons = QGroupBox()

        ######################
        ### Adding Widgets ###
        ######################

        self.labels_and_text_fields_layout.add_widget(self.button_open_file, 0, 0)
        self.labels_and_text_fields_layout.add_widget(self.combo_box_files,0, 1)
        self.labels_and_text_fields_layout.add_widget(self.label_station, 1, 0)
        self.labels_and_text_fields_layout.add_widget(self.input_station_code, 1, 1)
        self.labels_and_text_fields_layout.add_widget(self.label_year_day, 2, 0)
        self.labels_and_text_fields_layout.add_widget(self.input_year, 2, 1)
        self.labels_and_text_fields_layout.add_widget(self.label_start_time, 3, 0)
        self.labels_and_text_fields_layout.add_widget(self.start_time, 3, 1)
        self.labels_and_text_fields_layout.add_widget(self.label_end_time, 4, 0)
        self.labels_and_text_fields_layout.add_widget(self.end_time, 4, 1)
        self.labels_and_text_fields_layout.add_widget_stretch(self.button_graph_switch,5,0,1,0)

        self.min_max_xyz_layout.add_widget(self.label_min_x, 0, 0)
        self.min_max_xyz_layout.add_widget(self.spinbox_min_x, 0, 1)
        self.min_max_xyz_layout.add_widget(self.label_max_x, 1, 0)
        self.min_max_xyz_layout.add_widget(self.spinbox_max_x, 1, 1)
        self.min_max_xyz_layout.add_widget(self.label_min_y, 2, 0)
        self.min_max_xyz_layout.add_widget(self.spinbox_min_y, 2, 1)
        self.min_max_xyz_layout.add_widget(self.label_max_y, 3, 0)
        self.min_max_xyz_layout.add_widget(self.spinbox_max_y, 3, 1)
        self.min_max_xyz_layout.add_widget(self.label_min_z, 4, 0)
        self.min_max_xyz_layout.add_widget(self.spinbox_min_z, 4, 1)
        self.min_max_xyz_layout.add_widget(self.label_max_z, 5, 0)
        self.min_max_xyz_layout.add_widget(self.spinbox_max_z, 5, 1)

        self.checkbox_layout.add_widget(self.checkbox_x)
        self.checkbox_layout.add_widget(self.checkbox_y)
        self.checkbox_layout.add_widget(self.checkbox_z)

        self.button_layout.add_widget_stretch(self.button_plot,0,0,1,0)
        self.button_layout.add_widget_stretch(self.button_clear_plot, 1, 0,1,0)
        self.button_layout.add_widget_stretch(self.button_zoom, 2, 0,1,0)
        self.button_layout.add_widget_stretch(self.button_zoom_out,3,0,1,0)
        self.button_layout.add_widget(self.button_save, 4, 0)
        self.button_layout.add_widget(self.button_save_as, 4,1)
        self.button_layout.add_widget_stretch(self.button_quit,5,0,1,0)

        ###############################################
        ### Adding wdigets layouts into main Layout ###
        ###############################################
        self.parent_label_layout.add_widget(self.labels_and_text_fields_layout, 0, 0)
        #self.parent_label_layout.add_widget(self.line_sep,1,0)
        self.parent_label_layout.add_widget(self.checkbox_layout, 3, 0)
        self.parent_label_layout.add_widget(self.min_max_xyz_layout, 3, 0)
        #self.parent_label_layout.add_widget(self.second_line_sep, 4 ,0 )
        self.parent_label_layout.add_widget(self.button_layout, 5, 0)
        ###############################################
        ### Setting Row Stretches for Entry Layout  ###
        ###############################################
        self.main_layout.addWidget(self.parent_label_layout)
        self.main_layout.addWidget(self.mac_label,1)

        ##########################
        ### Set Central Widget ###
        ##########################
        self.update_layout()
        main_widget = QWidget()
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)
        
        ##########################
        ### Instance Variables ###
        ##########################
        self.file_path = None
        self.filename = ""
        self.file_ext = None
        self.launch_dialog_option = None
        ##########################
        self.x_arr = None
        self.y_arr = None
        self.z_arr = None
        self.time_arr = None
        ##########################
        self.figure = None
        self.graph = None
        self.graph_figure_flag = None
        self.start_time_stamp = None
        self.end_time_stamp = None
        self.prev_min_x = 0
        self.prev_max_x = 0
        self.prev_min_y = 0
        self.prev_max_y = 0
        self.prev_min_z = 0
        self.prev_max_z = 0
        self.prev_state_plot_x = 0
        self.prev_state_plot_y = 0
        self.prev_state_plot_z = 0
        self.one_plot_flag = False
        self.stacked_plot_flag = False
        self.readSettings()

    def closeEvent( self, event) :
        """
        When the window is closed it terminates the application.
        Write the current settings to a settings document.
        """
        print(f"closeEvent({event})")
        self.writeSettings()
        
    def readSettings( self) :
        """
        Reads in the data and plot file directories, storing the paths
        as instance variables.
        """
        self.settings = QSettings("Augsburg MACCS", "MACCS Plotter")
        self.data_file_directory = self.settings.value(
                "datadir",
                os.path.join( os.path.expanduser("~"), 'Documents'))
        self.plot_file_directory = self.settings.value(
                "plotdir",
                os.path.join( os.path.expanduser("~"), 'Documents'))
    
    def writeSettings( self) :
        """
        Writes the current data and plot file directory paths out to 
        settings.
        """
        self.settings = QSettings("Augsburg MACCS", "MACCS Plotter")
        self.settings.setValue( "datadir", self.data_file_directory)
        self.settings.setValue( "plotdir", self.plot_file_directory)
    
    def launch_dialog(self):
        '''
        Instance function to select a file filter.
        Filter index assigned to self.launch_dialog_option
        for plotting different file types in plot_graph().
        '''
        #Gets index of current part of drop down box which corresponds to what file we are able to see
        option = self.file_options.index(self.combo_box_files.currentText())
        self.launch_dialog_option = option

        if option == 0:
            file_filter = "Clean/Raw File (*.s2 | *.2hz | *.sec)"
            response = self.get_file_name(file_filter)
            
        elif option == 1:
            self.warning_message_pop_up("File not supported", "IAGA2000 Option Not Available Yet")

        elif option == 2:
            file_filter = "IAGA2002 (*sec)"
            response = self.get_file_name(file_filter)

        elif option == 3:

            self.file_extension = ".s2"
            file_filter = "Clean File (*.s2)"
            response = self.get_file_name(file_filter)
        
        elif option == 4:

            self.file_extension = ".2hz"
            file_filter = "Raw File (*.2hz)"
            response = self.get_file_name(file_filter)

        elif option == 5:

            self.warning_message_pop_up("File not supported", "Option Not Available Yet")

        else:
            print("Got nothing")

    def get_file_name(self, file_filter):
        '''
        User Dialog that prompts user to select a file to open to be read and plotted
        '''
        # Open the dialog in the user's most recently opened data
        # directory, default is the user's 'Documents' directory.
        response = QFileDialog.getOpenFileName(
            parent = self,
            caption = "Select a file",
            dir = self.data_file_directory,
            filter = file_filter
        )
        # if user cancels button, dont want to execute function
        if len(response[0]) == 0:
            # return false if calling from toolbar open
            return False

        filename, filetype_string = response
        self.file_path = filename
        # splitting up the path and selecting the filename
        self.data_file_directory = os.path.dirname( filename)
        filename = os.path.basename( filename)
        self.filename = filename     # name of the file with extension
        self.file_ext = filename.split('.')[-1]
        self.filename_noextension = filename.split('.')[0]
        # setting the station entry box from the filename
        # Ex: CH 20097 .2hz
        self.input_station_code.set_entry(filename[0:2])
        self.input_year.set_entry(filename[2:7])

        # Quick fix to get correct yearday, can probably move somewhere else
        if self.file_ext == "sec":
            yyyy_mmdd = filename[3:11] # Year: (first 4 digits YYYY) and day of year: (last 4 digits MMDD)
            year_value = str(yyyy_mmdd[2:4]) # The last 2 digits of the year YYYY
            month_value = str(yyyy_mmdd[4:6])
            day_value = str(int(yyyy_mmdd[6:8]))
            full_date = year_value + " " + month_value + " " + day_value
            datetime_object = datetime.datetime.strptime(full_date, "%y %m %d")
            # convert yy/mm/dd to DOY format (0 - 365 or 366 if counting leap years)
            day_of_year = datetime_object.strftime('%j')
            year_day_value = yyyy_mmdd[0:2] + day_of_year
            self.input_year.set_entry(year_day_value)

        # Ex for IAGA2002: chb20200406v_10_half_sec.sec
        if self.launch_dialog_option == 2 or self.file_ext == "sec":
            self.input_station_code.set_entry(filename[0:3])
        
        self.reset_axis_entries()
        self.reset_time_entries()
        # return true if calling from toolbar open

        # after we open a file call is plottable to check file inputs yearday and station code
        self.is_plottable()
        # time is set by the rest_time_entries
        # create_datetime_from .... needs timestamp value
        self.start_time_stamp, self.end_time_stamp = self.time_stamp()
        # get file data after we have filepath
        self.get_file_data()

        return True

    def toolbar_open(self):
        '''
        Function that opens a user dialog to open a file using the toolbar icon. 
        '''
        if not self.get_file_name("Raw File (*.2hz);;Clean File (*.s2)"):
            return
        # breaks up into [filename][extension]
        extension = self.filename.split('.')[1]

        if extension == "s2":
            self.combo_box.setCurrentIndex(3)
        
        if extension == "2hz":
            self.combo_box.setCurrentIndex(4)

        self.launch_dialog_option = self.options.index(self.combo_box.currentText())

    def time_stamp(self):
        '''
        Creates a Time stamp for the start time and end time
        '''

        start_time_stamp = datetime.time(hour = self.start_time.get_hour(),
                                        minute = self.start_time.get_minute(),
                                        second = self.start_time.get_second())

        end_time_stamp = datetime.time(hour = self.end_time.get_hour(),
                                            minute = self.end_time.get_minute(),
                                            second = self.end_time.get_second())

        return start_time_stamp, end_time_stamp

    def plot_graph(self):
        
        """
        Once plot graph button is enabled and pressed, we proceed
        to plot the input inside the gui. The type of graph is determined
        based on the state of our graph style button.
        Flow of function is to do some preliminary tests.
        If tests pass, we proceed to save current data as
        previous data. We then update the gui with our new values.
        Final step is to display the graph inside the gui.
        """

        # To prevent memory leak
        if not self.delete_figure_helper():
            return

        # If we got past initial check, means something changed.
        # Either time, axis entries, or checkboxes.
        # If axis entries are the same, that means that the time or axis choice changed.
        # So we reset the axis entries since user didnt change them.
        if gui.entry_check.same_axis_entries(self):
            self.reset_axis_entries()

        self.get_file_data()        

        self.prev_min_x = self.spinbox_min_x.get_entry()
        self.prev_max_x = self.spinbox_max_x.get_entry()
        self.prev_min_y = self.spinbox_min_y.get_entry()
        self.prev_max_y = self.spinbox_max_y.get_entry()
        self.prev_min_z = self.spinbox_min_z.get_entry()
        self.prev_max_z = self.spinbox_max_z.get_entry()

        # normalize the data to display even ticks
        # backward slash is a line continuation, looks ugly, but keep under 85 - 90 chars
        self.prev_min_x, self.prev_max_x, self.prev_min_y, \
        self.prev_max_y, self.prev_min_z, self.prev_max_z = gui.entry_check.axis_entry_checks(
            self.x_arr,
            self.y_arr,
            self.z_arr,
            self.prev_min_x, self.prev_max_x,
            self.prev_min_y, self.prev_max_y,
            self.prev_min_z, self.prev_max_z
        )

        gui.entry_check.set_axis_entrys(
            self, self.prev_min_x, self.prev_max_x, 
            self.prev_min_y, self.prev_max_y, 
            self.prev_min_z, self.prev_max_z)

        # if one plot button is toggled
        # call necessary functions for one plot
        
        if self.button_graph_switch.three_axis_style.isChecked():
            
            # keeping track of whats been plotted already
            self.prev_state_plot_x = self.checkbox_x.isChecked()
            self.prev_state_plot_y = self.checkbox_y.isChecked()
            self.prev_state_plot_z = self.checkbox_z.isChecked()

            self.figure = gui.entry_check.graph_from_plotter_entry_check( 
                                                        self.x_arr, 
                                                        self.y_arr, 
                                                        self.z_arr,
                                                        self.prev_state_plot_x,
                                                        self.prev_state_plot_y,
                                                        self.prev_state_plot_z, 
                                                        self.time_arr,
                                                        self.filename, 
                                                        self.start_time_stamp,
                                                        self.end_time_stamp,
                                                        format=self.file_ext)

            # set one plot flag to true, meaning we have plotted at least once
            self.one_plot_flag = True
            # set stacked flag to false, meaning next time we plot it
            # it will be the first time again
            self.stacked_plot_flag = False
        else:

            self.figure = plot.plot_stacked_graphs.plot_arrays(self.x_arr,
                                                self.y_arr,
                                                self.z_arr,
                                                self.time_arr,
                                                self.filename,
                                                self.start_time_stamp,
                                                self.end_time_stamp,
                                                format=self.file_ext,
                                                in_min_x=self.prev_min_x, 
                                                in_max_x=self.prev_max_x,
                                                in_min_y=self.prev_min_y, 
                                                in_max_y=self.prev_max_y,
                                                in_min_z=self.prev_min_z, 
                                                in_max_z=self.prev_max_z)
            # set one plot flag to false, meaning next time we plot it
            # it will be the first time again
            self.one_plot_flag = False
            # set staacked flag to true, meaninig we have plotted at least once
            self.stacked_plot_flag = True
        
        self.display_figure()

    def get_file_data(self):

        '''
        Gets file data once a file has been chosen inside the gui.
        Data consists of x axis list, y axis list, z axis list,
        time array list, and flag list for clean data files. Flag list
        provides additional information on the data collected and 
        additional measurements taken to clean the data.
        '''
        try:
            # Open file object, read, binary
            file = open(self.file_path, 'rb')
        except:
            self.warning_message_pop_up("File Open Error, couldn't open file")
            return

        '''
        Once future file types are supported, add here.
        Launch Dialog Option assigned when you open a file
        Adding a coupe more else if checks to get datetime lists
        '''
        # get new times
        self.start_time_stamp, self.end_time_stamp = self.time_stamp()

        if self.launch_dialog_option == 3 or self.file_ext == "s2":
            # Doing short names to stay around 80-85 chars per row
            x,y,z,t,f = model.read_clean_to_lists.create_datetime_lists_from_clean(
                                                            file, 
                                                            self.start_time_stamp, 
                                                            self.end_time_stamp)
            # easy to glance over, might be used for new feature?
            flag_arr = f
            #self.flag_arr = f
        elif self.launch_dialog_option == 4 or self.file_ext == "2hz":
            # Doing short names to stay around 80-85 chars per row
            x,y,z,t = model.read_raw_to_lists.create_datetime_lists_from_raw(
                                                            file, 
                                                            self.start_time_stamp,
                                                            self.end_time_stamp)

        elif self.launch_dialog_option == 2 or self.file_ext == "sec":
            x,y,z,t = model.read_IAGA2002_to_lists.create_datetime_lists_from_IAGA2002(
                                                            file,
                                                            self.start_time_stamp,
                                                            self.end_time_stamp)

        # Assign those short names here
        self.x_arr = x
        self.y_arr = y
        self.z_arr = z
        self.time_arr = t
        # close opened file
        file.close()

    def display_figure(self):
        """
        Separate function that will display the graph 
        created from matplotlib. Embeds the graph into a 
        figurecanvas that will become a widget in our layout. 
        This function will help when we load the data 
        but don't want to display the graph immediately.
        """
        # if we hid the entry layout from toolbar
        self.graph_layout.setHidden(False)
        # if we have a figure
        if self.graph_figure_flag:
            # remove plot from window
            self.graph.setParent(None)

        # create new figure
        self.graph = FigureCanvasQTAgg(self.figure)

        # add new figure to layout
        self.graph_layout.add_widget(self.graph)
        self.main_layout.addWidget(self.graph_layout,5)
        self.mac_label.setHidden(True)
        self.graph_figure_flag = True
        self.show()

    def delete_figure(self):
        '''
        Deletes widgets, setting parent to none on widgets
        leaves them hanging in the background process.
        Not garbage collected, so have to delete
        '''

        self.graph.deleteLater()
        plt.close(self.figure)

    def delete_figure_helper(self):
        # If there is a figure already saved
        if self.graph_figure_flag:
            # if this is toggled, do following test
            if self.button_graph_switch.three_axis_style.isChecked():
                # if !(test failed) and we have plotted one_plot already
                # means no new info to plot
                if not gui.entry_check.same_entries_one_toggled(self) and self.one_plot_flag:
                    return False
                else:
                    # delete old figure if we save a new figure
                    # prevent memory leak issues
                    self.delete_figure()
                    return True

            else:  
                # if !(test failed) and we have plotted stacked already
                # means no new info to plot
                if not gui.entry_check.same_entries(self) and self.stacked_plot_flag:
                    return False
                else:
                    self.delete_figure()
                    return True
        
        # if no graph, want to plot something
        return True

    def __call__(self, event):
        '''
        __call__ is the event listener connected to matplotlib.
        Matplotlib will listen for mouse clicks.
        Mouse clicks return xdata (datetime in float 64 format) and ydata
        in original form. This function will listen for two clicks
        and take both the xdata values, cast to datetime.
        From the datetime objects we pull our hour, minute, second values
        to zoom into the plot.
        '''
        # if we haven't graphed anything, cant listen for clicks
        if self.graph is None:
            return

        datetime_object = mdates.num2date(event.xdata)
        hour = int(datetime_object.strftime("%H"))
        minute = int(datetime_object.strftime("%M"))
        second = int(datetime_object.strftime("%S"))

        if self.temp_var == 0:
            self.start_time.time_widget.setTime(QTime(hour, minute, second))
            self.temp_var = self.temp_var + 1

        elif self.temp_var == 1:

            self.end_time.time_widget.setTime(QTime(hour, minute, second))
            self.temp_var = 0
            self.graph.mpl_disconnect(self.cid)
            self.action_zoom.setChecked(False)
            self.button_zoom.set_toggle_status_false()
            # reset axis entries so it can find new min/max values on graph
            self.reset_axis_entries()
            # plot graph
            self.plot_graph()

        self.button_zoom_out.setDisabled(False)
  
    def zoom_in_listener(self):
        '''
        Starts event listening, listens for user clicks on plot.
        Activated after user clicks the zoom icon on the toolbar,
        or the zoom button in the gui. Uses the __call__ function to 
        handle user clicks. After two clicks, event listener is
        disconnected from out matplotlib figure.
        '''
        # Every time we zoom in before we get the new zoom in data 
        # we collect the times we have now and save it if we want to zoom out
        self.s_hour = self.start_time.get_hour()
        self.s_minute = self.start_time.get_minute()
        self.s_second = self.start_time.get_second()

        self.e_hour = self.end_time.get_hour()
        self.e_minute = self.end_time.get_minute()
        self.e_second = self.end_time.get_second()
        self.zoom_out_helper()

        self.cid = self.graph.mpl_connect('button_press_event', self)

    def zoom_out_helper(self):
        """
        Helper function for zoom_out appends time data to a list so that we can hold on to 
        the times we zoomed in from and come walk our way back when we call zoom_out 
        and want to make sure we arent able to press zoom_out when time is at min max
        """
        self.prev_time.append((self.s_hour,self.s_minute ,self.s_second,self.e_hour,self.e_minute ,self.e_second))
        print(self.prev_time)
        if self.start_time.get_time() == (0,0,0) and self.end_time.get_time() == (23,59,59):
                self.button_zoom_out.setDisabled(True)

        
            

    def zoom_out(self):
        '''
        function to zoom out on the graph this allows you to zoom out to the previous state / time the graph was at when you last zoomed in
        when you zoom in multiple times we hold the times of that in a list, and then when zoom out is called 
        we grab the most recent time set the time widget to that time and re plot the graph 
        we then remove that time from the list as its no longer a time we can zoom out to 
        and once you zoom out to min max time the button becomes disabled again
        '''
        self.zoom_s_hour = self.prev_time[len(self.prev_time) - 1][0]
        self.zoom_s_min = self.prev_time[len(self.prev_time) - 1][1]
        self.zoom_s_sec = self.prev_time[len(self.prev_time) - 1][2]
        self.zoom_e_hour = self.prev_time[len(self.prev_time) - 1][3]
        self.zoom_e_min = self.prev_time[len(self.prev_time) - 1][4]
        self.zoom_e_sec = self.prev_time[len(self.prev_time) - 1][5]

        self.start_time.set_own_time(self.zoom_s_hour,self.zoom_s_min,self.zoom_s_sec)
        self.end_time.set_own_time(self.zoom_e_hour,self.zoom_e_min,self.zoom_e_sec)

        self.plot_graph()

        if self.start_time.get_time() == (0,0,0) and self.end_time.get_time() == (23,59,59):
                self.button_zoom_out.setDisabled(True)

        self.prev_time.remove(self.prev_time[len(self.prev_time)-1])

    def save(self):
        """
        Saves the plot as a PDF file.
        Creates the default filename for the plot and saves the pdf
        file in to the user's 'Documents' folder.
        """

        # can set the figure size in the save function with 
        # self.figure.set_size_inches(int, int) and can put an if stmt or something depending on stacked or multi axis
        # but just want to find best way that can have the figure size on the canvas

        if self.button_graph_switch.three_axis_style.isChecked():
            self.figure.set_size_inches(12,4)
        else:
            self.figure.set_size_inches(12,7)
        
        default_filename = create_2hz_plot_file_name(
                self.filename,
                str(self.start_time_stamp),
                str(self.end_time_stamp),
                self.what_graph_style())  # stacked or three-axis
        default_filename = default_filename + ".pdf"
        default_filename = os.path.join( 
                self.plot_file_directory,
                default_filename)                
        self.figure.savefig(default_filename,format="pdf",dpi=1200)
        
    def save_as(self):
        """
        Saves the plot as an image with user chosing either a PDF or PNG option 
        can easily incorperate more file types as needed
        """
       
        default_filename = create_2hz_plot_file_name(
                self.filename,
                str(self.start_time_stamp),
                str(self.end_time_stamp),
                self.what_graph_style())

        # Invokes the OS's save dialog. save_filename is an empty string
        # if the user cancels.
        save_filename, save_type = QFileDialog.getSaveFileName( 
                parent = self, 
                caption = "Save Plot As",
                dir = os.path.join( self.plot_file_directory, default_filename),
                filter = "PDF (*.pdf);;PNG (*.png)",
                selectedFilter = "PDF (*.pdf)")

        #sets the graph size to the proper size 
        if self.button_graph_switch.three_axis_style.isChecked():
            self.figure.set_size_inches(12,4)
        else:
            self.figure.set_size_inches(12,7)

        # If the user has picked a filename, save the plot to that name.
        if len( save_filename) > 0 :
            self.plot_file_directory = os.path.dirname( save_filename)
            if save_type == "PDF (*.pdf)" :
                self.figure.savefig( save_filename, format="pdf", dpi=1200)
            elif save_type == "PNG (*.png)" :
                self.figure.savefig( save_filename, format="png", dpi=1200)
            else :
                print("Error: save plot with unknown file type.")

    def error_message_pop_up(self,title, message):
        # pops up error message box with the title and message inputted
        error_mes = QMessageBox.critical(self, title, message)
        sys.exit(0)

    def warning_message_pop_up(self,title, message):
        # pops up warning message box with the title and message inputted
        warning_mes = QMessageBox.warning(self, title,message)

    def information_message_pop_up(self, title, message):
        
        question_mes = QMessageBox.information(self, title, message)

    def reset_time_entries(self):
        '''
        Helper function that sets min 
        time to 00:00:00 and max time to 23:59:59.
        '''
        self.start_time.set_min_time()
        self.end_time.set_max_time()

    def reset_axis_entries(self):
        '''
        Helper function that sets all min and max 
        values in stacked graph display to 0.
        '''
        self.spinbox_min_x.set_entry(0)
        self.spinbox_max_x.set_entry(0)
        self.spinbox_min_y.set_entry(0)
        self.spinbox_max_y.set_entry(0)
        self.spinbox_min_z.set_entry(0)
        self.spinbox_max_z.set_entry(0)
    
    def clear_plot(self):
        """
        Clears the GUI of any plots and redisplays the MACCS logo.
        Clear plot button also resets all entry values in the widgets. 
        """
        self.graph_layout.setHidden(True)
        self.mac_label.setHidden(False)
        self.one_plot_flag = False
        self.stacked_plot_flag = False
        self.reset_time_entries()
        self.reset_axis_entries()

    def update_layout(self):
        """
        Reactive display handling based on whether Graph Style button is set. 
        Which then determines the type of graph display we have either 
        Three Axis' or Stacked Graph.
        """

        if self.button_graph_switch.three_axis_style.isChecked():
            bool_value = True
            
            self.min_max_xyz_layout.setHidden(bool_value)

            opposite_bool_value = not bool_value
            self.checkbox_x.setHidden( opposite_bool_value)
            self.checkbox_y.setHidden(opposite_bool_value)
            self.checkbox_z.setHidden( opposite_bool_value)

        else:
            bool_value = False

            self.min_max_xyz_layout.setHidden(bool_value)
            opposite_bool_value = not bool_value

            self.checkbox_x.setHidden(opposite_bool_value)
            self.checkbox_y.setHidden(opposite_bool_value)
            self.checkbox_z.setHidden(opposite_bool_value)
        
        self.button_zoom.set_toggle_status_false()
        self.button_zoom.change_text()

    def hide_entry_layout(self):
        ''' 
        Function to hide entry layout from user, allows for fullscreen
        viewing of a graph.
        '''
        # If toolbar eye icon is toggled, hide entry layout
        bool_value = self.action_hide_entries.isChecked()
        
        self.parent_label_layout.setHidden(bool_value)
    
    def help_plot(self):

        self.information_message_pop_up("Help", 
            "Plot button could be disabled for " + 
            "many reasons.\n\n"+
            "1. Have you opened a file yet? If you " +
            "haven't, hit the open button.\n\n" +
            "2. You entered in a start time greater " + 
            "than your end time and vice versa.\n\n" +
            "3. Your min values are greater than " + 
            "your max values and vice versa.\n\n"+
            "4. You have not chosen an axis to plot.")
    
    def is_plottable(self):
        """
        Function that disables or enables the plot button
        based on current input inside the gui. For the button to
        be enabled it must pass our tests. 
        If any of these checks fail, then button will be disabled.
        Station Code is Valid
        Year Day is Valid
        Start Time is less than End Time 
        --- For Stacked Graph Min Max are valid entries and Min is Less than Max
        --- For Three Axis Display Checked States X Y Z 
        """

        checks_met_bool = False
        checks_met_bool = gui.entry_check.checks(self)



        if checks_met_bool:
            self.button_plot.setDisabled(False)
        else:
            self.button_plot.setDisabled(True)

    def what_graph_style(self):
        '''
        Helper function for file naming.py to determine what 
        graph style button is checked for proper naming
        '''
        if self.button_graph_switch.three_axis_style.isChecked():
            return '3axis'
        else:
            return 'stacked'

def main():
    app = QApplication([])
    window = MainWindow()
    color = QPalette()
    color.setColor(QPalette.Window,"#e4e4e4")
    window.setPalette(color)
    window.setAutoFillBackground(True)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()


