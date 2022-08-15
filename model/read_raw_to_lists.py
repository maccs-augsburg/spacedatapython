#  read_raw_to_lists.py
#
#  Reads raw 2 Hz data from a file, creating data lists of all three
#  axes and a list of times.
#
#  2021 July  -- Created  -- Erik Steinmetz
#

# Python 3 imports
import datetime

# MACCS imports
from model.raw_codecs import decode, time_of_record

def create_datetime_lists_from_raw( raw_file, start_time, end_time):
    """ Creates x, y, z, and time lists based on the 2 Hz raw data file. But for the time_arr list, it saves the values into the list as datetime.datetime objects
    
    Places x, y, z and time values into their own lists.

    Parameters
    ----------
    raw_file:
        An opened file object containing a day of data recorded
        in the SRI 2 Hz format.
    start_time:
        The datetime.time object from which to begin
    end_time:
        The datetime.time object at which to end

    Returns
    -------
    List
        x_arr: a list of x Values from our 2 Hz file
    List
        y_arr: a list of y Values from our 2 Hz file
    List
        z_arr: a list of z Values from our 2 Hz file
    List
        time_arr: a list of datetime.datetime Values from our 2 Hz file
    
    """    
    # Lists to hold data and return at end of function
    x_arr = []	    #x plot point storage
    y_arr = []	    #y plot point storage
    z_arr = []       #z plot point storage
    time_arr = []    #time plot point storage

    # Loop until the end of file or end time has been reached
    while True :
        # Grab a single record of information from the next 38 bytes
        one_record = raw_file.read( 38) 
        # if we reach the end then we break the loop
        if not one_record:
            break
        current_time = time_of_record(one_record) # getting the current time

        # if current time is greater than the start time we process and add it to arrays
        if current_time >= start_time :
            
            year = one_record[1]
            month = one_record[2]
            day = one_record[3]
            # splitting up the time records
            hour = one_record[4]
            minute = one_record[5]
            second = one_record[6]

            # converting it into hours for the time array but saving them as datetime objects
            time_in_hours_quarter_second = datetime.datetime(year= year,
                                                             month = month,
                                                             day = day,
                                                             hour=hour,
                                                             minute=minute,
                                                             second=second,
                                                             microsecond=250000)
            time_in_hours_three_quarter_second = datetime.datetime(year= year,
                                                                   month = month,
                                                                   day = day,
                                                                   hour=hour,
                                                                   minute=minute,
                                                                   second=second,
                                                                   microsecond=750000)

            # adding the datetime objects to the time_arr list
            time_arr.append(time_in_hours_quarter_second)
            time_arr.append(time_in_hours_three_quarter_second)

            # getting the x values
            x1 = decode( one_record[18:21]) / 40.0
            x_arr.append(x1)
            x2 = decode( one_record[27:30]) / 40.0
            x_arr.append(x2)

            # getting the y values
            y1 = decode( one_record[21:24]) / 40.0
            y_arr.append(y1) 
            y2 = decode( one_record[30:33]) / 40.0
            y_arr.append(y2) 

            # getting the z values
            z1 = decode( one_record[24:27]) / 40.0
            z_arr.append(z1)
            z2 = decode( one_record[33:36]) / 40.0
            z_arr.append(z2)

        # if current time is greater than or equal to the ending time then we stop
        if current_time >= end_time :
            break

    # returning the 4 lists -- This time, time_arr has datetime.datetime objects to display times on the x-axis of plots!
    return x_arr, y_arr, z_arr, time_arr

