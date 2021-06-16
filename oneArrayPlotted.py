#Plotting only one of the arrays
#Created bt- Annabelle 

import matplotlib.pyplot as plt
from matplotlib.ticker import(MultipleLocator, AutoMinorLocator)
import sys
import datetime

from raw_codecs import decode, time_of_record
import station_names



def create_Arrays (raw_record, stime, etime) :
    """
    Creates x, y, and z
    Places x, y, and z into according lists

    Parameters
    ----------
    raw_recod :

    stime :

    etime :

    Returns
    -------
    List
        xArr:
    List
        yArr:
    List
        zArr
    """
    xArr = []
    yArr = []
    zArr = []
    timeArr = []

    #This while loop is to place the information we are creating into the right arrays
    while True :
        one_record = raw_record.read( 38)
        if not one_record :
            break
        current_time = time_of_record(one_record)
        if current_time >= stime :

            
            x1 = decode( one_record[18:21]) / 40.0
            y1 = decode( one_record[21:24]) / 40.0
            z1 = decode( one_record[24:27]) / 40.0
            xArr.append(x1)
            yArr.append(y1)
            zArr.append(z1)

            hour = one_record[4]
            minute = one_record[5]
            second = one_record[6]
            time = hour + minute /60 + second / 3600
            timeArr.append(time)
            
        if current_time >= etime :
            break
        
    return xArr, yArr, zArr, timeArr


def plot_one(xArr, timeArr, filename, stime, etime, fileOption) :
    """
    """

    
    #To split up the file name 
    station = filename[0:2]
    yearDayValue = filename[2:7]
    stationName = station_names.find_full_name(station)


    #List of the hours and finding which ones to use
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
            currentTime += 1

    #Actual Plot

    fig = plt.figure(figsize=(12, 7))
    
    plt.plot(timeArr,xArr, linewidth = .25)
    plt.title("GeoMagnetic Bx of " + stationName + "      YEARDAY: " + yearDayValue) 
    plt.ylabel('Bx')

    plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted

    if (defaultHoursFlag):
        plt.xticks(defaultHoursArr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    #add an if statement for when if they want a pdf or a png
    fileOption = fileOption.lower()
    if(fileOption == 'pdf'):
        fig.savefig('singlePlotter.pdf', format='pdf', dpi=1200)
    elif(fileOption == 'png'):
        fig.savefig('SinglePlotter.png', format = 'png', dpi = 1200)
    else :
        print(fileOption + "is not supported filetype")
        sys.exit(0)

       
def plot_two(yArr, timeArr, filename, stime, etime, fileOption) :
    """
    """
    
    #To split up the file name 
    station = filename[0:2]
    yearDayValue = filename[2:7]
    stationName = station_names.find_full_name(station)


    #List of the hours and finding which ones to use
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
            currentTime += 1

    #Actual Plot

    fig = plt.figure(figsize=(12, 7))
    
    plt.plot(timeArr,yArr, linewidth = .25)
    plt.title("GeoMagnetic By of " + stationName + "      YEARDAY: " + yearDayValue) 
    plt.ylabel('By')

    plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted

    if (defaultHoursFlag):
        plt.xticks(defaultHoursArr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    #add an if statement for when if they want a pdf or a png
    fileOption = fileOption.lower()
    if(fileOption == 'pdf'):
        fig.savefig('singlePlotter.pdf', format='pdf', dpi=1200)
    elif(fileOption == 'png'):
        fig.savefig('SinglePlotter.png', format = 'png', dpi = 1200)
    else :
        print(fileOption + "is not supported filetype")
        sys.exit(0)

def plot_three(zArr, timeArr, filename, stime, etime, fileOption) :
    """
    """
    #To split up the file name 
    station = filename[0:2]
    yearDayValue = filename[2:7]
    stationName = station_names.find_full_name(station)


    #List of the hours and finding which ones to use
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
            currentTime += 1

    #Actual Plot

    fig = plt.figure(figsize=(12, 7))
    
    plt.plot(timeArr,zArr, linewidth = .25)
    plt.title("GeoMagnetic Bz of " + stationName + "      YEARDAY: " + yearDayValue) 
    plt.ylabel('Bz')

    plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted

    if (defaultHoursFlag):
        plt.xticks(defaultHoursArr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    

    #add an if statement for when if they want a pdf or a png
    fileOption = fileOption.lower()
    if(fileOption == 'pdf'):
        fig.savefig('oneArrayPlot.pdf', format='pdf', dpi=1200)
    elif(fileOption == 'png'):
        fig.savefig('oneArrayPlot.png', format = 'png', dpi = 1200)
    else :
        print(fileOption + "is not supported filetype")
        sys.exit(0)


if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        print( "Usage: python3 testPythonPlotter.py filename [starttime [endtime] ]")
        sys.exit(0) # Exiting without an error code

    filename = sys.argv[1]
    fileOption = 'pdf'

    try:
        two_hz_binary_file = open(filename, "rb")
    except:
        print('Can not open file: ' + filename)
        sys.exit(0)
    ### initializing start and end times
    start_time = datetime.time.fromisoformat( "00:00:00")
    end_time = datetime.time.fromisoformat("23:59:59")

    if len(sys.argv) == 3 :
        fileOption = sys.argv[2]
      
    elif len(sys.argv) >= 4 :
        start_time = datetime.time.fromisoformat(sys.argv[2])
        end_time = datetime.time.fromisoformat(sys.argv[3])
    if len(sys.argv) == 5:
        fileOption = sys.argv[4]
    if len(sys.argv) >= 6:
        print( "TOO many items entered please try again!" ) # Not sure what else we should do but we should have something to handle if we get toooo many inputs.
        sys.exit(0) # Exiting without an error code


    arrayX, arrayY, arrayZ, timeArr = create_Arrays(two_hz_binary_file, start_time, end_time)

    #try:
    #plot_one(arrayX, timeArr, filename, start_time, end_time, fileOption)
    plot_two(arrayY, timeArr, filename, start_time, end_time, fileOption)
    #plot_three(arrayZ, timeArr, filename, start_time, end_time, fileOption)
    #except:
        #print('Could not plot arrays to testgraph.pdf')
        #sys.exit(0)









