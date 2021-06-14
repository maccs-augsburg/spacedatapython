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
startHour_entry.grid(column = 2, row = 2, sticky = (E))

ttk.Label(mainframe, text = "Start Minute:").grid(column = 3, row = 2, sticky = W)
startMinute = IntVar()
startMinute_entry = ttk.Entry(mainframe, width = 5, textvariable = startMinute)
startMinute_entry.grid(column = 4, row = 2)

ttk.Label(mainframe, text = "End Hour:").grid(column = 1, row = 3, sticky = W)
endHour = IntVar()
endHour_entry = ttk.Entry(mainframe, width = 5, textvariable = endHour)
endHour_entry.grid(column = 2, row = 3)

ttk.Label(mainframe, text = "End Minute:").grid(column = 3, row = 3, sticky = W)
endMinute = IntVar()
endMinute_entry = ttk.Entry(mainframe, width = 5, textvariable = endMinute)
endMinute_entry.grid(column = 4, row = 3)

ttk.Label(mainframe, text = "Plot min(Leave at zero for default):").grid(column = 1, row = 4, sticky = W)
plotMin = IntVar()
plotMin_entry = ttk.Entry(mainframe, width = 5, textvariable = plotMin)
plotMin_entry.grid(column = 2, row = 4)


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()
