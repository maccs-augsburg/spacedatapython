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

#Imports from matplotlib
import matplotlib
from matplotlib.ft2font import LOAD_IGNORE_GLOBAL_ADVANCE_WIDTH
matplotlib.use('qtagg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

import subprocess

from custom_widgets import (
    LineEdit, Label, CheckBox, 
    PushButton, Spinbox, Time, 
    GridLayout, HLayout,
    Toolbar, VLayout)

from custom_time_widget import MinMaxTime

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

        self.setGeometry(60,60, 1000,800)

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
        action_openfile = QAction(QIcon("../spacedatapython/images/folder-open.png"),"Open File", self)
        action_savefile = QAction(QIcon("../spacedatapython/images/disk.png"),"Save File", self)
        action_zoom = QAction(QIcon("../spacedatapython/images/magnifier-zoom-in.png"),"Zoom in", self)
        action_help = QAction(QIcon("../spacedatapython/images/question-frame.png"),"Help", self)

        toolbar.addAction(action_openfile)
        toolbar.addAction(action_savefile)
        toolbar.addAction(action_zoom)
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
        self.input_year = LineEdit()

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

        #################
        ### Combo Box ###
        #################

        #### DROP DOWN MENU FOR FILE FORMATS ###########
        self.file_options = ("IAGA2000 - NW",       # Index 0 
                        "IAGA2002 - NW",       # Index 1
                        "Clean File",          # Index 2
                        "Raw 2hz File",        # Index 3
                        "Other -- Not Working")# Index 4

        self.combo_box_files = QComboBox()
        # Add items to combo box
        self.combo_box_files.addItems(self.file_options)
        self.combo_box_files.setCurrentIndex(3)

        #######################
        ### Checkbox Select ###
        #######################
        
        self.checkbox_plotx = CheckBox("X Plot")
        self.checkbox_ploty = CheckBox("Y Plot")
        self.checkbox_plotz = CheckBox("Z Plot")

        ###############
        ### Buttons ###
        ###############
        self.button_open_file = PushButton("Open file")
        self.button_graph_style = PushButton('Graph Style')
        self.button_quit = PushButton('Quit')
        self.button_save = PushButton('Save')
        self.button_save_as = PushButton('Save as...')
        self.button_clear_plot = PushButton('Clear Plot')
        self.button_plot_three_axis = PushButton("Plot Graph")
        self.button_plot_stacked_graph = PushButton("Plot Graph")

        ######################
        ### Adding Widgets ###
        ######################
        self.labels_and_text_fields_layout.add_widget(self.station_label,0,0)

        ###############################################
        ### Adding wdigets layouts into main Layout ###
        ###############################################
        self.main_layout.addWidget(self.parent_label_layout,1)
        self.parent_label_layout.add_widget(self.labels_and_text_fields_layout,0,0)
        self.parent_label_layout.add_widget(self.min_max_xyz_layout,1,0)
        self.parent_label_layout.add_widget(self.checkbox_layout,2,0)
        self.parent_label_layout.add_widget(self.button_layout,3,0)
                #######
        ### Set Central Widget ###
        main_widget = QWidget()
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)


    def __call__(self,event):
        '''
        __call__ is the event listener connected to matplotlib 
        it will listen for mouse clicks and record the xdata of the first and second click and converting them from matplotlib dates to datetime objects
        and then stripping the time down to hour min second spliting the values and settime our Time widget to that time and replotting normally so the scale is auto as it aslways is 

        '''
        datetime_object = mdates.num2date(event.xdata)
        time_value_on_click= datetime.datetime.strftime(datetime_object,"%H %M %S")
        zoom_values = time_value_on_click.split(" ")
        
        if self.temp_var == 0:
            self.custom_start_time.time_widget.setTime(QTime(int(zoom_values[0]),int(zoom_values[1]),int(zoom_values[2])))

        elif self.temp_var == 1:
            self.custom_end_time.time_widget.setTime(QTime(int(zoom_values[0]),int(zoom_values[1]),int(zoom_values[2])))

            self.graph.mpl_disconnect(self.cid)
            if self.button_plot_stacked_graph.isHidden() == True:
                self.plot_three_axis()
            elif self.button_plot_three_axis.isHidden() == True:
                self.plot_stacked_axis()
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
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()


