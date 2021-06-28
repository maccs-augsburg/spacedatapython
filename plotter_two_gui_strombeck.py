# Plotter2GUIStrombeck.py
#
# 2021 June - Created - Ted Strombeck
#

""" Python Plotter GUI - 2nd Version

GUI that allows for an easier interaction with our plotter program to test
and use MACCS data files which graphs the time-stamped x, y, and z values
on its' own plot.

"""

#TODO---------------------------------------------------------------------------------------
#   mess around with columnspan and custom columns
#   implement functionality
#-------------------------------------------------------------------------------------------

# tkinter imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Python 3 imports
import sys
import datetime

# Plotter program imports
import raw_to_plot

def plotter_complete_message(title, message):
    """
    Creates a message pop up to indicate that the GUI has finished its' operations

    Parameters
    ----------
    String
        title: the string message of the pop up box that is the title
        message: the string message of the pop up box to be used as the message of why the error occurred
    """
    # Using the messagebox package of tkinter to show an easy pop up info message
    messagebox.showinfo(title, message)
    sys.exit(0) # Exiting without an error

def error_message_pop_up(title, message):
    """
    Creates an error pop up message box with the given title and message

    Parameters
    ----------
    String
        title: the string message of the pop up box that is the title
        message: the string message of the pop up box to be used as the message of why the error occurred
    """
    # Using the messagebox package of tkinter to show an easy pop up error message
    messagebox.showerror(title = title, message = "ERROR: " + message)
    sys.exit(0) # Exiting without an error

def warning_message_pop_up(title, message):
    """
    Creates a warning pop up message box with the given title and message

    Parameters
    ----------
    String
        title: the string message of the pop up box that is the title
        message: the string message of the pop up box to be used as the message of why the error occurrred
    """
    # Using the messagebox package of tkinter to show an easy pop up warning message
    messagebox.showwarning(title = title, message = "WARNING: " + message)
    sys.exit(0) # Exiting without an error

def year_day_entry_check(year_day_value):
    """
    Checks the year day entry value to see if there was a value inputted for the yearday entry box

    Parameters
    ----------
    String
        year_day_value: the value that was inputted into the year_day_entry box
    """
    # Testing the input value of yearday so we can use it for a file lookup
    if(len(year_day_value) == 0):
        # show error as no input was received
        # using tkinter's message box
        error_message_pop_up(title="year_day Entry Error", message="There was no input for the year_day entry box")

def date_time_object_check(string_value):
    """
    Checks to see if the time string is a single digit, if so it converts it so that it can be used in the datetime format of HH:MM:SS

    Parameters
    ----------
    String
        string_value: the string of digit/s to check to see if can be used for datetime format

    Returns
    -------
    String
        string_value: altered (or not) to be in the correct state for being used in the datetime module
    """
    #
    if(len(string_value) == 1):
        # Adding a zero to the start so that it is in the correct format if inputted value is a single digit
        #   This is so we have the format "00:00:00" for the datetime object
        string_value = "0" + string_value

    return string_value





    

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
mainframe = ttk.Frame(root, padding="3 3 12 12") # 3 3 12 12
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

# Station code entries
stationcode1 = StringVar()
stationcode1_entry = ttk.Entry(mainframe, width=4, textvariable=stationcode1)
stationcode1_entry.grid(column=1, row=6)

### Button section ###
# Management buttons section
ok_button = ttk.Button(mainframe, text="OK", command=calculate)
ok_button.grid(column=2, row = 15, sticky=W)
cancel_button = ttk.Button(mainframe, text="Cancel", command=cancel)
cancel_button.grid(column=3, row=15, sticky=E)
# Listbox buttons section
listbox1 = Listbox(mainframe, height=10, width=15, bg="grey", font="Helvetica")
fillList(listbox1)
listbox1.grid(column=1, row=8, sticky=(W,E))

### Main ###
# child formatting in mainframe
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

yearday_entry.focus() # starting spot for tab control
root.bind("<Return>", calculate) # returns the calculate funciton when called

root.mainloop() # root loop running
