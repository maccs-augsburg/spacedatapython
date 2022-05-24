

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
from turtle import home

import one_array_plotted

def year_day_entry_check(self, year_day_value):

    """
    Checks the year day entry value to see if there was a value inputted for the yearday entry box
    Parameters
    ----------
    year_day_value: the value that was inputted into the year_day_entry box
    """
    # Checking to see if any input was put in the yearday entry box
    if (len(year_day_value) == 0):
        self.error_message_pop_up(title='year_day_entry Error', message='There was no input for the year day entry box')

def station_names_entry_check(self, station_names_value):

    """
    Checks the station_code_entry value and pops up an error message if it isn't a good entry
    Parameters
    ----------
    station_code_value: the value that was inputted into the station_code_entry box
    """
    # Checking to see if no input was put in the station code entry box
    if(len(station_names_value) == 0):
        # show error as no input was received
        self.error_message_pop_up(title="Station code entry error", message="There was no input for the station code entry box")

def file_format_entry_check(self, selection_file_value):
    """
    checks the file selection value and sets the ending value to match it

    Parameters
    ----------
    selection_file_value : the value of the file selection

    Returns
    -------
    file_ending_value : the ending value of the file
    """
    if(selection_file_value == '1'):
        # CDA-Web branch (NOT IMPLEMENTED)
        self.warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

    # Testing to see if user selected IAGA2000 branch
    elif(selection_file_value == '2'):
        #IAGA2000 branch (NOT IMPLEMENTED)
        self.warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

    # Testing to see if user selected IAGA2002 branch
    elif(selection_file_value == '3'):
        #IAGA2002 branch (NOT IMPLEMENTED)
        self.warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

    # Testing to see if user selected Raw 2hz branch
    elif(selection_file_value == '4'):
        #Raw 2hz file branch (TODO: IMPLEMENT SECTION)
        file_ending_value = '.2hz'

    elif(selection_file_value == '5'):
        #Raw 2hz file branch (TODO: IMPLEMENT SECTION)
        file_ending_value = '.s2'

    # Otherwise we can assume that no option had been selected
    else:
        # Message box error when no file format option has been selected
        self.error_message_pop_up(title="File format option error", message="Please select a file format option")

    # Returning the string of the file type to be used
    return file_ending_value

def graph_from_plotter_entry_check(self, graph_from_plotter_value_x,graph_from_plotter_value_y, graph_from_plotter_value_z, xArr, yArr, zArr, timeArr, filename, stime, etime, selection_file):

    """
    Checks the gui entries for plotting, x, y, z axis. If values are set, then we plot those axis

    Parameters
    ----------
    graph_from_plotter_value_x : value from GUI, set to 1 if box is checked, 0 if not

    graph_from_plotter_value_y : value from GUI, set to 1 if box is checked, 0 if not

    graph_from_plotter_value_z : value from GUI, set to 1 if box is checked, 0 if not

    xArr : the x array values

    yArr : the y array values

    zArr : the z array values

    timeArr : the time array values

    filename : the name of the file

    stime : the start time stamp

    etime : the end time stamp

    selection_file : value from GUI, if clean is checked value is set to 4, if raw --> set to 5

    Returns
    -------
    fig : the plotted figure
    """

    # create an alias from plotter values
    x_state = graph_from_plotter_value_x
    y_state = graph_from_plotter_value_y
    z_state = graph_from_plotter_value_z
    file_state = int(selection_file)
    any_plot_state = x_state + y_state + z_state
    
    # X, Y, Z plot, clean or raw
    # first check if all on, then two the two_plot checks, last should be one_axis
    if (x_state and y_state and z_state ):

        if (file_state >= 4):
            fig = one_array_plotted.x_y_and_z_plot (xArr, yArr, zArr, timeArr, filename, stime, etime)
        
    # Y, Z plot, clean or raw
    elif (y_state and z_state):
        
        if (file_state >= 4):
            fig = one_array_plotted.plot_two_axis(yArr, zArr, timeArr, filename, stime, etime, 'Y', 'Z')
    
    # X, Z plot, clean or raw
    elif (x_state and z_state):
        
        if (file_state >= 4):
            fig = one_array_plotted.plot_two_axis(xArr, zArr, timeArr, filename, stime, etime, 'X', 'Z')
        
    # X, Y plot, clean or raw
    elif (x_state and y_state):
        
        if (file_state >= 4):
            fig = one_array_plotted.plot_two_axis(xArr, yArr, timeArr, filename, stime, etime, 'X', 'Y')
    
    # For single axis plotting
    elif ( any_plot_state > 0 and file_state > 0):
        
        if (x_state):
            fig = one_array_plotted.plot_axis(xArr, timeArr, filename, stime, etime, 'X')
        
        if(y_state):
            fig = one_array_plotted.plot_axis(yArr, timeArr, filename, stime, etime, 'Y')
        
        if(z_state):
            fig = one_array_plotted.plot_axis(zArr, timeArr, filename, stime, etime, 'Z')
            
    #Warning Message
    else:
        self.warning_message_pop_up(title = "File Format Option Error", message = "Please select a file format option")

    #return graph_from_plotter_value_x, graph_from_plotter_value_y, graph_from_plotter_value_z, fig
    return fig
    
