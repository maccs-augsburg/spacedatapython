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

ttk.Label(mainframe, text = "Plot Min(Leave at zero for default):").grid(column = 1, row = 4, sticky = W)
plotMin = IntVar()
plotMin_entry = ttk.Entry(mainframe, width = 5, textvariable = plotMin)
plotMin_entry.grid(column = 2, row = 4)

ttk.Label(mainframe, text = "Plot Max(Leave at zero for default):").grid(column = 3, row = 4, sticky = W)
plotMax = IntVar()
plotMax_entry = ttk.Entry(mainframe, width = 5, textvariable = plotMax)
plotMax_entry.grid(column = 4, row = 4)

ttk.Label(mainframe, text = "Station File 1:").grid(column = 1, row = 5, sticky = W)
station_file1 = IntVar()
station_file1_entry = ttk.Entry(mainframe, width = 5, textvariable = station_file1)
station_file1_entry.grid(column = 2, row = 5)

ttk.Label(mainframe, text = "Station File 2:").grid(column = 1, row = 6, sticky = W)
station_file2 = IntVar()
station_file2_entry = ttk.Entry(mainframe, width = 5, textvariable = station_file2)
station_file2_entry.grid(column = 2, row = 6)

ttk.Label(mainframe, text = "Station File 3:").grid(column = 1, row = 7, sticky = W)
station_file3 = IntVar()
station_file3_entry = ttk.Entry(mainframe, width = 5, textvariable = station_file3)
station_file3_entry.grid(column = 2, row = 7)

#Creating the Radio Buttons widgets
ttk.Label(mainframe, text = "File 1 Format:").grid(column = 1, row = 8, sticky = W)
file_type = StringVar()
CDAWEB = ttk.Radiobutton(mainframe, text = "CDAWEB", variable = file_type, value = "CDAWEB").grid(column = 1, row = 9, sticky = W)
IAGA2000 = ttk.Radiobutton(mainframe, text = "IAGA2000", variable = file_type, value = "IAGA2000").grid(column = 1, row = 10, sticky = W) 
IAGA2002 =ttk.Radiobutton(mainframe, text = "IAGA2002", variable = file_type, value = "IAGA2002").grid(column = 1, row = 11, sticky = W)
Augsburg =ttk.Radiobutton(mainframe, text = "Augsburg", variable = file_type, value = "Augsburg").grid(column = 1, row = 12, sticky = W)
AAL_PIP =ttk.Radiobutton(mainframe, text = "AAL-PIP", variable = file_type, value = "AAL_PIP").grid(column = 1, row = 13, sticky = W)
SPole =ttk.Radiobutton(mainframe, text = "SPole", variable = file_type, value = "SPole").grid(column = 1, row = 14, sticky = W)
Other =ttk.Radiobutton(mainframe, text = "Other", variable = file_type, value = "Other").grid(column = 1, row = 15, sticky = W)



for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()
