#Gui implemented with classes
#Annabelle

#Refactored into PySide6 GUI 
# Chris Hance may 2022

#Import from PySide6 // QT

from PyQt6.QtWidgets import (QMainWindow, QApplication, 
    QLabel, QLineEdit, 
    QStatusBar, QWidget, 
    QHBoxLayout, QGridLayout,
    QPushButton, QToolBar,
    QFileDialog, QRadioButton,
    QCheckBox)
from PyQt6.QtGui import QIcon,QAction, QPixmap
from PyQt6.QtCore import Qt, QSize
from pathlib import Path
#from PySide6.QtWidgets import QMainWindow


#imports from python 
import sys
import datetime
from PIL import ImageTk, Image

#Imports from matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.cbook import open_file_cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

import numpy as np
import subprocess

#imports from plotter functions

import file_naming
import read_raw_to_lists
import read_clean_to_lists
import entry_checks
class MainWindow(QMainWindow):
    def __init__(self):

        """ 
        Description	
    
        
        :type self:
        :param self:
    
        :raises:
    
        :rtype:
        """    
        super().__init__()
       
        self.setWindowTitle("MACCS Plotting Program")

        self.setGeometry(60,60, 1000,800)

        ###############
        ### Toolbar ###
        ###############
        toolbar = QToolBar("Main Toolbar")    
        toolbar.setIconSize(QSize(16,16))
        openfile = QAction(QIcon("../folder-open.png"),"Open File", self)
        savefile = QAction(QIcon("../disk.png"),"Save File", self)
        zoom = QAction(QIcon("../magnifier-zoom-in.png"),"Zoom in", self)

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

        self.input_starthour = QLineEdit()
        self.input_startmin = QLineEdit()
        self.input_startsec = QLineEdit()

        self.input_endhour = QLineEdit()
        self.input_endmin = QLineEdit()
        self.input_endsec = QLineEdit()

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

        self.checkbox_plotx = QCheckBox("X Plot")
        self.checkbox_ploty = QCheckBox("Y Plot")
        self.checkbox_plotz = QCheckBox("Z Plot")

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

        self.button_open_file.clicked.connect(self.open_file)
        self.button_quit.clicked.connect(self.close)
        self.button_plot.clicked.connect(self.execute_plot_function)
        # self.button_save.clicked.connect(self.save)
        # self.button_save_as.clicked.connect(self.save_as)
        ###############
        ### Widgets ###
        ###############

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

        self.main_layout.addLayout(self.label_and_entry_layout)

        #self.main_layout.addWidget(self.test)
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
            #home_dir = str(Path(home))
            # # opening the dialog box
            # file_name = askopenfilename(title='test', filetypes = filetypes)
            # file_name = QFileDialog()
            # file_name.setFileMode(QFileDialog)
            # file_name.setFilter('Clean files *.s2')
            # file_name.getOpenFileName()

            file_name = QFileDialog.getOpenFileName(self, 'Open File', 'C:\\Users\\hancec\\Desktop\\spacedatapython', 'Raw or Clean (*.2hz *.s2)')
            file_name = str(file_name)
            # splitting up the path and selecting the filename
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
  
            # # raw file selection branch
            # if (self.file_name[7:] == '.2hz'):
            #     self.selection_file_value = 4
                
            # # clean file selection branch
            # elif (self.file_name[7:] == '.s2'):
            #     self.selection_file_value = 5
            # # else
            # else:
            #     print('Option not available yet :(')
   
    def execute_plot_function(self):
        '''
        '''
        station_name_value = self.input_station_code.text()
        year_day_value = self.input_year.text()

        start_hour_value = entry_checks.start_hour_entry_check(self.input_starthour.text())
        start_minute_value = entry_checks.start_minute_entry_check( self.input_startmin.text())
        start_second_value = entry_checks.start_second_entry_check( self.input_startsec.text())

        end_hour_value = entry_checks.end_hour_entry_check( self.input_endhour.text())
        end_minute_value = entry_checks.end_minute_entry_check(self.input_endmin.text())
        end_second_value = entry_checks.end_second_entry_check( self.input_endsec.text())

        # creating the start time stamp
        start_time_stamp = datetime.time(hour=start_hour_value, minute=start_minute_value, second=start_second_value)
        # creating the end time stamp
        end_time_stamp = datetime.time(hour=end_hour_value, minute=end_minute_value, second=end_second_value)

       # selection_file_value = self.selection_file_value
        #file_ending_value = ThreeGraphPlotter.file_format_entry_check(selection_file_value)


        # Making the Plot
        file_name_full = station_name_value + year_day_value + '.2hz'
        time_interval_string = file_naming.create_time_interval_string_hms(start_hour_value, start_minute_value, start_second_value, end_hour_value, end_minute_value, end_second_value)
        self.file_name = station_name_value + year_day_value + time_interval_string
        print(file_name_full)
        try:
            file = open(file_name_full, 'rb')
        except:
            # popping up an error if we can't open the file
            entry_checks.error_message_pop_up(self,"File open error", "couldn't find and open your file")

        xArr, yArr, zArr, timeArr = read_raw_to_lists.create_datetime_lists_from_raw(file, start_time_stamp,end_time_stamp, self.file_name)
        # plotting the arrays
        self.figure = entry_checks.graph_from_plotter_entry_check(1,
                                                            1, 
                                                            1, 
                                                            xArr, 
                                                            yArr, 
                                                            zArr,
                                                            timeArr, 
                                                            self.file_name, start_time_stamp, end_time_stamp, '4')
        self.fig = FigureCanvasQTAgg(self.figure)
        toolbar = NavigationToolbar2QT(self.fig, self)
        self.maccs_logo.setHidden(True)
        self.main_layout.addWidget(toolbar)
        self.main_layout.addWidget(self.fig)
        
