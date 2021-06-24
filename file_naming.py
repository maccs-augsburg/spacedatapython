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
    """
    answer = ""
    if( shour != 0 or sminute != 0 or ssecond != 0 or ehour != 23 or eminute != 59 or esecond != 59) :
        answer = f"_{shour:02}{sminute:02}{ssecond:02}_{ehour:02}{eminute:02}{esecond:02}"
    return answer
    
def create_time_interval_string( ssecond, esecond) :
    """
        Creates a time interval string for a filename given the start and end seconds of the day.
    """
    shour = ssecond // 3600
    ssecond = ssecond % 3600
    sminute = ssecond // 60
    ssecond = ssecond % 60
    ehour = esecond // 3600
    esecond = esecond % 3600
    eminute = esecond // 60
    esecond = esecond % 60
    return create_time_interval_string_hms( shour, sminute, ssecond, ehour, eminute, esecond)


