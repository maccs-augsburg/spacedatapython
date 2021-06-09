#First GUI Try
#Annabelle 

from tkinter import *
from tkinter import ttk

#Main Application Frame
root = Tk()
root.title("Lineplot INPUT")

#Content Frame
mainframe = ttk.Frame(root, padding= "12 12 3 3")
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
root.columnconfigure(0, weight= 1)
root.rowconfigure(0, weight = 1)


#Creating Entry Widget

start_Hour = StringVar()
start_Hour_entry = ttk.Entry(mainframe, width = 5, textvariable = "Start Hour")
start_Hour_entry.grid(column = 1, row = 1, sticky = (W,E))

start_Minute =StringVar()
start_Minute_entry = ttk.Entry(mainframe, width = 5, textvariable = "Start Minute")
start_Minute_entry.grid(column = 1, row = 2, sticky = (W,E))


start_Second =StringVar()
start_Second_entry = ttk.Entry(mainframe, width = 5, textvariable = "Start Second")
start_Second_entry.grid(column = 2, row = 1, sticky = (W,E))


end_Hour = StringVar()
end_Hour_entry = ttk.Entry(mainframe, width = 5, textvariable = "End Hour")
end_Hour_entry.grid(column = 3, row = 1, sticky = (W,E))


end_Minute = StringVar()
end_Minute_entry = ttk.Entry(mainframe, width = 5, textvariable = "End Minute")
end_Minute_entry.grid(column = 3, row = 2, sticky = (W,E))

end_Second =StringVar()
end_Second_entry = ttk.Entry(mainframe, width = 5, textvariable = "End Second")
end_Second_entry.grid(column = 4, row = 1, sticky = (W,E))




