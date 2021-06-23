# raw_to_plot.py
#
# 2021 June - Created - Ted Strombeck
#

""" Python Plotter

Rewritten example code to test and use for MACCS data file which graphs
the time-stamped x, y, and z values on its' own plot.

"""

#TODO----------------------------------------------------------------------------------------------------------
#   test importing this file into other files -----------------------------------------------------> done
#   have file take in y-axis limits as parameters -------------------------------------------------> 
#   implement the no save option ------------------------------------------------------------------> done
#   Date stamp on top of graph --------------------------------------------------------------------> working on
#   update save filename to be file name ----------------------------------------------------------> done
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

def find_max_differences_of_three(xArr, yArr, zArr) :
    """
    Finds the difference between the minimum value and maximum values in the list
        for the x, y, and z lists

    Parameters
    ----------
    List
        xArr: a list of x values to find the difference in
        yArr: a list of y values to find the difference in
        zArr: a list of z valeus to find the difference in

    Returns
    -------
    Float (not entirely sure)
        The maximum difference out of the differences in the 3 arrays
    """

    # getting the differences for the arrays
    x_difference = find_differences_in_list(xArr)
    y_difference = find_differences_in_list(yArr)
    z_difference = find_differences_in_list(zArr)

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

def create_Arrays (raw_record, stime, etime) :
    """ Creates x, y, z lists based on the 2 Hz raw data file.
    
    Places x, y, and z values into their specific lists.

    Parameters
    ----------
    raw_record:
        A byte array that is 38 bytes long, containing a single
        record in the SRI 2 Hz format.
    stime:
        The datetime.time object from which to begin
    etime:
        The datetime.time object at which to end

    Returns
    -------
    List
        xArr: a list of x Values from our 2 Hz file
    List
        yArr: a list of y Values from our 2 Hz file
    List
        zArr: a list of z Values from our 2 Hz file
    List
        timeArr: a list of time Values from our 2 Hz file
    """

    # Lists to hold data and return at end of function
    xArr = []	    #x plot point storage
    yArr = []	    #y plot point storage
    zArr = []       #z plot point storage
    timeArr = []    #time plot point storage

    #Initial while loop condition
    while True :
        one_record = raw_record.read( 38) # getting the information from the first 38 bytes

        # if we reach the end then we break the loop
        if not one_record:
            break
        current_time = time_of_record(one_record) # getting the current time

        # if current time is greater than the start time we process and add it to arrays
        if current_time >= stime :

            # splitting up the time records
            hour = one_record[4]
            minute = one_record[5]
            second = one_record[6]

            # converting it into hours for the time array 
            timeInHours = hour +  (minute / 60) + (second / 3600)
            timeArr.append(timeInHours) # Converted to hours

            # getting the x values
            x1 = decode( one_record[18:21]) / 40.0
            xArr.append(x1)

            # getting the y values
            y1 = decode( one_record[21:24]) / 40.0
            yArr.append(y1) 

            # getting the z values
            z1 = decode( one_record[24:27]) / 40.0
            zArr.append(z1)

        # if current time is greater than or equal to the ending time then we stop
        if current_time >= etime :
            break

    # returning the 4 lists
    return xArr, yArr, zArr, timeArr

