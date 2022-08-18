'''
plot_stacked_graphs.py

Plots x, y, z data values pulled from data files.

Created by- Annabelle Arns

Refactored - Chris Hance & Mark O.P 5/12/2022

https://peps.python.org/pep-0008/
'''
# Imports matplotlib library 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_interactions import ioff, panhandler, zoom_factory
import sys
import datetime
# Imports from our packaged files 
import util.station_names
import model.read_raw_to_lists

import plot.x_axis_time_formatter
#from raw_codecs import decode, time_of_record


def plot_axis(
        axis_list: list, time_list: list, filename: str, 
        stime: datetime.time, etime: datetime.time, axis: str, format="2hz"): 
    """
    Creates a single plot for any axis x, y, z

    Parameters
    ----------
    axis_list : list 
        List of x, y, z values pulled from data file.
    time_list : list
        List of time values from a data file in datetime.datetime format.
    filename : string
        Name of file we are reading.
    stime : datetime.time
        Start time stamp to plot.
    etime : datetime.time
        Ending time stamp to plot.f
    axis : string
        Axis you want to plot, x, y, z.

    Returns
    -------
    fig: Matplotlib.Figure 
        The plotted figure.

    """
    if format == "2hz" or format == "s2":
        ### splitting up the file name
        station = filename[0:2] # Two letter abbreviation of station
        station_name = util.station_names.find_full_name(station) # Getting the station name
        year_day_value = filename[2:7] # Year: (first two digits) and day of year: (last 3 digits)
        year_value = year_day_value[0:2] # The last 2 digits of the year
        day_of_year = year_day_value[2:] # The 3 digits corresponding with the day of the year

    else:
        # What is day of year
        # https://ag.arizona.edu/azmet/doy.htm
        station = filename[0:3]
        station_name = util.station_names.find_full_name(station)
        yyyy_mmdd = filename[3:11] # Year: (first 4 digits YYYY) and day of year: (last 4 digits MMDD)
        year_value = str(yyyy_mmdd[2:4]) # The last 2 digits of the year YYYY
        month_value = str(yyyy_mmdd[4:6])
        day_value = str(int(yyyy_mmdd[6:8]))
        full_date = year_value + " " + month_value + " " + day_value
        datetime_object = datetime.datetime.strptime(full_date, "%y %m %d")
        # convert yy/mm/dd to DOY format (0 - 365 or 366 if counting leap years)
        day_of_year = datetime_object.strftime('%j')
        year_day_value = yyyy_mmdd[2:4] + day_of_year

    # List of the hours and finding which ones to use
    #default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hours_arr = [] # list to use for custom times

    x_axis_label = ""
    
    x_axis_format = mdates.DateFormatter('%H')
    
    hours_arr, x_axis_format, x_axis_label = plot.x_axis_time_formatter.create_time_list(stime, etime, time_list[0])
    # Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_of_year, "%Y-%j").strftime("%m-%d-%Y")

    fig = plt.figure(figsize=(12, 4))
    fig.set_figwidth(12)
    fig.set_figheight(4)
    plt.plot(time_list,axis_list, linewidth = 1)
    plt.title("Geomagnetic B" + axis + " of " + station_name + "   YEARDAY: " + year_day_value + "   DATE: " + date) 
    plt.ylabel('B' + axis)

    # Make an if statement about changing the label with the x axis changing 
    plt.xlabel(x_axis_label)

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.xticks(hours_arr)
    plt.gca().xaxis.set_major_formatter(x_axis_format)
    #x_yticks = plt.yticks()
        
    #if (default_hours_flag):
        #plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    #else:
        #plt.xticks(hoursArr)
    
    # allows mouse wheel zoom
    ax = plt.gca()
    disconnect_zoom = zoom_factory(ax)
    
    return fig

