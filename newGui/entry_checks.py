'''
entry_checks.py

May 2022 -- Created -- Mark Ortega-Ponce

https://docs.python.org/3/library/typing.html
https://peps.python.org/pep-0008/

Note: Types in params and ->, are just used for type hinting in IDE's.
      Python does not enforce types.
      Try to stay under 80 characters for wrapping in IDE's.
'''
import sys
import os
import datetime
import View.plot_three_axis_graphs

def station_code_entry_check(station_name: str) -> bool:
    '''
    Additional check for the station code. 
    Makes sure station code entry is 2-4 characters.
    Warns user if input was off.

    Returns
    -------
    True/False : bool
        False it it failed test, true if it passed test.
    '''

    if len(station_name) <= 1:
        return False
    # If it passed check return True
    return True


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
        return False
    # If it passed check return True
    return True


def axis_entry_checks(x_arr: list, y_arr: list, z_arr: list,
                          min_x: int, max_x: int,
                          min_y: int, max_y: int,
                          min_z: int, max_z: int) -> tuple[int, int, int,
                                                           int, int, int]:
    '''
    Old axis entry checks from 
    raw_to_plot.plot_arrays() function.
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

    default_min_x = min(x_arr)
    default_max_x = max(x_arr)
    x_midpoint = (default_min_x + default_max_x) / 2
    default_x_range = default_max_x - default_min_x

    default_min_y = min(y_arr)
    default_max_y = max(y_arr)
    y_midpoint = (default_min_y + default_max_y) / 2
    default_y_range = default_max_y - default_min_y

    default_min_z = min(z_arr)
    default_max_z = max(z_arr)
    z_midpoint = (default_min_z + default_max_z) / 2
    default_z_range = default_max_z - default_min_z

    # start normalizing ranges between all three graphs
    axis_ranges = [default_x_range, default_y_range, default_z_range]
    max_axis_range = max(axis_ranges)
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

    # TODO: Ask if user would ever enter 0, cant just assume, so ask.
    '''
    If user enters 0, it is never going to go through, 
    always replaced by old code.
    Possibly start boxes with -1? Would look kinda weird
    '''
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


def graph_from_plotter_entry_check(xArr: list, yArr: list, zArr: list,
                                   x_state: bool, y_state: bool,
                                   z_state: bool, timeArr: list,
                                   filename: str, stime: datetime,
                                   etime: datetime):
    """
    Checks the gui entries for plotting, x, y, z axis. If values are set, then we plot those axis

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
    # first check if all on, then two the two_plot checks,
    # last should be one_axis
    if x_state and y_state and z_state:

        fig = View.plot_three_axis_graphs.x_y_and_z_plot(
            xArr, yArr, zArr, timeArr, filename, stime, etime)

    # Y, Z plot, clean or raw
    elif y_state and z_state:

        fig = View.plot_three_axis_graphs.plot_two_axis(
            yArr, zArr, timeArr, filename, stime, etime, 'Y', 'Z')

    # X, Z plot, clean or raw
    elif x_state and z_state:

        fig = View.plot_three_axis_graphs.plot_two_axis(
            xArr, zArr, timeArr, filename, stime, etime, 'X', 'Z')

    # X, Y plot, clean or raw
    elif x_state and y_state:

        fig = View.plot_three_axis_graphs.plot_two_axis(
            xArr, yArr, timeArr, filename, stime, etime, 'X', 'Y')

    # For single axis plotting
    else:

        if (x_state):
            fig = View.plot_three_axis_graphs.plot_axis(
                xArr, timeArr, filename, stime, etime, 'X')

        if(y_state):
            fig = View.plot_three_axis_graphs.plot_axis(
                yArr, timeArr, filename, stime, etime, 'Y')

        if(z_state):
            fig = View.plot_three_axis_graphs.plot_axis(
                zArr, timeArr, filename, stime, etime, 'Z')

    return fig


'''
Instance method, move back if this is bad practice?
Trying to change some to not use self at all.
'''


def set_axis_entrys(self, x_min: int, x_max: int, y_min:
                    int, y_max: int, z_min: int, z_max: int):
    '''
    Sets the min/max values for x, y, z inside the gui.
    Allows user to see exactly what is being used to plot.
    Note: Doesn't really matter if you pass int or string.
    Gets converted to string when you set anyway.
    It will probably end up being an int when your working with
    it, so hinting that it should be an int.

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


'''
Instance methods, move back if this is bad practice?
Trying to change some to not use self at all.
'''
def checks(self):

    if len(self.filename) == 0:
        self.warning_message_pop_up(
            "Failed Filename Check",
            "No file to work with. Open a file with open file button.")
        return False

    station_code = self.input_station_code.get_entry()
    if not station_code_entry_check(station_code):

        self.warning_message_popup(
            "Failed Filename Check"
            "Error invalid station code. Needs to be 2-4 characters")

        return False

    year_day = self.input_year.get_entry()
    if not year_day_entry_check(self):

        self.warning_message_pop_up(
            "Failed Year Day Check"
            "There was no input for the year day entry box")

        return False

    x_state = self.checkbox_x.isChecked()
    y_state = self.checkbox_y.isChecked()
    z_state = self.checkbox_z.isChecked()

    any_state = x_state or y_state or z_state

    if self.button_graph_style.is_toggled():
        if not any_state:
            self.warning_message_pop_up(
                "Choose Axis",
                "Choose Axis to plot (X, Y, Z)")
            return False

    return True

def same_entries(self):

    start_time_stamp, end_time_stamp = self.time_stamp()

    flag = 0

    if start_time_stamp == self.start_time_stamp:
        flag += 1
    if end_time_stamp == self.end_time_stamp:
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

def same_entries_one_toggled(self):

    start_time_stamp, end_time_stamp = self.time_stamp()

    flag = 0

    if start_time_stamp == self.start_time_stamp:
        flag += 1
    if end_time_stamp == self.end_time_stamp:
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