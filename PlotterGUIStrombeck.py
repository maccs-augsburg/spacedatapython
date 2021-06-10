# PlotterGUIStrombeck.py
#
# 2021 June - Created - Ted Strombeck
#

""" Python Plotter GUI - 1st Version

GUI that allows for an easier interaction with our plotter program to test
and use MACCS data files which graphs the time-stamped x, y, and z values
on its' own plot.

This GUI uses a radiobutton format for selection of file type

"""

# tkinter imports
from tkinter import *
from tkinter import ttk

def calculate(*args):
    pass
    #try:
    #    value = float(feet.get())
    #    meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    #except ValueError:
    #    pass

def cancel(*args):
    root.destroy() # Exiting without running any code after
    #global.root
    #root.quit() # Exiting with running code after

### Setting up GUI object ###
root = Tk()
root.title("Plot input")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

### Label section ###
# Yearday section
ttk.Label(mainframe, text="Yearday:").grid(column=1, row=1, sticky=W)

# Start time section
ttk.Label(mainframe, text="Start Hour:").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text="Start Minute:").grid(column=2, row=2, sticky=W)

# End time section
ttk.Label(mainframe, text="End Hour:").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text="End Minute:").grid(column=2, row=3, sticky=W)

# Plot min and max section
ttk.Label(mainframe, text="Plot Min (leave at 0 for default):").grid(column=1, row=4, sticky=W)
ttk.Label(mainframe, text="Plot Max (leave at 0 for default):").grid(column=1, row=5, sticky=W)

# Station file section
ttk.Label(mainframe, text="Station code:").grid(column=1, row=6, sticky=W)

# File format section
ttk.Label(mainframe, text="File format (pick from list below)").grid(column=1, row=7, sticky=W)

### Entry section ###
# Yearday entries
yearday = StringVar() ## storing as a string for now, might change to int later
yearday_entry = ttk.Entry(mainframe, width=6, textvariable=yearday) # setting a variable with the Entry box format
yearday_entry.grid(column=1, row=1) # selecting which column and row to place said variable

# Start Hour, Start Minute, End Hour and End Minute entries
startHour = IntVar()
startHour_entry = ttk.Entry(mainframe, width=3, textvariable=startHour)
startHour_entry.grid(column=1, row=2)

startMinute = IntVar()
startMinute_entry = ttk.Entry(mainframe, width=3, textvariable=startMinute)
startMinute_entry.grid(column=3, row=2, sticky=W)

endHour = IntVar()
endHour_entry = ttk.Entry(mainframe, width=3, textvariable=endHour)
endHour_entry.grid(column=1, row=3)

endMinute = IntVar()
endMinute_entry = ttk.Entry(mainframe, width=3, textvariable=endMinute)
endMinute_entry.grid(column=3, row=3, sticky=W)

# Plot min and Plot max entries
plotMin = IntVar()
plotMin_Entry = ttk.Entry(mainframe, width=3, textvariable=plotMin)
plotMin_Entry.grid(column=2, row=4, sticky=W)
plotMax = IntVar()
plotMax_Entry = ttk.Entry(mainframe, width=3, textvariable=plotMax)
plotMax_Entry.grid(column=2, row=5, sticky=W)

# Station file entries
stationcode1 = StringVar()
stationcode1_entry = ttk.Entry(mainframe, width=6, textvariable=stationcode1)
stationcode1_entry.grid(column=1, row=6)

### Button section ###
# Management buttons section
ok_button = ttk.Button(mainframe, text="OK", command=calculate).grid(column=1, row = 15, sticky=W)
cancel_button = ttk.Button(mainframe, text="Cancel", command=cancel).grid(column=1, row=15, sticky=E)

# Radiobutton section
fileSelection = StringVar()
rb1 = Radiobutton(mainframe, text="CDAWEB", value=1, variable=fileSelection).grid(column=1, row=8)
rb2 = Radiobutton(mainframe, text="IAGA2000", value=2, variable=fileSelection).grid(column=1, row=9)
rb3 = Radiobutton(mainframe, text="IAGA2002", value=3, variable=fileSelection).grid(column=1, row=10)
rb4 = Radiobutton(mainframe, text="Augsburg", value=4, variable=fileSelection).grid(column=1, row=11)
rb5 = Radiobutton(mainframe, text="AAL-PIP", value=5, variable=fileSelection).grid(column=1, row=12)
rb6 = Radiobutton(mainframe, text="SPole", value=6, variable=fileSelection).grid(column=1, row=13)
rb7 = Radiobutton(mainframe, text="other", value=7, variable=fileSelection).grid(column=1, row=14)

### Main ###
# child formatting in mainframe
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

yearday_entry.focus() # starting spot for tab control
root.bind("<Return>", calculate) # returns the calculate funciton when called

root.mainloop() # root loop running
