'''
entry_checks.py

May 2022 -- Created -- Mark Ortega-Ponce & Chris Hance

'''
import sys
import os
import datetime
import plot.plot_three_axis_graphs
import util.station_names
import numpy as np
from PySide6.QtWidgets import (QMessageBox)

def station_code_entry_check(station_name: str) -> bool:
    '''
    Additional check for the station code. 
    Makes sure station code entry is a valid 2-4 character station name.

    Returns
    -------
    True/False : bool
        False if passed string not in station names, true if it is.
    '''
    # Iterate over columns
    for i in range(0, 3):
        # Iterate over rows
        for x in range(2, 11):
            if station_name == util.station_names.names[x][i]:
                return True
    # If it passed check return True
    return False

def year_day_entry_check(self) -> bool:
    '''
    Checks to see if there was any input for the 
    year day value. Warns user if no input.

    Returns
    -------
    True/False : bool
        False if it failed test, true if it passed test.
    '''
    if (len(self.input_year.get_entry()) == 0):
        self.warning_message_pop_up(
            "Failed Year Day Check"
            "There was no input for the year day entry box")
        return False
    # If it passed check return True
    return True

def min_max_time_check(self) -> bool:
    '''
    Checks the two time widgets and 
    checks if the start time is less than the end time.

    Returns
    -------
    True/Fasle : bool
        False if it failed test, true if it passed test. 
    '''
    s_hour = self.start_time.get_hour()
    s_minute = self.start_time.get_minute()
    s_second = self.start_time.get_second()

    e_hour = self.end_time.get_hour()
    e_minute = self.end_time.get_minute()
    e_second = self.end_time.get_second()

    # start hour is already less than end hour no need to check min or sec
    if s_hour < e_hour:
        return True
    #if start and end hour is same we have to compare min and then sec if need be 
    elif s_hour == e_hour:
        # Compare minutes
        if s_minute < e_minute:
            return True
        elif s_minute == e_minute:
            #compare seconds
            if s_second < e_second:
                return True
    else: 
        return False

def axis_entry_checks(x_arr: np.array, y_arr: np.array, z_arr: np.array,
                          min_x: int, max_x: int,
                          min_y: int, max_y: int,
                          min_z: int, max_z: int) -> tuple[int, int, int,
                                                           int, int, int]:
    '''
    Normalizes range of graphs to be about the same.
    Present data in a non-biased view, rather than zoomed into min-max range.

    Parameters
    ----------
    x_arr : list
        List of x-values. Pulls min/max in case none were entered by user.
    y_arr : list
        List of y-values. Pulls min/max in case none were entered by user.
    z_arr : list
        List of z_values. Pulls min/max in case none were entered by user.
    min_x : int
        Min x entry from the user, if any.
    max_x : int
        Max x entry from the user, if any.
    min_y : int
        Min y entry from the user, if any.
    max_y : int
        Max y entry from the user, if any.
    min_z : int
        Min z entry from the user, if any.
    max_z : int
        Max z entry from the user, if any.

    Returns
    -------
    min_x : int 
        Returns default min_x if no input, else returns user input.
    max_x : int
        Returns default max_x if no input, else returns user input.
    min_y : int
        Returns default min_y if no input, else returns user input.
    max_y : int
        Returns default max_y if no input, else returns user input.
    min_z : int
        Returns default min_z if no input, else returns user input.
    max_z : int
        Returns default max_z if no input, else returns user input.
    '''

    default_min_x = np.min(x_arr)
    default_max_x = np.max(x_arr)
    x_midpoint = (default_min_x + default_max_x) / 2
    default_x_range = default_max_x - default_min_x

    default_min_y = np.min(y_arr)
    default_max_y = np.max(y_arr)
    y_midpoint = (default_min_y + default_max_y) / 2
    default_y_range = default_max_y - default_min_y

    default_min_z = np.min(z_arr)
    default_max_z = np.max(z_arr)
    z_midpoint = (default_min_z + default_max_z) / 2
    default_z_range = default_max_z - default_min_z

    # start normalizing ranges between all three graphs
    axis_ranges = [default_x_range, default_y_range, default_z_range]
    max_axis_range = np.max(axis_ranges)
    # increasing range by 5%
    # dont want min-max values to be on the
    # edge of the graph from my understanding
    max_axis_range = max_axis_range + max_axis_range * .05

    default_min_x = x_midpoint - max_axis_range
    default_min_y = y_midpoint - max_axis_range
    default_min_z = z_midpoint - max_axis_range

    default_max_x = x_midpoint + max_axis_range
    default_max_y = y_midpoint + max_axis_range
    default_max_z = z_midpoint + max_axis_range

    if min_x == 0:
        min_x = int(default_min_x)

    if max_x == 0:
        max_x = int(default_max_x)

    if min_y == 0:
        min_y = int(default_min_y)

    if max_y == 0:
        max_y = int(default_max_y)

    if min_z == 0:
        min_z = int(default_min_z)

    if max_z == 0:
        max_z = int(default_max_z)

    return min_x, max_x, min_y, max_y, min_z, max_z

