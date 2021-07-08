#Plotting only one of the arrays
#Created by- Annabelle Arns


#Imports matplotlib library 
import matplotlib.pyplot as plt
from matplotlib.ticker import(MultipleLocator, AutoMinorLocator)


import sys
import datetime
#Imports from our other previous files 
from raw_codecs import decode, time_of_record
import station_names



def create_arrays (raw_record, stime, etime) :
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


def x_plot(xArr, timeArr, filename, stime, etime, file_option) :
    """
    Creates a single plot of just the xArr and timeArr.

    Parameters
    ----------
    xArr :

    timeArr :

    filename :

    stime :

    etime :

    file_option :

    Returns
    -------
    
    """

    
    #To split up the file name 
    station = filename[0:2]
    year_day_value = filename[2:7]
    year_value = year_day_value[0:2]
    day_value = year_day_value[2:]
    station_name = station_names.find_full_name(station)


    #List of the hours and finding which ones to use
    default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hoursArr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    default_hours_flag = False # using a flag to better optimize operations


    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hoursArr.append(currentTime) # adding the odd numbers to the list
            currentTime += 1

    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")



    #Actual Plot

            

    fig = plt.figure(figsize=(12, 7))
    
    plt.plot(timeArr,xArr, linewidth = 1)
    plt.title("Geomagnetic Bx of " + station_name + "      YEARDAY: " + year_day_value + "      DATE: " + date) 
    plt.ylabel('Bx')

    #Make an if statement about changing the label with the x axis changing 
    plt.xlabel("Universal Time (Hours)")
    

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted

    

    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    #add an if statement for when if they want a pdf or a png
    file_option = file_option.lower()
    #print(file_option)
    if(file_option == 'pdf'):
        fig.savefig('x_array_plot.pdf', format='pdf', dpi=1200)
    elif(file_option == 'png'):
        fig.savefig('x_array_plot.png', format = 'png', dpi = 1200)
    else :
        print(file_option + "is not supported filetype")
        sys.exit(0)

       
def y_plot(yArr, timeArr, filename, stime, etime, file_option) :
    """
    Creates a single plot of just the yArr and timeArr.

    Parameters
    ----------
    yArr :

    timeArr :

    filename :

    stime :

    etime :

    file_option :

    Returns
    -------
    
    """
    
    #To split up the file name 
    station = filename[0:2]
    year_day_value = filename[2:7]
    year_value = year_day_value[0:2]
    day_value = year_day_value[2:]
    station_name = station_names.find_full_name(station)


    #List of the hours and finding which ones to use
    default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hoursArr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    default_hours_flag = False # using a flag to better optimize operations


    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hoursArr.append(currentTime) # adding the odd numbers to the list
            currentTime += 1


    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")
    #Actual Plot

    fig = plt.figure(figsize=(12, 7))
    
    plt.plot(timeArr,yArr, linewidth = 1)
    plt.title("Geomagnetic By of " + station_name + "      YEARDAY: " + year_day_value +  "      DATE: " + date) 
    plt.ylabel('By')
    plt.xlabel("Universal Time (Hour)")

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted

    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    #add an if statement for when if they want a pdf or a png
    file_option = file_option.lower()
    if(file_option == 'pdf'):
        fig.savefig('y_array_plot.pdf', format='pdf', dpi=1200)
    elif(file_option == 'png'):
        fig.savefig('y_array_plot.png', format = 'png', dpi = 1200)
    else :
        print(file_option + "is not supported filetype")
        sys.exit(0)

def z_plot(zArr, timeArr, filename, stime, etime, file_option) :
    """
    Creates a single plot of just the zArr and timeArr.

    Parameters
    ----------
    zArr :

    timeArr :

    filename :

    stime :

    etime :

    file_option :

    Returns
    -------
    
    """
    #To split up the file name 
    station = filename[0:2]
    year_day_value = filename[2:7]
    year_value = year_day_value[0:2]
    day_value = year_day_value[2:]
    station_name = station_names.find_full_name(station)


    #List of the hours and finding which ones to use
    default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hoursArr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    default_hours_flag = False # using a flag to better optimize operations


    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hoursArr.append(currentTime) # adding the odd numbers to the list
            currentTime += 1


    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")
    #Actual Plot

    fig = plt.figure(figsize=(12, 7))
    
    plt.plot(timeArr,zArr, linewidth = 1)
    plt.title("Geomagnetic Bz of " + station_name + "      YEARDAY: " + year_day_value+  "      DATE: " + date) 
    plt.ylabel('Bz')
    plt.xlabel("Universal Time (Hours)")
    

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted

    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    

    #add an if statement for when if they want a pdf or a png
    file_option = file_option.lower()
    if(file_option == 'pdf'):
        fig.savefig('z_array_plot.pdf', format='pdf', dpi=1200)
    elif(file_option == 'png'):
        fig.savefig('z_array_plot.png', format = 'png', dpi = 1200)
    else :
        print(file_option + "is not supported filetype")
        sys.exit(0)