def plot_Arrays(xArr, yArr, zArr, timeArr, filename, stime, etime, fileOption) :
    """ Places x, y, z arrays on a plot.

    Places x, y, and z arrays which contain values from the
    2 Hz raw data file into its own subplot (3 subplots total)

    Parameters
    ----------
    xArr:
        List of x values from a 2 Hz raw data file.
    yArr:
        List of y values from a 2 Hz raw data file.
    zArr:
        List of z values from a 2 Hz raw data file.
    timeArr:
        List of time values from a 2Hz raw data file.
    filename:
        Name of the 2Hz raw data file.
    stime:
        The datetime.time object from which to begin
    etime:
        The datetime.time object at which to end
    fileOption:
        String to indicate what type of file to save (PDF or PNG)
    """

    ### splitting up the file name
    station = filename[0:2] # Two letter abbreviation of station
    stationName = station_names.find_full_name(station) # Getting the station name
    yearDayValue = filename[2:7] # Year: (first two digits) and day of year: (last 3 digits)
    yearValue = yearDayValue[0:2] # The last 2 digits of the year
    dayValue = yearDayValue[2:] # The 3 digits corresponding with the day of the year

    if((int)(yearValue) > 50): # Not sure what the cutoff should be, just defaulted to 50 to start with
        yearValue = "19" + yearValue
    else:
        yearValue = "20" + yearValue

    # Converting the date and setting it up
    date = datetime.datetime.strptime(yearValue + "-" + dayValue, "%Y-%j").strftime("%m-%d-%Y") 
    

    ### hour list and determining which one to use
    defaultHoursArr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hoursArr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    defaultHoursFlag = False # using a flag to better optimize operations

    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        defaultHoursFlag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not defaultHoursFlag:
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hoursArr.append(currentTime) # adding the odd numbers to the list
            currentTime += 1 # incrementing currentTime

    ### figure settings
    fig = plt.figure(figsize=(12, 7)) #12, 7, dictates width, height
    fig.patch.set_facecolor('#d3d3d3') # "#d3d3d3" is a grey color for the plot
    fig.subplots_adjust(hspace=0.03)

    ### first plot
    # plt.ylim(minimum, maximum)
    plt.subplot(311)	# subplot allows multiple plots on 1 page
                        # 3 dictates the range (row), allowing 3 graphs
                        # 1 indicates columns, more than 1 for matrices for example
                        # 1 indicates which subplot out of 3 to work on
    plt.plot(timeArr,xArr, linewidth=0.25) # this was plt.scatter, we used plt.plot for a line graph
    plt.title("Geomagnetic Bx By Bz of " + stationName + "          YEARDAY: " + yearDayValue + "            DATE: " + date) # setting up the title and yearday
    plt.ylabel('Bx')	# side label
    plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    if (defaultHoursFlag):
        plt.xticks(defaultHoursArr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr) # setting the xaxis time ticks to custom values

    ### Now build the second plot, this time using y-axis data
    plt.subplot(312)
    plt.plot(timeArr,yArr, linewidth=0.25)
    plt.ylabel('By')	# side label
    plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    if (defaultHoursFlag):
        plt.xticks(defaultHoursArr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr) # setting the xaxis time ticks to custom values
    
    ### Third plot using z-axis data. Add the x-axis label at the bottom
    plt.subplot(313)
    plt.plot(timeArr,zArr, linewidth=0.25)
    plt.ylabel('Bz')	# side label
    plt.xlabel('Time in Hours') # label underneath
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    if (defaultHoursFlag):
        plt.xticks(defaultHoursArr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr) # setting the xaxis time ticks to custom values

    fileOption = fileOption.lower()
    if(fileOption == 'pdf'):
        # saving plot into a pdf file
        fig.savefig(filename + '.pdf', format='pdf', dpi=1200)
    elif (fileOption == 'png'):
        # saving plot into a png file
        fig.savefig(filename + '.png', format='png', dpi=1200)
    elif (fileOption == 'no'):
        # not saving plot but showing it instead
        plt.show()
    else :
        print(fileOption + ' is not a supported filetype Option')
        sys.exit(0)# Exiting without an error code

if __name__ == "__main__":
    ### usage message in console
    if len(sys.argv) < 2 :
        print( "Usage: python3 testPythonPlotter.py filename [starttime [endtime] ]")
        sys.exit(0) # Exiting without an error code
        
    # filename
    filename = sys.argv[1]

    # file option
    fileOption = 'pdf' # defaulting with the pdf option

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
        fileOption = sys.argv[2]
    elif len(sys.argv) >= 4 :
        # iso format for a time is HH:MM:SS
        start_time = datetime.time.fromisoformat(sys.argv[2])
        end_time = datetime.time.fromisoformat(sys.argv[3])
    if len(sys.argv) == 5:
        fileOption = sys.argv[4]
    if len(sys.argv) >= 6:
        print( "TOO many items entered please try again!" ) # Not sure what else we should do but we should have something to handle if we get toooo many inputs.
        sys.exit(0) # Exiting without an error code


    ### Creating x, y, and z arrays -- NOW INCLUDING START AND END TIMES!!!
    arrayX, arrayY, arrayZ, timeArr = create_Arrays(two_hz_binary_file, start_time, end_time)

    ### Plotting said arrays -- NOW INCLUDING START AND END TIMES AND FILE OPTION!!!
    # try and catch block to handle error in case file is already open
    try:
        plot_Arrays(arrayX, arrayY, arrayZ, timeArr, filename, start_time, end_time, fileOption)
    except:
        print('Could not plot arrays to testgraph.pdf, file is open')
        sys.exit(0) # Exiting without an error code