###################
## TO DO 
##################
'''
MOVE WIDGET CALLS AND ALL BUTTON SIGNALS AND ACTIONS INTO OWN CLASS FOR BETTER CODE LAYOUT  
'''
#####

class LabelWidget(QWidget):
    def __init__(self,text):
        super(LabelWidget, self).__init__()
        self.label = QLabel()
        self.label.setText(text)
        self.label.setMaximumWidth(50)

class ButtonActions(MainWindow):
    def __init__(self):
        MainWindow.__init__(self)
    def open_file(self, input_hour):
        
    
        """ Description
        :type self:
        :param self:
    
        :raises:
    
        :rtype:
        """    """
        Opens a open file dialog box where the user picks the appropriate file type. Once that is
        selected, it inputs the data into the boxes automatically based on the filename.
        """
        # listing the types of file types we currently support
        filetypes = (
            ('Raw files', '*.2hz'),
            ('Clean files', '*.s2')
        )

        # # opening the dialog box
        # file_name = askopenfilename(title='test', filetypes = filetypes)

        # # splitting up the path and selecting the filename
        # self.file_name = file_name.split('/')[-1]

        # # setting the station code from the filename
        # self.station_code
        # # setting the yearday from the filename
        # self.year_day.setText(self.file_name[2:7])

        self.input_starthour = input_hour
        # resetting the start times and end times
        self.input_starthour.setText("0")
        # self.input_startmin.setText("0")
        # self.input_startsec.setText("0")
        # self.input_endhour.setText("23")
        # self.input_endmin.setText("59")
        # self.input_endsec.setText("59")
        # # raw file selection branch
        # if (self.file_name[7:] == '.2hz'):
        #     self.selection_file.set(4)
            
        # # clean file selection branch
        # elif (self.file_name[7:] == '.s2'):
        #     self.selection_file.set(5)

        # # else
        # else:
        #     print('Option not available yet :(')