def plot_two_axis(
        first_list: list, second_list: list, time_list: list, 
        filename: str, stime: datetime.time , etime: datetime.time, 
        first_axis: str, second_axis: str, format="2hz"):
    """
    Creates a single plot of any two axis x, y, z.

    Parameters
    ----------
    first_list : list 
        List of x, y, z values pulled from data file.
    second_list : list
        List of x, y, z values pulled from data file.
    time_list : list
        List of time values from a data file in datetime.datetime format.
    filename : string
        Name of file we are reading.
    stime : datetime.time
        Start time stamp to plot.
    etime : datetime.time
        End time stamp to plot.
    first_axis : string
        First axis to plot x, y, z.
    second_axis : string
        Second acis to plot x, y, z.

    Returns
    -------
    fig: Matplotlib.Figure 
        The plotted figure.
    """

    if format == "2hz" or format == "s2":
        ### splitting up the file name
        station = filename[0:2] # Two letter abbreviation of station
        station_name = util.station_names.find_full_name(station) # Getting the station name
        year_day_value = filename[2:7] # Year: (first two digits) and day of year: (last 3 digits)
        year_value = year_day_value[0:2] # The last 2 digits of the year
        day_of_year = year_day_value[2:] # The 3 digits corresponding with the day of the year

    else:
        # What is day of year
        # https://ag.arizona.edu/azmet/doy.htm
        station = filename[0:3]
        station_name = util.station_names.find_full_name(station)
        yyyy_mmdd = filename[3:11] # Year: (first 4 digits YYYY) and day of year: (last 4 digits MMDD)
        year_value = str(yyyy_mmdd[2:4]) # The last 2 digits of the year YYYY
        month_value = str(yyyy_mmdd[4:6])
        day_value = str(int(yyyy_mmdd[6:8]))
        full_date = year_value + " " + month_value + " " + day_value
        datetime_object = datetime.datetime.strptime(full_date, "%y %m %d")
        # convert yy/mm/dd to DOY format (0 - 365 or 366 if counting leap years)
        day_of_year = datetime_object.strftime('%j')
        year_day_value = yyyy_mmdd[0:2] + day_of_year

    #List of the hours and finding which ones to use
    hours_arr = [] # list to use for custom times
    
    x_axis_label = ""
    
    x_axis_format = mdates.DateFormatter('%H')

    # Calling our helper function to get our 
    # time_stamps inside our hours_arr for axis labeling and formatting.
    # X_axis_label will return label corresponding to time gaps.
    # hours_array will contain the timestamps for labeling x-axis.
    # x_axis_format might be hours, hours and seconds.
    hours_arr, x_axis_format, x_axis_label = plot.x_axis_time_formatter.create_time_list(stime, etime, time_list[0])
            
    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_of_year, "%Y-%j").strftime("%m-%d-%Y")

    # Actual Plot                
    fig = plt.figure(figsize=(12, 4))# Size of graph

    x_values = first_list # The list of values to change 
    offset = first_list[0] # The amount to subtract from each value
    # Applies the subtraction x-offset to each value, converts the result back to a list  
    x_values = list(map(lambda x : x - offset, x_values)) 

    y_values = second_list # The list of values to change 
    offset = second_list[0] # The amount to subtract from each value
    y_values = list(map(lambda y : y - offset, y_values))
    
    
    plt.plot(time_list,x_values, linewidth = 1, label = 'B' + first_axis +' Values')
    plt.plot(time_list,y_values, linewidth = 1, label = 'B' + second_axis+ ' Values')
    
    plt.title("Geomagnetic B" + first_axis + " and B" + second_axis + " of " + station_name + "    YEARDAY:  " +  year_day_value +   "  DATE: " + date) 
    plt.ylabel('B' + first_axis + ' and B' + second_axis)
    plt.xlabel(x_axis_label)

    plt.legend( prop={'size': 8}, fontsize='medium')
    #loc = 'upper left',
    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    #plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.xticks(hours_arr) # setting the xaxis time ticks to custom values
    plt.gca().xaxis.set_major_formatter(x_axis_format)
    plt.axhline(y = 0,color = 'tab:gray', linestyle = '-')

    return fig