def x_and_y_plot(xArr, yArr, timeArr, filename, stime, etime, file_option) :
    """
    Creates a single plot of just the zArr and timeArr.

    Parameters
    ----------
    zArr :

    timeArr :

    filename :

    stime :

    etime :

    file_option :

    Returns
    -------
    
    """
    #To split up the file name 
    station = filename[0:2]
    year_day_value = filename[2:7]
    year_value = year_day_value[0:2]
    day_value = year_day_value[2:]
    station_name = station_names.find_full_name(station)


    #List of the hours and finding which ones to use
    default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hoursArr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    default_hours_flag = False # using a flag to better optimize operations


    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hoursArr.append(currentTime) # adding the odd numbers to the list
            currentTime += 1


    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")
    #Actual Plot

    fig = plt.figure(figsize=(12, 7))


    for i in range(len(xArr)):
        xArr[i] = int(xArr[i] - xArr[0])

    for j in range(len(yArr)):
        yArr[j] = int(yArr[j] - yArr[0])
    
    plt.plot(timeArr,xArr, linewidth = 1)
    plt.plot(timeArr,yArr, linewidth = 1)
    
    plt.title("Geomagnetic Bx and By of " + station_name + "      YEARDAY: " + year_day_value +  "      DATE: " + date) 
    plt.ylabel('Bx and By')
    plt.xlabel("Universal Time (Hours)")

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted


    
        

    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    

    #add an if statement for when if they want a pdf or a png
    file_option = file_option.lower()
    if(file_option == 'pdf'):
        fig.savefig('x_and_y_plot.pdf', format='pdf', dpi=1200)
    elif(file_option == 'png'):
        fig.savefig('x_and_y_plot.png', format = 'png', dpi = 1200)
    else :
        print(file_option + "is not supported filetype")
        sys.exit(0)

def x_and_z_plot(xArr, zArr, timeArr, filename, stime, etime, file_option) :
    """
    Creates a single plot of just the zArr and timeArr.

    Parameters
    ----------
    zArr :

    timeArr :

    filename :

    stime :

    etime :

    file_option :

    Returns
    -------
    
    """
    #To split up the file name 
    station = filename[0:2]
    year_day_value = filename[2:7]
    year_value = year_day_value[0:2]
    day_value = year_day_value[2:]
    station_name = station_names.find_full_name(station)


    #List of the hours and finding which ones to use
    default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hoursArr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    default_hours_flag = False # using a flag to better optimize operations


    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hoursArr.append(currentTime) # adding the odd numbers to the list
            currentTime += 1


    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")
    #Actual Plot

    fig = plt.figure(figsize=(12, 7))
    
    plt.plot(timeArr,xArr, linewidth = 1)
    plt.plot(timeArr,zArr, linewidth = 1)
    
    plt.title("Geomagnetic Bx and Bz of " + station_name + "      YEARDAY: " + year_day_value +  "      DATE: " + date) 
    plt.ylabel('Bx and Bz')
    plt.xlabel("Universal Time (Hours)")

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted

    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    

    #add an if statement for when if they want a pdf or a png
    file_option = file_option.lower()
    if(file_option == 'pdf'):
        fig.savefig('x_and_z_plot.pdf', format='pdf', dpi=1200)
    elif(file_option == 'png'):
        fig.savefig('x_and_z_plot.png', format = 'png', dpi = 1200)
    else :
        print(file_option + "is not supported filetype")
        sys.exit(0)


