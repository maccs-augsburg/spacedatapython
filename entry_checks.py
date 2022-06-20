## Created by: Annabelle Arns 

# Entry Check file moved from line_XYZ.py by Chris Hance 
# Refactored by Chris Hance 2022
# Now using PySide GUI to display warning pop ups and Error Messeges 
# Test bench // Checking each Entry from the file input for proper values
# and then graphs the proper plot

import plot_three_axis_graphs
import view_maccsGUI


def year_day_entry_check( self,year_day_value):

    """
    Checks the year day entry value to see if there was a value inputted for the yearday entry box
    Parameters
    ----------
    year_day_value: the value that was inputted into the year_day_entry box
    """
    # Checking to see if any input was put in the yearday entry box
    if (len(year_day_value) == 0):
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Time Entry Error", "Invalid time entry in Year Day box \nValue invalid; Most likely empty\nPlease make sure value on file is correct")

def station_names_entry_check(self,station_names_value):

    """
    Checks the station_code_entry value and pops up an error message if it isn't a good entry
    Parameters
    ----------
    station_code_value: the value that was inputted into the station_code_entry box
    """
    # Checking to see if no input was put in the station code entry box
    if(len(station_names_value) == 0):
        # show error as no input was received
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Station Code Error", "Invalid Station Code on file \nPlease make sure you select proper file \nExiting program")

def file_format_entry_check(self,selection_file_value):
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
        view_maccsGUI.MainWindow.warning_message_pop_up(self, "File format option error", "Sorry! But we don't have this option available yet, please try picking a different option")

    # Testing to see if user selected IAGA2000 branch
    elif(selection_file_value == '2'):
        #IAGA2000 branch (NOT IMPLEMENTED)
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"File format option error", "Sorry! But we don't have this option available yet, please try picking a different option")

    # Testing to see if user selected IAGA2002 branch
    elif(selection_file_value == '3'):
        #IAGA2002 branch (NOT IMPLEMENTED)
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"File format option error", "Sorry! But we don't have this option available yet, please try picking a different option")

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
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"File open error", "Couldn't find and open your file \nPlease make sure you select proper file \nPlease try again.")

    # Returning the string of the file type to be used
    return file_ending_value

def graph_from_plotter_entry_check(self,graph_from_plotter_value_x,graph_from_plotter_value_y, graph_from_plotter_value_z, xArr, yArr, zArr, timeArr, filename, stime, etime, selection_file,zoom, left_xlim, right_xlim):

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
            fig = plot_three_axis_graphs.x_y_and_z_plot (xArr, yArr, zArr, timeArr, filename, stime, etime)
        
    # Y, Z plot, clean or raw
    elif (y_state and z_state):
        
        if (file_state >= 4):
            fig = plot_three_axis_graphs.plot_two_axis(yArr, zArr, timeArr, filename, stime, etime, 'Y', 'Z')
    
    # X, Z plot, clean or raw
    elif (x_state and z_state):
        
        if (file_state >= 4):
            fig = plot_three_axis_graphs.plot_two_axis(xArr, zArr, timeArr, filename, stime, etime, 'X', 'Z')
        
    # X, Y plot, clean or raw
    elif (x_state and y_state):
        
        if (file_state >= 4):
            fig = plot_three_axis_graphs.plot_two_axis(xArr, yArr, timeArr, filename, stime, etime, 'X', 'Y')
    
    # For single axis plotting
    elif ( any_plot_state > 0 and file_state > 0):
        
        if (x_state):
            print(zoom)
            print(left_xlim)
            print(right_xlim)
            fig = plot_three_axis_graphs.plot_axis(xArr, timeArr, filename, stime, etime, 'X',zoom, left_xlim, right_xlim)
        
        if(y_state):
            fig = plot_three_axis_graphs.plot_axis(yArr, timeArr, filename, stime, etime, 'Y',zoom, left_xlim, right_xlim)
        
        if(z_state):
            fig = plot_three_axis_graphs.plot_axis(zArr, timeArr, filename, stime, etime, 'Z',zoom, left_xlim, right_xlim)
            
    #Warning Message
    else:
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Axis Selection",  "Please select an axis\' to plot")

    #return graph_from_plotter_value_x, graph_from_plotter_value_y, graph_from_plotter_value_z, fig
    return fig
    
def start_hour_entry_check(self,start_hour_string):
        
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
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Time Entry Error", "Invalid time entry in Start Hour box \nValue too large\nPlease make sure value is less than 24")
        
    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Time Entry Error", "Invalid time entry in Start Hour box \nValue too small\nPlease make sure value is greater or equal to 0")

    # Returning the start_hour_string so that whatever changes we made to it get returned
    return value

def start_minute_entry_check(self,start_minute_string):

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
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Time Entry Error", "Invalid time entry in Start Min box \nValue too large\nPlease make sure value is less than 60")

    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Time Entry Error", "Invalid time entry in Start Min box \nValue too small\nPlease make sure value is greater or equal to 0")

    # Returning the start_minute_string so whatever changes we made to it get returned
    return value

def start_second_entry_check(self,start_second_string):

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
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Time Entry Error", "Invalid time entry in Start Second box \nValue too large\nPlease make sure value is less than 60")

    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Time Entry Error", "Invalid time entry in Start Second box \nValue too small\nPlease make sure value is greater or equal to 0")

    # Returning the start_second_string so whatever changes we made to it get returned
    return value

def end_hour_entry_check(self,end_hour_string):

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
    if(value > 24):
        # Have error message box pop up because it can't be more than 23
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Time Entry Error", "Invalid time entry in End Hour box \nValue too large\nPlease make sure value is less than 24")

        # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Time Entry Error", "Invalid time entry in End Hour box \nValue too small\nPlease make sure value is greater or equal to 0")

    # Returning the end_hour_string so whatever changes we made to it get returned
    return value

def end_minute_entry_check(self,end_minute_string):

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
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Time Entry Error", "Invalid time entry in End Min box \nValue too large\nPlease make sure value is less than 60")
    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Time Entry Error", "Invalid time entry in End Min box \nValue too small\nPlease make sure value is greater or equal to 0")

    # Returning the end_minute_string so whatever changes we made to it get returned
    return value

def end_second_entry_check(self,end_second_string):
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
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"Time Entry Error", "Invalid time entry in End Sec box \nValue too large\nPlease make sure value is less than 60")

    # Testing to see if the inputted value is less than what it can be
    elif(value < 0):
        # Have error message box pop up because it can't be a negative number
        view_maccsGUI.MainWindow.warning_message_pop_up(self,"File open error", "Invalid time entry in End Sec box \nValue too small\nPlease make sure value is greater or equal to 0")

    # Returning the end_second_string so whatever changes we made to it get returned
    return value

        