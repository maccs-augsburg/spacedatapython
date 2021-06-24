# file_naming.py
#
# 2021 June - Created - Erik Steinmetz
#

""" Utilities for naming files

Functions that help create correct names for MACCS files.

For example, a plot of a single station should have a name with the pattern
twoLetterStationCodeLowerCase + yearday + timeInterval + "_l" + level + cadence + ".png" or ".pdf"
where timeInterval is blank if it is the whole day and cadence is
"_eighth_sec" or "_half_sec" or "_one_sec" or "_five_sec"

"""

def create_time_interval_string_hms( shour, sminute, ssecond, ehour, eminute, esecond) :
    """
    Creates a time interval string for a filename given the hour, minute, and second
    of the start and end times.
        
    Returns
    -------
    string
        The time interval string or a zero-length string if all day.
    """
    answer = ""
    if( shour != 0 or sminute != 0 or ssecond != 0 or 
        ehour != 23 or eminute != 59 or esecond != 59) :
        answer = f"_{shour:02}{sminute:02}{ssecond:02}_{ehour:02}{eminute:02}{esecond:02}"
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

