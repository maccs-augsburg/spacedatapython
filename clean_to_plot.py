# clean_to_plot.py
#
# August 2021 -- Created -- Ted Strombeck
#

""" Python Plotter

Code to test and use clean MACCS data files which graphs the time-stamped
x, y, and z values on its' own plot.

"""

#TODO----------------------------------------------------------------------------------------------------------
	# Get the new algorithm idea up and running ------------------------------------------------------ Not Done
		# algorithm concept
			# x-axis time formatter create_time_list function passes in time_arr
			# first if statement (changes the label and format) 
			# pick a delta (10, 15, 20, 1hr)
			# walk through every single datetime in the list
				# if evenly divisible by delta
				# tick_list.add(datetime object)
#--------------------------------------------------------------------------------------------------------------

# Python 3 import
import sys
import datetime
import statistics as stats

# MACCS imports
from raw_codecs import decode, time_of_record
import station_names

# Matplotlib imports
import matplotlib.pyplot as plt
from matplotlib.ticker import(MultipleLocator, AutoMinorLocator)
import matplotlib.dates as mdates

# Plotter program imports
import read_clean_to_lists
import x_axis_time_formatter

def plot_arrays(x_arr, y_arr, z_arr, time_arr, filename,
                stime, etime, in_min_x=0, in_max_x=0,
                in_min_y=0, in_max_y=0,
                in_min_z=0, in_max_z=0) :
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


    hours_arr, x_axis_format, x_axis_label = x_axis_time_formatter.create_time_list(stime, etime)
    
    ### figure settings
    fig = plt.figure(figsize=(12, 7)) #12, 7, dictates width, height
    fig.subplots_adjust(hspace=0.03)

    # x min, max, middle and difference
    x_max = max(x_arr)
    x_min = min(x_arr)
    x_mid = (x_max + x_min) / 2
    x_difference = x_max - x_min

    # y min, max, middle and difference
    y_max = max(y_arr)
    y_min = min(y_arr)
    y_mid = (y_max + y_min) / 2
    y_difference = y_max - y_min
    
    # z min, max, middle and difference
    z_max = max(z_arr)
    z_min = min(z_arr)
    z_mid = (z_max + z_min) / 2
    z_difference = z_max - z_min

    # getting all differences and finding the biggest difference
    differences = [x_difference, y_difference, z_difference]
    max_difference = max(differences)

    # increasing the max_difference by 5%
    max_difference = max_difference + max_difference * 0.05

    # x max and min
    x_max = x_mid + max_difference
    x_min = x_mid - max_difference

    # y max and min
    y_max = y_mid + max_difference
    y_min = y_mid - max_difference

    # z max and min
    z_max = z_mid + max_difference
    z_min = z_mid - max_difference

    ### first plot
    
    # plt.ylim(minimum, maximum)
    plt.subplot(311)	# subplot allows multiple plots on 1 page
                        # 3 dictates the range (row), allowing 3 graphs
                        # 1 indicates columns, more than 1 for matrices for example
                        # 1 indicates which subplot out of 3 to work on
    plt.plot(time_arr,x_arr, linewidth=1) # this was plt.scatter, we used plt.plot for a line graph
    
    # testing to see if we need to set the x and y limits for the first subplot
    if(in_min_x == 0 and in_max_x == 0):
        plt.ylim(x_min, x_max)
    elif(in_min_x == 0):
        plt.ylim(x_min, in_max_x)
    elif(in_max_x == 0):
        plt.ylim(in_min_x, x_max)
    else:
        plt.ylim(in_min_x, in_max_x)
    
    plt.title("Geomagnetic Bx By Bz of " + station_name + "          YEARDAY: " + year_day_value + "            DATE: " + date) # setting up the title and yearday
    plt.ylabel('Bx')	# side label
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.xticks(hours_arr) # setting the xaxis time ticks to custom values
    plt.gca().xaxis.set_major_formatter(x_axis_format)
    plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    x_yticks = plt.yticks()

    ### Now build the second plot, this time using y-axis data
    plt.subplot(312)
    plt.plot(time_arr,y_arr, linewidth=1)

	# testing to see if we need to set the x and y limits for the second subplot
    if(in_min_y == 0 and in_max_y == 0):
        plt.ylim(y_min, y_max)
    elif(in_min_y == 0):
        plt.ylim(y_min, in_max_y)
    elif(in_max_y == 0):
        plt.ylim(in_min_y, y_max)
    else:
        plt.ylim(in_min_y, in_max_y)
    
    plt.ylabel('By')	# side label
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.xticks(hours_arr) # setting the xaxis time ticks to custom values
    plt.gca().xaxis.set_major_formatter(x_axis_format)
    plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    y_yticks = plt.yticks()
    
    ### Third plot using z-axis data. Add the x-axis label at the bottom
    plt.subplot(313)
    plt.plot(time_arr,z_arr, linewidth=1)

	# testing to see if we need to set the x and y limits for the third subplot
    if(in_min_z == 0 and in_max_z == 0):
        plt.ylim(z_min, z_max)
    elif(in_min_z == 0):
        plt.ylim(z_min, in_max_z)
    elif(in_max_z == 0):
        plt.ylim(in_min_z, z_max)
    else:
        plt.ylim(in_min_z, in_max_z)
    
    plt.ylabel('Bz')	# side label
    plt.xlabel(x_axis_label) # label underneath
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in',which='major', pad=10) # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.xticks(hours_arr) # setting the xaxis time ticks to custom values
    plt.gca().xaxis.set_major_formatter(x_axis_format)
    z_yticks = plt.yticks()
    
    # returning the fig object
    return fig