def graph_from_plotter_entry_check(xArr: np.array, yArr: np.array, zArr: np.array,
                                   x_state: bool, y_state: bool,
                                   z_state: bool, timeArr: np.array,
                                   filename: str, stime: datetime,
                                   etime: datetime, format="2hz"):
    """
    Plot x, y, z axis depending if they are checked inside the gui.

    Parameters
    ----------
    xArr : list
        The x array values.
    yArr : list
        The y array values.
    zArr : list
        The z array values.
    x_state : bool
        The state of x_checkbox in gui.
    y_state : bool
        The state of y_checkbox in gui.
    z_state : bool
        The state of z_checkbox in gui.
    timeArr : list
        The time array values.
    filename : list 
        The name of the file.
    stime : Datetime
        The start time stamp HH:MM:SS.
    etime : Datetime
        The end time stamp HH:MM:SS.

    Returns
    -------
    fig : Matplotlib.Figure
        The plotted figure.
    """

    # X, Y, Z plot, clean or raw
    if x_state and y_state and z_state:

        fig = plot.plot_three_axis_graphs.x_y_and_z_plot(
            xArr, yArr, zArr, timeArr, filename, stime, etime, format)

    # Y, Z plot, clean or raw
    elif y_state and z_state:

        fig = plot.plot_three_axis_graphs.plot_two_axis(
            yArr, zArr, timeArr, filename, stime, etime, 'Y', 'Z', format)

    # X, Z plot, clean or raw
    elif x_state and z_state:

        fig = plot.plot_three_axis_graphs.plot_two_axis(
            xArr, zArr, timeArr, filename, stime, etime, 'X', 'Z', format)

    # X, Y plot, clean or raw
    elif x_state and y_state:

        fig = plot.plot_three_axis_graphs.plot_two_axis(
            xArr, yArr, timeArr, filename, stime, etime, 'X', 'Y', format)

    # For single axis plotting
    else:

        if (x_state):
            fig = plot.plot_three_axis_graphs.plot_axis(
                xArr, timeArr, filename, stime, etime, 'X', format)

        if(y_state):
            fig = plot.plot_three_axis_graphs.plot_axis(
                yArr, timeArr, filename, stime, etime, 'Y', format)

        if(z_state):
            fig = plot.plot_three_axis_graphs.plot_axis(
                zArr, timeArr, filename, stime, etime, 'Z', format)

    return fig

def set_axis_entrys(self, x_min: int, x_max: int, y_min:
                    int, y_max: int, z_min: int, z_max: int):
    '''
    Sets the min/max values for x, y, z inside the gui.
    Allows user to see exactly what is being used to plot.

    Parameters
    ----------
    x_min : int
        Min x value to set inside the gui.
    x_max : int
        Max x value to set inside the gui.
    y_min : int
        Min y value to set inside the gui.
    y_max : int
        Max y value to set inside the gui.
    z_min : int
        Min z value to set inside the gui.
    z_max : int
        Max z value to set inside the gui.
    '''
    self.spinbox_min_x.set_entry(x_min)
    self.spinbox_max_x.set_entry(x_max)
    self.spinbox_min_y.set_entry(y_min)
    self.spinbox_max_y.set_entry(y_max)
    self.spinbox_min_z.set_entry(z_min)
    self.spinbox_max_z.set_entry(z_max)

