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
#   implement functionality -----------------------------------------------------------------------> working on
#       - use the default flags and determine y-axis scaling -----> 
#       - add try and catch blocks -------------------------------> 
#   view box around radio buttons ----------------------------------------------------------------->
#   do not save option rectangles to move all subplots at the same time ---------------------------> 
#
#   Change values to integers ---------------------------------------------------------------------> done
#--------------------------------------------------------------------------------------------------------------

# tkinter imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Python 3 imports
import sys
import datetime

# Plotter program imports
import raw_to_plot
import file_naming
import read_raw_to_lists

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

    #TODO: Add more tests to get yearday values

"""def date_time_object_check(string_value):
    
    Checks to see if the time string is a single digit, if so it converts it so that it can be used in the datetime format of HH:MM:SS

    Parameters
    ----------
    String
        string_value: the string of digit/s to check to see if can be used for datetime format

    Returns
    -------
    String
        string_value: altered (or not) to be in the correct state for being used in the datetime module
    
    #
    if(len(string_value) == 1):
        # Adding a zero to the start so that it is in the correct format if inputted value is a single digit
        #   This is so we have the format "00:00:00" for the datetime object
        string_value = "0" + string_value

    return string_value"""

def start_hour_entry_check(start_hour_string):
    """
    Checks the start hour entry value and pops up an error message if it isn't a good entry

    Parameters
    ----------
    String
        start_hour_string: the value that was inputted into the start_hour_entry box

    Returns
    -------
    Int
        value: the int version of the inputted value in the start_hour_entry box
    """
    value = int(start_hour_string)
    
    ### Start hour input tests ###
    # Testing to see if the inputted value exceeds what it can be
    if(value > 23):
        # Have error message box pop up because it can't be more than 23
        error_message_pop_up(title="Start Hour Entry Error", message="Start hour cannot be more than 23")
        
    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        error_message_pop_up(title="Start Hour Entry Error", message="Start hour cannot be negative")

    # Returning the start_hour_string so that whatever changes we made to it get returned
    return value


