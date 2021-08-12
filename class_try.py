#Gui implemented with classes
#Annabelle

#Imports from tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


#imports from python 
import sys
import datetime
from PIL import ImageTk, Image

#imports from plotter functions

import file_naming
import read_raw_to_lists
import one_array_plotted 


class ThreeGraphPlotter:
    """
    """
def __init__(self):
    """
    """
    #Creation of the window 
    window = Tk()
    window.geometry('1500x600')
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
    ttk.label(mainframe, text = "Year Day: ").grid(column = 1, row = 2, sticky = E)
    
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
    
    x_plot = ttk.Checkbutton(mainframe, text = "X Plot", variable = self.graph_from_plotter_x, onvalue = 1).grid(column = 2, row = 10,padx = 25 , sticky = W)
    y_plot = ttk.Checkbutton(mainframe, text = "Y Plot", variable = self.graph_from_plotter_y, onvalue = 2).grid(column = 2, row = 11,padx = 25 , sticky = W) 
    z_plot = ttk.Checkbutton(mainframe, text = "Z Plot", variable = self.graph_from_plotter_z, onvalue = 3).grid(column = 2, row = 12,padx = 25 , sticky = W)

    self.file_selection = StringVar()
    cda_web = Radiobutton(mainframe, text = "CDAWEB:NA", value = 1, variable = self.file_selection).grid(column = 2, row = 15, padx = 25,  sticky = W)
    iaga_00 = Radiobutton(mainframe, text = "IAGA2000:NA", value = 2, variable = self.file_selection).grid(column = 2, row = 16, padx = 25,  sticky = W)
    iaga_02 = Radiobutton(mainframe, text =     "IAGA2002:NA", value = 3, variable = fself.ile_selection).grid(column = 2, row = 17, padx = 25, sticky = W)
    raw_hz_file = Radiobutton(mainframe, text = "Raw 2hz file", value = 4, variable = self.file_selection).grid(column = 2, row = 18, padx = 25,  sticky = W)
    clean_data = Radiobutton(mainframe, text = "Clean Data", value = 5, variable = self.file_selection).grid(column = 2, row = 19, padx = 25, sticky = W)



