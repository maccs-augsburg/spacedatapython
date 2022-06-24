# Mark Ortega-Ponce & Chris Hance 
# June 2022
#Import from PySide6 // QT
from PySide6.QtWidgets import (QMainWindow, QApplication, 
                                QLabel, QLineEdit, 
                                QWidget, QHBoxLayout, 
                                QGridLayout,QPushButton, 
                                QToolBar,QVBoxLayout,
                                QFileDialog, QRadioButton,
                                QCheckBox,QMessageBox, 
                                QButtonGroup, QSizePolicy,
                                QComboBox
                                )
from PySide6.QtGui import QIcon, QAction, QPixmap, Qt, QPalette,QKeySequence
from PySide6.QtCore import  QSize, QTime

# path for file open 
from pathlib import Path

#imports from python 
import sys
import datetime
import os

#Imports from matplotlib
import matplotlib
from matplotlib.ft2font import LOAD_IGNORE_GLOBAL_ADVANCE_WIDTH
matplotlib.use('qtagg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

import subprocess
import entry_checks

from custom_widgets import (
    LineEdit, Label, CheckBox, 
    PushButton, Spinbox, Time, 
    GridLayout, HLayout,
    Toolbar, VLayout)

from custom_time_widget import MinMaxTime
sys.path.append("../")
import file_naming
import read_raw_to_lists
import read_clean_to_lists
import plot_stacked_graphs

MINIMUM_WINDOW_HEIGHT = 800
MINIMUM_WINDOW_WIDTH = 1000

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
        """    
        super().__init__()
        self.setWindowTitle("MACCS Plotting Program")

        self.setMinimumHeight(MINIMUM_WINDOW_HEIGHT)
        self.setMinimumWidth(MINIMUM_WINDOW_WIDTH)

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
        pixmap = QPixmap('../maccslogo_nobg.png')
        self.mac_label.setPixmap(pixmap)
        self.mac_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        ###############
        ### Toolbar ###
        ###############

        toolbar = QToolBar("Main Toolbar")    
        toolbar.setIconSize(QSize(16,16))
        action_openfile = QAction(QIcon("images/folder-open.png"),"Open...       ", self)
        action_savefile = QAction(QIcon("images/disk.png"),"Save File", self)
        action_zoom = QAction(QIcon("images/magnifier-zoom-in.png"),"Zoom in", self)
        action_help = QAction(QIcon("images/question-frame.png"),"Help", self)
        self.action_hide_entries = QAction(QIcon("images/inactive_eye.png"), "Hide Entries", self)
        self.action_hide_entries.setCheckable(True)
        self.action_hide_entries.setStatusTip("Hide Entries")

        toolbar.addAction(action_openfile)
        toolbar.addAction(action_savefile)
        toolbar.addAction(action_zoom)
        toolbar.addAction(self.action_hide_entries)
        toolbar.addSeparator()

        self.addToolBar(toolbar)

        #TODO add save as tool bar icon and button crtl shift S

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

        #TODO add more layouts that add the group widgets from marks custom widget file
        # layout for buttons and checkboxs
        self.main_layout = QHBoxLayout()
        self.parent_label_layout = GridLayout()
        self.labels_and_text_fields_layout = GridLayout()

        self.graph_layout = VLayout()
        self.checkbox_layout = HLayout()
        self.button_layout = GridLayout()
        self.min_max_xyz_layout = GridLayout()
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
        self.button_open_file = PushButton("Open file")
        self.button_open_file.set_uncheckable()
        self.button_open_file.clicked.connect(self.launch_dialog)
        self.button_graph_style = PushButton('Graph Style', "Graph Style")
        self.button_graph_style.clicked.connect(self.update_layout)
        self.button_save = PushButton('Save')
        self.button_save_as = PushButton('Save as...')
        self.button_plot = PushButton("Plot File")
        self.button_plot.set_uncheckable()
        self.button_zoom = PushButton("Zoom", "Zoom")
        self.button_zoom.clicked.connect(self.zoom_in_listener)
        self.button_clear_plot = PushButton('Clear Plot')
        self.button_quit = PushButton('Quit')

        ########################
        ### Signals / Events ###
        ########################

        action_openfile.triggered.connect(self.toolbar_open)
        action_savefile.triggered.connect(self.save)
        action_zoom.triggered.connect(self.zoom_in_listener)
        self.button_plot.clicked.connect(self.plot_graph)
        self.action_hide_entries.triggered.connect(self.hide_entry_layout)


        ######################
        ### Adding Widgets ###
        ######################
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
        
        ###############################################
        ### Adding wdigets layouts into main Layout ###
        ###############################################
        self.main_layout.addWidget(self.parent_label_layout,1)
        self.main_layout.addWidget(self.mac_label, 5)
        self.parent_label_layout.add_widget(self.labels_and_text_fields_layout,0,0)
        self.parent_label_layout.set_row_stretch(0, 24)
        self.parent_label_layout.add_widget(self.min_max_xyz_layout,1,0)
        self.parent_label_layout.set_row_stretch(1, 36)
        self.parent_label_layout.add_widget(self.checkbox_layout,2,0)
        self.parent_label_layout.set_row_stretch(2, 6)
        self.parent_label_layout.add_widget(self.button_layout,3,0)
        self.parent_label_layout.set_row_stretch(3, 18)

        self.button_layout.add_widget(self.combo_box_files, 0, 0)
        self.button_layout.add_widget(self.button_open_file, 0, 1)
        self.button_layout.add_widget(self.button_plot, 2, 0)
        self.button_layout.add_widget(self.button_zoom, 2, 1)
        self.button_layout.add_widget(self.button_save, 3, 0)
        self.button_layout.add_widget(self.button_save_as, 3, 1)
        # take one row, use 2 columns for now
        self.button_layout.add_widget(self.button_quit, 4, 0)
        
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
        self.file_extension = None
        self.x_arr = None
        self.y_arr = None
        self.z_arr = None
        self.time_arr = None
        ##########################
        self.figure = None
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
        ##########################
        
    def launch_dialog(self):
        '''
        Instance function to select a file filter.
        Filter index assigned to self.launch_dialog_option
        for plotting different file types in plot_graph().
        '''
        option = self.file_options.index(self.combo_box_files.currentText())
        self.launch_dialog_option = option

        if option == 0:

            file_filter = "Clean File (*.s2);;Raw File (*.2hz)"
            response = self.get_file_name(file_filter)
            
        elif option == 1:
            self.warning_message_popup("File not supported", "IAGA2000 Option Not Available Yet")

        elif option == 2:
            self.warning_message_popup("File not supported", "IAGA2002 Option Not Available Yet")

        elif option == 3:

            self.file_extension = ".s2"
            file_filter = "Clean File (*.s2)"
            response = self.get_file_name(file_filter)
        
        elif option == 4:

            self.file_extension = ".2hz"
            file_filter = "Raw File (*.2hz)"
            response = self.get_file_name(file_filter)

        elif option == 5:

            self.warning_message_dialog("File not supported", "Option Not Available Yet")

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
        return True

    def toolbar_open(self):

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
        
        if self.filename is None:
            return
        # if checks test return false, don't plot
        if not entry_checks.checks(self):
            return
        # only check after the first successful plot
        # gets set at the end of this function and remains True

        if self.graph_figure_flag:
            # if this is toggled, do following test
            if self.button_graph_style.is_toggled():
                # if !(test failed) and we have plotted one_plot already
                # means no new info to plot
                if not entry_checks.same_entries_one_toggled(self) and self.one_plot_flag:
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
        if self.launch_dialog_option == 3:
            # Doing short names to stay around 80-85 chars per row
            x,y,z,t,f = read_clean_to_lists.create_datetime_lists_from_clean(
                                                            file, 
                                                            self.start_time_stamp, 
                                                            self.end_time_stamp, 
                                                            self.filename)
            # easy to glance over, might be used for new feature?
            flag_arr = f

        elif self.launch_dialog_option == 4:
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
        min_x = self.spinbox_min_x.get_entry()
        max_x = self.spinbox_max_x.get_entry()
        min_y = self.spinbox_min_y.get_entry()
        max_y = self.spinbox_max_y.get_entry()
        min_z = self.spinbox_min_z.get_entry()
        max_z = self.spinbox_max_z.get_entry()

        # normalize the data to display even ticks
        min_x, max_x, min_y, max_y, min_z, max_z = entry_checks.axis_entry_checks(
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

        entry_checks.set_axis_entrys(self, min_x, max_x, min_y, max_y, min_z, max_z)
        # if one plot button is toggled
        # call necessary functions for one plot
        if self.button_graph_style.is_toggled():
            
            # keeping track of whats been plotted already
            self.prev_state_plot_x = self.x_checkbox.isChecked()
            self.prev_state_plot_y = self.y_checkbox.isChecked()
            self.prev_state_plot_z = self.z_checkbox.isChecked()

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

    def display_figure(self):

        self.graph_layout.setHidden(False)

        if self.graph_figure_flag:
            # remove plot from window
            self.figure_canvas.setParent(None)
        # create new figure
        self.figure_canvas = FigureCanvasQTAgg(self.figure)
        # add new figure to layout
        self.graph_layout.add_widget(self.figure_canvas)
        self.main_layout.addWidget(self.graph_layout, 5)
        self.mac_label.setHidden(True)
        self.figure_canvas_flag = True
        self.show()

    def __call__(self, event):
        '''
        __call__ is the event listener connected to matplotlib 
        it will listen for mouse clicks and record the xdata of the first and second click and converting them from matplotlib dates to datetime objects
        and then stripping the time down to hour min second spliting the values and settime our Time widget to that time and replotting normally so the scale is auto as it aslways is 

        '''
        datetime_object = mdates.num2date(event.xdata)
        hour = int(datetime_object.strftime("%H"))
        minute = int(datetime_object.strftime("%M"))
        second = int(datetime_object.strftime("%S"))

        if self.temp_var == 0:
            self.custom_start_time.time_widget.setTime(QTime(hour, minute, second))

        elif self.temp_var == 1:
            self.custom_end_time.time_widget.setTime(QTime(hour, minute, second))

            self.graph.mpl_disconnect(self.cid)
            self.plot_graph()

        self.temp_var = self.temp_var + 1

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

        self.start_time.set_min_time()
        self.end_time.set_max_time()

    def reset_axis_entries(self):

        self.spinbox_min_x.set_entry(0)
        self.spinbox_max_x.set_entry(0)
        self.spinbox_min_y.set_entry(0)
        self.spinbox_max_y.set_entry(0)
        self.spinbox_min_z.set_entry(0)
        self.spinbox_max_z.set_entry(0)

    def update_layout(self):

        bool_value = self.button_graph_style.is_toggled()

        self.button_zoom.set_toggle_status_false()
        self.button_zoom.change_text()
        self.min_max_xyz_layout.setHidden(bool_value)

        if bool_value:
            self.parent_label_layout.set_row_stretch(0, 27)
            self.parent_label_layout.set_row_stretch(1, 0)
            self.parent_label_layout.set_row_stretch(2, 3)
            self.parent_label_layout.set_row_stretch(3, 9)
        else:
            self.parent_label_layout.set_row_stretch(0, 24)
            self.parent_label_layout.set_row_stretch(1, 36)
            self.parent_label_layout.set_row_stretch(2, 6)
            self.parent_label_layout.set_row_stretch(3, 18)

    def hide_entry_layout(self):
        
        bool_value = self.action_hide_entries.isChecked()
        
        self.parent_label_layout.setHidden(bool_value)

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()


