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
    ttk.Entry(window, width= 5, textvariable = year_day).grid(column = 2, row = 2,   sticky = W)

    self.start_hour = IntVar()
    
