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

#TODO----------------------------------------------------------------------------------------------------------
#   mess around with columnspan and custom columns ------------------------------------------------>
#   implement functionality -----------------------------------------------------------------------> working on
#   add seconds as input for time as well ---------------------------------------------------------> done
#   add initial tests to file types and file save as to see which values are selected -------------> 
#--------------------------------------------------------------------------------------------------------------

# tkinter imports
from tkinter import *
from tkinter import ttk

# Python 3 imports
import sys
import datetime

def calculate(*args):
### Getting input values ###

    ### yearday entry ###
    yearday_value=yearday_entry.get()
    if(len(yearday_value) == 0):
        # show error as no input was received
        pass

    ### Start hour, minute, and second entries ###
    startHour_value = startHour_entry.get()
    startMinute_value = startMinute_entry.get()
    startSecond_value = startSecond_entry.get()

    # Start hour portion
    if(len(startHour_value) == 1): ## -- Works!
        # Adding a zero to the start so that it is in the correct format
        startHour_value = "0" + startHour_value

    # Start minute portion
    if(len(startMinute_value) == 1): # -- Works!
        # Adding a zero to the start so that it is in the correct format
        startMinute_value = "0" + startMinute_value

    # Start second portion
    if(len(startSecond_value) == 1): # -- Works!
        # Adding a zero to the start so that it is in the correct format
        startSecond_value = "0" + startSecond_value
           
    ### End hour, minute, and second entries ###
    endHour_value = endHour_entry.get()
    endMinute_value = endMinute_entry.get()
    endSecond_value = endSecond_entry.get()

    # End hour portion
    if(len(endHour_value) == 0): # -- Not yet tested
        print("End Hour no value inputted test") 
        # end at 23
        pass

    # End minute portion
    if(len(endMinute_value) == 0): # -- Not yet tested
        print("End Minute no value inputted test") 
        # end at 59
        pass

    # End second portion
    if(len(endSecond_value) ==0): # -- Not yet tested
        print("End Second no value inputted test")
        # end at 59
        pass

    ### Plot min and max entries ###
    plotMin_value = plotMin_entry.get()
    if(len(plotMin_value) == 0): # -- Not yet tested
        print("plot Min no value inputted test") 
        # use default params
        pass

    plotMax_value = plotMax_entry.get()
    if(plotMax_value == 0): # -- Not yet tested
        print("plot Max no value inputted test") 
        # use default params
        pass

    ### Station code entry ###
    stationcode1_value = stationcode1_entry.get()
    if(len(stationcode1_value) == 0):  # -- Works!
        # show error as no input was received
        pass

    ### File format entry ###


    ### File option to save as entry ###
    

    
    pass

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
ttk.Label(mainframe, text="StartSecond:").grid(column=4, row=2, sticky=W)

# End time section
ttk.Label(mainframe, text="End Hour:").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text="End Minute:").grid(column=2, row=3, sticky=W)
ttk.Label(mainframe, text="End Second:").grid(column=4, row=3, sticky=W)

# Plot min and max section
ttk.Label(mainframe, text="Plot Min (leave at 0 for default): NW").grid(column=1, row=4, sticky=W)
ttk.Label(mainframe, text="Plot Max (leave at 0 for default): NW").grid(column=1, row=5, sticky=W)

# Station file section
ttk.Label(mainframe, text="Station code (3-4):").grid(column=1, row=6, sticky=W)

# File format section
ttk.Label(mainframe, text="Format of file to Open (pick from list below) NW").grid(column=1, row=7, sticky=W)

# File to save as section
ttk.Label(mainframe, text="Save file as (pick from list below) NW").grid(column=1, row=15, sticky=W)

### Entry section ###
# Yearday
yearday = StringVar() ## storing as a string for now, might change to int later
yearday_entry = ttk.Entry(mainframe, width=6, textvariable=yearday) # setting a variable with the Entry box format
yearday_entry.grid(column=1, row=1) # selecting which column and row to place said variable

