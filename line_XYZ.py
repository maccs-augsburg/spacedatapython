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
                                QCheckBox,QMessageBox
                                )
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtCore import  QSize

# path for file open 
from pathlib import Path

#imports from python 
import sys
import datetime

#Imports from matplotlib
import matplotlib
matplotlib.use('qtagg')

import matplotlib.pyplot as plt
import matplotlib.figure as figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

import subprocess

#imports from other python files
import file_naming
import read_raw_to_lists
import read_clean_to_lists
import entry_checks

class MainWindow(QMainWindow):
    '''
    Class Containing GUI using PySide6 module from QT using its framework 
    The Gui is able to Graph a Single graph that can plot any combantion of axis'
    X Y or Z, one two, or three. While also able to alter the graph via zooming in and saving images of the graph
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
        self.flag = False
        self.setWindowTitle("MACCS Plotting Program")

        self.setGeometry(60,60, 1000,800)
        self.selection_file_value = ''

        ###############
        ### Toolbar ###
        ###############

        toolbar = QToolBar("Main Toolbar")    
        toolbar.setIconSize(QSize(16,16))
        openfile = QAction(QIcon("../spacedatapython/images/folder-open.png"),"Open File", self)
        savefile = QAction(QIcon("../spacedatapython/images/disk.png"),"Save File", self)
        zoom = QAction(QIcon("../spacedatapython/images/magnifier-zoom-in.png"),"Zoom in", self)

        toolbar.addAction(openfile)
        toolbar.addAction(savefile)
        toolbar.addAction(zoom)
        toolbar.addSeparator()

        self.addToolBar(toolbar)
    
        ############
        ### Menu ###
        ############

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(openfile)
        file_menu.addAction(savefile)
        file_menu.addAction(zoom)

        edit_menu = menu.addMenu("&Edit")

        tool_menu = menu.addMenu("&Tools")

        help_menu = menu.addMenu("&Help")

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

        self.test = QLabel("Welcome to the Magnetometer Array for Cusp and Cleft Studies")

        self.start_hour.setMaximumWidth(60)
        self.plot_xyz_label.setFixedHeight(20)
        self.format_file_text.setFixedHeight(20)

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

        self.input_station_code.setMaximumWidth(35)
        self.input_starthour.setMaximumWidth(35)
        self.input_startmin.setMaximumWidth(35)
        self.input_startsec.setMaximumWidth(35)
        self.input_endhour.setMaximumWidth(35)
        self.input_endmin.setMaximumWidth(35)
        self.input_endsec.setMaximumWidth(35)
        self.input_year.setMaximumWidth(35)
        
        #######################
        ### Checkbox Select ###
        #######################

        self.checkbox_plotx = QCheckBox("X Plot", self)
        self.checkbox_ploty = QCheckBox("Y Plot", self)
        self.checkbox_plotz = QCheckBox("Z Plot", self)

        ########################
        ### Radial Selectors ###
        ########################

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
        self.button_plot = QPushButton('Plot')
        self.button_plot.setFixedWidth(75)
        self.button_quit = QPushButton('Quit')
        self.button_quit.setFixedWidth(75)
        self.button_save = QPushButton('Save')
        self.button_save.setFixedWidth(75)
        self.button_save_as = QPushButton('Save as...')
        self.button_save_as.setFixedWidth(75)

        ########################
        ### Signals / Events ###
        ########################

        openfile.triggered.connect(self.open_file)
        savefile.triggered.connect(self.save)
        
        self.button_open_file.clicked.connect(self.open_file)
        self.button_quit.clicked.connect(self.close)
        self.button_plot.clicked.connect(self.execute_plot_function)
        self.button_save.clicked.connect(self.save)
        # self.button_save_as.clicked.connect(self.save_as)

        ######################
        ### Adding Widgets ###
        ######################

        self.label_and_entry_layout.addWidget(self.station_code,0,0)
        self.label_and_entry_layout.addWidget(self.year_day, 1,0)

        self.label_and_entry_layout.addWidget(self.start_hour, 2,0)
        self.label_and_entry_layout.addWidget(self.start_min, 3,0)
        self.label_and_entry_layout.addWidget(self.start_sec, 4,0)
        
        self.label_and_entry_layout.addWidget(self.end_hour, 5,0)
        self.label_and_entry_layout.addWidget(self.end_min, 6,0)
        self.label_and_entry_layout.addWidget(self.end_sec, 7,0)

        self.label_and_entry_layout.addWidget(self.input_station_code,0, 1)
        self.label_and_entry_layout.addWidget(self.input_year, 1, 1)

        self.label_and_entry_layout.addWidget(self.input_starthour, 2, 1)
        self.label_and_entry_layout.addWidget(self.input_startmin, 3, 1)
        self.label_and_entry_layout.addWidget(self.input_startsec, 4, 1)

        self.label_and_entry_layout.addWidget(self.input_endhour, 5, 1)
        self.label_and_entry_layout.addWidget(self.input_endmin, 6, 1)
        self.label_and_entry_layout.addWidget(self.input_endsec, 7, 1)

        self.label_and_entry_layout.addWidget(self.plot_xyz_label, 8, 0)
        self.label_and_entry_layout.addWidget(self.checkbox_plotx, 9, 0)
        self.label_and_entry_layout.addWidget(self.checkbox_ploty, 10, 0)
        self.label_and_entry_layout.addWidget(self.checkbox_plotz, 11, 0)

        self.label_and_entry_layout.addWidget(self.format_file_text, 14, 0)

        self.label_and_entry_layout.addWidget(self.radio_iaga2000, 15,0)
        self.label_and_entry_layout.addWidget(self.radio_iaga2002, 16,0)
        self.label_and_entry_layout.addWidget(self.radio_clean_file, 17,0)
        self.label_and_entry_layout.addWidget(self.radio_raw_file, 18, 0)
        self.label_and_entry_layout.addWidget(self.radio_other, 19, 0)
        self.label_and_entry_layout.addWidget(self.button_open_file, 20, 0)
        self.label_and_entry_layout.addWidget(self.button_plot, 20, 1)
        self.label_and_entry_layout.addWidget(self.button_save_as, 21, 0)
        self.label_and_entry_layout.addWidget(self.button_save, 21, 1)
        self.label_and_entry_layout.addWidget(self.button_quit, 22, 0)

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
    def execute_plot_function(self):
        '''
        Obtains the values entered in the GUI and runs the plotting program with the inputted values
        '''
        # Getting entries from the user / the file
        #Station code and year
        station_name_value = self.input_station_code.text()
        year_day_value = self.input_year.text()

        # Start hour, minute, and second entries
        start_hour_value = entry_checks.start_hour_entry_check(self, self.input_starthour.text())
        start_minute_value = entry_checks.start_minute_entry_check(self, self.input_startmin.text())
        start_second_value = entry_checks.start_second_entry_check( self, self.input_startsec.text())

        # End hour, minute and second entries
        end_hour_value = entry_checks.end_hour_entry_check( self,self.input_endhour.text())
        end_minute_value = entry_checks.end_minute_entry_check(self,self.input_endmin.text())
        end_second_value = entry_checks.end_second_entry_check( self,self.input_endsec.text())

        # creating the start time stamp
        start_time_stamp = datetime.time(hour=start_hour_value, minute=start_minute_value, second=start_second_value)
        # creating the end time stamp
        end_time_stamp = datetime.time(hour=end_hour_value, minute=end_minute_value, second=end_second_value)
        #file_value = self.selection_file_value
        file_ending_value = entry_checks.file_format_entry_check(self,self.selection_file_value)
       
        # Making the Plot
        file_name_full = station_name_value + year_day_value + file_ending_value
        time_interval_string = file_naming.create_time_interval_string_hms(start_hour_value, start_minute_value, start_second_value, end_hour_value, end_minute_value, end_second_value)
        self.file_name = station_name_value + year_day_value + time_interval_string

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
            file = open(file_name_full, 'rb')
        except:
            # popping up an error if we can't open the file
            self.error_message_pop_up(self,"File open error", "Couldn't find and open your file \nPlease make sure you select proper file \nExiting program")

        # Creating the arrays
        if (self.selection_file_value == '4'):
            xArr, yArr, zArr, timeArr = read_raw_to_lists.create_datetime_lists_from_raw(file, start_time_stamp,end_time_stamp, self.file_name)
            # plotting the arrays
            self.graph = entry_checks.graph_from_plotter_entry_check(self,plot_x_axis,
                                                                plot_y_axis, 
                                                                plot_z_axis, 
                                                                xArr, 
                                                                yArr, 
                                                                zArr,
                                                                timeArr, 
                                                                self.file_name, start_time_stamp, end_time_stamp, '4')

        elif (self.selection_file_value == '5'):
            xArr, yArr, zArr, timeArr, flag_arr = read_clean_to_lists.create_datetime_lists_from_clean(file, start_time_stamp,end_time_stamp, self.file_name)
            # plotting the arrays
            self.graph = entry_checks.graph_from_plotter_entry_check(self,plot_x_axis,
                                                                plot_y_axis, 
                                                                plot_z_axis, 
                                                                xArr, 
                                                                yArr, 
                                                                zArr,
                                                                timeArr, 
                                                                self.file_name, start_time_stamp, end_time_stamp, '5')

        # Clears all widgets in the graph_layout, and allows for only one graph to be displayed at a time
        for i in reversed(range(self.graph_layout.count())): 
            self.graph_layout.itemAt(i).widget().setParent(None)
        # Putting the arrays into the gui
        self.graph = FigureCanvasQTAgg(self.graph)
        self.toolbar = NavigationToolbar2QT(self.graph, self)
        self.maccs_logo.setHidden(True)
        self.graph_layout.addWidget(self.toolbar) 
        self.graph_layout.addWidget(self.graph)

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

#### TODO Convert save and save as functions into PySide package useage isntead of TK 

    def save(self):
         
        """
        saves the file as a pdf document
        
        using self.file_name to get the filename already used for the specfic file we are using
        plt.savefig grabs the most recent figure we have plotted
        """

        plt.savefig(self.file_name + ".pdf")
        subprocess.Popen(self.file_name + '.pdf', shell=True)

    def save_as(self, fig, file_name):
         
        """
        saves the file as either a pdf or png

        Parameters
        ----------
        fig : the plotted figure

        file_name : the name of the file to be saved as
        
        
        # Specifying the supported file types that can be saved
        
        files = [('PDF Files', '*.pdf'), ('PNG Files', '*.png'), ('All Files', '*.*')]
        # Popping up the save as file dialog box
        #save_as_file = asksaveasfile(filetypes = files, defaultextension = files, initialfile=(file_name + '.pdf'))

        # if save_as_file is None:
        #     return
        # else:
        #     file_ending = save_as_file.name.split('/')[-1][-4:]
        #     if file_ending == ".pdf":
        #         fig.savefig(file_name + file_ending, format = "pdf", dpi = 1200)
        #     elif file_ending == ".png":
        #         fig.savefig(file_name + file_ending, format = "png", dpi = 1200)
        """

'''       
###################
## TO DO 
##################

MOVE WIDGET CALLS AND ALL BUTTON SIGNALS AND ACTIONS INTO OWN CLASS FOR BETTER CODE LAYOUT  
'''


 
# TODO Possible work on making widget create it owns class to clean up MainWindow Class

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()