def same_entries(self) -> bool:
    '''
    Function to check if current information in the gui
    has already  been plotted in the stacked graph style.
    Checks to see if:
        - Current start time is equal to previous start time.
        - Current end time is equal to previous end time.
        - Current x/y/z min values are equal to previous min x/y/z values.
        - Current x/y/z max values are equal to previous max x/y/z values.
    If all these 8 checks result in true, then we return false to indicate
    test failed, and to not plot the graph again. Plotting takes (~1.5 seconds)
    and gui cannot respond to any other user events during this time.

    Returns
    -------
    True/False : bool
        False if passed string not in station names, true if it is.
    '''

    # get current start times, and end time
    curr_start_time, curr_end_time = self.time_stamp()

    flag = 0

    if curr_start_time == self.start_time_stamp:
        flag += 1
    if curr_end_time == self.end_time_stamp:
        flag += 1
    if self.prev_min_x == self.spinbox_min_x.get_entry():
        flag += 1
    if self.prev_max_x == self.spinbox_max_x.get_entry():
        flag += 1
    if self.prev_min_y == self.spinbox_min_y.get_entry():
        flag += 1
    if self.prev_max_y == self.spinbox_max_y.get_entry():
        flag += 1
    if self.prev_min_z == self.spinbox_min_z.get_entry():
        flag += 1
    if self.prev_max_z == self.spinbox_max_z.get_entry():
        flag += 1

    if flag == 8:
        # exact same entries
        return False
    else:
        return True

def same_axis_entries(self) -> bool:

    flag = 0

    if self.prev_min_x == self.spinbox_min_x.get_entry():
        flag += 1
    if self.prev_max_x == self.spinbox_max_x.get_entry():
        flag += 1
    if self.prev_min_y == self.spinbox_min_y.get_entry():
        flag += 1
    if self.prev_max_y == self.spinbox_max_y.get_entry():
        flag += 1
    if self.prev_min_z == self.spinbox_min_z.get_entry():
        flag += 1
    if self.prev_max_z == self.spinbox_max_z.get_entry():
        flag += 1

    if flag == 6:
        return True
    else:
        return False

def same_entries_one_toggled(self) -> bool:
    '''
    Function to check if current information in the gui
    has already been plotted in the three graph axis style graph.
    Checks to see if:
        - Current start time is equal to previous start time.
        - Current end time is equal to previous end time.
        - Current x checkbox state is same as previous state.
        - Current y checkbox state is same as previous state.
        - Current z checkbox state is same as previous state.
    If all these 5 checks result in true, then we return false to
    indicate test failed, and to not plot the graph again. Plotting
    takes (~1.5 seconds) and gui cannot respond to any other user
    events during this time.

    Returns
    -------
    True/False : bool
        False if passed string not in station names, true if it is.
    '''

    curr_start_time, curr_end_time = self.time_stamp()

    flag = 0

    if curr_start_time == self.start_time_stamp:
        flag += 1
    if curr_end_time == self.end_time_stamp:
        flag += 1

    if self.prev_state_plot_x == self.checkbox_x.isChecked():
        flag += 1

    if self.prev_state_plot_y == self.checkbox_y.isChecked():
        flag += 1

    if self.prev_state_plot_z == self.checkbox_z.isChecked():
        flag += 1

    if flag == 5:
        return False
    else:
        return True

def checks(self) -> bool:
    
    '''
    Function that goes through most of the entry_check.py functions.
    - Checks for filename, has user chosen a file yet?
    - Checks for valid station code.
    - Checks for valid year day value.
    - Checks that start time is less than end time.
    - Checks that at least one checkbox is checked if we 
        are in one graph mode.
    If any of these tests fail, we return false.

    Returns
    -------
    True/False : bool
        False if passed string not in station names, true if it is.
    '''
    
    # Makes sure we have a file
    if len(self.filename) == 0:
        return False

    # Checks the 2 char station code is a code that fits in our station_names.py array
    station_code = self.input_station_code.get_entry()
    if not station_code_entry_check(station_code):
        return False

    # Just makes sure there is some entry in the yearday slot 
    # Right now no real check to see if the year day is a valid combo
    # but if we have a value the file itself should lay it properly before hand
    year_day = self.input_year.get_entry()
    if not year_day_entry_check(self):
        return False

    if not min_max_time_check(self):
        return False

    x_state = self.checkbox_x.isChecked()
    y_state = self.checkbox_y.isChecked()
    z_state = self.checkbox_z.isChecked()

    any_state = x_state or y_state or z_state

    if self.button_graph_switch.three_axis_style.isChecked():
        if not any_state:
            return False

    return True
