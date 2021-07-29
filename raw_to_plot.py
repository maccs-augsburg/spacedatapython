# raw_to_plot.py
#
# 2021 June - Created - Ted Strombeck
#

""" Python Plotter

Rewritten example code to test and use for MACCS data file which graphs
the time-stamped x, y, and z values on its' own plot.

"""

#TODO----------------------------------------------------------------------------------------------------------
#   have file take in y-axis limits as parameters -------------------------------------------------> 
#   Use file_naming.py for helping to name the files ----------------------------------------------> working on
#--------------------------------------------------------------------------------------------------------------

# Python 3 imports
import sys
import datetime

# MACCS imports
from raw_codecs import decode, time_of_record
import station_names

# Matplotlib imports
import matplotlib.pyplot as plt
from matplotlib.ticker import(MultipleLocator, AutoMinorLocator)
import matplotlib.dates as mdates

# Plotter program imports
import read_raw_to_lists

def find_max_differences_of_three(x_arr, y_arr, z_arr) :
    """
    Finds the difference between the minimum value and maximum values in the list
        for the x, y, and z lists

    Parameters
    ----------
    List
        x_arr: a list of x values to find the difference in
        y_arr: a list of y values to find the difference in
        z_arr: a list of z valeus to find the difference in

    Returns
    -------
    Float (not entirely sure)
        The maximum difference out of the differences in the 3 arrays
    """

    # getting the differences for the arrays
    x_difference = find_differences_in_list(x_arr)
    y_difference = find_differences_in_list(y_arr)
    z_difference = find_differences_in_list(z_arr)

    # setting the max to be the x_difference initially
    max_difference = x_difference

    # if statement to determine which difference is the max difference
    if (y_difference > x_difference) and (y_difference > z_difference):
        max_difference = y_difference
    elif (z_difference > x_difference) and (z_difference > y_difference):
        max_difference = z_difference

    # returning the maximum difference out of all differences
    return max_difference

def find_differences_in_list (arr) :
    """
    Finds the difference between the minimum value and maximum values in the list

    Parameters
    ----------
    List
        arr: a list of valuees to find the difference in

    Returns
    -------
    Float (not entirely sure)
        The difference between the min and max values in the list
    """

    # if the list passed in is empty, then we can assume that something went wrong
    if (len(arr) <= 0):
        print("ERROR: find_differences_in_list parameter arr didn't contain any values")
        sys.exit(0) # Exiting without an error code

    # Otherwise set the max and min to the first item in the list
    minimum_value = arr[0]
    maximum_value = arr[0]

    # iterate throughout the list
    for item in arr:
        if item > maximum_value:    # if item is greater than our max
            maximum_value = item    #   assign a new max value
        elif item < minimum_value:  # if item is smaller than our min
            minimum_value = item    #   assign a new min value

    # Once we find our max and min, get the difference and return it
    difference = maximum_value - minimum_value
    return difference

def plot_arrays(x_arr, y_arr, z_arr, time_arr, filename, stime, etime) :
    """ Places x, y, z arrays on a plot.

    Places x, y, and z arrays which contain values from the
    2 Hz raw data file into its own subplot (3 subplots total)

    Parameters
    ----------
    x_arr:
        List of x values from a 2 Hz raw data file.
    y_arr:
        List of y values from a 2 Hz raw data file.
    z_arr:
        List of z values from a 2 Hz raw data file.
    time_arr:
        List of time values from a 2Hz raw data file.
    filename:
        Name of the 2Hz raw data file.
    stime:
        The datetime.time object from which to begin
    etime:
        The datetime.time object at which to end

    Returns
    -------
    Figure
        fig:
            figure object that contains the completed plot
    """

    ### splitting up the file name
    station = filename[0:2] # Two letter abbreviation of station
    station_name = station_names.find_full_name(station) # Getting the station name
    year_day_value = filename[2:7] # Year: (first two digits) and day of year: (last 3 digits)
    year_value = year_day_value[0:2] # The last 2 digits of the year
    day_value = year_day_value[2:] # The 3 digits corresponding with the day of the year

    if((int)(year_value) > 50): # Not sure what the cutoff should be, just defaulted to 50 to start with
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    # Converting the date and setting it up
    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")

    year_of_record = (int)(date[6:])
    month_of_record = (int)(date[0:2])
    day_of_record = (int)(date[3:5])
    

    ### hour list and determining which one to use
    #default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    default_hours_arr = []
    for i in range(24):
        if (i % 2 != 0):
            default_hours_arr.append(datetime.datetime(year=year_of_record, month=month_of_record, day=day_of_record, hour = i))
    
    hours_arr = [] # list to use for custom times
    current_hour = stime.hour # setting the hour to start at
    current_minute = stime.minute # setting the minute to start at
    current_second = stime.second # setting the second to start at
    default_hours_flag = False # using a flag to better optimize operations

    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        difference = etime.hour - stime.hour # Getting the difference in time

        if (difference >= 8): # More than 8 hour branch
            for i in range(stime.hour, etime.hour + 1, 1):
                if (i % 2 != 0):
                    hours_arr.append(current_hour)
                current_hour += 1
        elif (difference >= 3):
            ## HH:MM
            print(current_hour)
            time = datetime.time(hour=current_hour, minute=current_minute, second=current_second)
            for i in range(stime.hour, etime.hour, 1):
                hours_arr.append(time)
                current_hour = current_hour+1
                time = datetime.time(hour=current_hour, minute=current_minute, second=current_second)
                #stime = datetime.datetime(year=1, month=1, day=1,hour=current_hour+1, minute=current_minute, second=current_second)
        
