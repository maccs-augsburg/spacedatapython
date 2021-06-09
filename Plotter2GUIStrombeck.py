# Plotter2GUIStrombeck.py
#
# 2021 June - Created - Ted Strombeck
#

""" Python Plotter GUI - 2nd Version

GUI that allows for an easier interaction with our plotter program to test
and use MACCS data files which graphs the time-stamped x, y, and z values
on its' own plot.

"""

# tkinter imports
from tkinter import *
from tkinter import ttk

def fillList(listbox):
    # Keeping this list as a local variable which takes more time and power to process
    #   meaning it might be a bit slower but it eliminates the risk of having it as a
    #   global variable
    options_list = ["CDAWEB", "IAGA2000", "IAGA2002", "Augsburg", "AAL-PIP", "SPole", "other"]
    
    for i in range(0, len(options_list)):
        listbox.insert(i, options_list[i])

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
ttk.Label(mainframe, text="Station file:").grid(column=1, row=6, sticky=W)

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
stationfile1 = StringVar()
stationfile1_entry = ttk.Entry(mainframe, width=3, textvariable=stationfile1)
stationfile1_entry.grid(column=1, row=6)

### Button section ###
# Management buttons section
ok_button = ttk.Button(mainframe, text="OK", command=calculate).grid(column=1, row = 15, sticky=W)
cancel_button = ttk.Button(mainframe, text="Cancel", command=cancel).grid(column=1, row=15, sticky=E)
# Listbox buttons section
listbox1 = Listbox(mainframe, height=10, width=15, bg="grey", font="Helvetica")
fillList(listbox1)
listbox1.grid(column=1, row=7, sticky=(W,E))

### Main ###
# child formatting in mainframe
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

yearday_entry.focus() # starting spot for tab control
root.bind("<Return>", calculate) # returns the calculate funciton when called

root.mainloop() # root loop running
