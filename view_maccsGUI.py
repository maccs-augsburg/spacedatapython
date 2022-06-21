#Gui implemented with classes
#Annabelle

#Refactored into PySide6 GUI 
# By Chris Hance may 2022

#Import from PySide6 // QT


from PySide6.QtWidgets import (QMainWindow, QApplication, 
                                QLabel, QLineEdit, 
                                QWidget, QHBoxLayout, 
                                QGridLayout,QPushButton, 
                                QToolBar,QVBoxLayout,
                                QFileDialog, QRadioButton,
                                QCheckBox,QMessageBox, 
                                QButtonGroup, QSizePolicy
                                )
from PySide6.QtGui import QIcon, QAction, QPixmap, Qt, QPalette
from PySide6.QtCore import  QSize, QTime

# path for file open 
from pathlib import Path

#imports from python 
import sys
import datetime

#Imports from matplotlib
import matplotlib
from matplotlib.axes import Axes
from numpy import minimum
matplotlib.use('qtagg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from mpl_interactions import ioff, panhandler, zoom_factory


import subprocess

#imports from other python files
from file_naming import create_time_interval_string_hms
import read_raw_to_lists
import read_clean_to_lists
from entry_checks import ( start_hour_entry_check, start_minute_entry_check, start_second_entry_check,
                            end_hour_entry_check, end_minute_entry_check, end_second_entry_check,
                            graph_from_plotter_entry_check, file_format_entry_check)
import plot_stacked_graphs
from custom_time_widget import MinMaxTime

class MainWindow(QMainWindow):
    """
    Using PySide6 creates GUI that display and visualizes data coming from the Magtometers in the artic from files currently
    in .2hz or .s2 format. 
    This Class holds all GUI related functions and widgets to display the proper information. 

    ''' 

    Methods
    -----------
    open_file
        Creates a dialog for the user to select a file in .2hz or .s2 format and once selected 
        sets proper widgets input to match the data read from file
    get_graph_entries

    choose_graph_style

    plot_three_axis

    __call__

    zoom_in_listener

    plot_stacked_axis

    clear_plots

    custom_toobar

    radio_file_check

    error_message_pop_up

    warning_message_pop_up

    convert_hours_list_to_datetime_object

    save

    save_as

    set_stacked_options_hidden

    set_stacked_options_visable

    set_three_axis_options_hidden

    set_three_axis_options_visable
    """
    def __init__(self):

        """ 	
        All the widgets so many o.o
        
        :type self:
        :param self:
    
        :raises:
    
        :rtype:
        """    
        super().__init__()
        self.setWindowTitle("MACCS Plotting Program")

        self.setGeometry(60,60, 1000,800)
        self.selection_file_value = ''

        ###############
        ### Toolbar ###
        ###############

        toolbar = QToolBar("Main Toolbar")    
        toolbar.setIconSize(QSize(16,16))
        action_openfile = QAction(QIcon("../spacedatapython/images/folder-open.png"),"Open File", self)
        action_savefile = QAction(QIcon("../spacedatapython/images/disk.png"),"Save File", self)
        action_zoom = QAction(QIcon("../spacedatapython/images/magnifier-zoom-in.png"),"Zoom in", self)
        action_help = QAction(QIcon("../spacedatapython/images/question-frame.png"),"Help", self)

        toolbar.addAction(action_openfile)
        toolbar.addAction(action_savefile)
        toolbar.addAction(action_zoom)
        toolbar.addSeparator()

        self.addToolBar(toolbar)
    
        ###########################
        ### Place Holder Values ###
        ###########################

        self.zoom_flag = False
        self.temp_var = 0
        self.left_lim = 0.0
        self.right_lim = 0.0

        ############
        ### Menu ###
        ############

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(action_openfile)
        file_menu.addAction(action_savefile)

        edit_menu = menu.addMenu("&Edit")

        tool_menu = menu.addMenu("&Tools")
        tool_menu.addAction(action_zoom)

        help_menu = menu.addMenu("&Help")
        help_menu.addAction(action_help)

        ###############
        ### Labels ####
        ###############

        self.station_code = QLabel("Station Code: ")
        self.year_day = QLabel("Year Day: ")
        
        self.label_start_time = QLabel("Start Time: ")
        self.label_end_time = QLabel("End Time: ")

        self.plot_xyz_label = QLabel("Plot X, Y, or Z: ")
        self.format_file_text = QLabel("Format of File to Open: ")

        self.maccs_logo = QLabel()
        self.maccs_logo.setPixmap(QPixmap("maccslogo_870.jpeg"))
        self.maccs_logo.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.test = QLabel("Welcome to the Magnetometer Array for Cusp and Cleft Studies")

        self.label_start_time.setMaximumWidth(60)
        self.year_day.setMaximumWidth(60)
        self.plot_xyz_label.setFixedHeight(20)
        self.format_file_text.setFixedHeight(20)

        self.min_x = QLabel("Plot min x: ")
        self.max_x = QLabel("Plot max x: ")

        self.min_y = QLabel("Plot min y: ")
        self.max_y = QLabel("Plot max y: ")

        self.min_z = QLabel("Plot min z: ")
        self.max_z = QLabel("Plot max z: ")

        ###################
        ### Text Fields ###
        ###################

        self.input_station_code = QLineEdit()
        self.input_year = QLineEdit()

        self.input_min_x = QLineEdit("0")
        self.input_max_x = QLineEdit("0")
        self.input_min_y = QLineEdit("0")
        self.input_max_y = QLineEdit("0")
        self.input_min_z = QLineEdit("0")
        self.input_max_z = QLineEdit("0")

        self.input_station_code.setMaximumWidth(35)
        self.input_year.setMaximumWidth(35)
        self.input_min_x.setMaximumWidth(35)
        self.input_max_x.setMaximumWidth(35)
        self.input_min_y.setMaximumWidth(35)
        self.input_max_y.setMaximumWidth(35)
        self.input_min_z.setMaximumWidth(35)
        self.input_max_z.setMaximumWidth(35)

        #####################
        ### QTime Widgets ###
        #####################
        self.custom_start_time = MinMaxTime('Min')
        self.custom_end_time = MinMaxTime('Max')
        self.custom_start_time.time_widget.setTime(QTime(00,00,00))
        self.custom_end_time.time_widget.setTime(QTime(23,59,59))

        self.custom_start_time.setMaximumWidth(165)
        self.custom_end_time.setMaximumWidth(165)
        self.custom_start_time.time_widget.setAlignment(Qt.AlignLeft)

        #######################
        ### Checkbox Select ###
        #######################
        self.graph_display_button_group = QButtonGroup()
        self.graph_display_button_group.setExclusive(False)

        self.checkbox_plotx = QCheckBox("X Plot", self)
        self.checkbox_ploty = QCheckBox("Y Plot", self)
        self.checkbox_plotz = QCheckBox("Z Plot", self)

        self.graph_display_button_group.addButton(self.checkbox_plotx)
        self.graph_display_button_group.setId(self.checkbox_plotx,0)
        self.graph_display_button_group.addButton(self.checkbox_ploty)
        self.graph_display_button_group.setId(self.checkbox_ploty,1)
        self.graph_display_button_group.addButton(self.checkbox_plotz)
        self.graph_display_button_group.setId(self.checkbox_plotz,2)

        #######################
        ### Radio Selectors ###
        #######################
        self.radio_iaga2000 = QRadioButton("IAGA2000 - NW")
        self.radio_iaga2002 = QRadioButton("IAGA2002 - NW")
        self.radio_clean_file = QRadioButton("Clean file")
        self.radio_raw_file = QRadioButton("Raw 2hz file")
        self.radio_other = QRadioButton("Other - Not working")

        ###############
        ### Layouts ###
        ###############

        self.main_layout = QHBoxLayout()
        self.label_and_entry_layout = QGridLayout()
        self.graph_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(5,0,0,0)
        self.label_and_entry_layout.setVerticalSpacing(-10)
        
        ###############
        ### Buttons ###
        ###############
         
        self.button_open_file = QPushButton("Open file")
        self.button_open_file.setFixedWidth(75)
        self.button_graph_style = QPushButton('Graph Style')
        self.button_graph_style.setFixedWidth(75)
        self.button_quit = QPushButton('Quit')
        self.button_quit.setFixedWidth(75)
        self.button_save = QPushButton('Save')
        self.button_save.setFixedWidth(75)
        self.button_save_as = QPushButton('Save as...')
        self.button_save_as.setFixedWidth(75)
        self.button_clear_plot = QPushButton('Clear Plot')
        self.button_clear_plot.setFixedWidth(75)
        self.button_plot_three_axis = QPushButton("Plot Graph")
        self.button_plot_three_axis.setFixedWidth(75)
        self.button_plot_stacked_graph = QPushButton("Plot Graph")
        self.button_plot_stacked_graph.setFixedWidth(75)

        ########################
        ### Signals / Events ###
        ########################

        action_openfile.triggered.connect(self.open_file)
        action_savefile.triggered.connect(self.save)
        action_zoom.triggered.connect(self.zoom_in_listener)

        self.button_open_file.clicked.connect(self.open_file)
        self.button_quit.clicked.connect(self.close)
        self.button_graph_style.clicked.connect(self.choose_graph_style)
        self.button_save.clicked.connect(self.save)
        self.button_save_as.clicked.connect(self.save_as)
        self.button_clear_plot.clicked.connect(self.clear_plots)
        self.button_plot_three_axis.clicked.connect(self.plot_three_axis)
        self.button_plot_stacked_graph.clicked.connect(self.plot_stacked_axis)

        ######################
        ### Adding Widgets ###
        ######################

        self.label_and_entry_layout.addWidget(self.station_code,0,0)
        self.label_and_entry_layout.addWidget(self.year_day, 1,0)

        self.label_and_entry_layout.addWidget(self.custom_start_time,2, 1)
        self.label_and_entry_layout.addWidget(self.custom_end_time,3, 1)


        self.label_and_entry_layout.addWidget(self.label_start_time, 2,0)
        self.label_and_entry_layout.addWidget(self.label_end_time, 3,0)

        self.label_and_entry_layout.addWidget(self.input_station_code,0, 1)
        self.label_and_entry_layout.addWidget(self.input_year, 1, 1)

        self.label_and_entry_layout.addWidget(self.plot_xyz_label, 8, 0)
       
        self.label_and_entry_layout.addWidget(self.input_max_x, 9,1)
        self.label_and_entry_layout.addWidget(self.input_min_x, 10,1)
        self.label_and_entry_layout.addWidget(self.input_max_y, 11,1)
        self.label_and_entry_layout.addWidget(self.input_min_y, 12,1)
        self.label_and_entry_layout.addWidget(self.input_max_z, 13,1)
        self.label_and_entry_layout.addWidget(self.input_min_z, 14,1)

        self.label_and_entry_layout.addWidget(self.max_x, 9,0)
        self.label_and_entry_layout.addWidget(self.min_x, 10,0)
        self.label_and_entry_layout.addWidget(self.max_y, 11,0)
        self.label_and_entry_layout.addWidget(self.min_y, 12,0)
        self.label_and_entry_layout.addWidget(self.max_z, 13,0)
        self.label_and_entry_layout.addWidget(self.min_z, 14,0)
        
        self.label_and_entry_layout.addWidget(self.graph_display_button_group.button(0), 9, 0)
        self.label_and_entry_layout.addWidget(self.graph_display_button_group.button(1), 10, 0)
        self.label_and_entry_layout.addWidget(self.graph_display_button_group.button(2), 11, 0)
        self.label_and_entry_layout.addWidget(self.button_plot_three_axis, 15 ,0)
        self.label_and_entry_layout.addWidget(self.button_plot_stacked_graph,15 ,0)

        self.label_and_entry_layout.addWidget(self.format_file_text, 16, 0)

        self.label_and_entry_layout.addWidget(self.radio_iaga2000, 17,0)
        self.label_and_entry_layout.addWidget(self.radio_iaga2002, 18,0)
        self.label_and_entry_layout.addWidget(self.radio_clean_file, 19,0)
        self.label_and_entry_layout.addWidget(self.radio_raw_file, 20, 0)
        self.label_and_entry_layout.addWidget(self.radio_other, 21, 0)

        self.label_and_entry_layout.addWidget(self.button_graph_style, 22, 0)
        self.label_and_entry_layout.addWidget(self.button_clear_plot, 22, 1)
        self.label_and_entry_layout.addWidget(self.button_save_as, 23, 0)
        self.label_and_entry_layout.addWidget(self.button_save, 23, 1)
        self.label_and_entry_layout.addWidget(self.button_open_file, 24, 0)
        self.label_and_entry_layout.addWidget(self.button_quit, 24, 1)

        self.button_plot_three_axis.setHidden(True)
        self.button_plot_stacked_graph.setHidden(True)
        self.set_stacked_options_hidden()
        self.set_three_axis_options_hidden()

        ########################################
        ### Adding all layouts into the main ###
        ########################################

        self.main_layout.addLayout(self.label_and_entry_layout)
        self.main_layout.addLayout(self.graph_layout)
        self.main_layout.addWidget(self.maccs_logo)
    
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.main_widget.setMinimumSize(1100,800)
        self.setCentralWidget(self.main_widget)

    def open_file(self):
    
            """
            Opens a open file dialog box where the user picks the appropriate file type. Once that is
            selected, it inputs the data into the boxes automatically based on the filename.
            """
            # listing the types of file types we currently support
            filetypes = [
                ('Raw files', '*.2hz'),
                ('Clean files', '*.s2')
            ]

            '''
            CAUTION !!!
            self.file_name[x : x] and file_name 
            can cause issues currently if file names are a little off than what I (have) or currently if 
            we use different files
            '''

            # # opening the dialog box
            home_dir = str(Path.home())
            file_name = QFileDialog.getOpenFileName(self, 'Open File', home_dir, '(*.2hz *.s2)')
            self.abs_file_name = file_name[0]
            file_name = str(file_name)

            # splitting up the path and selecting the filename
            self.file_name = file_name.split(',')[0]

            self.file_name = file_name.split('/')[-1]

            # # setting the station code from the filename
            self.input_station_code.setText(str(self.file_name[0:2]))

            # # setting the yearday from the filename
            self.input_year.setText(str(self.file_name[2:7]))
            # resetting the start times and end times

            #temp var
            file_type = ''

            # raw file selection branch
            if (self.file_name[7:11] == '.2hz'):
                self.selection_file_value = '4'
                file_type = '.2hz'
                
            # clean file selection branch
            elif (self.file_name[7:10] == '.s2'):
                self.selection_file_value = '5'
                file_type = '.s2'

            # else
            else:
                print('Option not available yet :(')
            # checks the radio button with the proper file type
            self.radio_file_check(file_type)

    def get_graph_entries(self):
        '''
        Obtains the values the Widgets on the GUI 
        Station name, Year Day, and the time from QTime
        All values get checked for validlity then we create the time stamps and file name to pass on
        '''
        # Getting entries from the user / the file
        #Station code and year
        station_name_value = self.input_station_code.text()
        year_day_value = self.input_year.text()
        
        # Start hour, minute, and second entries
        start_hour_value = start_hour_entry_check(self, self.custom_start_time.time_widget.sectionText(self.custom_start_time.time_widget.sectionAt(0)))
        start_minute_value = start_minute_entry_check(self, self.custom_start_time.time_widget.sectionText(self.custom_start_time.time_widget.sectionAt(1)))
        start_second_value = start_second_entry_check( self, self.custom_start_time.time_widget.sectionText(self.custom_start_time.time_widget.sectionAt(2)))

        # End hour, minute and second entries

        end_hour_value = end_hour_entry_check( self, self.custom_end_time.time_widget.sectionText(self.custom_end_time.time_widget.sectionAt(0)))
        end_minute_value = end_minute_entry_check(self, self.custom_end_time.time_widget.sectionText(self.custom_end_time.time_widget.sectionAt(1)))
        end_second_value = end_second_entry_check( self, self.custom_end_time.time_widget.sectionText(self.custom_end_time.time_widget.sectionAt(2)))

        # creating the start time stamp
        self.start_time_stamp = datetime.time(hour=start_hour_value, minute=start_minute_value, second=start_second_value)
        # creating the end time stamp
        self.end_time_stamp = datetime.time(hour=end_hour_value, minute=end_minute_value, second=end_second_value)
        #file_value = self.selection_file_value
        file_ending_value = file_format_entry_check(self,self.selection_file_value)
       
        # Making the Plot
        self.file_name_full = station_name_value + year_day_value + file_ending_value
        time_interval_string = create_time_interval_string_hms(start_hour_value, start_minute_value, start_second_value, end_hour_value, end_minute_value, end_second_value)
        self.file_name = station_name_value + year_day_value + time_interval_string

    def choose_graph_style(self):
        '''
        Message Box Pops up for user to select what kind of graph display they want
        the stacked version with all three axis' on top of each other OR
        three axis display where the user can choose 1-3 axis to view on the same graph show the derivatives of the axis 
        '''
        
        # Message box that asks what type of graph verison you want
        self.which_graph_type_box = QMessageBox(self)

        self.three_axis_option = self.which_graph_type_box.addButton(str('Three Axis'), QMessageBox.ActionRole)
        self.stacked_display = self.which_graph_type_box.addButton(str('Stacked Display'),QMessageBox.ActionRole)
        self.cancel_button = self.which_graph_type_box.addButton(str('Cancel'),QMessageBox.ActionRole)
        self.window_title_text = self.which_graph_type_box.setWindowTitle("Graph type")
        self.message_text = self.which_graph_type_box.setText("Choose what type of graphing layout you would like \n Three Axis Option or Stacked Display")
        self.start = self.which_graph_type_box.exec()

        if self.which_graph_type_box.clickedButton() == self.three_axis_option:
            self.clear_plots()
            self.set_stacked_options_hidden()
            self.set_three_axis_options_visable()
            self.button_plot_three_axis.setHidden(False)
            self.button_plot_stacked_graph.setHidden(True)
            
        elif self.which_graph_type_box.clickedButton() == self.stacked_display:
            self.clear_plots()
            self.set_stacked_options_visable()
            self.set_three_axis_options_hidden()
            self.button_plot_stacked_graph.setHidden(False)
            self.button_plot_three_axis.setHidden(True)

        elif self.which_graph_type_box.clickedButton() == self.cancel_button:
            self.which_graph_type_box.close()

    def plot_three_axis(self):
        '''
        Function to plot the three axis display using checkboxs to determine what axis are dispalyed
        then values are checked for validility and then put into a figure via matplotlib
        and then set into a PySide Canvas and embeded into our MainWindow
        '''
        #calls the function that will always check the validility of the values in each text field and box prior to graphing 
        # if anything is wrong incorrect etc we will display a warning / error 
        self.get_graph_entries()

        # Setting default values of the checkbox values 
        plot_x_axis = 0         
        plot_y_axis = 0
        plot_z_axis = 0

        #if 0 we dont plot that axis if checked its value is 1 and it is plotted 
        if (self.checkbox_plotx.isChecked()):
            plot_x_axis = 1        
        if (self.checkbox_ploty.isChecked()):
            plot_y_axis = 1        
        if (self.checkbox_plotz.isChecked()):
            plot_z_axis = 1

        # trying to open the file
        try:
            file = open(self.abs_file_name, 'rb')
        except:
            # popping up an error if we can't open the file
            self.warning_message_pop_up("File open error", "Couldn't find and open your file \nPlease make sure you select proper file \n Try again please")

        #Creating the arrays
        if (self.selection_file_value == '4'):
            #
            xArr, yArr, zArr, timeArr = read_raw_to_lists.create_datetime_lists_from_raw(file, self.start_time_stamp,self.end_time_stamp, self.file_name)
            # plotting the arrays
            self.graph = graph_from_plotter_entry_check(self,plot_x_axis,
                                                                plot_y_axis, 
                                                                plot_z_axis, 
                                                                xArr, 
                                                                yArr, 
                                                                zArr,
                                                                timeArr, 
                                                                self.file_name, self.start_time_stamp, self.end_time_stamp, '4',self.zoom_flag, self.left_lim, self.right_lim)

        elif (self.selection_file_value == '5'):
            xArr, yArr, zArr, timeArr, flag_arr = read_clean_to_lists.create_datetime_lists_from_clean(file, self.start_time_stamp,self.end_time_stamp, self.file_name)
            # plotting the arrays
            self.graph = graph_from_plotter_entry_check(self,plot_x_axis,
                                                                plot_y_axis, 
                                                                plot_z_axis, 
                                                                xArr, 
                                                                yArr, 
                                                                zArr,
                                                                timeArr, 
                                                                self.file_name, self.start_time_stamp, self.end_time_stamp, '5',self.zoom_flag, self.left_lim, self.right_lim)
        # Clears all widgets in the graph_layout, and allows for only one graph to be displayed at a time
        self.clear_plots()

        # Putting the arrays into the gui
        self.graph = FigureCanvasQTAgg(self.graph)
        self.toolbar = NavigationToolbar2QT(self.graph, self)
        self.maccs_logo.setHidden(True)
        self.graph_layout.addWidget(self.toolbar) 
        self.graph_layout.addWidget(self.graph)

    def __call__(self,event):
        '''
        __call__ is the event listener connected to matplotlib 
        it will listen for mouse clicks and record the xdata of the first and second click passing them to 
        varibles that we will then set our new xlims too (left and right) 
        after left and right x lims are stored we call the proper graph 
        '''

        if self.temp_var == 0:
            self.left_lim = event.xdata
            #print(self.left_lim, ' in func')
        elif self.temp_var == 1:
            self.right_lim = event.xdata
            self.graph.mpl_disconnect(self.cid)
            self.zoom_flag = True
            print('zoom flag in zoom in func: ', self.zoom_flag)
            self.plot_three_axis()
        #print(self.temp_var) 
        self.temp_var = self.temp_var + 1

        # xdata = event.xdata
        # print('X Data: ', xdata)
        # print('X data % 1 : ', xdata % 1)
        # xdata = xdata % 1
        # print('X data % 1 * 100000 : ', xdata * 1000000)
        # xdata = xdata * 1000000
        # print('xdata as float: ', float(xdata) )
        # print('xdata as datetime.datetime:  ', datetime.datetime.fromtimestamp(xdata))
        # print('Type xdata: ', type(xdata))
        # print()

    def zoom_in_listener(self):
        '''
        Starts event listening that listens for clicks after clicking the zoom icon
        and uses the __call__ function to handle to clicks 
        and we get two clicks we call other function in __call__ after zoom_in_listner is called after button events happened
        the values are reset so we can continune more zoomin 
        '''
        self.cid = self.graph.mpl_connect('button_press_event', self)
        if self.temp_var > 1:
            self.temp_var = 0
            self.zoom_flag = False

    def plot_stacked_axis(self):
        '''
        Function to plot all three axis stacked up and the ability to change the min and max scale of each 
        axis (Y axis) and values are checked for validility and then put into a figure via matplotlib
        and then set into a PySide Canvas and embeded into our MainWindow
        '''
        self.get_graph_entries()
        plot_min_value_x = int(self.input_min_x.text())
        plot_max_value_x = int(self.input_max_x.text())
        plot_min_value_y = int(self.input_min_y.text())
        plot_max_value_y = int(self.input_max_y.text())
        plot_min_value_z = int(self.input_min_z.text())
        plot_max_value_z = int(self.input_max_z.text())
        
        try:
            file = open(self.abs_file_name, 'rb')
        except:
            # popping up an error if we can't open the file
            self.warning_message_pop_up("File open error", "couldn't find and open your file")

        # Creating the arrays
        if (self.selection_file_value == '4'):
            xArr, yArr, zArr, timeArr = read_raw_to_lists.create_datetime_lists_from_raw(file, self.start_time_stamp,
                                                                                        self.end_time_stamp, self.file_name)
            # plotting the arrays
            self.graph = plot_stacked_graphs.plot_arrays(xArr, yArr, zArr, timeArr, self.file_name, self.start_time_stamp, self.end_time_stamp,
                                                in_min_x=plot_min_value_x, in_max_x=plot_max_value_x,
                                                in_min_y=plot_min_value_y, in_max_y=plot_max_value_y,
                                                in_min_z=plot_min_value_z, in_max_z=plot_max_value_z)
        elif (self.selection_file_value == '5'):
            xArr, yArr, zArr, timeArr, flag_arr = read_clean_to_lists.create_datetime_lists_from_clean(file, self.start_time_stamp, self.end_time_stamp, self.file_name)
            # plotting the arrays
            self.graph = plot_stacked_graphs.plot_arrays(xArr, yArr, zArr, timeArr, self.file_name, self.start_time_stamp, self.end_time_stamp,
                                                    in_min_x=plot_min_value_x, in_max_x=plot_max_value_x,
                                                    in_min_y=plot_min_value_y, in_max_y=plot_max_value_y,
                                                    in_min_z=plot_min_value_z, in_max_z=plot_max_value_z)

        # Clears all widgets in the graph_layout, and allows for only one graph to be displayed at a time
        self.clear_plots()
    
        # Putting the arrays into the gui
        self.graph = FigureCanvasQTAgg(self.graph)
        self.toolbar = NavigationToolbar2QT(self.graph, self)
        self.maccs_logo.setHidden(True)
        self.graph_layout.addWidget(self.toolbar) 
        self.graph_layout.addWidget(self.graph)

    def clear_plots(self):
        """
        Simple function to clear the widgets in a layout 
        This specifically removes all widgets in the graph layout 
        which removes all graphs and canvas' in the layout so we can re-draw with an update graph when the user wants
        """
        for i in reversed(range(self.graph_layout.count())): 
            self.graph_layout.itemAt(i).widget().setParent(None)      
        self.maccs_logo.setHidden(False)

    def custom_toobar(self):
        '''
        still in progress
        '''
        foobar = NavigationToolbar2QT(self.graph, self)
        foobar.zoom()

    def radio_file_check(self,file_type):
        '''
        function used to check the proper radio button with the file that is opened
        '''
        if file_type == '.2hz':
            self.radio_raw_file.setChecked(True)
        elif file_type == '.s2':
            self.radio_clean_file.setChecked(True)    

    def error_message_pop_up(self,title, message):
        # pops up error message box with the title and message inputted
        error_mes = QMessageBox.critical(self, title, message)
        sys.exit(0)

    def warning_message_pop_up(self,title, message):
        # pops up warning message box with the title and message inputted
        warning_mes = QMessageBox.warning(self, title,message)

    '''
    ##########
            # NOTICE ----------  I DONT KNOW WHAT THIS FUNCTION WAS USED FOR IN THREE GRAPH PLOTTER WORKS FINE WITH OUT IT AND ISNT USED ? 
            # BUT NOT GOING TO REMOVE UNTIL I FIGURE OUT WHAT IS NEEDED
    ###########
    '''

    def convert_hours_list_to_datetime_object(self, list_to_convert):
        """
        converts the hours list into datetime objects

        Parameters
        ----------
        list_to_convert : the list of items to convert

        Returns
        -------
        converted_list : the list of converted items
        """
        converted_list = []
            
        for i in range(len(list_to_convert)):
            total_time = list_to_convert[i]
            hour = int(total_time / 24)

            total_time = total_time - hour
            minute = int(total_time / 59)

            total_time = total_time - minute
            second = total_time

            converted_list.append(datetime.datetime(year=1111, month=1, day=1, hour=hour, minute=minute, second=second))

        return converted_list

    def save(self):
         
        """
        Description:
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
        Description:
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

    def set_stacked_options_hidden(self):
        '''
        Sets button group hidden when display type is not choosen
        '''

        self.min_x.setHidden(True)
        self.max_x.setHidden(True)
        self.min_y.setHidden(True)
        self.max_y.setHidden(True)
        self.min_z.setHidden(True)
        self.max_z.setHidden(True)
        self.input_min_x.setHidden(True)
        self.input_max_x.setHidden(True)
        self.input_min_y.setHidden(True)
        self.input_max_y.setHidden(True)
        self.input_min_z.setHidden(True)
        self.input_max_z.setHidden(True)

    def set_stacked_options_visable(self):
        '''
        Sets button group visable when display type is choosen
        '''

        self.min_x.setHidden(False)
        self.max_x.setHidden(False)
        self.min_y.setHidden(False)
        self.max_y.setHidden(False)
        self.min_z.setHidden(False)
        self.max_z.setHidden(False)
        self.input_min_x.setHidden(False)
        self.input_max_x.setHidden(False)
        self.input_min_y.setHidden(False)
        self.input_max_y.setHidden(False)
        self.input_min_z.setHidden(False)
        self.input_max_z.setHidden(False)

    def set_three_axis_options_hidden(self):
        '''
        Sets button group hidden when display type is not choosen
        '''

        self.plot_xyz_label.setHidden(True)
        self.graph_display_button_group.button(0).setHidden(True)
        self.graph_display_button_group.button(1).setHidden(True)
        self.graph_display_button_group.button(2).setHidden(True)

    def set_three_axis_options_visable(self):
        '''
        Sets button group visable when display type is choosen
        '''

        self.plot_xyz_label.setHidden(False)
        self.graph_display_button_group.button(0).setHidden(False)
        self.graph_display_button_group.button(1).setHidden(False)
        self.graph_display_button_group.button(2).setHidden(False)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    pal = QPalette()
    pal.setColor(QPalette.Window,'white')
    window.setPalette(pal)
    window.setAutoFillBackground(True)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()



