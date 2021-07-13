# file_naming.py
#
# 2021 June - Created - Erik Steinmetz
# 2021 July - Modified - Ted Strombeck
#

""" Utilities for naming files

Functions that help create correct names for MACCS files.

For example, a plot of a single station should have a name with the pattern
twoLetterStationCodeLowerCase + yearday + timeInterval + "_l" + level + cadence + ".png" or ".pdf"
where timeInterval is blank if it is the whole day and cadence is
"_eighth_sec" or "_half_sec" or "_one_sec" or "_five_sec"

"""

def create_time_interval_string_hms_from_strings( s_hour, s_minute, s_second, e_hour, e_minute, e_second) :
    """
    Creates a time interval string for a filename given the hour, minute, and second
    of the start and end times as strings.

    Parameters
    ----------
    String
        s_hour:
        The start time hour in hours of the day, 0 to 23
        s_minute:
            The start time minute in minutes of an hour, 0 to 59
        s_second:
            The start time second in seconds of a minute, 0 to 59.
        e_hour:
            The end time hour in hours of the day, 0 to 23
        e_minute:
            The end time minute in minutes of an hour, 0 to 59
        e_second:
            The end time second in seconds of a minute, 0 to 59.

    Returns
    -------
    String
        answer = The time interval string or a zero-length string if all day.
    """
    answer = create_time_interval_string_hms(int(s_hour), int(s_minute), int(s_second), int(e_hour), int(e_minute), int(e_second))
    return answer

def create_time_interval_string_hms( s_hour, s_minute, s_second, e_hour, e_minute, e_second) :
    """
    Creates a time interval string for a filename given the hour, minute, and second
    of the start and end times as integers.
        
    Parameters
    ----------
    s_hour:
        The start time hour in hours of the day, 0 to 23
    s_minute:
        The start time minute in minutes of an hour, 0 to 59
    s_second:
        The start time second in seconds of a minute, 0 to 59.
    e_hour:
        The end time hour in hours of the day, 0 to 23
    e_minute:
        The end time minute in minutes of an hour, 0 to 59
    e_second:
        The end time second in seconds of a minute, 0 to 59.
        
    Returns
    -------
    string
        The time interval string or a zero-length string if all day.
    """
    answer = ""
    if( s_hour != 0 or s_minute != 0 or s_second != 0 or e_hour != 23 or e_minute != 59 or e_second != 59) :
        answer = f"_{s_hour:02}{s_minute:02}{s_second:02}_{e_hour:02}{e_minute:02}{e_second:02}"
    return answer
    
def create_time_interval_string( start_second, end_second) :
    """
    Creates a time interval string for a filename given the start and end seconds of the day.
    
    Parameters
    ----------
    start_second:
        The start time in seconds of the day, 0 to 86399.
    end_second:
        The end time in seconds of the day, 0 to 86399.
        
    Returns
    -------
    string
        The time interval string or a zero-length string if all day.
    """
    start_hour = start_second // 3600
    start_second = start_second % 3600
    start_minute = start_second // 60
    start_second = start_second % 60
    end_hour = end_second // 3600
    end_second = end_second % 3600
    end_minute = end_second // 60
    end_second = end_second % 60
    return create_time_interval_string_hms( start_hour, start_minute, start_second, 
                                            end_hour, end_minute, end_second)
