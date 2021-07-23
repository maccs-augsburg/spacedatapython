#  read_clean_to_lists.py
#
#  Reads raw 2 Hz data from a file, creating data lists of all three
#  axes and a list of times.
#
#  2021 July  -- Created  -- Erik Steinmetz
#

# Python 3 imports
import datetime


def create_lists_from_clean (clean_file, start_time, end_time) :
    """ Creates x, y, z, time, and flag lists based on the 2 Hz clean data file.
    
    Places x, y, z, time, and flag values into their own lists.

    Parameters
    ----------
    clean_file:
        An opened file object containing a day of data recorded
        in the clean 2 Hz format.
    start_time:
        The datetime.time object from which to begin
    end_time:
        The datetime.time object at which to end

    Returns
    -------
    List
        x_arr: a list of x values from our 2 Hz file
    List
        y_arr: a list of y values from our 2 Hz file
    List
        z_arr: a list of z values from our 2 Hz file
    List
        time_arr: a list of time values from our 2 Hz file
    List
        flag_arr: a list of flag values from the 2 Hz file
    """

    # Quarter and three-quarter second constants expressed in terms of
    # hours to add to the time list
    QUARTER_SECOND = 0.25 / 3600.0
    THREE_QUARTER_SECOND = 0.75 / 3600.0
    
    # Lists to hold data and return at end of function
    x_arr = []	     # x plot point storage
    y_arr = []	     # y plot point storage
    z_arr = []       # z plot point storage
    time_arr = []    # time plot point storage
    flag_arr = []    # status flag storage

    # Loop until the end of file or end time has been reached
    while True :
        # Grab a single record of information from the next 28 bytes
        clean_record = raw_file.read( 28) 
        # if we reach the end then we break the loop
        if not clean_record:
            break
        
        # grab the time
        hour = clean_record[1]
        minute = clean_record[2]
        second = clean_record[3]
        current_time = datetime.time( hour, minute, second)
        #current_time = time_of_record(one_record) # getting the current time

        # if current time is greater than the start time we process and add it to arrays
        if current_time >= start_time :


            # converting it into hours for the time array 
            time_in_hours = hour +  (minute / 60) + (second / 3600)
            time_arr.append(time_in_hours + QUARTER_SECOND)
            time_arr.append(time_in_hours + THREE_QUARTER_SECOND)

            # getting the x values
            x1 = int.from_bytes(clean_record[4:8], byteorder='big', signed=True) / 1000.0
            x_arr.append(x1)
            x2 = int.from_bytes(clean_record[8:12], byteorder='big', signed=True) / 1000.0
            x_arr.append(x2)

            # getting the y values
            y1 = int.from_bytes(clean_record[12:16], byteorder='big', signed=True) / 1000.0
            y_arr.append(y1) 
            y2 = int.from_bytes(clean_record[16:20], byteorder='big', signed=True) / 1000.0
            y_arr.append(y2) 

            # getting the z values
            z1 = int.from_bytes(clean_record[20:24], byteorder='big', signed=True) / 1000.0
            z_arr.append(z1)
            z2 = int.from_bytes(clean_record[24:28], byteorder='big', signed=True) / 1000.0
            z_arr.append(z2)
            
            # getting the flag values
            flag = clean_record[0]
            flag_arr.append( flag)
            flag_arr.append( flag)

        # if current time is greater than or equal to the ending time then we stop
        if current_time >= end_time :
            break

    # returning the 5 lists
    return x_arr, y_arr, z_arr, time_arr, flag_arr
