#Linestack GUI
#Annabelle Arns 

from tkinter import *
from tkinter import ttk

#Main Application Frame
root = Tk()
root.title = ("Plot Input")

#Content Frame
mainframe = ttk.Frame(root, padding = "3 3 12 12")
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)




#Creating the Entry Widgets


