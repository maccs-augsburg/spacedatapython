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
from raw_codecs import decode, time_of_record

def create_datetime_lists_from_raw( raw_file, start_time, end_time, file_name):
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
    file_name:
        The name of the file that excludes the suffix (.2hz) and includes the yearday value

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
    #station = filename[0:2] # Two letter abbreviation of station
    #station_name = station_names.find_full_name(station) # Getting the station name
    year_day_value = file_name[2:7] # Year: (first two digits) and day of year: (last 3 digits)
    year_value = year_day_value[0:2] # The last 2 digits of the year
    day_value = year_day_value[2:] # The 3 digits corresponding with the day of the year

    if((int)(year_value) > 50): # Not sure what the cutoff should be, just defaulted to 50 to start with
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    # Converting the date and setting it up
    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")
    
    # Quarter and three-quarter second constants expressed in terms of
    # hours to add to the time list
##    QUARTER_SECOND = 0.25 / 3600.0
##    THREE_QUARTER_SECOND = 0.75 / 3600.0
    
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

            # splitting up the time records
            hour = one_record[4]
            minute = one_record[5]
            second = one_record[6]

            # converting it into hours for the time array but saving them as datetime objects
            time_in_hours_quarter_second = datetime.datetime(year=1111,
                                                             month = 1,
                                                             day = 1,
                                                             hour=hour,
                                                             minute=minute,
                                                             second=second,
                                                             microsecond=250000)
            time_in_hours_three_quarter_second = datetime.datetime(year=1111,
                                                                   month = 1,
                                                                   day = 1,
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

def create_lists_from_raw( raw_file, start_time, end_time) :
    """ Creates x, y, z, and time lists based on the 2 Hz raw data file.
    
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
        time_arr: a list of time Values from our 2 Hz file
    """

    # Quarter and three-quarter second constants expressed in terms of
    # hours to add to the time list
    QUARTER_SECOND = 0.25 / 3600.0
    THREE_QUARTER_SECOND = 0.75 / 3600.0
    
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

            # splitting up the time records
            hour = one_record[4]
            minute = one_record[5]
            second = one_record[6]

            # converting it into hours for the time array 
            time_in_hours = hour +  (minute / 60) + (second / 3600)
            time_arr.append(time_in_hours + QUARTER_SECOND)
            time_arr.append(time_in_hours + THREE_QUARTER_SECOND)

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

    # returning the 4 lists
    return x_arr, y_arr, z_arr, time_arr
