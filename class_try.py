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
import raw_to_plot
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

    #mainframe = ttk.Frame(window, padding = "3 3 12 12")
    #mainframe.grid(column = 0, row = 0, sticky = (N,W,E,S))

    window.columnconfigure(0, weight = 1)
    window.rowconfigure(0, weight = 1)

    #File name values for saving figure
    self.figure = None
    self.file_name = None


    
    