##        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times
##
##            # only adding the odd numbers to the list
##            if(current_time % 2 != 0):
##                hours_arr.append(current_time) # adding the odd numbers to the list
##            current_time += 1 # incrementing current_time

    ### figure settings
    fig = plt.figure(figsize=(12, 7)) #12, 7, dictates width, height
    fig.subplots_adjust(hspace=0.03)
    x_axis_format = mdates.DateFormatter('%H:%M')

    ### first plot
    # plt.ylim(minimum, maximum)
    plt.subplot(311)	# subplot allows multiple plots on 1 page
                        # 3 dictates the range (row), allowing 3 graphs
                        # 1 indicates columns, more than 1 for matrices for example
                        # 1 indicates which subplot out of 3 to work on
    plt.plot(time_arr,x_arr, linewidth=1) # this was plt.scatter, we used plt.plot for a line graph
    plt.title("Geomagnetic Bx By Bz of " + station_name + "          YEARDAY: " + year_day_value + "            DATE: " + date) # setting up the title and yearday
    plt.ylabel('Bx')	# side label
    plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hours_arr) # setting the xaxis time ticks to custom values
    plt.gca().xaxis.set_major_formatter(x_axis_format)

    ### Now build the second plot, this time using y-axis data
    plt.subplot(312)
    plt.plot(time_arr,y_arr, linewidth=1)
    plt.ylabel('By')	# side label
    plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hours_arr) # setting the xaxis time ticks to custom values
    plt.gca().xaxis.set_major_formatter(x_axis_format)
    
    ### Third plot using z-axis data. Add the x-axis label at the bottom
    plt.subplot(313)
    plt.plot(time_arr,z_arr, linewidth=1)
    plt.ylabel('Bz')	# side label
    plt.xlabel('Universal Time (Hours)') # label underneath
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hours_arr) # setting the xaxis time ticks to custom values
    plt.gca().xaxis.set_major_formatter(x_axis_format)

    # returning the fig and plt objects
    return fig #, plt 


if __name__ == "__main__":
    ### usage message in console
    if len(sys.argv) < 2 :
        print( "Usage: python3 testPythonPlotter.py filename [starttime [endtime] ]")
        sys.exit(0) # Exiting without an error code
        
    # filename
    filename = sys.argv[1]

    # file option
    file_option = 'pdf' # defaulting with the pdf option

    # try and catch block for bad file name
    try:
        two_hz_binary_file = open(filename, "rb") # attempting to open the file
    except:
        print('Could not open file: ' + filename)
        sys.exit(0) # Exiting without an error code

    ### initializing start and end times
    start_time = datetime.time.fromisoformat( "00:00:00")
    end_time = datetime.time.fromisoformat("23:59:59")

    ### If we get more than 2 items in the console/command line
    if len(sys.argv) == 3 : # if we have 3 items in the command line we assume that it is for specifying file type option
        file_option = sys.argv[2]
    elif len(sys.argv) >= 4 :
        # iso format for a time is HH:MM:SS
        start_time = datetime.time.fromisoformat(sys.argv[2])
        end_time = datetime.time.fromisoformat(sys.argv[3])
    if len(sys.argv) == 5:
        file_option = sys.argv[4]
    if len(sys.argv) >= 6:
        print( "TOO many items entered please try again!" ) # Not sure what else we should do but we should have something to handle if we get toooo many inputs.
        sys.exit(0) # Exiting without an error code


    ### Creating x, y, and z arrays -- NOW INCLUDING START AND END TIMES!!!
    arrayX, arrayY, arrayZ, time_arr = read_raw_to_lists.create_lists_from_raw(two_hz_binary_file, start_time, end_time)

    ### Plotting said arrays -- NOW INCLUDING START AND END TIMES AND FILE OPTION!!!
    # try and catch block to handle error in case file is already open
    try:
        plot_arrays(arrayX, arrayY, arrayZ, time_arr, filename, start_time, end_time, file_option)
    except:
        print('Could not plot arrays to testgraph.pdf, file is open')
        sys.exit(0) # Exiting without an error code
