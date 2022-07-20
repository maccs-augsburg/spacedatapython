#  read_IAGA2002_to_lists.py
#
#  Reads raw 2 Hz data from a file, creating data lists of all three
#  axes and a list of times.
#
#  2021 July  -- Created  -- Erik Steinmetz
#  2022 July  -- Modified raw to IAGA2002 -- Mark O.P

# Python 3 imports
import datetime
import numpy as np
# MACCS imports
# import from current directory
from Model.raw_codecs import decode, time_of_record

def create_datetime_lists_from_IAGA2002( IAGA2002_file, start_time, end_time, file_name):
    """ Creates x, y, z, and time lists based on the 2 Hz raw data file. But for the time_arr list, it saves the values into the list as datetime.datetime objects
    
    Places x, y, z and time values into their own lists.

    Parameters
    ----------
    IAGA2002_file:
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
    
    # When creating from raw filename, we switch from using
    # 2 letter station names to 3 letter station names
    year_day_value = file_name[3:11] # Year: (first 4 digits YYYY) and day of year: (last 4 digits MMDD)
    year_value = str(year_day_value[2:4]) # The last 2 digits of the year YYYY
    day_value = str(year_day_value[4:6]) # The 3 digits corresponding with the day of the year

    if((int)(year_value) > 50): # Not sure what the cutoff should be, just defaulted to 50 to start with
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    # Converting the date and setting it up
    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")
    
    # Quarter and three-quarter second constants expressed in terms of
    # hours to add to the time list
    QUARTER_SECOND = 0.25 / 3600.0
    THREE_QUARTER_SECOND = 0.75 / 3600.0
    
    # Lists to hold data and return at end of function
    x_arr = []	    #x plot point storage
    y_arr = []	    #y plot point storage
    z_arr = []       #z plot point storage
    time_arr = []    #time plot point storage

    # Skip first 18 lines because its header info
    for i in range(0, 100):
        dummy_record = str(IAGA2002_file.readline())
        dummy_record = dummy_record.split()
        if dummy_record[0].__contains__("DATE"):
            break
        
    # Loop until the end of file or end time has been reached
    while True:

        one_record_first_line = IAGA2002_file.readline()
        one_record_first_line = one_record_first_line.split()

        one_record_second_line = IAGA2002_file.readline()
        one_record_second_line = one_record_second_line.split()

        # if we reach the end then we break the loop
        if not one_record_first_line:
            break
        
        time = str(one_record_first_line[1])
        # Grab up to hh:mm:ss ignoring the microseconds
        time = time[2:10]
        datetime_object = datetime.datetime.strptime(time, "%H:%M:%S").time()
        hour = int(datetime_object.strftime("%H"))
        minute = int(datetime_object.strftime("%M"))
        second = int(datetime_object.strftime("%S"))

        #second = one_record[17:23] //second with microsecond
        current_time = datetime.time(hour, minute, second) # getting the current time

        # if current time is greater than the start time we process and add it to arrays
        if current_time >= start_time :

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
            x1 = float(one_record_first_line[3])
            x_arr.append(x1)
            x2 = float(one_record_second_line[3])
            x_arr.append(x2)

            # getting the y values
            y1 = float(one_record_first_line[4])
            y_arr.append(y1) 
            y2 = float(one_record_second_line[4])
            y_arr.append(y2) 

            # getting the z values
            z1 = float(one_record_first_line[5])
            z_arr.append(z1)
            z2 = float(one_record_second_line[5])
            z_arr.append(z2)

        # if current time is greater than or equal to the ending time then we stop
        if current_time >= end_time :
            break

    np_x_arr = np.array(x_arr)
    np_y_arr = np.array(y_arr)
    np_z_arr = np.array(z_arr)
    np_time_arr = np.array(time_arr)

    # returning the 4 lists -- This time, time_arr has datetime.datetime objects to display times on the x-axis of plots!
    return np_x_arr, np_y_arr, np_z_arr, np_time_arr
