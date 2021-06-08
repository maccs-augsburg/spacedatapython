# PlotterGUIStrombeck.py
#
# 2021 June - Created - Ted Strombeck
#

""" Python Plotter GUI

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
startMinute_entry.grid(column=2, row=2)

endHour = IntVar()
endHour_entry = ttk.Entry(mainframe, width=3, textvariable=endHour)
endHour_entry.grid(column=1, row=3)

endMinute = IntVar()
endMinute_entry = ttk.Entry(mainframe, width=3, textvariable=endMinute)
endMinute_entry.grid(column=2, row=3)

# Plot min and Plot max entries
    # TODO: add plot min and plot max entry boxes

# Station file entries
stationfile1 = StringVar()
stationfile1_entry = ttk.Entry(mainframe, width=3, textvariable=stationfile1)
stationfile1_entry.grid(column=1, row=5)

stationfile2 = StringVar()
stationfile2_entry = ttk.Entry(mainframe, width=3, textvariable=stationfile2)
stationfile2_entry.grid(column=2, row=5)

stationfile3 = StringVar()
stationfile3_entry = ttk.Entry(mainframe, width=3, textvariable=stationfile3)
stationfile3_entry.grid(column=4, row=5)

### Button section ###
# Management buttons section
ok_button = ttk.Button(mainframe, text="OK", command=calculate).grid(column=1, row = 14, sticky=W)
cancel_button = ttk.Button(mainframe, text="Cancel", command=cancel).grid(column=2, row=14, sticky=W)
# Listbox buttons section
#listbox1 = Listbox(mainframe, height=10, width=15, bg="grey", font="Helvetica")
#listbox2 = Listbox(mainframe, height=10, width=15, bg="grey", font="Helvetica")
#listbox3 = Listbox(mainframe, height=10, width=15, bg="grey", font="Helvetica")
    #selectmode="multiple"
#fillList(listbox1)
#fillList(listbox2)
#fillList(listbox3)
#listbox1.grid(column=1, row=7, sticky=(W,E))
#listbox2.grid(column=2, row=7, sticky=(W,E))
#listbox3.grid(column=3, row=7, sticky=(W,E))

# Radiobutton section
fileSelection = StringVar()
rb1 = Radiobutton(mainframe, text="CDAWEB", value=1, variable=fileSelection).grid(column=1, row=7)
rb2 = Radiobutton(mainframe, text="IAGA2000", value=2, variable=fileSelection).grid(column=1, row=8)
rb3 = Radiobutton(mainframe, text="IAGA2002", value=3, variable=fileSelection).grid(column=1, row=9)
rb4 = Radiobutton(mainframe, text="Augsburg", value=4, variable=fileSelection).grid(column=1, row=10)
rb5 = Radiobutton(mainframe, text="AAL-PIP", value=5, variable=fileSelection).grid(column=1, row=11)
rb6 = Radiobutton(mainframe, text="SPole", value=6, variable=fileSelection).grid(column=1, row=12)
rb7 = Radiobutton(mainframe, text="other", value=7, variable=fileSelection).grid(column=1, row=13)

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
ttk.Label(mainframe, text="Plot Max (leave at 0 for default):").grid(column=2, row=4, sticky=W)
# Station file section
ttk.Label(mainframe, text="Station file 1:").grid(column=1, row=5, sticky=W)
ttk.Label(mainframe, text="Station file 2:").grid(column=2, row=5, sticky=W)
ttk.Label(mainframe, text="Station file 3:").grid(column=3, row=5, sticky=W)
# File format section
ttk.Label(mainframe, text="File 1 format:").grid(column=1, row=6, sticky=W)
ttk.Label(mainframe, text="File 2 format:").grid(column=2, row=6, sticky=W)
ttk.Label(mainframe, text="File 3 format:").grid(column=3, row=6, sticky=W)
