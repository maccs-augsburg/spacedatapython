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
    
