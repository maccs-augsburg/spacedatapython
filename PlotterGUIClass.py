# PlotterGUIClass.py
#
# 2021 June - Created - Ted Strombeck

""" Python Plotter GUI Class

GUI class that allows for an easier interaction with our plotter program
using various functions to access and use MACCS data files which graphs
the time-stamped x, y, and z values on its' own plot.

"""

# tkinter imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Python 3 imports
import sys
import datetime

class Single_File_Plotter_GUI:
    def __init__(self, master):
        self.master = master
        master.title("")

        self.label = Label(master, text="")


        #self.greet_button = Button(master, text="Greet", command=self.greet)

    def someotherfunction(self):
        
root = Tk()
my_gui = Single_File_PlotterGUI(root)
root.mainloop()