def start_hour_entry_check(self, start_hour_string):
        
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
    # making sure the inputted value is an int not a float
    value = int(start_hour_string)

    if(value > 23):
        # Have error message box pop up because it can't be more than 23
        self.error_message_pop_up(title="Start Hour Entry Error", message="Start hour cannot be more than 23")
        
    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        self.error_message_pop_up(title="Start Hour Entry Error", message="Start hour cannot be negative")

    # Returning the start_hour_string so that whatever changes we made to it get returned
    return value

def start_minute_entry_check(self, start_minute_string):

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
    # making sure the inputted value is an int not a float
    value = int(start_minute_string)

    if(value > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        self.error_message_pop_up(title="Start Minute Entry Error", message="Start minute cannot be more than 59")

    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        self.error_message_pop_up(title="Start Minute Entry Error", message="Start minute cannot be negative")

    # Returning the start_minute_string so whatever changes we made to it get returned
    return value

def start_second_entry_check(self, start_second_string):

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
    # making sure the inputted value is an int not a float
    value = int(start_second_string)

    if(value > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        self.error_message_pop_up(title="Start Second Entry Error", message="Start second cannot be more than 59")

    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        self.error_message_pop_up(title="Start Second Entry Error", message="Start second cannot be negative")

    # Returning the start_second_string so whatever changes we made to it get returned
    return value

def end_hour_entry_check(self, end_hour_string):

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
    # making sure the inputted value is an int not a float
    value = int(end_hour_string)

    # Testing to see if the inputted value exceeds what it can be
    if(value > 23):
        # Have error message box pop up because it can't be more than 23
        self.error_message_pop_up(title="End Hour Entry Error", message="End hour cannot be more than 23")

        # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        self.error_message_pop_up(title="End Hour Entry Error", message="End hour cannot be negative")

    # Returning the end_hour_string so whatever changes we made to it get returned
    return value

def end_minute_entry_check(self, end_minute_string):

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
    # making sure the inputted value is an int not a float
    value = int(end_minute_string)

    # Testing to see if the inputted value exceeds what it can be
    if(value > 59):
        #Have error messsage box pop up becuase it can't be more than 59
        self.error_message_pop_up(title="End Minute Entry Error", message="End minute cannot be more than 59")

    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        self.error_message_pop_up(title="End Minute Entry Error", message="End minute cannot be negative")

    # Returning the end_minute_string so whatever changes we made to it get returned
    return value

def end_second_entry_check(self, end_second_string):
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
    # making sure the inputted value is an int not a float
    value = int(end_second_string)

    # Testing to see if the inputted value exceeds what it can be
    if(value > 59):
        # Have error messsage box pop up becuase it can't be more than 59
        self.error_message_pop_up(title="End Second Entry Error", message="End second cannot be more than 59")

    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        self.error_message_pop_up(title="End Second Entry Error", message="End second cannot be negative")

    # Returning the end_second_string so whatever changes we made to it get returned
    return value

def error_message_pop_up(self, title, message):
        
    # pops up error message box with the title and message inputted
    messagebox.showerror(title=title, message = "ERROR: " + message)
    sys.exit(0)

def warning_message_pop_up(self, title, message):
    # pops up warning message box with the title and message inputted
    messagebox.showwarning(title=title, message="WARNING: " + message)
        