# Start Hour
startHour = IntVar()
startHour.set(0)
startHour_entry = ttk.Entry(mainframe, width=3, textvariable=startHour)
startHour_entry.grid(column=1, row=2)

# Start Minute
startMinute = IntVar()
startMinute_entry = ttk.Entry(mainframe, width=3, textvariable=startMinute)
startMinute_entry.grid(column=3, row=2, sticky=W)

# Start Second
startSecond = IntVar()
startSecond_entry = ttk.Entry(mainframe, width=3, textvariable=startSecond)
startSecond_entry.grid(column=5, row=2, sticky=W)

# End Hour
endHour = IntVar()
endHour.set(23)
endHour_entry = ttk.Entry(mainframe, width=3, textvariable=endHour)
endHour_entry.grid(column=1, row=3)

# End Minute
endMinute = IntVar()
endMinute.set(59)
endMinute_entry = ttk.Entry(mainframe, width=3, textvariable=endMinute)
endMinute_entry.grid(column=3, row=3, sticky=W)

# End Second
endSecond = IntVar()
endSecond.set(59)
endSecond_entry = ttk.Entry(mainframe, width=3, textvariable=endSecond)
endSecond_entry.grid(column=5, row=3, sticky=W)

# Plot min and Plot max entries
plotMin = IntVar()
plotMin_entry = ttk.Entry(mainframe, width=3, textvariable=plotMin)
plotMin_entry.grid(column=2, row=4, sticky=W)
plotMax = IntVar()
plotMax_entry = ttk.Entry(mainframe, width=3, textvariable=plotMax)
plotMax_entry.grid(column=2, row=5, sticky=W)

# Station file entries
stationcode1 = StringVar()
stationcode1_entry = ttk.Entry(mainframe, width=4, textvariable=stationcode1)
stationcode1_entry.grid(column=1, row=6)

### Button section ###
# Management buttons section
ok_button = ttk.Button(mainframe, text="OK", command=calculate).grid(column=2, row = 19, sticky=W)
cancel_button = ttk.Button(mainframe, text="Cancel", command=cancel).grid(column=3, row=19, sticky=E)

# Radiobutton section
# file selection of type of file to open
fileSelection = StringVar()
rb1 = Radiobutton(mainframe, text="CDAWEB", value=1, variable=fileSelection).grid(column=1, row=8, sticky=W)
rb2 = Radiobutton(mainframe, text="IAGA2000", value=2, variable=fileSelection).grid(column=1, row=9, sticky=W)
rb3 = Radiobutton(mainframe, text="IAGA2002", value=3, variable=fileSelection).grid(column=1, row=10, sticky=W)
rb4 = Radiobutton(mainframe, text="Augsburg", value=4, variable=fileSelection).grid(column=1, row=11, sticky=W)
rb5 = Radiobutton(mainframe, text="AAL-PIP", value=5, variable=fileSelection).grid(column=1, row=12, sticky=W)
rb6 = Radiobutton(mainframe, text="SPole", value=6, variable=fileSelection).grid(column=1, row=13, sticky=W)
rb7 = Radiobutton(mainframe, text="other", value=7, variable=fileSelection).grid(column=1, row=14, sticky=W)

# file selection of type of file to save it as
fileToSaveAs = StringVar()
rb8 = Radiobutton(mainframe, text="pdf", value=8, variable=fileToSaveAs).grid(column=1, row=16, sticky=W)
rb9 = Radiobutton(mainframe, text="png", value=9, variable=fileToSaveAs).grid(column=1, row=17, sticky=W)
rb10 = Radiobutton(mainframe, text="Do not save", value=10, variable=fileToSaveAs).grid(column=1, row=18, sticky=W)

### Main ###
# child formatting in mainframe
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

yearday_entry.focus() # starting spot for tab control
root.bind("<Return>", calculate) # returns the calculate funciton when called

root.mainloop() # root loop running
