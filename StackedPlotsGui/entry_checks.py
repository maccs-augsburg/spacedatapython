'''
custom_widgets.py

May 2022 -- Created -- Mark Ortega-Ponce

https://docs.python.org/3/library/typing.html
https://peps.python.org/pep-0008/

Note: Types in params and ->, are just used for type hinting in IDE's.
      Python does not enforce types.
'''

def station_code_entry_check(self) -> bool:
    '''
    Additional check for the station code. 
    Makes sure it is 2-4 character.
    Warns user if input was off.

    Returns
    -------
    True/False : bool
        False it it failed test, true if it passed test.
    '''
    if len(self.station_edit.get_entry()) <= 1:
        self.warning_message_dialog(
            "Error invalid station code, needs to be 2-4 uppercase characters")
        return False
    # If it passed check return True
    return True

def year_day_entry_check(self) -> bool:
    '''
    Checks to see if there was any input for the 
    year day value, warns user if input was off.

    Returns
    -------
    True/False : bool
        False if it failed test, true if it passed test.
    '''
    if (len(self.year_day_edit.get_entry()) == 0):
        self.warning_message_dialog(
            "There was no input for the year day entry box")
        return False
    # If it passed check return True
    return True

def hour_entry_check(self, hour_entry: int, end_or_start: int) -> int:
    '''
    Checks both the start and end hour 
    entries, warns use if input was off.
    Also sets the entries in the gui.

    Parameters
    ----------
    hour_entry : int
        The value that was inputted into start or end input. Cast to int.
    end_or_start : int
        If hour is a start entry enter a 1 or non-zero. Else enter 0.
    
    Returns
    -------
    hour : int
        Hour value in integer form for plotting.
    '''

    hour = hour_entry

    if hour > 24 or hour < 0:
        self.warning_message_dialog(
            "Hour Entry Error. Valid input (0 - 23)")
        if end_or_start:
            self.start_hour_edit.set_entry(0)
            return 0
        else:
            self.end_hour_edit.set_entry(24)
            return 24

    if end_or_start:
        self.start_hour_edit.set_entry(hour)
    else:
        self.end_hour_edit.set_entry(hour)

    return hour

def minute_entry_check(self, minute_entry: int, end_or_start: int) -> int:
    '''
    Checks both the start and end minute
    entries. Warns the user if input was off.
    Also sets the entries in the gui.

    Parameters
    ----------
    minute_entry : int
        The value that was inputted into start or end input. Cast to int. 
    end_or_start : int
        If minute is a start entry, enter 1 or non-zero. Else enter 0.
    
    Returns
    -------
    minute : int
        Minute value in integer form for plotting.
    '''

    minute = minute_entry

    if minute > 59 or minute < 0:
        self.warning_message_dialog(
            "Minute Entry Error. Valid input (0 - 59)")

        if end_or_start:
            self.start_minute_edit.set_entry(0)
            return 0
        else:
            self.end_minute_edit.set_entry(59)
            return 59
        
    if end_or_start:
        self.start_minute_edit.set_entry(minute)
    else:
        self.end_minute_edit.set_entry(minute)

    return minute

def second_entry_check(self, second_entry: int, end_or_start: int) -> int:
    '''
    Checks both the start and end second
    entries, warns the user if input was off.
    Also sets the entries in the gui

    Parameters
    ----------
    second_entry : str
        The value that was inputted into start of end input
    end_or_start : int
        If second is a start entry, enter 1 or non-zero. Else enter 0.
    
    Returns
    -------
    Int
        second: second value in integer form for plotting
    '''

    second = int(second_entry)

    if second > 59 or second < 0:
        self.warning_message_dialog(
            "Second Entry Error. Valid input (0- 59)")

        if end_or_start:
            self.start_second_edit.set_entry(0)
            return 0
        else:
            self.end_second_edit.set_entry(59)
            return 59

    if end_or_start:
        self.start_second_edit.set_entry(second)
    else:
        self.end_second_edit.set_entry(second)

    return second

def axis_entry_checks_old(x_arr: list, y_arr: list, z_arr: list, 
                        min_x: int, max_x: int, 
                        min_y: int, max_y: int, 
                        min_z: int, max_z: int) -> tuple[int,int,int,int,int,int]:
    '''
    Old axis entry checks from 
    raw_to_plot.py.plot_arrays() function.
    Normalizes range of graphs to be about the same.
    Present data in a non-biased view, rather than zoomed into min-max range.

    Parameters
    ----------
    List
        x_arr: array of x-values. Pulls min/max in case none were entered
    List
        y_arr: array of y-values. Pulls min/max in case none were entered
    List
        z_arr: array of z_values. Pulls min/max in case none were entered
    Int
        min_x: min_x entry from the user, if any
    Int
        max_x: max_x entry from the user, if any
    Int
        min_y: min_y entry from the user, if any
    Int
        max_y: max_y entry from the user, if any
    Int
        min_z: min_z entry from the user, if any
    Int
        max_z: max_z entry from the user, if any

    Returns
    -------
    Int
        min_x: Returns default min_x if no input, else returns input
    Int
        max_x: Return default max_x if no input, else returns input
    Int
        min_y: Return default min_y if no input, else returns input
    Int
        max_y: Returns default max_y if no input, else returns input
    Int
        min_z: Returns default min_z if no input, else returns input
    Int
        max_z: Returns default max_z if no input, else returns input
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
    # dont want min-max values to be on the edge of the graph from my understanding
    max_axis_range = max_axis_range + max_axis_range * .05

    default_min_x = x_midpoint - max_axis_range
    default_min_y = y_midpoint - max_axis_range
    default_min_z = z_midpoint - max_axis_range

    default_max_x = x_midpoint + max_axis_range
    default_max_y = y_midpoint + max_axis_range
    default_max_z = z_midpoint + max_axis_range

    # TODO: Ask if user would ever enter 0 for axis ranges, im assuming no, but ask anyway
    '''
    If user enters 0, it is never going to go through, always replaced by old code.
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

def axis_entry_checks_new(axis_array, min_value, max_value):

    # if one of the values is zero then we don't return
    if min_value and max_value:
        return min_value, max_value 

    default_min = min(axis_array)
    default_max = max(axis_array)
    axis_midpoint = (default_min + default_max) / 2
    default_range = default_max - default_min

    axis_padding = .05

    axis_padding = axis_padding * default_range

    default_min = default_min - axis_padding
    default_max = default_max + axis_padding

    if min_value == 0:
        min_value = int(default_min)
    
    if max_value == 0:
        max_value = int(default_max)

    return min_value, max_value


def set_axis_entrys(self, x_min, x_max, y_min, y_max, z_min, z_max):

    self.min_x_edit.set_entry(x_min)
    self.max_x_edit.set_entry(x_max)
    self.min_y_edit.set_entry(y_min)
    self.max_y_edit.set_entry(y_max)
    self.min_z_edit.set_entry(z_min)
    self.max_z_edit.set_entry(z_max)