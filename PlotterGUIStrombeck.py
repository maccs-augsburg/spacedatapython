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
#   implement functionality -----------------------------------------------------------------------> 
#   add seconds as input for time as well ---------------------------------------------------------> done
#   add initial tests to file types and file save as to see which values are selected -------------> done
#   add error messages for bad inputs -------------------------------------------------------------> done
#   Create datetime objects of inputted times -----------------------------------------------------> done
#   documentation --------------------------------------------------------------------------------->
#   main function ---------------------------------------------------------------------------------> working on
#   error message popup function ------------------------------------------------------------------> done
#   general gui function -------------------------------------------------------------------------->
#   gui display function -------------------------------------------------------------------------->
#   change calculate function name to something like display plot --------------------------------->
#   view box around radio buttons ----------------------------------------------------------------->
#   go through and fully comment code ------------------------------------------------------------->
#   variable names change -------------------------------------------------------------------------> working on
#--------------------------------------------------------------------------------------------------------------

# tkinter imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Python 3 imports
import sys
import datetime

def errorMessagePopUp(title, message):
    messagebox.showerror(title = title, message = "ERROR: " + message)
    sys.exit(0)

def calculate(*args):
### Getting input values ###

    ### yearday entry ###
    yearday_value=yearday_entry.get()
    if(len(yearday_value) == 0):
        # show error as no input was received
        # using tkinter's message box
        errorMessagePopUp(title="YearDay Entry Error", message="There was no input for the yearday entry box")

    ### Start hour, minute, and second entries ###
    startHour_value = startHour_entry.get()
    startMinute_value = startMinute_entry.get()
    startSecond_value = startSecond_entry.get()

    # Start hour portion
    if(len(startHour_value) == 1): 
        # Adding a zero to the start so that it is in the correct format
        startHour_value = "0" + startHour_value
    if((int)(startHour_value) > 23):
        # Have error message box pop up because it can't be more than 23
        errorMessagePopUp(title="Start Hour Entry Error", message="Start hour cannot be more than 23")

    # Start minute portion
    if(len(startMinute_value) == 1):
        # Adding a zero to the start so that it is in the correct format
        startMinute_value = "0" + startMinute_value
    if((int)(startMinute_value) > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        errorMessagePopUp(title="Start Minute Entry Error", message="Start minute cannot be more than 59")

    # Start second portion
    if(len(startSecond_value) == 1):
        # Adding a zero to the start so that it is in the correct format
        startSecond_value = "0" + startSecond_value
    if((int)(startSecond_value) > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        errorMessagePopUp(title="Start Second Entry Error", message="Start second cannot be more than 59")

    startTime_timeStamp = datetime.time.fromisoformat(startHour_value + ":" + startMinute_value + ":" + startSecond_value)
           
    ### End hour, minute, and second entries ###
    endHour_value = endHour_entry.get()
    endMinute_value = endMinute_entry.get()
    endSecond_value = endSecond_entry.get()

    # End hour portion
    if(len(endHour_value) == 1):
        # Adding a zero to the start so that it is in the correct format
        endHour_value = "0" + endHour_value
    if((int)(endHour_value) > 23):
        # Have error message box pop up because it can't be more than 23
        errorMessagePopUp(title="End Hour Entry Error", message="End hour cannot be more than 23")
        
    # End minute portion
    if(len(endMinute_value) == 1):
        # Adding a zero to the start so that it is in the correct format
        endMinute_value = "0" + endMinute_value
    if((int)(endMinute_value) > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        errorMessagePopUp(title="End Minute Entry Error", message="End minute cannot be more than 59")

    # End second portion
    if(len(endSecond_value) ==1):
        # Adding a zero to the start so that it is in the correct format
        endSecond_value = "0" + endSecond_value
    if((int)(endSecond_value) > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        errorMessagePopUp(title="End Second Entry Error", message="End second cannot be more than 59")

    endTime_timeStamp = datetime.time.fromisoformat(endHour_value + ":" + endMinute_value + ":" + endSecond_value)
    
    ### Plot min and max entries ###
    plotMinDefaultFlag = False
    plotMaxDefaultFlag = False
    
    plotMin_value = plotMin_entry.get()
    if(plotMin_value == '0'): 
        # use default params
        plotMinDefaultFlag = True

    plotMax_value = plotMax_entry.get()
    if(plotMax_value == '0'):
        # use default params
        plotMaxDefaultFlag = True

    ### Station code entry ###
    stationcode1_value = stationcode1_entry.get()
    if(len(stationcode1_value) == 0):
        # show error as no input was received
        errorMessagePopUp(title="Station code entry error", message="There was no input for the station code entry box")

    ### File format entry ###

    # RB buttons used: 1, 2, 3, 4, 7
    fileSelection_value = fileSelection.get()
    if(fileSelection_value == '1'):
        # CDA-Web branch (NOT IMPLEMENTED)
        pass
    elif(fileSelection_value == '2'):
        #IAGA2000 branch (NOT IMPLEMENTED)
        pass
    elif(fileSelection_value == '3'):
        #IAGA2002 branch (NOT IMPLEMENTED)
        pass
    elif(fileSelection_value == '4'):
        #Raw 2hz file branch (TODO: IMPLEMENT SECTION)
        pass
    elif(fileSelection_value == '7'):
        #Other option branch (NOT IMPLEMENTED YET)
        pass
    else:
        # Message box error when no file format option has been selected
        errorMessagePopUp(title="File format option error", message="Please select a file format option")
        
    ### File option to save as entry ###

    # RB buttons used: 8, 9, 10
    fileSaveAsOption_value = fileToSaveAs.get()
    if(fileSaveAsOption_value == '8'):
        #pdf branch
        pass
    elif(fileSaveAsOption_value == '9'):
        #png branch
        pass
    elif(fileSaveAsOption_value == '10'):
        #Do not save branch
        pass
    else:
        # Message box error when no file save option has been selected
        errorMessagePopUp(title="File Save Option error", message="Please select an option to save the file as")
    


def cancel(*args):
    root.destroy() # Exiting without running any code after
    #global.root
    #root.quit() # Exiting with running code after

def GUILabels():
    # Yearday label
    ttk.Label(mainframe, text="Yearday:").grid(column=1, row=1, sticky=W)

    # Start time labels
    ttk.Label(mainframe, text="Start Hour:").grid(column=1, row=2, sticky=W)
    ttk.Label(mainframe, text="Start Minute:").grid(column=2, row=2, sticky=W)
    ttk.Label(mainframe, text="StartSecond:").grid(column=4, row=2, sticky=W)

    # End time labels
    ttk.Label(mainframe, text="End Hour:").grid(column=1, row=3, sticky=W)
    ttk.Label(mainframe, text="End Minute:").grid(column=2, row=3, sticky=W)
    ttk.Label(mainframe, text="End Second:").grid(column=4, row=3, sticky=W)

    # Plot min and max labels
    ttk.Label(mainframe, text="Plot Min (leave at 0 for default):").grid(column=1, row=4, sticky=W)
    ttk.Label(mainframe, text="Plot Max (leave at 0 for default):").grid(column=1, row=5, sticky=W)

    # Station file label
    ttk.Label(mainframe, text="Station code (3-4):").grid(column=1, row=6, sticky=W)

    # File format label
    ttk.Label(mainframe, text="Format of file to Open (pick from list below)").grid(column=1, row=7, sticky=W)

    # File save as label
    ttk.Label(mainframe, text="Save file as (pick from list below)").grid(column=1, row=15, sticky=W)

def GUIEntries():
    ### Global variables ###
    global yearday, yearday_entry
    global startHour, startHour_entry, startMinute, startMinute_entry, startSecond, startSecond_entry
    global endHour, endHour_entry, endMinute, endMinute_entry, endSecond, endSecond_entry
    global plotMin, plotMin_entry, plotMax, plotMax_entry
    global stationcode1, stationcode1_entry
    global fileSelection, rb1, rb2, rb3, rb4, rb7, fileToSaveAs, rb8, rb9, rb10
    
    # Yearday entry
    yearday = StringVar() ## storing as a string for now, might change to int later
    yearday_entry = ttk.Entry(mainframe, width=6, textvariable=yearday) # setting a variable with the Entry box format
    yearday_entry.grid(column=1, row=1) # selecting which column and row to place said variable

    # Start Hour entry
    startHour = IntVar()
    startHour.set(0)
    startHour_entry = ttk.Entry(mainframe, width=3, textvariable=startHour)
    startHour_entry.grid(column=1, row=2)

    # Start Minute entry
    startMinute = IntVar()
    startMinute_entry = ttk.Entry(mainframe, width=3, textvariable=startMinute)
    startMinute_entry.grid(column=3, row=2, sticky=W)

    # Start Second entry
    startSecond = IntVar()
    startSecond_entry = ttk.Entry(mainframe, width=3, textvariable=startSecond)
    startSecond_entry.grid(column=5, row=2, sticky=W)

    # End Hour entry
    endHour = IntVar()
    endHour.set(23)
    endHour_entry = ttk.Entry(mainframe, width=3, textvariable=endHour)
    endHour_entry.grid(column=1, row=3)

    # End Minute entry
    endMinute = IntVar()
    endMinute.set(59)
    endMinute_entry = ttk.Entry(mainframe, width=3, textvariable=endMinute)
    endMinute_entry.grid(column=3, row=3, sticky=W)

    # End Second entry
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
    rb1 = Radiobutton(mainframe, text="CDAWEB -- Not working", value=1, variable=fileSelection).grid(column=1, row=8, sticky=W)
    rb2 = Radiobutton(mainframe, text="IAGA2000 -- Not working ", value=2, variable=fileSelection).grid(column=1, row=9, sticky=W)
    rb3 = Radiobutton(mainframe, text="IAGA2002 -- Not working", value=3, variable=fileSelection).grid(column=1, row=10, sticky=W)
    rb4 = Radiobutton(mainframe, text="Raw 2hz file", value=4, variable=fileSelection).grid(column=1, row=11, sticky=W)
    #rb5 = Radiobutton(mainframe, text="AAL-PIP", value=5, variable=fileSelection).grid(column=1, row=12, sticky=W)
    #rb6 = Radiobutton(mainframe, text="SPole", value=6, variable=fileSelection).grid(column=1, row=13, sticky=W)
    rb7 = Radiobutton(mainframe, text="other -- Not working", value=7, variable=fileSelection).grid(column=1, row=14, sticky=W)

    # file selection of type of file to save it as
    fileToSaveAs = StringVar()
    rb8 = Radiobutton(mainframe, text="pdf", value=8, variable=fileToSaveAs).grid(column=1, row=16, sticky=W)
    rb9 = Radiobutton(mainframe, text="png", value=9, variable=fileToSaveAs).grid(column=1, row=17, sticky=W)
    rb10 = Radiobutton(mainframe, text="Do not save", value=10, variable=fileToSaveAs).grid(column=1, row=18, sticky=W)

def child_formatting(mainframe):
    # child formatting in mainframe
    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    
def main(root, mainframe):
    ### Label section ###
    GUILabels()
    
    ### Entry section ###
    GUIEntries()
    
    ### Child formatting ###
    child_formatting(mainframe)

    yearday_entry.focus() # starting spot for tab control
    root.bind("<Return>", calculate) # returns the calculate funciton when called


### Setting up GUI object ###
root = Tk()
root.title("Plot input")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

main(root, mainframe)

root.mainloop() # root loop running
