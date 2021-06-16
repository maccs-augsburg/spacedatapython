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
#   documentation ---------------------------------------------------------------------------------> done
#   main function ---------------------------------------------------------------------------------> working on
#   error message popup function ------------------------------------------------------------------> done
#   general gui function -------------------------------------------------------------------------->
#   gui display function -------------------------------------------------------------------------->
#   change calculate function name to something like display plot --------------------------------->
#   view box around radio buttons ----------------------------------------------------------------->
#   go through and fully comment code ------------------------------------------------------------->
#   variable names change -------------------------------------------------------------------------> done
#--------------------------------------------------------------------------------------------------------------

# tkinter imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Python 3 imports
import sys
import datetime

def error_message_pop_up(title, message):
    """
    Creates an error pop up message box with the given title and message

    Parameters
    ----------
    String
        title: the string message of the pop up box that is the title
        message: the string message of the pop up box to be used as the message of why the error occurred
    """
    messagebox.showerror(title = title, message = "ERROR: " + message)
    sys.exit(0)

def year_day_entry_check(year_day_value):
    """
    Checks the year day entry value and pops up an error message if it isn't a good entry

    Parameters
    ----------
    String
        year_day_value: the value that was inputted into the year_day_entry box
    """
    
    if(len(year_day_value) == 0):
        # show error as no input was received
        # using tkinter's message box
        error_message_pop_up(title="year_day Entry Error", message="There was no input for the year_day entry box")

def calculate(*args):
    """
    Obtains the values entered in the GUI and runs the plotting program with the inputted values

    (*args is technically a parameter but it isn't required) -- Not sure what to do here for this documentation?
    the way to call this function would look something like this: "root.bind("<Return>", calculate)"
    """
