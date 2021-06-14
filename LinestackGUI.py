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
ttk.Label(mainframe, text = "Yearday:").grid(column = 1, row = 1, sticky = W)
yearday = IntVar()
yearday_entry = ttk.Entry(mainframe, width = 5, textvariable = yearday)
yearday_entry.grid(column = 2, row = 1)



ttk.Label(mainframe, text = "Start Hour:").grid(column = 1, row = 2, sticky = W)
startHour = IntVar()
startHour_entry = ttk.Entry(mainframe, width = 5, textvariable = startHour)
startHour_entry.grid(column = 2, row = 2)










for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()
