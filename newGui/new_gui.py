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
                                QMessageBox,QComboBox
                                )
from PySide6.QtGui import QIcon, QAction, QPixmap, Qt,QKeySequence
from PySide6.QtCore import  QSize, QTime

# Imports from matplotlib
import matplotlib
matplotlib.use('qtagg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

# Imports from python 
import sys
import datetime
import os
import subprocess
import entry_check

#Custom Widget Imports
from custom_widgets import (
    LineEdit, Label, CheckBox, 
    PushButton, Spinbox, Time, 
    GridLayout, HLayout,
    Toolbar, VLayout)

# Imports from subpackages
from custom_time_widget import MinMaxTime
import Model.station_names
import Model.read_clean_to_lists
import Model.read_raw_to_lists
import View.plot_stacked_graphs
import View.plot_three_axis_graphs

MINIMUM_WINDOW_HEIGHT = 1000
MINIMUM_WINDOW_WIDTH = 1400

class MainWindow(QMainWindow):
    """

    Using PySide6 creates GUI that display and visualizes data coming from the Magtometers in the artic from files currently
    in .2hz or .s2 format. 
    This Class holds all GUI related functions and widgets to display the proper information. 

    """
    def __init__(self):

        """ 	
        All the widgets so many o.o
        
        :type self:
        :param self:
    
        :raises:
    
        :rtype:

        Methods
        -----------
        """    
        super().__init__()
        self.setWindowTitle("MACCS Plotting Program")

        self.setFixedHeight(MINIMUM_WINDOW_HEIGHT)
        self.setFixedWidth(MINIMUM_WINDOW_WIDTH)

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
        pixmap = QPixmap('images/maccslogo_nobg.png')
        self.mac_label.setPixmap(pixmap)
        self.mac_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        ###############
        ### Toolbar ###
        ###############

        toolbar = QToolBar("Main Toolbar")    
        toolbar.setIconSize(QSize(16,16))
        action_home = QAction(QIcon("images/home.png"), "Home", self)
        action_openfile = QAction(QIcon("images/folder-open.png"),"Open...       ", self)
        action_savefile = QAction(QIcon("images/disk.png"),"Save File", self)
        action_zoom = QAction(QIcon("images/magnifier-zoom-in.png"),"Zoom in", self)
        action_help = QAction(QIcon("images/question-frame.png"),"Help", self)
        self.action_hide_entries = QAction(QIcon("images/inactive_eye.png"), "Hide Entries", self)
        self.action_hide_entries.setCheckable(True)
        self.action_hide_entries.setStatusTip("Hide Entries")

        toolbar.addAction(action_home)
        toolbar.addAction(action_openfile)
        toolbar.addAction(action_savefile)
        toolbar.addAction(action_zoom)
        toolbar.addAction(self.action_hide_entries)
        toolbar.addSeparator()

        self.addToolBar(toolbar)

        action_openfile.setShortcut(QKeySequence("Ctrl+O"))
        action_savefile.setShortcut(QKeySequence("Ctrl+S"))

        ############
        ### Menu ###
        ############

        menu = self.menuBar()
        menu_file = menu.addMenu("&File")
        menu_file.addAction(action_openfile)
        menu_file.addAction(action_savefile)
        menu_edit = menu.addMenu("&Edit")
        menu_tool = menu.addMenu("&Tools")
        menu_tool.addAction(action_zoom)
        menu_help = menu.addMenu("&Help")
        menu_help.addAction(action_help)

        ###############
        ### Layouts ###
        ###############

        # layout for buttons and checkboxs
        self.main_layout = QHBoxLayout()
        self.parent_label_layout = GridLayout()
        self.labels_and_text_fields_layout = GridLayout()
        self.graph_layout = VLayout()
        self.checkbox_layout = HLayout()
        self.button_layout_top = GridLayout()
        self.button_layout = GridLayout()
        self.min_max_xyz_layout = GridLayout()
        # left, top, right, bottom
        # align time_widget with rest of widgets
        #  offset of about 14 + any offset from other layouts
        self.button_layout_top.setContentsMargins(10, 0, 0, 0)
        self.labels_and_text_fields_layout.layout.setContentsMargins(24, 10, 0, 0)
        self.min_max_xyz_layout.layout.setContentsMargins(10, 0, 0, 0)
        self.checkbox_layout.layout.setContentsMargins(10, 0, 0, 0)
        self.button_layout.layout.setContentsMargins(10, 0, 0, 15)
        ###############
        ### Labels ####
        ###############
        self.label_year_day = Label("Year Day: ")
        self.label_start_time = Label("Start Time: ")
        self.label_end_time = Label("End Time: ")
        self.station_label = Label("Station Code:")

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
        self.start_time.time_widget.setAlignment(Qt.AlignLeft)

        #################
        ### Combo Box ###
        #################

        #### DROP DOWN MENU FOR FILE FORMATS ###########
        self.file_options = (
                        "All",                 # Index 0
                        "IAGA2000 - NW",       # Index 1 
                        "IAGA2002 - NW",       # Index 2
                        "Clean File",          # Index 3
                        "Raw 2hz File",        # Index 4
                        "Other -- Not Working")# Index 5

        self.combo_box_files = QComboBox()
        self.combo_box_files.setMaximumWidth(150)
        # Add items to combo box
        self.combo_box_files.addItems(self.file_options)
        self.combo_box_files.setCurrentIndex(3)

        #######################
        ### Checkbox Select ###
        #######################
        
        self.checkbox_x = CheckBox("X")
        self.checkbox_y = CheckBox("Y")
        self.checkbox_z = CheckBox("Z")

        ###############
        ### Buttons ###
        ###############
        self.button_open_file = PushButton("Open file...")
        self.button_open_file.set_uncheckable()
        self.button_graph_style = PushButton('Graph Style', "Graph Style")
        self.button_save = PushButton('Save')
        self.button_save.set_uncheckable()
        self.button_save_as = PushButton('Save as...')
        self.button_save_as.set_uncheckable()
        self.button_plot = PushButton("Plot File")
        self.button_plot.set_uncheckable()
        self.button_zoom = PushButton("Zoom", "Zoom")
        self.button_clear_plot = PushButton('Clear Plot')
        self.button_clear_plot.set_uncheckable()
        self.button_quit = PushButton('Quit')
        self.button_quit.set_uncheckable()
        self.button_quit.setMinimumWidth(250)

        ########################
        ### Signals / Events ###
        ########################

        action_openfile.triggered.connect(self.toolbar_open)
        action_savefile.triggered.connect(self.save)
        action_zoom.triggered.connect(self.zoom_in_listener)
        action_home.triggered.connect(self.clear_plot)
        self.action_hide_entries.triggered.connect(self.hide_entry_layout)

        self.button_quit.clicked.connect(self.close)
        self.button_open_file.clicked.connect(self.launch_dialog)
        self.button_save.clicked.connect(self.save)
        self.button_save_as.clicked.connect(self.save_as)
        self.button_graph_style.clicked.connect(self.update_layout)
        self.button_graph_style.clicked.connect(self.is_plottable)
        self.button_plot.clicked.connect(self.plot_graph)
        # set the plot button disabled until all entry checks go through 
        self.button_plot.setDisabled(True)
        self.button_zoom.clicked.connect(self.zoom_in_listener)
        self.button_clear_plot.clicked.connect(self.clear_plot)
        
        # Since we have a entry check that checks for the state of what axis is being plotted when we 3 axis display so we dont enable the plot button until atleast one checkbox is displayed 
        self.checkbox_x.clicked.connect(self.is_plottable)
        self.checkbox_y.clicked.connect(self.is_plottable)
        self.checkbox_z.clicked.connect(self.is_plottable)

        ######################
        ### Adding Widgets ###
        ######################
        self.button_layout_top.add_widget_stretch(self.combo_box_files, 0, 0, 1, 2)
        self.button_layout_top.add_widget(self.button_open_file, 1, 0)
        self.button_layout_top.add_widget(self.button_plot, 1, 1)

        self.labels_and_text_fields_layout.add_widget(self.station_label, 0, 0)
        self.labels_and_text_fields_layout.add_widget(self.input_station_code, 0, 1)
        self.labels_and_text_fields_layout.add_widget(self.label_year_day, 1, 0)
        self.labels_and_text_fields_layout.add_widget(self.input_year, 1, 1)
        self.labels_and_text_fields_layout.add_widget(self.label_start_time, 2, 0)
        self.labels_and_text_fields_layout.add_widget(self.start_time, 2, 1)
        self.labels_and_text_fields_layout.add_widget(self.label_end_time, 3, 0)
        self.labels_and_text_fields_layout.add_widget(self.end_time, 3, 1)

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

        self.checkbox_layout.add_widget(self.button_graph_style)
        self.checkbox_layout.add_widget(self.checkbox_x)
        self.checkbox_layout.add_widget(self.checkbox_y)
        self.checkbox_layout.add_widget(self.checkbox_z)

        self.button_layout.add_widget(self.button_clear_plot, 0, 0)
        self.button_layout.add_widget(self.button_zoom, 0, 1)
        self.button_layout.add_widget(self.button_save, 1, 0)
        self.button_layout.add_widget(self.button_save_as, 1, 1)
        self.button_layout.add_widget_stretch(self.button_quit, 2, 0, 1, 2)
        
        ###############################################
        ### Adding wdigets layouts into main Layout ###
        ###############################################
        self.parent_label_layout.add_widget(self.button_layout_top, 0, 0)
        self.parent_label_layout.add_widget(self.labels_and_text_fields_layout, 1, 0)
        self.parent_label_layout.add_widget(self.min_max_xyz_layout, 2, 0)
        self.parent_label_layout.add_widget(self.checkbox_layout, 3, 0)
        self.parent_label_layout.add_widget(self.button_layout, 4, 0)

        ###############################################
        ### Setting Row Stretches for Entry Layout  ###
        ###############################################
        self.main_layout.addWidget(self.parent_label_layout,1)
        self.main_layout.addWidget(self.mac_label, 5)
        
        self.parent_label_layout.set_row_stretch(0, 2)
        # five widgets in one row, station/year/open, plot button
        self.parent_label_layout.set_row_stretch(1, 4)
        # six widgets in one row, x/y/z min max
        self.parent_label_layout.set_row_stretch(2, 6)
        # one widgets in one row, toggle button (x, y, z)
        self.parent_label_layout.set_row_stretch(3, 1)
        # three widgets in one row, buttons
        self.parent_label_layout.set_row_stretch(4, 3)

        ##########################
        ### Set Central Widget ###
        ##########################
        main_widget = QWidget()
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)
        
        ##########################
        ### Instance Variables ###
        ##########################
        self.file_path = None
        self.filename = None
        self.file_extension = None
        self.launch_dialog_option = None
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

            file_filter = "Clean File (*.s2);;Raw File (*.2hz)"
            response = self.get_file_name(file_filter)
            
        elif option == 1:
            self.warning_message_pop_up("File not supported", "IAGA2000 Option Not Available Yet")

        elif option == 2:
            self.warning_message_pop_up("File not supported", "IAGA2002 Option Not Available Yet")

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

    def get_file_name(self, f_filter):
        '''
        Simple user Dialog that prompts user to select a file to open to be read and graphed
        '''

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
            # return false if calling from toolbar open
            return False

        filename, _ = response
        self.file_path = filename
        # splitting up the path and selecting the filename
        filename = filename.split('/')[-1]
        self.filename = filename
        self.filename_noextension = filename.split('.')[0]
        # setting the station entry box from the filename
        # Ex: CH 20097 .2hz
        self.input_station_code.set_entry(filename[0:2])
        self.input_year.set_entry(filename[2:7])
        
        self.reset_axis_entries()
        self.reset_time_entries()
        # return true if calling from toolbar open

        #after we open a file call is plottable to check file inputs yearday and station code
        self.is_plottable()
        return True

    def toolbar_open(self):
        '''
        Function that opens a user dialog to open a file using the toolbar icon 
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
        Once Plot Graph button is pressed we call plot_graph which goes through all entry checks and benchmark testing 
        to make sure all field in the digets and file opened are valid. Once then we check to see which graph style we have
        and then create the lists of data x y z axis and datetime list for the times of the graph 

        """

        #call is plottable even after the button is enable just for more security in making sure all entrys are valid 
        self.is_plottable()

        # If there is a figure already saved
        if self.graph_figure_flag:
            # if graph style button is toggled, either check same entries
            # for one_plot or three_plots
            if self.button_graph_style.is_toggled():
                # if !(test failed) and we have plotted one_plot already
                # means no new info to plot
                if not entry_check.same_entries_one_toggled(self) and self.one_plot_flag:
                    return
                else:
                    # delete old figure if we save a new figure
                    # prevent memory leak issues
                    self.delete_figure()

            else:  
                # if !(test failed) and we have plotted stacked already
                # means no new info to plot
                if not entry_check.same_entries(self) and self.stacked_plot_flag:
                    return
                else:
                    self.delete_figure()

        self.start_time_stamp, self.end_time_stamp = self.time_stamp()
        
        ####################################
        ######### Making the plot ##########
        ####################################
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
        if self.launch_dialog_option == 3:
            # Doing short names to stay around 80-85 chars per row
            x,y,z,t,f = Model.read_clean_to_lists.create_datetime_lists_from_clean(
                                                            file, 
                                                            self.start_time_stamp, 
                                                            self.end_time_stamp, 
                                                            self.filename)
            # easy to glance over, might be used for new feature?
            flag_arr = f

        elif self.launch_dialog_option == 4:
            # Doing short names to stay around 80-85 chars per row
            x,y,z,t = Model.read_raw_to_lists.create_datetime_lists_from_raw(
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
        min_x = self.spinbox_min_x.get_entry()
        max_x = self.spinbox_max_x.get_entry()
        min_y = self.spinbox_min_y.get_entry()
        max_y = self.spinbox_max_y.get_entry()
        min_z = self.spinbox_min_z.get_entry()
        max_z = self.spinbox_max_z.get_entry()

        # normalize the data to display even ticks
        min_x, max_x, min_y, max_y, min_z, max_z = entry_check.axis_entry_checks(
            self.x_arr,
            self.y_arr,
            self.z_arr,
            min_x, max_x,
            min_y, max_y,
            min_z, max_z
        )
        # assign these to self to keep track of what's been plotted
        self.prev_min_x = min_x
        self.prev_max_x = max_x
        self.prev_min_y = min_y
        self.prev_max_y = max_y
        self.prev_min_z = min_z
        self.prev_max_z = max_z

        entry_check.set_axis_entrys(self, min_x, max_x, min_y, max_y, min_z, max_z)
        # if one plot button is toggled
        # call necessary functions for one plot
        
        if self.button_graph_style.is_toggled():
            
            # keeping track of whats been plotted already
            self.prev_state_plot_x = self.checkbox_x.isChecked()
            self.prev_state_plot_y = self.checkbox_y.isChecked()
            self.prev_state_plot_z = self.checkbox_z.isChecked()

            self.figure = entry_check.graph_from_plotter_entry_check( 
                                                        self.x_arr, 
                                                        self.y_arr, 
                                                        self.z_arr,
                                                        self.prev_state_plot_x,
                                                        self.prev_state_plot_y,
                                                        self.prev_state_plot_z, 
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

            self.figure = View.plot_stacked_graphs.plot_arrays(self.x_arr,
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

    def display_figure(self):
        """
        Seperate Function that will display the graph created from matplotlib 
        embedding the graph into a figurecanvas that will become a widget in our layout 
        this function will help when we load the data but dont display any of it yet
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
        self.main_layout.addWidget(self.graph_layout, 5)
        self.mac_label.setHidden(True)
        self.graph_figure_flag = True
        self.show()

    def delete_figure(self):
        '''Deletes widgets, setting parent to none on widgets
        leaves them hanging in the background process.
        Not garbage collected, so have to delete'''
        self.graph.deleteLater()
        plt.close(self.figure)

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
            self.button_zoom.set_toggle_status_false()
            # reset axis entries so it can find new min/max values on graph
            self.reset_axis_entries()
            self.graph.mpl_disconnect(self.cid)
            self.temp_var = 0
            self.plot_graph()

    def zoom_in_listener(self):
        '''
        Starts event listening, listens for user clicks on plot.
        Activated after user clicks the zoom icon on the toolbar,
        or the zoom button in the gui. Uses the __call__ function to 
        handle user clicks. After two clicks, event listener is
        disconnected from out matplotlib figure.
        '''
        self.cid = self.graph.mpl_connect('button_press_event', self)

    def save(self):
        """
            Saves the Graph as a PDF Image

            file_type is a QMessageBox that pops up once the Save as QButton is pressed 
        """

        question_box = QMessageBox(self)

        save_image_button = question_box.addButton(str('Save Image'), QMessageBox.ActionRole)
        cancel_button = question_box.addButton(str('Cancel'),QMessageBox.ActionRole)
        window_title_text = question_box.setWindowTitle("Save Image")
        message_text = question_box.setText("Would you like to save this image as a PDF?")
        start = question_box.exec()

        if question_box.clickedButton() == save_image_button:
            plt.savefig(self.file_name + ".pdf")
            subprocess.Popen(self.file_name + '.pdf', shell=True)
        elif question_box.clickedButton() == cancel_button:
            question_box.close()

    def save_as(self):
         
        """
            Saves the Graph as an image with user chosing either a PDF or PNG option 
            can easily incorperate more files as needed 

            file_type is a QMessageBox that pops up once the Save as QButton is pressed 
        """
        #def information (parent, title, text, button0[, button1=QMessageBox.StandardButton.NoButton])

        file_type = QMessageBox(self)

        pdf_button = file_type.addButton(str("PDF"), QMessageBox.ActionRole)
        png_button = file_type.addButton(str('PNG'), QMessageBox.ActionRole)
        cancel_button = file_type.addButton(str('Cancel'), QMessageBox.ActionRole)

        window_title_text = file_type.setWindowTitle("Save as...")
        message_text = file_type.setText("Select would image type you would like to save as... \n PDF or PNG")

        start = file_type.exec()

        if file_type.clickedButton() == pdf_button:
            plt.savefig(self.file_name + ".pdf")
            subprocess.Popen(self.file_name + '.pdf', shell=True)
        elif file_type.clickedButton() == png_button:
            plt.savefig(self.file_name + ".png")
            subprocess.Popen(self.file_name + '.png', shell=True)
        elif file_type.clickedButton() == cancel_button:
            file_type.close()

    def error_message_pop_up(self,title, message):
        # pops up error message box with the title and message inputted
        error_mes = QMessageBox.critical(self, title, message)
        sys.exit(0)

    def warning_message_pop_up(self,title, message):
        # pops up warning message box with the title and message inputted
        warning_mes = QMessageBox.warning(self, title,message)

    def reset_time_entries(self):
        '''
        Helper function that sets min time to 00 00 00 and max time to 23 59 59
        '''
        self.start_time.set_min_time()
        self.end_time.set_max_time()

    def reset_axis_entries(self):
        '''
        Ez helper Function that sets all min and max values in stacked graph display to 0
        '''
        self.spinbox_min_x.set_entry(0)
        self.spinbox_max_x.set_entry(0)
        self.spinbox_min_y.set_entry(0)
        self.spinbox_max_y.set_entry(0)
        self.spinbox_min_z.set_entry(0)
        self.spinbox_max_z.set_entry(0)
    
    def clear_plot(self):
        """
        Clears the GUI of any of all plots that would be displayed and redispalys the MACCS Logo
        clear plot button also resets all entry values in the widgets 
        """
        self.graph_layout.setHidden(True)
        self.mac_label.setHidden(False)
        self.one_plot_flag = False
        self.stacked_plot_flag = False
        self.reset_time_entries()
        self.reset_axis_entries()

    def update_layout(self):
        """
        Reactive display handling based on wether Graph Style button is Clicked on Unclicked 
        Which Then determines the type of graph display we have either Three Axis' or Stacked Graph
        """
        bool_value = self.button_graph_style.is_toggled()

        self.button_zoom.set_toggle_status_false()
        self.button_zoom.change_text()
        self.min_max_xyz_layout.setHidden(bool_value)

        if bool_value:
            self.parent_label_layout.set_row_stretch(0, 4)
            self.parent_label_layout.set_row_stretch(1, 12)
            self.parent_label_layout.set_row_stretch(2, 0)
            self.parent_label_layout.set_row_stretch(3, 1)
            self.parent_label_layout.set_row_stretch(4, 8)
        else:
            self.parent_label_layout.set_row_stretch(0, 2)
            self.parent_label_layout.set_row_stretch(1, 4)
            self.parent_label_layout.set_row_stretch(2, 6)
            self.parent_label_layout.set_row_stretch(3, 1)
            self.parent_label_layout.set_row_stretch(4, 3)

    def hide_entry_layout(self):
        ''' 
        Function to hide entry layout from user, allows for fullscreen
        viewing of a graph.
        '''
        # If toolbar eye icon is toggled, hide entry layout
        bool_value = self.action_hide_entries.isChecked()
        
        self.parent_label_layout.setHidden(bool_value)
    
    def is_plottable(self):
        """
        full function that will encompass all entry checks that we have, and if we have all 
        entry checks pass the user will be able to press the plot button and plot the graph, 
        if a check fails or not all checks are met yet the plot graph button will still be greyed out
        """

        # Proper Entry Checks include 
        '''
        Station Code is Valid
        Year Day is Valid
        Start Time is less than End Time 
        --- For Stacked Graph Min Max are valid entries and Min is Less than Max
        --- For Three Axis Display Checked States X Y Z 
        '''
        checks_met_bool = False
        checks_met_bool = entry_check.checks(self)

        '''
        This if stmt casuses more issues and delete_figure() when opening the same file or a new file 
        it fully deleletes the figure canvas and isnt reestablished 
        '''
        if checks_met_bool:
            self.button_plot.setDisabled(False)
        else:
            self.button_plot.setDisabled(True)

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()


