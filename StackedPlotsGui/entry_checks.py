

def station_code_entry_check(self):

    if len(self.station_edit.get_entry()) <= 1:
        print("Failed statio code entry check")
        self.warning_message_dialog("Error invalid station code, needs to be 2-4 uppercase characters")

    # If it passed check return True
    return True

def year_day_entry_check(self):

    if (len(self.year_day_edit.get_entry()) == 0):
        self.warning_message_dialog("There was no input for the year day entry box")

    # If it passed check return True
    return True

def hour_entry_check(self, hour_entry, end_or_start):

    hour = int(hour_entry)

    if hour > 24 or hour < 0:
        self.warning_message_dialog(
            "Hour Entry Error. Valid input (0 - 23)")

    else:
        return hour

    if end_or_start:
        self.start_hour_edit.set_entry(0)
        return 0
    else:
        self.end_hour_edit.set_entry(24)
        return 24

def minute_entry_check(self, minute_entry, end_or_start):

    minute = int(minute_entry)

    if minute > 59 or minute < 0:
        self.warning_message_dialog(
            "Minute Entry Error. Valid input (0 - 59)")
    else:
        return minute

    if end_or_start:
        self.start_minute_edit.set_entry(0)
        return 0
    else:
        self.end_minute_edit.set_entry(59)
        return 59

def second_entry_check(self, second_entry, end_or_start):

    second = int(second_entry)

    if second > 59 or second < 0:
        self.warning_message_dialog(
            "Second Entry Error. Valid input (0- 59)")

    else:
        return second

    if end_or_start:
        self.start_second_edit.set_entry(0)
        return 0
    else:
        self.end_second_edit.set_entry(59)
        return 59


def axis_entry_checks_old(x_arr, y_arr, z_arr, min_x, max_x, min_y, max_y, min_z, max_z):

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
    Im just now realizing Teds function had a fault with it,
    if user enters 0, it is never going to go through, always replaced by Ted's code
    Now realizing it because I want to be able to update the values for the user
    Does it even matter though? I have my QLabel widget keep track of entries
    Should I set start entry to -1 and compare against that rather than 0?
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