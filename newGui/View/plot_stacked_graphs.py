# raw_to_plot.py
#
# 2021 June - Created - Ted Strombeck
#

""" Python Plotter

Rewritten example code to test and use for MACCS data file which graphs
the time-stamped x, y, and z values on its' own plot.

"""

# Python 3 imports
import datetime
import numpy as np

# MACCS import
from Model import station_names

# Matplotlib imports
import matplotlib.pyplot as plt
import matplotlib as mpl
# Plotter program imports
from Model import read_raw_to_lists
from Model import x_axis_time_formatter


def plot_arrays(x_arr, y_arr, z_arr, time_arr, filename,
                stime, etime, in_min_x=0, in_max_x=0,
                in_min_y=0, in_max_y=0,
                in_min_z=0, in_max_z=0) :
    """ Places x, y, z arrays on a plot.

    Places x, y, and z arrays which contain values from a
    2 Hz data file, each into its own subplot (3 subplots total)

    Parameters
    ----------
    x_arr:
        List of x values from a 2 Hz data file.
    y_arr:
        List of y values from a 2 Hz data file.
    z_arr:
        List of z values from a 2 Hz data file.
    time_arr:
        List of time values from a 2Hz data file in datetime.datetime format.
    filename:
        Name of the 2Hz raw data file.
    stime:
        The datetime.time object from which to begin.
    etime:
        The datetime.time object at which to end.

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
    hours_arr, x_axis_format, x_axis_label = x_axis_time_formatter.create_timelists(stime, etime)
    
    ### figure settings
    fig = plt.figure(figsize=(12,7))#12, 7, dictates width, height
    #fig.subplots_adjust(hspace=0.1)
    #mpl.rcParams['figure.figsize'] = [20, 8]

    ### first plot    
    # plt.ylim(minimum, maximum)
    axis_x = plt.subplot(311)	# subplot allows multiple plots on 1 page
                        # 3 dictates the range (row), allowing 3 graphs
                        # 1 indicates columns, more than 1 for matrices for example
                        # 1 indicates which subplot out of 3 to work on
    plt.ylim(in_min_x, in_max_x)
    plt.plot(time_arr,x_arr, linewidth=1) # this was plt.scatter, we used plt.plot for a line graph
    plt.title("Geomagnetic Bx By Bz of " + station_name + "          YEARDAY: " + year_day_value + "            DATE: " + date) # setting up the title and yearday
    # Commits gone, this is to change padding on y-axis for graphs.
    # Should look nice for papers, not sure if there is a certain margin scientific papers need.
    plt.ylabel('Bx', labelpad=10)	# side label
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in', which='major', pad=10) # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.xticks(hours_arr) # setting the xaxis time ticks to custom values
    plt.gca().xaxis.set_major_formatter(x_axis_format)
    # old line would remove (_, y) x from interactive matplotlib
    # this next line makes it visible
    plt.gca().axes.xaxis.set_visible(False)
    x_yticks = plt.yticks()
    ### Now build the second plot, this time using y-axis data
    axis_y = plt.subplot(312, sharex= axis_x)
    plt.ylim(in_min_y, in_max_y)
    plt.plot(time_arr,y_arr, linewidth=1)
    # Change padding here for 2nd graph
    plt.ylabel('By', labelpad=17)	# side label
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.gca().axes.xaxis.set_visible(False)
    y_yticks = plt.yticks()
    
    ### Third plot using z-axis data. Add the x-axis label at the bottom
    axis_z = plt.subplot(313, sharex= axis_x)
    plt.ylim(in_min_z, in_max_z)
    plt.plot(time_arr,z_arr, linewidth=1)
    # Changed padding here for 3rd graph
    plt.ylabel('Bz', labelpad=6)	# side label
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    z_yticks = plt.yticks()
    # returning the fig object
    plt.xlabel(x_axis_label)
    return fig

def set_yaxis(yticks_list, scale_difference):
    """
    Updates the y axis ticks list with the given scale 
    difference which fleshes out the list of the same size 
    incrementing with the given scale_difference.

    Parameters
    ----------
    List
        yticks_list: A list of values to update.
    Float
        scale_difference: Float value (xx.00) that the list should increment by.

    Returns
    -------
    List
        new_yticks: A list of the updated values.
    """
    
    # Creating a new list to add the new values into
    new_yticks = []
    
    # Keeping the starting point element the same
    new_yticks.append(yticks_list[int(len(yticks_list)/2)])
    
    # Deleting the item from the yticks_list
    yticks_list = np.delete(yticks_list, int(len(yticks_list)/2))

    # Below middle number for loop
    for i in range(int(len(yticks_list) / 2)):
        # Adding new item to our new list
        new_yticks.append(new_yticks[0] - ((i+1) * scale_difference))
        # Deleting item from the yticks_list
        yticks_list = np.delete(yticks_list, i)

    # Above middle number for loop
    for i in range(len(yticks_list)-1):
        # Adding new item to our new list
        new_yticks.append(new_yticks[0] + ((i+1) * scale_difference))

    # Sorting the list so that values are properly in order
    new_yticks.sort()

    # If the new_yticks list has more than 5 values we shrink it
    # down by eliminating both the first and last digits until we
    # get to 5 or less values in the list
    if (len(new_yticks) > 5):
        while(len(new_yticks) > 5):
            new_yticks.pop(0)
            new_yticks.pop(-1)

    # Returning the list
    return new_yticks
