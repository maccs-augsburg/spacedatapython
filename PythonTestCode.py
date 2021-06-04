 #To create plots we need to install the matplotlib library plt is the most common name
import matplotlib.pyplot as plt
import sys
import datetime

#we want to use the code that has been 
from raw_codecs import decode, time_of_record
from raw_to_iaga2002 import one_record_to_string
import station_names



def create_arrays (raw_record, stime, etime) :
    """
    Creates x, y, z ...
    Places x, y, and z ...

    Parameters
    ----------
    raw_record:

    stime:

    etime:

    Returns
    -------
    List
        xArr:
    List
        yArr:
    List
        zArr:
    """
    xArr = []	#x plot point storage
    yArr = []	#y plot point storage
    zArr = []  #z plot point storage
    timeArr = [] #time plot point storage

       

#This while loop is creating our information to add to the arrays and then adds
#them to the correct arrays
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







def plot_arrays(xArr, yArr, zArr, timeArr, filename, stime, etime) :
    """
    Places x, y, z arrays on a plot.
    Places x, y, and z...

    Parameters
    ----------
    xArr:
    yArr:
    zArr:
    timeArr:
    filename:
    start_time:
    end_time:
    """

    #Split up the file name
    station = filename[0:2]
    yearDayValue = filename[2:7]
    stationName = station_names.find_unabbreviated_name(station)




    #Hour list and finding which one to use
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

            #if()



    
    #plt.style.use('ggplot')
    fig = plt.figure(figsize=(12, 7)) #12, 7, dictates width, height

    #This is to get ride of the extra space
    fig, axes = plt.subplots(nrows = 2, ncols = 2)
    fig.subplots_adjust(left = .15, bottom = .1, right = .98, top = .90)
    
    #This is to change the background color to grey and to take away space away from
    #the subplots from

    #add an if statement for if pdf then background white or
    # if png background grey
    
    fig.patch.set_facecolor('#D3D3D3')
    fig.subplots_adjust(hspace= 0.02)

    

    plt.subplot(311)	#subplot allows multiple plots on 1 page
                        #3 dictates the range, allowing 3 graphs

    
    
    
    plt.plot(timeArr,xArr, linewidth = .25) #s = size
    plt.title("GeoMagnetic Bx By Bz of " + stationName + "      YEARDAY: " + yearDayValue) 
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
    
    

    
    
    
    # Now build the second plot, this time using y-axis data

    
    
    plt.subplot(312)
    plt.plot(timeArr,yArr, linewidth = .25)
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
    
    
    

    # Third plot using z-axis data. Add the x-axis label at the bottom
    plt.subplot(313)
    plt.plot(timeArr,zArr, linewidth = .25)
    plt.ylabel('Bz')
    plt.xlabel('Time in Hours')
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    if (defaultHoursFlag):
        plt.xticks(defaultHoursArr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    # Write out the plots onto a page as pdf file

    #add an if statement for when if they want a pdf or a png
    fig.savefig('thegraph.pdf', format='pdf', dpi=1200)

    
    fig.savefig('TestGraph.png', format = 'png', dpi = 1200)
    


if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        print( "Usage: python3 testPythonPlotter.py filename [starttime [endtime] ]")
        sys.exit(0) # Exiting without an error code
        
    filename = sys.argv[1]
    two_hz_binary_file = open(filename, "rb")

    ### initializing start and end times
    start_time = datetime.time.fromisoformat( "00:00:00")
    end_time = datetime.time.fromisoformat("23:59:59")

    ### If we get more than 2 items in the console/command line
    if len(sys.argv) >= 3 :
        # iso format for a time is HH:MM:SS
        start_time = datetime.time.fromisoformat(sys.argv[2])
    if len(sys.argv) == 4 :
        end_time = datetime.time.fromisoformat(sys.argv[3])
    if len(sys.argv) >= 5:
        print( "TOO many items entered please try again!" ) # Not sure what else we should do but we should have something to handle if we get toooo many inputs.
        sys.exit(0) # Exiting without an error code


    ### Creating x, y, and z arrays -- NOW INCLUDING START AND END TIMES!!!
    arrayX, arrayY, arrayZ, timeArr = create_arrays(two_hz_binary_file, start_time, end_time)

    ### Plotting said arrays -- NOW INCLUDING START AND END TIMES!!!
    plot_arrays(arrayX, arrayY, arrayZ, timeArr, filename, start_time, end_time)
    



