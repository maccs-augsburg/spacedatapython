# raw_to_plot.py
#
# 2021 June - Created - Ted Strombeck
#

""" Python Plotter

Rewritten example code to test and use for MACCS data file which graphs
the time-stamped x, y, and z values on its' own plot.

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

# Python 3 imports
import datetime
import numpy as np
import statistics as stats

# MACCS imports
from raw_codecs import decode, time_of_record
import station_names

# Matplotlib imports
import matplotlib.pyplot as plt
from matplotlib.ticker import(MultipleLocator, AutoMinorLocator)
import matplotlib.dates as mdates

# Plotter program imports
import model.read_raw_to_lists
import x_axis_time_formatter


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
        The datetime.time object from which to begin
    etime:
        The datetime.time object at which to end

    Returns
    -------
    Figure
        fig:
            figure object that contains the completed plot
    """

    
    #print( "called plot_arrays(", len(x_arr), ",", len(y_arr.len), ",", len(time_arr), ",", len(time_arr))

    # adding this here so it doesn't break Chris gui code, plan would be to remove this call
    # and call inside plotting button function instead because all entry checks being made there
    in_min_x, in_max_x, in_min_y, in_max_y, in_min_z, in_max_z = axis_entry_checks_old(
             x_arr, y_arr, z_arr, in_min_x, in_max_x, in_min_y, in_max_y, in_min_z, in_max_z
    )

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
    print( "   date is", date)
    hours_arr, x_axis_format, x_axis_label = x_axis_time_formatter.create_time_list(stime, etime)
    
    ### figure settings
    fig = plt.figure(figsize=(12, 7)) #12, 7, dictates width, height
    fig.subplots_adjust(hspace=0.1)

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

# adding this here for now, import not working for some reason
# theres a quick fix with vscode, but not sure if it would work for every comp without vscode
def axis_entry_checks_old(x_arr: list, y_arr: list, z_arr: list, 
                        min_x: int, max_x: int, 
                        min_y: int, max_y: int, 
                        min_z: int, max_z: int) -> tuple[int,int,int,
                                                        int,int,int]:
    '''
    Old axis entry checks from 
    raw_to_plot.plot_arrays() function.
    Normalizes range of graphs to be about the same.
    Present data in a non-biased view, rather than zoomed into min-max range.

    Parameters
    ----------
    x_arr : list
        List of x-values. Pulls min/max in case none were entered by user.
    y_arr : list
        List of y-values. Pulls min/max in case none were entered by user.
    z_arr : list
        List of z_values. Pulls min/max in case none were entered by user.
    min_x : int
        Min x entry from the user, if any.
    max_x : int
        Max x entry from the user, if any.
    min_y : int
        Min y entry from the user, if any.
    max_y : int
        Max y entry from the user, if any.
    min_z : int
        Min z entry from the user, if any.
    max_z : int
        Max z entry from the user, if any.

    Returns
    -------
    min_x : int 
        Returns default min_x if no input, else returns user input.
    max_x : int
        Returns default max_x if no input, else returns user input.
    min_y : int
        Returns default min_y if no input, else returns user input.
    max_y : int
        Returns default max_y if no input, else returns user input.
    min_z : int
        Returns default min_z if no input, else returns user input.
    max_z : int
        Returns default max_z if no input, else returns user input.
    '''

    default_min_x = min(x_arr)
    default_max_x = max(x_arr)
    x_midpoint = (default_min_x + default_max_x) / 2
    default_x_range = default_max_x - default_min_x

    default_min_y = min(y_arr)
    default_max_y = max(y_arr)
    y_midpoint = (default_min_y + default_max_y) / 2
    default_y_range = default_max_y - default_min_y

    default_min_z = min(z_arr)
    default_max_z = max(z_arr)
    z_midpoint = (default_min_z + default_max_z) / 2
    default_z_range = default_max_z - default_min_z

    # start normalizing ranges between all three graphs
    axis_ranges = [default_x_range, default_y_range, default_z_range]
    max_axis_range = max(axis_ranges)
    # increasing range by 5%
    # dont want min-max values to be on the 
    # edge of the graph from my understanding
    max_axis_range = max_axis_range + max_axis_range * .05

    default_min_x = x_midpoint - max_axis_range
    default_min_y = y_midpoint - max_axis_range
    default_min_z = z_midpoint - max_axis_range

    default_max_x = x_midpoint + max_axis_range
    default_max_y = y_midpoint + max_axis_range
    default_max_z = z_midpoint + max_axis_range

    # TODO: Ask if user would ever enter 0, cant just assume, so ask.
    '''
    If user enters 0, it is never going to go through, 
    always replaced by old code.
    Possibly start boxes with -1? Would look kinda weird
    '''
    if min_x == 0:
        min_x = int(default_min_x)

    if max_x == 0:
        max_x = int(default_max_x)

    if min_y == 0:
        min_y = int(default_min_y)
    
    if max_y == 0:
        max_y = int(default_max_y)

    if min_z == 0:
        min_z = int(default_min_z)

    if max_z == 0:
        max_z = int(default_max_z)
    

    return min_x, max_x, min_y, max_y, min_z, max_z