class ThreeGraphPlotter(MainWindow):
    def __init__(self):
        #Creation of the window 
        window = Tk()
        window.geometry('1500x700')
        window.title('X, Y and Z Plotter')

        mainframe = ttk.Frame(window, padding = "3 3 12 12")
        mainframe.grid(column = 0, row = 0, sticky = (N,W,E,S))

        window.columnconfigure(0, weight = 1)
        window.rowconfigure(0, weight = 1)

        #File name values for saving figure
        self.figure = None
        self.file_name = None

        ###Labels###

        #Year day entry box label 
        ttk.Label(mainframe, text = "Year Day: ").grid(column = 1, row = 2, sticky = E)

        #Start hour entry box label
        ttk.Label(mainframe, text = "Start Hour: ").grid(column = 1, row = 3, sticky = E)

        #Start minute entry box label
        ttk.Label(mainframe, text = "Start Minute: ").grid(column = 1, row = 4,sticky = E)

        #Start second entry box label
        ttk.Label(mainframe, text = "Start Second: ").grid(column = 1, row = 5, sticky = E)

        #End hour entry box label
        ttk.Label(mainframe, text = "End Hour: ").grid(column = 1, row = 6, sticky = E)

        #End minute entry box label
        ttk.Label(mainframe, text = "End Minute: ").grid(column = 1, row = 7, sticky = E)

        #End second entry box label
        ttk.Label(mainframe, text = "End Second: ").grid(column = 1, row = 8, sticky = E)

        #Plot x, y, or z checkbox label
        ttk.Label(mainframe, text = "Plot X, Y or Z: ").grid(column = 1, row = 9, sticky = E)

        #Station code entry box label
        ttk.Label(mainframe, text = "Station Code: ").grid(column = 1, row = 1, pady = (25, 0), sticky = E)

        #File option radiobutton label
        ttk.Label(mainframe, text = "File Option: ").grid(column = 1, row = 14, sticky = E)



        ###Entry Boxes###
        self.year_day = StringVar()
        ttk.Entry(mainframe, width= 5, textvariable = self.year_day).grid(column = 2, row = 2,   sticky = W)

        self.start_hour = IntVar()
        self.start_hour.set(0)
        ttk.Entry(mainframe, width = 5, textvariable = self.start_hour).grid(column = 2, row = 3, sticky = W)

        self.start_minute = IntVar()
        self.start_minute.set(0)
        ttk.Entry(mainframe, width = 5, textvariable = self.start_minute).grid(column = 2, row = 4, sticky = W)

        self.start_second = IntVar()
        self.start_second.set(0)
        ttk.Entry(mainframe, width = 5, textvariable = self.start_second).grid(column = 2, row = 5,sticky = W)

        self.end_hour = IntVar()
        self.end_hour.set(23)
        ttk.Entry(mainframe, width = 5, textvariable = self.end_hour).grid(column = 2, row = 6, sticky = W)

        self.end_minute = IntVar()
        self.end_minute.set(59)
        ttk.Entry(mainframe, width = 5, textvariable = self.end_minute).grid(column = 2, row = 7, sticky = W)

        self.end_second = IntVar()
        self.end_second.set(59)
        ttk.Entry(mainframe, width = 5, textvariable = self.end_second).grid(column = 2, row = 8, sticky = W)

        self.station_names = StringVar()
        ttk.Entry(mainframe, width = 5, textvariable = self.station_names).grid(column = 2, row = 1, pady = (25, 0), sticky = W)

        ###Check Boxes and Radiobuttons###
        self.graph_from_plotter_x = IntVar()
        self.graph_from_plotter_y = IntVar()
        self.graph_from_plotter_z = IntVar()
        
        # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Checkbutton.html
        # onvalue = 1 when checked inside gui by default, can also change onvalue to something we specify
        x_plot = ttk.Checkbutton(mainframe, text = "X Plot", variable = self.graph_from_plotter_x, onvalue = 1).grid(column = 2, row = 10,padx = 25 , sticky = W)
        y_plot = ttk.Checkbutton(mainframe, text = "Y Plot", variable = self.graph_from_plotter_y, onvalue = 1).grid(column = 2, row = 11,padx = 25 , sticky = W) 
        z_plot = ttk.Checkbutton(mainframe, text = "Z Plot", variable = self.graph_from_plotter_z, onvalue = 1).grid(column = 2, row = 12,padx = 25 , sticky = W)

        self.selection_file = StringVar()
        cda_web = Radiobutton(mainframe, text = "CDAWEB:NA", value = 1, variable = self.selection_file).grid(column = 2, row = 15, padx = 25,  sticky = W)
        iaga_00 = Radiobutton(mainframe, text = "IAGA2000:NA", value = 2, variable = self.selection_file).grid(column = 2, row = 16, padx = 25,  sticky = W)
        iaga_02 = Radiobutton(mainframe, text = "IAGA2002:NA", value = 3, variable = self.selection_file).grid(column = 2, row = 17, padx = 25, sticky = W)
        raw_hz_file = Radiobutton(mainframe, text = "Raw 2hz file", value = 4, variable = self.selection_file).grid(column = 2, row = 18, padx = 25,  sticky = W)
        clean_data = Radiobutton(mainframe, text = "Clean Data", value = 5, variable = self.selection_file).grid(column = 2, row = 19, padx = 25, sticky = W)


        ###Buttons###

        ttk.Button(mainframe, text = "Plot", command = lambda: self.execute_functions(mainframe)).grid(column = 2, row = 20,  sticky = W)
        ttk.Button(mainframe, text = "Quit", command = lambda: self.cancel(window)).grid(column =1, row = 22,columnspan = 2,  padx = 25, sticky = W)
        ttk.Button(mainframe, text="Save", command=lambda: self.save(self.figure, self.file_name)).grid(column=2, row=21, sticky=W)
        ttk.Button(mainframe, text="Save As...", command=lambda: self.save_as(self.figure, self.file_name)).grid(column=1, row=21, sticky=W)
        ttk.Button(mainframe, text="Open File...", command=lambda: self.open_file()).grid(column=1, row=20, sticky=W)
        #

        image=Image.open('maccslogo_870.jpeg')
        image_file = ImageTk.PhotoImage(image)
        image_label = ttk.Label(mainframe, image=image_file)
        image_label.image = image_file
        image_label.grid(column=7,row=1, columnspan=8, rowspan=24)

        
        for child in mainframe.winfo_children(): 
                child.grid_configure(padx=5, pady=5)

        #Puts our execute_functions to the return key
        window.bind("<Return>", self.execute_functions)

        window.mainloop()    

    def execute_functions(self, mainframe, *args):
        """
        executes the functions that are in the gui

        Parameters
        ----------
        mainframe : the main frame that the gui is placed in
        """

        ###Getting the user entries###
        station_names_value = self.station_names.get()
        self.station_names_entry_check(station_names_value)

        year_day_value = self.year_day.get()
        self.year_day_entry_check(year_day_value)

        start_hour_value = self.start_hour_entry_check(self.start_hour.get())
        start_minute_value = self.start_minute_entry_check( self.start_minute.get())
        start_second_value = self.start_second_entry_check( self.start_second.get())

        # creating the start time stamp
        start_time_stamp = datetime.time(hour=start_hour_value, minute=start_minute_value, second=start_second_value)


        end_hour_value = self.end_hour_entry_check( self.end_hour.get())
        end_minute_value = self.end_minute_entry_check( self.end_minute.get())
        end_second_value = self.end_second_entry_check( self.end_second.get())

        # creating the end time stamp
        end_time_stamp = datetime.time(hour=end_hour_value, minute=end_minute_value, second=end_second_value)

        selection_file_value = self.selection_file.get()
        file_ending_value = self.file_format_entry_check(selection_file_value)


        # Making the Plot
        file_name_full = station_names_value + year_day_value + file_ending_value
        time_interval_string = file_naming.create_time_interval_string_hms(start_hour_value, start_minute_value, start_second_value, end_hour_value, end_minute_value, end_second_value)
        self.file_name = station_names_value + year_day_value + time_interval_string
        
        # Get associated values to GUI, if x,y,z checked, then they are set to some value, respectively 1, 2, 3
        graph_from_plotter_value_x = self.graph_from_plotter_x.get()
        graph_from_plotter_value_y = self.graph_from_plotter_y.get()
        graph_from_plotter_value_z = self.graph_from_plotter_z.get()

        # Distinguishing between clean, and raw lists inside here. No need to check in graph_from_plotter_entry_check
        # Do any file checks in here for future additions
        try:
            file = open(file_name_full, 'rb')
        except:
            # popping up an error if we can't open the file
            self.error_message_pop_up("File open error", "couldn't find and open your file")

        if (selection_file_value == '4'):
            
            xArr, yArr, zArr, timeArr = read_raw_to_lists.create_datetime_lists_from_raw(file, start_time_stamp,end_time_stamp, self.file_name)
            # plotting the arrays
            self.figure = self.graph_from_plotter_entry_check(graph_from_plotter_value_x,
                                                              graph_from_plotter_value_y, 
                                                              graph_from_plotter_value_z, 
                                                              xArr, 
                                                              yArr, 
                                                              zArr,
                                                              timeArr, 
                                                              self.file_name, start_time_stamp, end_time_stamp, selection_file_value)

        elif (selection_file_value == '5'):
            
            xArr, yArr, zArr, timeArr, flag_arr = read_clean_to_lists.create_datetime_lists_from_clean(file, start_time_stamp, end_time_stamp, self.file_name)
            # plotting the arrays
            self.figure = self.graph_from_plotter_entry_check(graph_from_plotter_value_x,
                                                              graph_from_plotter_value_y, 
                                                              graph_from_plotter_value_z, 
                                                              xArr, 
                                                              yArr, 
                                                              zArr,
                                                              timeArr, 
                                                              self.file_name, start_time_stamp, end_time_stamp, selection_file_value)
                                          
        
        canvas = FigureCanvasTkAgg(self.figure, master = mainframe)
        canvas.draw()

        canvas.get_tk_widget().grid(column=4, row=1, columnspan=8, rowspan=24)

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

    def save(self, fig, file_name):
         
        """
        saves the file as a pdf document

        Parameters
        ----------
        fig : the plotted figure

        file_name : the name of the file to be saved as
        """
        # Saving the file as a defualt pdf
        fig.savefig(file_name + '.pdf', format='pdf', dpi=1200)
        # Opening the file after saving so the user knows it has been saved and can see it
        subprocess.Popen(file_name + '.pdf', shell=True)

    def save_as(self, fig, file_name):
         
        """
        saves the file as either a pdf or png

        Parameters
        ----------
        fig : the plotted figure

        file_name : the name of the file to be saved as
        """
        
        # Specifying the supported file types that can be saved
        
        files = [('PDF Files', '*.pdf'), ('PNG Files', '*.png'), ('All Files', '*.*')]
        # Popping up the save as file dialog box
        save_as_file = asksaveasfile(filetypes = files, defaultextension = files, initialfile=(file_name + '.pdf'))

        if save_as_file is None:
            return
        else:
            file_ending = save_as_file.name.split('/')[-1][-4:]
            if file_ending == ".pdf":
                fig.savefig(file_name + file_ending, format = "pdf", dpi = 1200)
            elif file_ending == ".png":
                fig.savefig(file_name + file_ending, format = "png", dpi = 1200)

    def open_file(self):
        """
        Opens a open file dialog box where the user picks the appropriate file type. Once that is
        selected, it inputs the data into the boxes automatically based on the filename.
        """
        # listing the types of file types we currently support
        filetypes = (
            ('Raw files', '*.2hz'),
            ('Clean files', '*.s2')
        )

        # opening the dialog box
        file_name = askopenfilename(title='test', filetypes = filetypes)
        

        # splitting up the path and selecting the filename
        self.file_name = file_name.split('/')[-1]

        # setting the station code from the filename
        self.station_names.set(self.file_name[0:2])

        # setting the yearday from the filename
        self.year_day.set(self.file_name[2:7])

        # resetting the start times and end times
        self.start_hour.set(0)
        self.start_minute.set(0)
        self.start_second.set(0)
        self.end_hour.set(23)
        self.end_minute.set(59)
        self.end_second.set(59)

        # raw file selection branch
        if (self.file_name[7:] == '.2hz'):
            self.selection_file.set(4)
            
        # clean file selection branch
        elif (self.file_name[7:] == '.s2'):
            self.selection_file.set(5)

        # else
        else:
            print('Option not available yet :(')

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()



