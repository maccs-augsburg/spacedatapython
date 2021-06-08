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
