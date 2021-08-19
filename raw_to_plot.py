# raw_to_plot.py
#
# 2021 June - Created - Ted Strombeck
#

""" Python Plotter

Rewritten example code to test and use for MACCS data file which graphs
the time-stamped x, y, and z values on its' own plot.

"""

#TODO----------------------------------------------------------------------------------------------------------
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
import x_axis_time_formatter

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

##    hours_arr = []
##    x_axis_label = ''
##    x_axis_format = mdates.DateFormatter('%H')

    hours_arr, x_axis_format, x_axis_label = x_axis_time_formatter.create_time_list(stime, etime)
    
    ### figure settings
    fig = plt.figure(figsize=(12, 7)) #12, 7, dictates width, height
    fig.subplots_adjust(hspace=0.03)

    ### first plot
    # plt.ylim(minimum, maximum)
    plt.subplot(311)	# subplot allows multiple plots on 1 page
                        # 3 dictates the range (row), allowing 3 graphs
                        # 1 indicates columns, more than 1 for matrices for example
                        # 1 indicates which subplot out of 3 to work on
    plt.plot(time_arr,x_arr, linewidth=1) # this was plt.scatter, we used plt.plot for a line graph
    plt.title("Geomagnetic Bx By Bz of " + station_name + "          YEARDAY: " + year_day_value + "            DATE: " + date) # setting up the title and yearday
    plt.ylabel('Bx')	# side label
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    #plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
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
    plt.ylabel('By')	# side label
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    #plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
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
    plt.ylabel('Bz')	# side label
    plt.xlabel(x_axis_label) # label underneath
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    #plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.xticks(hours_arr) # setting the xaxis time ticks to custom values
    plt.gca().xaxis.set_major_formatter(x_axis_format)
    z_yticks = plt.yticks()

    # x, y, and z, y-axis plotting scale values
    x_yticks = x_yticks[0]
    x_plot_scale = x_yticks[1] - x_yticks[0]
    y_yticks = y_yticks[0]
    y_plot_scale = y_yticks[1] - y_yticks[0]
    z_yticks = z_yticks[0]
    z_plot_scale = z_yticks[1] - z_yticks[0]

    # setting the scale_differences array and finding max difference in list
    scale_differences = [x_plot_scale, y_plot_scale, z_plot_scale]
    max_scale_value = max(scale_differences)

    # x suplot y_scaling section
    if (x_plot_scale < max_scale_value):
        # getting new list with correct scale from set_yaxis function
        x_yticks = set_yaxis(x_yticks, max_scale_value)
        # switching to the correct subplot
        plt.subplot(311)
        # Setting the ticks (not including the ticks on the top and bottom of the subplot)
        plt.gca().set_ylim(x_yticks[0], x_yticks[-1])
        # Preparing the setting the tick labels to also not include the ticks on top and bottom of subplot
        x_yticks = x_yticks[1:-1]
        plt.yticks(x_yticks)

    # y suplot y_scaling section
    if (y_plot_scale < max_scale_value):
        # getting new list with correct scale from set_yaxis function
        y_yticks = set_yaxis(y_yticks, max_scale_value)
        # switching to the correct subplot
        plt.subplot(312)
        # Setting the ticks (not including the ticks on the top and bottom of the subplot)
        plt.gca().set_ylim(y_yticks[0], y_yticks[-1])
        # Preparing the setting the tick labels to also not include the ticks on top and bottom of subplot
        y_yticks = y_yticks[1:-1]
        plt.yticks(y_yticks)

    # z suplot y_scaling section
    if (z_plot_scale < max_scale_value):
        # getting new list with correct scale from set_yaxis function
        z_yticks = set_yaxis(z_yticks, max_scale_value)
        # switching to the correct subplot
        plt.subplot(313)
        # Setting the ticks (not including the ticks on the top and bottom of the subplot)
        plt.gca().set_ylim(z_yticks[0], z_yticks[-1])
        # Preparing the setting the tick labels to also not include the ticks on top and bottom of subplot
        z_yticks = z_yticks[1:-1]
        plt.yticks(z_yticks)
    
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
    new_yticks.append(yticks_list[0])
    
    # Iterating through the rest of the list
    for i in range(1, len(yticks_list)):
        # Adding the correctly updated value
        if (len(new_yticks) < 5):
            new_yticks.append(yticks_list[0] + (i * scale_difference))
        else:
            return new_yticks

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
    arrayX, arrayY, arrayZ, time_arr = read_raw_to_lists.create_lists_from_raw(two_hz_binary_file, start_time, end_time)

    ### Plotting said arrays -- NOW INCLUDING START AND END TIMES AND FILE OPTION!!!
    # try and catch block to handle error in case file is already open
    try:
        plot_arrays(arrayX, arrayY, arrayZ, time_arr, filename, start_time, end_time, file_option)
    except:
        print('Could not plot arrays to testgraph.pdf, file is open')
        sys.exit(0) # Exiting without an error code