### Getting input values ###

    ### year_day entry ###
    year_day_value = year_day_entry.get()
    year_day_entry_check(year_day_value)
    

    ### Start hour, minute, and second entries ###
    start_hour_value = start_hour_entry.get()
    start_minute_value = start_minute_entry.get()
    start_second_value = start_second_entry.get()

    # Start hour portion
    if(len(start_hour_value) == 1): 
        # Adding a zero to the start so that it is in the correct format
        start_hour_value = "0" + start_hour_value
    if((int)(start_hour_value) > 23):
        # Have error message box pop up because it can't be more than 23
        error_message_pop_up(title="Start Hour Entry Error", message="Start hour cannot be more than 23")

    # Start minute portion
    if(len(start_minute_value) == 1):
        # Adding a zero to the start so that it is in the correct format
        start_minute_value = "0" + start_minute_value
    if((int)(start_minute_value) > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        error_message_pop_up(title="Start Minute Entry Error", message="Start minute cannot be more than 59")

    # Start second portion
    if(len(start_second_value) == 1):
        # Adding a zero to the start so that it is in the correct format
        start_second_value = "0" + start_second_value
    if((int)(start_second_value) > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        error_message_pop_up(title="Start Second Entry Error", message="Start second cannot be more than 59")

    start_time_stamp = datetime.time.fromisoformat(start_hour_value + ":" + start_minute_value + ":" + start_second_value)
           
    ### End hour, minute, and second entries ###
    end_hour_value = end_hour_entry.get()
    end_minute_value = end_minute_entry.get()
    end_second_value = end_second_entry.get()

    # End hour portion
    if(len(end_hour_value) == 1):
        # Adding a zero to the start so that it is in the correct format
        end_hour_value = "0" + end_hour_value
    if((int)(end_hour_value) > 23):
        # Have error message box pop up because it can't be more than 23
        error_message_pop_up(title="End Hour Entry Error", message="End hour cannot be more than 23")
        
    # End minute portion
    if(len(end_minute_value) == 1):
        # Adding a zero to the start so that it is in the correct format
        end_minute_value = "0" + end_minute_value
    if((int)(end_minute_value) > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        error_message_pop_up(title="End Minute Entry Error", message="End minute cannot be more than 59")

    # End second portion
    if(len(end_second_value) ==1):
        # Adding a zero to the start so that it is in the correct format
        end_second_value = "0" + end_second_value
    if((int)(end_second_value) > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        error_message_pop_up(title="End Second Entry Error", message="End second cannot be more than 59")

    end_time_stamp = datetime.time.fromisoformat(end_hour_value + ":" + end_minute_value + ":" + end_second_value)
    
    ### Plot min and max entries ###
    plot_min_default_flag = False
    plot_max_default_flag = False
    
    plot_min_value = plot_min_entry.get()
    if(plot_min_value == '0'): 
        # use default params
        plot_min_default_flag = True

    plot_max_value = plot_max_entry.get()
    if(plot_max_value == '0'):
        # use default params
        plot_max_default_flag = True

    ### Station code entry ###
    station_code_value = station_code_entry.get()
    if(len(station_code_value) == 0):
        # show error as no input was received
        error_message_pop_up(title="Station code entry error", message="There was no input for the station code entry box")

    ### File format entry ###

    # radio_button_ buttons used: 1, 2, 3, 4, 7
    file_selection_value = file_selection.get()
    if(file_selection_value == '1'):
        # CDA-Web branch (NOT IMPLEMENTED)
        pass
    elif(file_selection_value == '2'):
        #IAGA2000 branch (NOT IMPLEMENTED)
        pass
    elif(file_selection_value == '3'):
        #IAGA2002 branch (NOT IMPLEMENTED)
        pass
    elif(file_selection_value == '4'):
        #Raw 2hz file branch (TODO: IMPLEMENT SECTION)
        pass
    elif(file_selection_value == '7'):
        #Other option branch (NOT IMPLEMENTED YET)
        pass
    else:
        # Message box error when no file format option has been selected
        error_message_pop_up(title="File format option error", message="Please select a file format option")
        
    ### File option to save as entry ###

    # radio_button_ buttons used: 8, 9, 10
    file_save_as_option_value = file_to_save_as.get()
    if(file_save_as_option_value == '8'):
        #pdf branch
        pass
    elif(file_save_as_option_value == '9'):
        #png branch
        pass
    elif(file_save_as_option_value == '10'):
        #Do not save branch
        pass
    else:
        # Message box error when no file save option has been selected
        error_message_pop_up(title="File Save Option error", message="Please select an option to save the file as")

def cancel(*args):
    """
    Cancel function quits out of the gui when run.
    It doesn't save any variables or store any information,
    it just destroys everything for that current GUI.
    """
    root.destroy() # Exiting without running any code after
    #global.root
    #root.quit() # Exiting with running code after

def GUI_labels():
    """
    Creates the Labels and places them into the GUI. 
    """
    # year_day label
    ttk.Label(mainframe, text="year_day:").grid(column=1, row=1, sticky=W)

    # Start time labels
    ttk.Label(mainframe, text="Start Hour:").grid(column=1, row=2, sticky=W)
    ttk.Label(mainframe, text="Start Minute:").grid(column=2, row=2, sticky=W)
    ttk.Label(mainframe, text="start_second:").grid(column=4, row=2, sticky=W)

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

def GUI_entries():
    """
    Creates the entry boxes and places them into the GUI.
    """
    ### Global variables ###
    global year_day, year_day_entry
    global start_hour, start_hour_entry, start_minute, start_minute_entry, start_second, start_second_entry
    global end_hour, end_hour_entry, end_minute, end_minute_entry, end_second, end_second_entry
    global plot_min, plot_min_entry, plot_max, plot_max_entry
    global station_code, station_code_entry
    global file_selection, radio_button_1, radio_button_2, radio_button_3, radio_button_4, radio_button_7, file_to_save_as, radio_button_8, radio_button_9, radio_button_10
    
    # year_day entry
    year_day = StringVar() ## storing as a string for now, might change to int later
    year_day_entry = ttk.Entry(mainframe, width=6, textvariable=year_day) # setting a variable with the Entry box format
    year_day_entry.grid(column=1, row=1) # selecting which column and row to place said variable

    # Start Hour entry
    start_hour = IntVar()
    start_hour.set(0)
    start_hour_entry = ttk.Entry(mainframe, width=3, textvariable=start_hour)
    start_hour_entry.grid(column=1, row=2)

    # Start Minute entry
    start_minute = IntVar()
    start_minute_entry = ttk.Entry(mainframe, width=3, textvariable=start_minute)
    start_minute_entry.grid(column=3, row=2, sticky=W)

    # Start Second entry
    start_second = IntVar()
    start_second_entry = ttk.Entry(mainframe, width=3, textvariable=start_second)
    start_second_entry.grid(column=5, row=2, sticky=W)

    # End Hour entry
    end_hour = IntVar()
    end_hour.set(23)
    end_hour_entry = ttk.Entry(mainframe, width=3, textvariable=end_hour)
    end_hour_entry.grid(column=1, row=3)

    # End Minute entry
    end_minute = IntVar()
    end_minute.set(59)
    end_minute_entry = ttk.Entry(mainframe, width=3, textvariable=end_minute)
    end_minute_entry.grid(column=3, row=3, sticky=W)

    # End Second entry
    end_second = IntVar()
    end_second.set(59)
    end_second_entry = ttk.Entry(mainframe, width=3, textvariable=end_second)
    end_second_entry.grid(column=5, row=3, sticky=W)

    # Plot min and Plot max entries
    plot_min = IntVar()
    plot_min_entry = ttk.Entry(mainframe, width=3, textvariable=plot_min)
    plot_min_entry.grid(column=2, row=4, sticky=W)
    plot_max = IntVar()
    plot_max_entry = ttk.Entry(mainframe, width=3, textvariable=plot_max)
    plot_max_entry.grid(column=2, row=5, sticky=W)

    # Station file entries
    station_code = StringVar()
    station_code_entry = ttk.Entry(mainframe, width=4, textvariable=station_code)
    station_code_entry.grid(column=1, row=6)

    ### Button section ###
    # Management buttons section
    ok_button = ttk.Button(mainframe, text="OK", command=calculate).grid(column=2, row = 19, sticky=W)
    cancel_button = ttk.Button(mainframe, text="Cancel", command=cancel).grid(column=3, row=19, sticky=E)

    # Radiobutton section
    # file selection of type of file to open
    file_selection = StringVar()
    radio_button_1 = Radiobutton(mainframe, text="CDAWEB -- Not working", value=1, variable=file_selection).grid(column=1, row=8, sticky=W)
    radio_button_2 = Radiobutton(mainframe, text="IAGA2000 -- Not working ", value=2, variable=file_selection).grid(column=1, row=9, sticky=W)
    radio_button_3 = Radiobutton(mainframe, text="IAGA2002 -- Not working", value=3, variable=file_selection).grid(column=1, row=10, sticky=W)
    radio_button_4 = Radiobutton(mainframe, text="Raw 2hz file", value=4, variable=file_selection).grid(column=1, row=11, sticky=W)
    #radio_button_5 = Radiobutton(mainframe, text="AAL-PIP", value=5, variable=file_selection).grid(column=1, row=12, sticky=W)
    #radio_button_6 = Radiobutton(mainframe, text="SPole", value=6, variable=file_selection).grid(column=1, row=13, sticky=W)
    radio_button_7 = Radiobutton(mainframe, text="other -- Not working", value=7, variable=file_selection).grid(column=1, row=14, sticky=W)

    # file selection of type of file to save it as
    file_to_save_as = StringVar()
    radio_button_8 = Radiobutton(mainframe, text="pdf", value=8, variable=file_to_save_as).grid(column=1, row=16, sticky=W)
    radio_button_9 = Radiobutton(mainframe, text="png", value=9, variable=file_to_save_as).grid(column=1, row=17, sticky=W)
    radio_button_10 = Radiobutton(mainframe, text="Do not save", value=10, variable=file_to_save_as).grid(column=1, row=18, sticky=W)

def child_formatting(mainframe):
    """
    Formats the x and y pads for each child/object in the mainframe

    Parameters
    ----------
    Frame
        mainframe: a frame object that holds and stores the attributes and objects of the GUI frame
    """
    # child formatting in mainframe
    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    
def main(root, mainframe):
    """
    Main place that organizes and runs all functions to make up a functioning GUI

    Parameters
    ----------
    Tk
        root: Tk object to allow for creating a GUI with Tkinter
    Frame
        mainframe: a frame object that holds and stores the attributes and objects of the GUI frame
    """
    ### Label section ###
    GUI_labels()
    
    ### Entry section ###
    GUI_entries()
    
    ### Child formatting ###
    child_formatting(mainframe)

    year_day_entry.focus() # starting spot for tab control
    root.bind("<Return>", calculate) # returns the calculate funciton when called


if __name__ == "__main__":
    ### Setting up GUI object ###
    root = Tk()
    root.title("Plot input")
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    main(root, mainframe)

    root.mainloop() # root loop running