def y_and_z_plot(yArr, zArr, timeArr, filename, stime, etime, file_option) :
    """
    Creates a single plot of just the zArr and timeArr.

    Parameters
    ----------
    zArr :

    timeArr :

    filename :

    stime :

    etime :

    file_option :

    Returns
    -------
    
    """
    #To split up the file name 
    station = filename[0:2]
    year_day_value = filename[2:7]
    year_value = year_day_value[0:2]
    day_value = year_day_value[2:]
    station_name = station_names.find_full_name(station)


    #List of the hours and finding which ones to use
    default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hoursArr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    default_hours_flag = False # using a flag to better optimize operations


    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hoursArr.append(currentTime) # adding the odd numbers to the list
            currentTime += 1


    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")
    #Actual Plot

    fig = plt.figure(figsize=(12, 7))
    
    plt.plot(timeArr,yArr, linewidth = 1)
    plt.plot(timeArr,zArr, linewidth = 1)
    
    plt.title("Geomagnetic By and Bz of " + station_name + "      YEARDAY: " + year_day_value +  "      DATE: " + date) 
    plt.ylabel('By and Bz')
    plt.xlabel("Universal Time (Hours)")

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted

    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    

    #add an if statement for when if they want a pdf or a png
    file_option = file_option.lower()
    if(file_option == 'pdf'):
        fig.savefig('y_and_z_plot.pdf', format='pdf', dpi=1200)
    elif(file_option == 'png'):
        fig.savefig('y_and_z_plot.png', format = 'png', dpi = 1200)
    else :
        print(file_option + "is not supported filetype")
        sys.exit(0)


def x_y_and_z_plot(xArr, yArr, zArr, timeArr, filename, stime, etime, file_option) :
    """
    Creates a single plot of just the zArr and timeArr.

    Parameters
    ----------
    zArr :

    timeArr :

    filename :

    stime :

    etime :

    file_option :

    Returns
    -------
    
    """
    #To split up the file name 
    station = filename[0:2]
    year_day_value = filename[2:7]
    year_value = year_day_value[0:2]
    day_value = year_day_value[2:]
    station_name = station_names.find_full_name(station)


    #List of the hours and finding which ones to use
    default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hoursArr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    default_hours_flag = False # using a flag to better optimize operations


    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hoursArr.append(currentTime) # adding the odd numbers to the list
            currentTime += 1


    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")
    #Actual Plot

    fig = plt.figure(figsize=(12, 7))

    plt.plot(timeArr,xArr, linewidth = 1)
    plt.plot(timeArr,yArr, linewidth = 1)
    plt.plot(timeArr,zArr, linewidth = 1)
    
    plt.title("Geomagnetic Bx, By and Bz of " + station_name + "      YEARDAY: " + year_day_value +  "      DATE: " + date) 
    plt.ylabel('Bx, By and Bz')
    plt.xlabel("Univeral Time (Hours)")

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted

    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    

    #add an if statement for when if they want a pdf or a png
    file_option = file_option.lower()
    if(file_option == 'pdf'):
        fig.savefig('x_y_and_z_plot.pdf', format='pdf', dpi=1200)
    elif(file_option == 'png'):
        fig.savefig('x_y_and_z_plot.png', format = 'png', dpi = 1200)
    else :
        print(file_option + "is not supported filetype")
        sys.exit(0)




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
        print( "TOO many items entered please try again!" ) # Not sure what else we should do but we should have something to handle if we get toooo many inputs.
        sys.exit(0) # Exiting without an error code


    arrayX, arrayY, arrayZ, timeArr = create_arrays(two_hz_binary_file, start_time, end_time)

    #try:
    x_plot(arrayX, timeArr, filename, start_time, end_time)
    y_plot(arrayY, timeArr, filename, start_time, end_time)
    z_plot(arrayZ, timeArr, filename, start_time, end_time)
    x_and_y_plot(arrayX, arrayY, timeArr, filename, start_time, end_time)
    x_and_z_plot(arrayX, arrayZ, timeArr, filename, start_time, end_time)
    y_and_z_plot(arrayY, arrayZ, timeArr, filename, start_time, end_time)
    x_y_and_z_plot(arrayX, arrayY, arrayZ, timeArr, filename, start_time, end_time)
    
    
    #except:
        #print('Could not plot arrays to testgraph.pdf')
        #sys.exit(0)