def start_minute_entry_check(start_minute_string):
    """
    Checks the start minute entry value and pops up an error message if it isn't a good entry

    Parameters
    ----------
    String
        start_minute_string: the value that was inputted into the start_minute_entry box

    Returns
    -------
    Int
        value: the inputted value in the start_minute_entry box
    """
    value = int(start_minute_string)
    
    ### Start minute input tests ###
    # Testing to see if the inputted value exceeds what it can be
    if(value > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        error_message_pop_up(title="Start Minute Entry Error", message="Start minute cannot be more than 59")

    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        error_message_pop_up(title="Start Minute Entry Error", message="Start minute cannot be negative")

    # Returning the start_minute_string so whatever changes we made to it get returned
    return value

def start_second_entry_check(start_second_string):
    """
    Checks the start second entry value and pops up an error message if it isn't a good entry

    Parameters
    ----------
    String
        start_second_string: the value that was inputted into the start_second_entry box

    Returns
    -------
    Int
        value: the inputted value in the start_second_entry box
    """
    value = int(start_second_string)
    
    ### Start second input tests ###
    # Testing to see if the inputted value exceeds what it can be    
    if(value > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        error_message_pop_up(title="Start Second Entry Error", message="Start second cannot be more than 59")

    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        error_message_pop_up(title="Start Second Entry Error", message="Start second cannot be negative")

    # Returning the start_second_string so whatever changes we made to it get returned
    return value

def end_hour_entry_check(end_hour_string):
    """
    Checks the end hour entry value and pops up an error message if it isn't a good entry

    Parameters
    ----------
    String
        end_hour_string: the value that was inputted into the end_hour_entry box

    Returns
    -------
    Int
        value: the inputted value in the end_hour_entry box
    """
    value = int(end_hour_string)
    
    ### End hour input tests ###
    # Testing to see if the inputted value exceeds what it can be
    if(value > 23):
        # Have error message box pop up because it can't be more than 23
        error_message_pop_up(title="End Hour Entry Error", message="End hour cannot be more than 23")

    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        error_message_pop_up(title="End Hour Entry Error", message="End hour cannot be negative")

    # Returning the end_hour_string so whatever changes we made to it get returned
    return value

def end_minute_entry_check(end_minute_string):
    """
    Checks the end minute entry value and pops up an error message if it isn't a good entry

    Parameters
    ----------
    String
        end_minute_string: the value that was inputted into the end_minute_entry box

    Returns
    -------
    Int
        value: the inputted value in the end_hour_entry box
    """
    value = int(end_minute_string)
    
    ### End minute input tests ###
    # Testing to see if the inputted value exceeds what it can be
    if(value > 59):
        #Have error messsage box pop up becuase it can't be more than 59
        error_message_pop_up(title="End Minute Entry Error", message="End minute cannot be more than 59")

    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        error_message_pop_up(title="End Minute Entry Error", message="End minute cannot be negative")

    # Returning the end_minute_string so whatever changes we made to it get returned
    return value

def end_second_entry_check(end_second_string):
    """
    Checks the end second entry value and pops up an error message if it isn't a good entry

    Parameters
    ----------
    String
        end_second_string: the value that was inputted into the end_second_entry box

    Returns
    -------
    Int
        end_second_string: the inputted value in the end_second_entry box
    """
    value = int(end_second_string)
    
    ### End second input tests ###
    # Testing to see if the inputted value exceeds what it can be
    if(value > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        error_message_pop_up(title="End Second Entry Error", message="End second cannot be more than 59")

    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        error_message_pop_up(title="End Second Entry Error", message="End second cannot be negative")

    # Returning the end_second_string so whatever changes we made to it get returned
    return value

def plot_min_default_flag_check(plot_min_value):
    """
    Determines to use default values for scaling on the y-axis in the plot or if to use custom min values

    Parameters
    ----------
    String
        plot_min_value: the value from the plot_min_entry box in the GUI

    Returns
    -------
    Boolean
        plot_min_default_flag: which is true if we use default values, and false if we should use custom values
    """
    ### Plot min default flag input tests ###
    # Setting the flag initially to be false
    plot_min_default_flag = False

    # Checking to see if the inputted value was untouched or set to zero to keep default selection
    if(plot_min_value == '0'): 
        # use default params if value is equal to zero
        # and update the flag
        plot_min_default_flag = True

    # Return the results
    return plot_min_default_flag

def plot_max_default_flag_check(plot_max_value):
    """
    Determines to use default values for scaling on the y-axis in the plot or if to use custom max values

    Parameters
    ----------
    String
        plot_max_value: the value from the plot_max_entry box in the GUI

    Returns
    -------
    Boolean
        plot_max_default_flag: which is true if we use default values, and false if we should use custom values
    """
    ### Plot max default flag input tests ###
    # Setting the flag initially to be false
    plot_max_default_flag = False

    # Checking to see if the inputted value was untouched or set to zero to keep default selection
    if(plot_max_value == '0'):
        # use default params if value is equal to zero
        # and update the flag
        plot_max_default_flag = True

    # Return the results
    return plot_max_default_flag

def plot_min_and_max_check(plot_min_value, plot_max_value):
    """
    Helper function to run both functions to test for whether to use default values or custom values for y-axis scaling and returns the results

    Parameters
    ----------
    String
        plot_min_value: the value from the plot_min_entry box in the GUI
        plot_max_value: the value from the plot_max_entry box in the GUI

    Returns
    -------
    Boolean
        plot_min_default_flag: which is true if we use default values, and false if we should use custom values
        plot_max_default_flag: which is true if we use default values, and false if we should use custom values
    """
    # Run both plotting min and max related functions and store the results
    plot_min_default_flag = plot_min_default_flag_check(plot_min_value)
    plot_max_default_flag = plot_max_default_flag_check(plot_max_value)

    # Return the results so we know if we should use default values or custom values
    return plot_min_default_flag, plot_max_default_flag

def station_code_entry_check(station_code_value):
    """
    Checks the station_code_entry value and pops up an error message if it isn't a good entry

    Parameters
    ----------
    String
        station_code_value: the value that was inputted into the station_code_entry box
    """
    ### Station code input tests ###
    # Checking to see if no input was put in the station code entry box
    if(len(station_code_value) == 0):
        # show error as no input was received
        error_message_pop_up(title="Station code entry error", message="There was no input for the station code entry box")
        
def file_format_entry_checker(file_selection_value):
    """
    Checks the file_selection_entry value and either pops up a message if input was bad or specifies the ending value of the filename which specifies which type of file to use

    Parameters
    ----------
    String
        file_selection_value: the value that was inputted into the file_selection_entry box

    Returns
    -------
    String
        file_ending_value: the value that specifies the type of file to use
        
    """
    ### File format input tests ###
    # Setting the initial file ending value to an empty string
    file_ending_value = ''

    # Testing to see if user selected CDA-Web branch
    if(file_selection_value == '1'):
        # CDA-Web branch (NOT IMPLEMENTED)
        warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

    # Testing to see if user selected IAGA2000 branch
    elif(file_selection_value == '2'):
        #IAGA2000 branch (NOT IMPLEMENTED)
        warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

    # Testing to see if user selected IAGA2002 branch
    elif(file_selection_value == '3'):
        #IAGA2002 branch (NOT IMPLEMENTED)
        warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

    # Testing to see if user selected Raw 2hz branch
    elif(file_selection_value == '4'):
        #Raw 2hz file branch (TODO: IMPLEMENT SECTION)
        file_ending_value = '.2hz'

    # Testing to see if user selected other branch
    elif(file_selection_value == '7'):
        #Other option branch (NOT IMPLEMENTED YET) -- for now just show warning message and exit
        warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

    # Otherwise we can assume that no option had been selected
    else:
        # Message box error when no file format option has been selected
        error_message_pop_up(title="File format option error", message="Please select a file format option")

    # Returning the string of the file type to be used
    return file_ending_value

def file_save_as_entry_checker(file_save_as_option_value):
    """
    Checks the file_save_as_option_value and pops up an error message if the input is bad or sets the string file option to be used later on by the program

    Parameters
    ----------
    String
        file_save_as_option_value: the value that was inputted into the file_save_as_entry box

    Returns
    -------
    String
        file_save_as_option: the string to indicate in which way we are saving the file
    """
    ### File save as input tests ###
    # Setting the initial file save as value to an empty string
    file_save_as_option = ''

    # Testing to see if user selected pdf branch
    if(file_save_as_option_value == '8'):
        #pdf branch
        file_save_as_option = 'pdf'

    # Testing to see if user selected png branch
    elif(file_save_as_option_value == '9'):
        #png branch
        file_save_as_option = 'png'

    # Testing to see if user selected do not save branch
    elif(file_save_as_option_value == '10'):
        #Do not save branch
        file_save_as_option = 'no'
        
    elif(file_save_as_option_value == '1'):
        # Save as both branch
        file_save_as_option = 'pdf and png'

    # Otherwise we can assume that no option had been selected
    else:
        # Message box error when no file save option has been selected
        error_message_pop_up(title="File Save Option error", message="Please select an option to save the file as")

    # Returning the string of the file save as option to be used
    return file_save_as_option

def execute_functions(*args): # change to some other function name like "execute_okay_button" or "execute_functions" etc.
    """
    Obtains the values entered in the GUI and runs the plotting program with the inputted values
    """

    ### Input values ### --------------------------------------------------------------------------------------

    ### year_day entry ###
    year_day_value = year_day_entry.get()
    year_day_entry_check(year_day_value)
    

    ### Start hour, minute, and second entries ###
    start_hour_value = start_hour_entry_check(start_hour_entry.get())
    
    start_minute_value = start_minute_entry_check(start_minute_entry.get())
    
    start_second_value = start_second_entry_check(start_second_entry.get())

    start_time_stamp = datetime.time(hour=start_hour_value, minute=start_minute_value, second=start_second_value)

           
    ### End hour, minute, and second entries ###
    end_hour_value = end_hour_entry_check(end_hour_entry.get())
    
    end_minute_value = end_minute_entry_check(end_minute_entry.get())
    
    end_second_value = end_second_entry_check(end_second_entry.get())

    end_time_stamp = datetime.time(hour=end_hour_value, minute=end_minute_value, second=end_second_value)
    
    ### Plot min and max entries ###
    plot_min_value_x = plot_min_entry_x.get()
    plot_max_value_x = plot_max_entry_x.get()
    plot_min_value_y = plot_min_entry_y.get()
    plot_max_value_y = plot_max_entry_y.get()
    plot_min_value_z = plot_min_entry_z.get()
    plot_max_value_z = plot_min_entry_z.get()

    #plot_min_default_flag, plot_max_default_flag = plot_min_and_max_check(plot_min_value, plot_max_value) 

    ### Station code entry ###
    station_code_value = station_code_entry.get()
    station_code_entry_check(station_code_value)

    ### File format entry ###
    # radio_button_ buttons used: 1, 2, 3, 4, 7
    file_selection_value = file_selection.get()
    file_ending_value = file_format_entry_checker(file_selection_value)
    
        
    ### File option to save as entry ###
    # radio_button_ buttons used: 8, 9, 10
    #file_save_as_option_value = file_to_save_as.get()
    file_save_as_option_value = '1'
    file_save_as_option_value = file_save_as_entry_checker(file_save_as_option_value)

    ### End Input values ### ----------------------------------------------------------------------------------

    
    ### Putting information gathered together and calling the plotting program! ### ---------------------------
    file_name_full = station_code_value + year_day_value + file_ending_value
    time_interval_string = file_naming.create_time_interval_string_hms(start_hour_value, start_minute_value, start_second_value, end_hour_value, end_minute_value, end_second_value)
    file_name = station_code_value + year_day_value + time_interval_string
    
    # Opening the file
    try:
        file = open(file_name_full, 'rb')
    except:
        error_message_pop_up("File open error", "Couldn't find and open filename")
        sys.exit(0)
    
    # Creating the arrays from the file
    xArr, yArr, zArr, timeArr = raw_to_plot.create_arrays(file, start_time_stamp, end_time_stamp)

    # Plotting the arrays
    raw_to_plot.plot_arrays(xArr, yArr, zArr, timeArr, file_name, start_time_stamp, end_time_stamp, file_save_as_option_value)

    plotter_complete_message(title="Plotting Program Complete", message="The plotting program has plotted your desired file!") 
    ### End Putting information gathered together and calling the plotting program! ### -----------------------
    

def cancel(root):
    """
    Cancel function quits out of the gui when run.
    It doesn't save any variables or store any information,
    it just destroys everything for that current GUI.
    """
    root.destroy() # Exiting without running any code after

def gui_labels(mainframe):
    """
    Creates the Labels and places them into the GUI.

    Parameters
    ----------
    Frame
        mainframe: the ttk frame object to save labels to
    """
    # year_day label
    ttk.Label(mainframe, text="Year Day:").grid(column=2, row=1, sticky=W)

    # Start time labels
    ttk.Label(mainframe, text="Start Hour:").grid(column=1, row=2, sticky=W)
    ttk.Label(mainframe, text="Start Minute:").grid(column=2, row=2, sticky=W)
    ttk.Label(mainframe, text="Start Second:").grid(column=4, row=2, sticky=W)

    # End time labels
    ttk.Label(mainframe, text="End Hour:").grid(column=1, row=3, sticky=W)
    ttk.Label(mainframe, text="End Minute:").grid(column=2, row=3, sticky=W)
    ttk.Label(mainframe, text="End Second:").grid(column=4, row=3, sticky=W)

    # Plot min and max labels
    # X labels
    ttk.Label(mainframe, text="Plot Min x (leave at 0 for default):").grid(column=1, row=4, sticky=W)
    ttk.Label(mainframe, text="Plot Max x (leave at 0 for default):").grid(column=1, row=5, sticky=W)
    # Y labels
    ttk.Label(mainframe, text="Plot Min y (leave at 0 for default):").grid(column=1, row=6, sticky=W)
    ttk.Label(mainframe, text="Plot Max y (leave at 0 for default):").grid(column=1, row=7, sticky=W)   
    #Z labels
    ttk.Label(mainframe, text="Plot Min z (leave at 0 for default):").grid(column=1, row=8, sticky=W)
    ttk.Label(mainframe, text="Plot Max z (leave at 0 for default):").grid(column=1, row=9, sticky=W)
    
    # Station file label
    ttk.Label(mainframe, text="Station code:").grid(column=1, row=1, sticky=W)

    # File format label
    ttk.Label(mainframe, text="Format of file to Open (pick from list below)").grid(column=1, row=10, sticky=W)


    # File save as label
    #ttk.Label(mainframe, text="Save file as (pick from list below)").grid(column=1, row=15, sticky=W)

def gui_entries(mainframe, root):
    """
    Creates the entry boxes and places them into the GUI.

    Parameters
    ----------
    Frame
        mainframe: the ttk frame object to save labels to
    Tk
        root: the main Tk object that runs the gui window (this is just used for the okay and cancel buttons)
    """
    ### Global variables ###
    global year_day_entry
    global start_hour, start_hour_entry, start_minute, start_minute_entry, start_second, start_second_entry
    global end_hour, end_hour_entry, end_minute, end_minute_entry, end_second, end_second_entry
    global plot_min_x, plot_max_x, plot_min_entry_x, plot_max_entry_x
    global plot_min_y, plot_max_y, plot_min_entry_y, plot_max_entry_y
    global plot_min_z, plot_max_z, plot_min_entry_z, plot_max_entry_z
    global station_code, station_code_entry
    global file_selection, radio_button_1, radio_button_2, radio_button_3, radio_button_4, radio_button_7, file_to_save_as, radio_button_8, radio_button_9, radio_button_10

    # Station file entries
    station_code = StringVar()
    station_code_entry = ttk.Entry(mainframe, width=4, textvariable=station_code)
    station_code_entry.grid(column=1, row=1)
    
    # year_day entry
    year_day = StringVar() ## storing as a string for now, might change to int later
    year_day_entry = ttk.Entry(mainframe, width=6, textvariable=year_day) # setting a variable with the Entry box format
    year_day_entry.grid(column=3, row=1, sticky=W) # selecting which column and row to place said variable

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
    # Plot min and max x
    plot_min_x = IntVar()
    plot_min_x.set(0)
    plot_min_entry_x = ttk.Entry(mainframe, width=3, textvariable=plot_min_x)
    plot_min_entry_x.grid(column=2, row=4, sticky=W)
    plot_max_x = IntVar()
    plot_max_x.set(0)
    plot_max_entry_x = ttk.Entry(mainframe, width=3, textvariable=plot_max_x)
    plot_max_entry_x.grid(column=2, row=5, sticky=W)

    plot_min_y = IntVar()
    plot_min_y.set(0)
    plot_min_entry_y = ttk.Entry(mainframe, width=3, textvariable=plot_min_y)
    plot_min_entry_y.grid(column=2, row=6, sticky=W)
    plot_max_y = IntVar()
    plot_max_y.set(0)
    plot_max_entry_y = ttk.Entry(mainframe, width=3, textvariable=plot_max_y)
    plot_max_entry_y.grid(column=2, row=7, sticky=W)

    plot_min_z = IntVar()
    plot_min_z.set(0)
    plot_min_entry_z = ttk.Entry(mainframe, width=3, textvariable=plot_min_z)
    plot_min_entry_z.grid(column=2, row=8, sticky=W)
    plot_max_z = IntVar()
    plot_max_z.set(0)
    plot_max_entry_z = ttk.Entry(mainframe, width=3, textvariable=plot_max_z)
    plot_max_entry_z.grid(column=2, row=9,sticky=W)

    ### Button section ###

    # Radiobutton section
    # file selection of type of file to open
    file_selection = StringVar()
    radio_button_1 = Radiobutton(mainframe, text="CDAWEB -- Not working", value=1, variable=file_selection).grid(column=1, row=11, sticky=W)
    radio_button_2 = Radiobutton(mainframe, text="IAGA2000 -- Not working ", value=2, variable=file_selection).grid(column=1, row=12, sticky=W)
    radio_button_3 = Radiobutton(mainframe, text="IAGA2002 -- Not working", value=3, variable=file_selection).grid(column=1, row=13, sticky=W)
    radio_button_4 = Radiobutton(mainframe, text="Raw 2hz file", value=4, variable=file_selection).grid(column=1, row=14, sticky=W)
    #radio_button_5 = Radiobutton(mainframe, text="AAL-PIP", value=5, variable=file_selection).grid(column=1, row=12, sticky=W)
    #radio_button_6 = Radiobutton(mainframe, text="SPole", value=6, variable=file_selection).grid(column=1, row=13, sticky=W)
    radio_button_7 = Radiobutton(mainframe, text="other -- Not working", value=7, variable=file_selection).grid(column=1, row=15, sticky=W)

    # file selection of type of file to save it as
    #file_to_save_as = StringVar()
    #radio_button_8 = Radiobutton(mainframe, text="pdf", value=8, variable=file_to_save_as).grid(column=1, row=16, sticky=W)
    #radio_button_9 = Radiobutton(mainframe, text="png", value=9, variable=file_to_save_as).grid(column=1, row=17, sticky=W)
    #radio_button_10 = Radiobutton(mainframe, text="Do not save", value=10, variable=file_to_save_as).grid(column=1, row=18, sticky=W)

    # Management buttons section
    plot_button = ttk.Button(mainframe, text="Plot", command=execute_functions).grid(column=2, row = 19, sticky=W)
    cancel_button = ttk.Button(mainframe, text="Cancel", command=lambda: cancel(root)).grid(column=3, row=19, sticky=E)
    
def main():
    """
    Sets up  object, calls _labels and _entries, formats children in mainframe and calls root's mainloop function
    """
    
    ### Setting up GUI object ###
    root = Tk()
    root.title("Plot input")
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    ### Label section ###
    gui_labels(mainframe)    
    
    ### Entry section ###
    gui_entries(mainframe, root)
    
    ### Child formatting ###
    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    station_code_entry.focus() # starting spot for tab control
    
    root.bind("<Return>", execute_functions)

    root.mainloop() # root loop running


if __name__ == "__main__":
    main()

    
