#  read_clean_to_lists.py
#
#  Reads raw 2 Hz data from a file, creating data lists of all three
#  axes and a list of times.
#
#  2021 July  -- Created  -- Erik Steinmetz
#

# Python 3 imports
import datetime
import sys

def create_datetime_lists_from_clean( clean_file, start_time, end_time):
    """ Creates x, y, z, time, and flag lists based on the 2 Hz clean data file.
    
    Places x, y, z, time, and flag values into their own lists.
    
    Notable flag values are 0 - good data, 1 - questionable data, time
    may not have been properly recorded, 2 - missing data, a record with
    the value 32,767.0 nT has been inserted, 4 - despiked data, data was
    present in the raw, but replaced during despiking, 8 - near spike
    data, a record with its recorded data intact, but near enough to a
    spike to be questionable.
    
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

    # get filename from open file object
    clean_file_string = clean_file.name
    # if filename is an abs filepath, take the last element from splitting
    clean_file_string = clean_file_string.split('/')[-1]
    year_day_value = clean_file_string[2:7] # Year: (first two digits) and day of year: (last 3 digits)
    year_value = year_day_value[0:2] # The last 2 digits of the year

    if int(year_value) < 20:
        century_string = "19"
    else:
        century_string = "20"
        
    full_year_value = century_string + str(year_value)
    day_of_year = year_day_value[2:] # The 3 digits corresponding with the day of the year
    year_and_doy = full_year_value + " " + day_of_year 
    date_object = datetime.datetime.strptime(year_and_doy, '%Y %j')
    date = date_object.strftime('%Y/%m/%d')
    datetime_object = datetime.datetime.strptime(date, '%Y/%m/%d')
    year = datetime_object.year
    month = datetime_object.month
    day = datetime_object.day

    # Lists to hold data and return at end of function
    x_arr = []	     # x plot point storage
    y_arr = []	     # y plot point storage
    z_arr = []       # z plot point storage
    time_arr = []    # time plot point storage
    flag_arr = []    # status flag storage

    # Loop until the end of file or end time has been reached
    while True :
        # Grab a single record of information from the next 28 bytes
        clean_record = clean_file.read( 28) 
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

            # creating a test for no data variable
            test_for_no_data = int.from_bytes(clean_record[4:8], byteorder='big', signed=True)

            # TODO: Should not be continue, put in fake record (99_999.99)
            # eg. 
            #     time array stuff above if else check
            #     if test_no_data:
            #           put fake record in
            #     else:
            #           put regular record in
            # if we don't have data, we don't add it to the time arrays
            if test_for_no_data == 32767000:
                continue
            
            # converting it into hours for the time array 
            time_in_hours_quarter_second = datetime.datetime(year=year,
                                                             month=month,
                                                             day=day,
                                                             hour=hour,
                                                             minute=minute,
                                                             second=second,
                                                             microsecond=250000)

            time_in_hours_three_quarter_second = datetime.datetime(year=year,
                                                                   month=month,
                                                                   day=day,
                                                                   hour=hour,
                                                                   minute=minute,
                                                                   second=second,
                                                                   microsecond=750000)

            time_arr.append(time_in_hours_quarter_second)
            time_arr.append(time_in_hours_three_quarter_second)

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


if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        print( "Usage: python3 read_clean_to_lists.py filename [starttime [endtime]]")
        sys.exit(0)   # Exit with no error code
    filename = sys.argv[1]
    two_hz_clean_file = open(filename, "rb")
    start_time = datetime.time.fromisoformat( "00:00:00")
    end_time = datetime.time.fromisoformat("23:59:59")
    if len(sys.argv) >= 3 :
        # iso format for a time is HH:MM:SS
        start_time = datetime.time.fromisoformat(sys.argv[2])
    if len(sys.argv) == 4 :
        end_time = datetime.time.fromisoformat(sys.argv[3])
    xa, ya, za, ta, fa = create_datetime_lists_from_clean( two_hz_clean_file, start_time, end_time)
    print( xa)
    print( fa)
    