def set_yaxis(yticks_list, scale_difference):
    """
    Updates the y axis ticks list with the given scale difference which fleshes out the list of the same size incrementing with the given scale_difference

    Parameters
    ----------
    List
        yticks_list: A list of values to update
    Float
        scale_difference: the float (usually some_number.00) that the list should increment by

    Returns
    -------
    List
        new_yticks: A list of the updated values
    """
    
    # creating a new list to add the new values into
    new_yticks = []
    
    # Keeping the starting point element the same
    new_yticks.append(yticks_list[int(len(yticks_list)/2)])
    
    # Deleting the item from the yticks_list
    yticks_list = np.delete(yticks_list, int(len(yticks_list)/2))

    # below middle number for loop
    for i in range(int(len(yticks_list) / 2)):
        # Adding new item to our new list
        new_yticks.append(new_yticks[0] - ((i+1) * scale_difference))
        # Deleting item from the yticks_list
        yticks_list = np.delete(yticks_list, i)

    # above middle number for loop
    for i in range(len(yticks_list)-1):
        # Adding new item to our new list
        new_yticks.append(new_yticks[0] + ((i+1) * scale_difference))

    # sorting the list so that values are properly in order
    new_yticks.sort()

    # if the new_yticks list has more than 5 values we shrink it
    # down by eliminating both the first and last digits until we
    # get to 5 or less values in the list
    if (len(new_yticks) > 5):
        while(len(new_yticks) > 5):
            new_yticks.pop(0)
            new_yticks.pop(-1)

    # Returning the list
    return new_yticks

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
    arrayX, arrayY, arrayZ, time_arr = read_clean_to_lists.create_lists_from_raw(two_hz_binary_file, start_time, end_time)

    ### Plotting said arrays -- NOW INCLUDING START AND END TIMES AND FILE OPTION!!!
    # try and catch block to handle error in case file is already open
    try:
        plot_arrays(arrayX, arrayY, arrayZ, time_arr, filename, start_time, end_time, file_option)
    except:
        print('Could not plot arrays to testgraph.pdf, file is open')
        sys.exit(0) # Exiting without an error code