def x_y_and_z_plot(
        x_list: list, y_list: list, z_list: list, 
        time_list: list, filename: str, 
        stime: datetime.time, etime: datetime.time, format="2hz"):
    """
    Creates a single plot with x, y, z values overlayed.

    Parameters
    ----------
    x_list : list 
        List of x values pulled from data file.
    y_list : list
        List of y values pulled from data file.
    z_list : list
        List of z values pulled from data file.
    time_list : list
        List of time values from a data file in datetime.datetime format.
    filename : string
        Name of file we are reading.
    stime : datetime.time
        Start time stamp to plot.
    etime : datetime.time
        Ending time stamp to plot.

    Returns
    -------
    fig: Matplotlib.Figure 
        The plotted figure.

    """
    # Split up the file name string. 
    if format == "2hz" or format == "s2":
        ### splitting up the file name
        station = filename[0:2] # Two letter abbreviation of station
        station_name = util.station_names.find_full_name(station) # Getting the station name
        year_day_value = filename[2:7] # Year: (first two digits) and day of year: (last 3 digits)
        year_value = year_day_value[0:2] # The last 2 digits of the year
        day_of_year = year_day_value[2:] # The 3 digits corresponding with the day of the year

    else:
        # What is day of year
        # https://ag.arizona.edu/azmet/doy.htm
        station = filename[0:3]
        station_name = util.station_names.find_full_name(station)
        yyyy_mmdd = filename[3:11] # Year: (first 4 digits YYYY) and day of year: (last 4 digits MMDD)
        year_value = str(yyyy_mmdd[2:4]) # The last 2 digits of the year YYYY
        month_value = str(yyyy_mmdd[4:6])
        day_value = str(int(yyyy_mmdd[6:8]))
        full_date = year_value + " " + month_value + " " + day_value
        datetime_object = datetime.datetime.strptime(full_date, "%y %m %d")
        # convert yy/mm/dd to DOY format (0 - 365 or 366 if counting leap years)
        day_of_year = datetime_object.strftime('%j')
        year_day_value = yyyy_mmdd[0:2] + day_of_year

    # List of the hours and finding which ones to use
    # default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hours_arr = [] # list to use for custom times

    x_axis_label = ""

    x_axis_format = mdates.DateFormatter('%H')
    
    hours_arr, x_axis_format, x_axis_label = plot.x_axis_time_formatter.create_time_list(stime, etime, time_list[0])

    # Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_of_year, "%Y-%j").strftime("%m-%d-%Y")
        
    fig = plt.figure(figsize=(12, 4))#size of graph

    x_values = x_list # The list of values to change 
    offset = x_list[0] # The amount to subtract from each value  
    x_values = list(map(lambda x : x - offset, x_values)) # Applies the subtraction x-offset 

    y_values = y_list # The list of values to change 
    offset = y_list[0] # The amount to subtract from each value
    # Applies the subtraction x-offset to each value, converts the result back to a list  
    y_values = list(map(lambda y : y - offset, y_values)) 

    z_values = z_list # The list of values to change 
    offset = z_list[0] # The amount to subtract from each value
    z_values = list(map(lambda z : z - offset, z_values)) #applies the subtracti

    plt.plot(time_list,x_values, linewidth = 1, label = "Bx Values")
    plt.plot(time_list,y_values, linewidth = 1, label = 'By Values')
    plt.plot(time_list,z_values, linewidth = 1, label = 'Bz Values')
    
    plt.title("Geomagnetic Bx, By and Bz of " + station_name + "   YEARDAY: " + year_day_value +  "   DATE: " + date) 
    plt.ylabel('Bx, By and Bz')
    plt.xlabel(x_axis_label)

    plt.legend(loc = 'upper left', prop={'size': 8}, fontsize='medium')
    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.xticks(hours_arr) # setting the xaxis time ticks to custom values
    plt.gca().xaxis.set_major_formatter(x_axis_format)
    plt.axhline(y = 0,color = 'tab:gray', linestyle = '-') #zero axis

    return fig

if __name__ == "__main__" :
    
    if len(sys.argv) < 2 :
        print( "Usage: python3 testPythonPlotter.py filename [starttime [endtime] ]")
        sys.exit(0) # Exiting without an error code

    filename = sys.argv[1]
    file_option = "pdf"

    try:
        two_hz_binary_file = open(filename, "rb")
    except:
        print('Can not open file: ' + filename)
        sys.exit(0)
    ### initializing start and end times
    start_time = datetime.time.fromisoformat( "00:00:00")
    end_time = datetime.time.fromisoformat("23:59:59")

    if len(sys.argv) == 3 :
        file_option = sys.argv[2]
      
    elif len(sys.argv) >= 4 :
        start_time = datetime.time.fromisoformat(sys.argv[2])
        end_time = datetime.time.fromisoformat(sys.argv[3])
    if len(sys.argv) == 5:
        file_option = sys.argv[4]
    if len(sys.argv) >= 6:
        # Not sure what else we should do but we should have something to handle if we get too many inputs.
        print( "TOO many items entered please try again!" )
        sys.exit(0) # Exiting without an error code

    arrayX, arrayY, arrayZ, timeArr = model.read_raw_to_lists(two_hz_binary_file, start_time, end_time)

