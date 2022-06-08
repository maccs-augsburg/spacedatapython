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
                                QCheckBox,QMessageBox, QButtonGroup, QTimeEdit
                                )
from PySide6.QtGui import QIcon, QAction, QPixmap, Qt
from PySide6.QtCore import  QSize, QTime

# path for file open 
from pathlib import Path

#imports from python 
import sys
import datetime

#Imports from matplotlib
import matplotlib
matplotlib.use('qtagg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

import subprocess

#imports from other python files
import file_naming
import read_raw_to_lists
import read_clean_to_lists
import entry_checks
import plot_stacked_graphs

class MainWindow(QMainWindow):
    '''
    Class Containing GUI using PySide6 module from QT using its framework 
    The Gui is able to Graph a Single graph that can plot any combantion of axis'
    X Y or Z, one two, or three. While also able to alter the graph via zooming in and saving images of the graph
    We have ability to save as pdf or png using built in toolbar with matplotlib we can zoom and acess subplots of the graph
    we can also pin point a zoom using the text labels on the left of the GUI and re pressing plot
    '''
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

        self.start_hour = QLabel("Start Hour: ")
        self.start_min = QLabel("Start Minute: ")
        self.start_sec = QLabel("Start Second: ")

        self.end_hour = QLabel("End Hour: ")
        self.end_min = QLabel("End Minute: ")
        self.end_sec = QLabel("End Second: ")

        self.plot_xyz_label = QLabel("Plot X, Y, or Z: ")

        self.format_file_text = QLabel("Format of File to Open: ")

        self.maccs_logo = QLabel()
        self.maccs_logo.setPixmap(QPixmap("maccslogo_870.jpeg"))
        self.maccs_logo.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.test = QLabel("Welcome to the Magnetometer Array for Cusp and Cleft Studies")

        self.start_hour.setMaximumWidth(60)
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

        self.input_starthour = QLineEdit("0")
        self.input_startmin = QLineEdit("0")
        self.input_startsec = QLineEdit("0")

        self.input_endhour = QLineEdit("23")
        self.input_endmin = QLineEdit("59")
        self.input_endsec = QLineEdit("59")

        self.input_min_x = QLineEdit("0")
        self.input_max_x = QLineEdit("0")
        self.input_min_y = QLineEdit("0")
        self.input_max_y = QLineEdit("0")
        self.input_min_z = QLineEdit("0")
        self.input_max_z = QLineEdit("0")

        self.input_station_code.setMaximumWidth(35)
        self.input_starthour.setMaximumWidth(35)
        self.input_startmin.setMaximumWidth(35)
        self.input_startsec.setMaximumWidth(35)
        self.input_endhour.setMaximumWidth(35)
        self.input_endmin.setMaximumWidth(35)
        self.input_endsec.setMaximumWidth(35)
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
        self.qtime_start_time = QTimeEdit()
        self.qtime_start_time.setTimeRange(QTime(00,00,00), QTime(24,00,00))
        self.qtime_start_time.setDisplayFormat('hh:mm:ss')

        self.qtime_end_time = QTimeEdit()
        self.qtime_end_time.setTimeRange(QTime(00,00,00), QTime(24,00,00))
        self.qtime_end_time.setDisplayFormat('hh:mm:ss')

        self.qtime_start_time.setTime(QTime(00,00,00))
        self.qtime_end_time.setTime(QTime(23,59,59))

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

        self.label_and_entry_layout.addWidget(self.qtime_start_time, 2,1)
        self.label_and_entry_layout.addWidget(self.qtime_end_time, 3,1)

        self.label_and_entry_layout.addWidget(self.start_hour, 2,0)
        self.label_and_entry_layout.addWidget(self.start_min, 3,0)
        self.label_and_entry_layout.addWidget(self.start_sec, 4,0)
        
        self.label_and_entry_layout.addWidget(self.end_hour, 5,0)
        self.label_and_entry_layout.addWidget(self.end_min, 6,0)
        self.label_and_entry_layout.addWidget(self.end_sec, 7,0)

        self.label_and_entry_layout.addWidget(self.input_station_code,0, 1)
        self.label_and_entry_layout.addWidget(self.input_year, 1, 1)

        # self.label_and_entry_layout.addWidget(self.input_starthour, 2, 1)
        # self.label_and_entry_layout.addWidget(self.input_startmin, 3, 1)
        self.label_and_entry_layout.addWidget(self.input_startsec, 4, 1)

        self.label_and_entry_layout.addWidget(self.input_endhour, 5, 1)
        self.label_and_entry_layout.addWidget(self.input_endmin, 6, 1)
        self.label_and_entry_layout.addWidget(self.input_endsec, 7, 1)

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
            file_name = QFileDialog.getOpenFileName(self, 'Open File', home_dir, ' (*.2hz *.s2)')
            file_name = str(file_name)

            # splitting up the path and selecting the filename
            self.file_name = file_name.split(',')[0]

            self.file_name = file_name.split('/')[-1]

            # # setting the station code from the filename
            self.input_station_code.setText(str(self.file_name[0:2]))

            # # setting the yearday from the filename
            self.input_year.setText(str(self.file_name[2:7]))
            # resetting the start times and end times

            self.input_starthour.setText("0")
            self.input_startmin.setText("0")
            self.input_startsec.setText("0")
            self.input_endhour.setText("23")
            self.input_endmin.setText("59")
            self.input_endsec.setText("59")

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

    '''
    TODO
    IF putting both graphing dispaly into one 
 
    I have to depending on what display show 
    -- Checkboxs for X Y Z 
    OR
    -- min and max X Y Z values 

    After chosing what graph to display

    Proper fields show up and another "ok" button is displayed by those fields and after inputting or 
    checking click ok and plot is displayed and is faster    
    after already chosing what style instead of going through the message box everytime 
    sepreate the if statements of three axis and stack display into functions so that after we decided what 

    -- Open File
     -- Press Plot and Choose What Display you want Three Axis or Stacked Display (Rename button to choose graph type?)
      -- Proper input fields will then be shown 
                                            - Checkbox for three axis
                                            - plot min and max text fields for stacked display
        -- button by those fields that you press that plots the graph then can do normal alterations as before 

    '''

    def get_graph_entries(self):

        # Getting entries from the user / the file
        #Station code and year
        station_name_value = self.input_station_code.text()
        year_day_value = self.input_year.text()
        
        
        
        
        
        
        # Start hour, minute, and second entries
        # start_hour_value = entry_checks.start_hour_entry_check(self, self.input_starthour.text())
        # start_minute_value = entry_checks.start_minute_entry_check(self, self.input_startmin.text())
        # start_second_value = entry_checks.start_second_entry_check( self, self.input_startsec.text())

        start_hour_value = entry_checks.start_hour_entry_check(self, self.qtime_start_time.sectionText(self.qtime_start_time.sectionAt(0)))
        start_minute_value = entry_checks.start_minute_entry_check(self, self.qtime_start_time.sectionText(self.qtime_start_time.sectionAt(1)))
        start_second_value = entry_checks.start_second_entry_check( self, self.qtime_start_time.sectionText(self.qtime_start_time.sectionAt(2)))

        # End hour, minute and second entries
        # end_hour_value = entry_checks.end_hour_entry_check( self,self.input_endhour.text())
        # end_minute_value = entry_checks.end_minute_entry_check(self,self.input_endmin.text())
        # end_second_value = entry_checks.end_second_entry_check( self,self.input_endsec.text())   

        end_hour_value = entry_checks.end_hour_entry_check( self, self.qtime_end_time.sectionText(self.qtime_end_time.sectionAt(0)))
        end_minute_value = entry_checks.end_minute_entry_check(self, self.qtime_end_time.sectionText(self.qtime_end_time.sectionAt(1)))
        end_second_value = entry_checks.end_second_entry_check( self, self.qtime_end_time.sectionText(self.qtime_end_time.sectionAt(2)))

        # creating the start time stamp
        self.start_time_stamp = datetime.time(hour=start_hour_value, minute=start_minute_value, second=start_second_value)
        # creating the end time stamp
        self.end_time_stamp = datetime.time(hour=end_hour_value, minute=end_minute_value, second=end_second_value)
        #file_value = self.selection_file_value
        file_ending_value = entry_checks.file_format_entry_check(self,self.selection_file_value)
       
        # Making the Plot
        self.file_name_full = station_name_value + year_day_value + file_ending_value
        time_interval_string = file_naming.create_time_interval_string_hms(start_hour_value, start_minute_value, start_second_value, end_hour_value, end_minute_value, end_second_value)
        self.file_name = station_name_value + year_day_value + time_interval_string

    def choose_graph_style(self):
        '''
        Obtains the values entered in the GUI and runs the plotting program with the inputted values
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
        self.get_graph_entries()
        # Setting default values of the checkbox values if 0 we dont plot that axis if checked its a 1 and it is plotted 
        plot_x_axis = 0         
        plot_y_axis = 0
        plot_z_axis = 0

        if (self.checkbox_plotx.isChecked()):
            plot_x_axis = 1        
        if (self.checkbox_ploty.isChecked()):
            plot_y_axis = 1        
        if (self.checkbox_plotz.isChecked()):
            plot_z_axis = 1

        # trying to open the file
        try:
            file = open(self.file_name_full, 'rb')
        except:
            # popping up an error if we can't open the file
            self.warning_message_pop_up(self,"File open error", "Couldn't find and open your file \nPlease make sure you select proper file \n Try again please")

        #Creating the arrays
        if (self.selection_file_value == '4'):
            xArr, yArr, zArr, timeArr = read_raw_to_lists.create_datetime_lists_from_raw(file, self.start_time_stamp,self.end_time_stamp, self.file_name)
            # plotting the arrays
            self.graph = entry_checks.graph_from_plotter_entry_check(self,plot_x_axis,
                                                                plot_y_axis, 
                                                                plot_z_axis, 
                                                                xArr, 
                                                                yArr, 
                                                                zArr,
                                                                timeArr, 
                                                                self.file_name, self.start_time_stamp, self.end_time_stamp, '4')

        elif (self.selection_file_value == '5'):
            xArr, yArr, zArr, timeArr, flag_arr = read_clean_to_lists.create_datetime_lists_from_clean(file, self.start_time_stamp,self.end_time_stamp, self.file_name)
            # plotting the arrays
            self.graph = entry_checks.graph_from_plotter_entry_check(self,plot_x_axis,
                                                                plot_y_axis, 
                                                                plot_z_axis, 
                                                                xArr, 
                                                                yArr, 
                                                                zArr,
                                                                timeArr, 
                                                                self.file_name, self.start_time_stamp, self.end_time_stamp, '5')
        # Clears all widgets in the graph_layout, and allows for only one graph to be displayed at a time
        self.clear_plots()
    
        # Putting the arrays into the gui
        self.graph = FigureCanvasQTAgg(self.graph)
        self.toolbar = NavigationToolbar2QT(self.graph, self)
        self.maccs_logo.setHidden(True)
        self.graph_layout.addWidget(self.toolbar) 
        self.graph_layout.addWidget(self.graph)

    def plot_stacked_axis(self):
        self.get_graph_entries()

        plot_min_value_x = int(self.input_min_x.text())
        plot_max_value_x = int(self.input_max_x.text())
        plot_min_value_y = int(self.input_min_y.text())
        plot_max_value_y = int(self.input_max_y.text())
        plot_min_value_z = int(self.input_min_z.text())
        plot_max_value_z = int(self.input_max_z.text())

        try:
            file = open(self.file_name_full, 'rb')
        except:
            # popping up an error if we can't open the file
            self.warning_message_pop_up(self,"File open error", "couldn't find and open your file")

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
        for i in reversed(range(self.graph_layout.count())): 
            self.graph_layout.itemAt(i).widget().setParent(None)      
        self.maccs_logo.setHidden(False)

    def custom_toobar(self):
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
        self.plot_xyz_label.setHidden(True)
        self.graph_display_button_group.button(0).setHidden(True)
        self.graph_display_button_group.button(1).setHidden(True)
        self.graph_display_button_group.button(2).setHidden(True)

    def set_three_axis_options_visable(self):
        self.plot_xyz_label.setHidden(False)
        self.graph_display_button_group.button(0).setHidden(False)
        self.graph_display_button_group.button(1).setHidden(False)
        self.graph_display_button_group.button(2).setHidden(False)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()



