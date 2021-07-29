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
import read_raw_to_lists

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

            

    fig = plt.figure(figsize=(12, 4))
    
    plt.plot(timeArr,xArr, linewidth = 1)
    plt.title("Geomagnetic Bx of " + station_name + "   YEARDAY: " + year_day_value + "   DATE: " + date) 
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


    return fig

    #add an if statement for when if they want a pdf or a png
    #file_option = file_option.lower()
    #print(file_option)
    #if(file_option == 'pdf'):
        #fig.savefig('x_array_plot.pdf', format='pdf', dpi=1200)
    #elif(file_option == 'png'):
        #fig.savefig('x_array_plot.png', format = 'png', dpi = 1200)
    #else :
        #print(file_option + "is not supported filetype")
        #sys.exit(0)

       
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

    fig = plt.figure(figsize=(12, 4))
    
    plt.plot(timeArr,yArr, linewidth = 1)
    plt.title("Geomagnetic By of " + station_name + "   YEARDAY: " + year_day_value +  "   DATE: " + date) 
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


    return fig

    #add an if statement for when if they want a pdf or a png
    #file_option = file_option.lower()
    #if(file_option == 'pdf'):
        #fig.savefig('y_array_plot.pdf', format='pdf', dpi=1200)
    #elif(file_option == 'png'):
        #fig.savefig('y_array_plot.png', format = 'png', dpi = 1200)
    #else :
        #print(file_option + "is not supported filetype")
        #sys.exit(0)

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

    fig = plt.figure(figsize=(12, 4)) #size of graph
    
    plt.plot(timeArr,zArr, linewidth = 1)
    plt.title("Geomagnetic Bz of " + station_name + "   YEARDAY: " + year_day_value+  "   DATE: " + date) 
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

    return fig

    

    #add an if statement for when if they want a pdf or a png
    #file_option = file_option.lower()
    #if(file_option == 'pdf'):
        #fig.savefig('z_array_plot.pdf', format='pdf', dpi=1200)
    #elif(file_option == 'png'):
        #fig.savefig('z_array_plot.png', format = 'png', dpi = 1200)
    #else :
        #print(file_option + "is not supported filetype")
        #sys.exit(0)

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

    fig = plt.figure(figsize=(12, 4))#size of graph


    x_values = xArr #The list of values to change 
    offset = xArr[0] #The amount to subtract from each value  
    x_values = list(map(lambda x : x - offset, x_values)) #applies the subtraction x-offset to each value, converts the result back to a list

    y_values = yArr #The list of values to change 
    offset = yArr[0] #the amount to subtract from each value
    y_values = list(map(lambda y : y - offset, y_values)) #applies the subtraction x-offset to each value, converts the result back to a list
    
    plt.plot(timeArr,x_values, linewidth = 1, label = 'Bx Values')
    plt.plot(timeArr,y_values, linewidth = 1, label = 'By Values')
    
    plt.title("Geomagnetic Bx and By of " + station_name + "   YEARDAY: " + year_day_value +  "   DATE: " + date) 
    plt.ylabel('Bx and By')
    plt.xlabel("Universal Time (Hours)")

    plt.legend(loc = 'upper left', prop={'size': 6})

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    #plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.axhline(y = 0,color = 'tab:gray', linestyle = '-')

    
        

    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    return fig
    

    #add an if statement for when if they want a pdf or a png
    #file_option = file_option.lower()
    #if(file_option == 'pdf'):
        #fig.savefig('x_and_y_plot.pdf', format='pdf', dpi=1200)
    #elif(file_option == 'png'):
        #fig.savefig('x_and_y_plot.png', format = 'png', dpi = 1200)
    #else :
        #print(file_option + "is not supported filetype")
        #sys.exit(0)

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

    fig = plt.figure(figsize=(12, 4))#size of graph


    x_values = xArr #The list of values to change 
    offset = xArr[0] #The amount to subtract from each value  
    x_values = list(map(lambda x : x - offset, x_values)) #applies the subtraction x-offset to each value, converts the result back to a list

    z_values = zArr #The list of values to change 
    offset = zArr[0] #the amount to subtract from each value
    z_values = list(map(lambda z : z - offset, z_values)) #applies the subtracti


    
    plt.plot(timeArr,x_values, linewidth = 1, label = 'Bx Values')
    plt.plot(timeArr,z_values, linewidth = 1, label = 'By Values')
    
    plt.title("Geomagnetic Bx and Bz of " + station_name + "   YEARDAY: " + year_day_value +  "   DATE: " + date) 
    plt.ylabel('Bx and Bz')
    plt.xlabel("Universal Time (Hours)")


    plt.legend(loc = 'upper left', prop={'size': 6})
    
    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.axhline(y = 0,color = 'tab:gray', linestyle = '-')

    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    return fig

    #add an if statement for when if they want a pdf or a png
    #file_option = file_option.lower()
    #if(file_option == 'pdf'):
        #fig.savefig('x_and_z_plot.pdf', format='pdf', dpi=1200)
    #elif(file_option == 'png'):
        #fig.savefig('x_and_z_plot.png', format = 'png', dpi = 1200)
    #else :
        #print(file_option + "is not supported filetype")
        #sys.exit(0)


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

    fig = plt.figure(figsize=(12, 4))#size pf graph

    y_values = yArr #The list of values to change 
    offset = yArr[0] #The amount to subtract from each value  
    y_values = list(map(lambda y : y - offset, y_values)) #applies the subtraction x-offset to each value, converts the result back to a list

    z_values = zArr #The list of values to change 
    offset = zArr[0] #the amount to subtract from each value
    z_values = list(map(lambda z : z - offset, z_values)) #applies the subtracti

    
    plt.plot(timeArr,y_values, linewidth = 1, label = 'By Values')
    plt.plot(timeArr,z_values, linewidth = 1, label = 'Bz Values')
    
    plt.title("Geomagnetic By and Bz of " + station_name + "   YEARDAY: " + year_day_value +  "   DATE: " + date) 
    plt.ylabel('By and Bz')#y label 
    plt.xlabel("Universal Time (Hours)")#x label 


    plt.legend(loc = 'upper left', prop={'size': 6})#legend
    
    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.axhline(y = 0,color = 'tab:gray', linestyle = '-') #zero axis 


    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    return fig
    

    #add an if statement for when if they want a pdf or a png
    #file_option = file_option.lower()
    #if(file_option == 'pdf'):
        #fig.savefig('y_and_z_plot.pdf', format='pdf', dpi=1200)
    #elif(file_option == 'png'):
        #fig.savefig('y_and_z_plot.png', format = 'png', dpi = 1200)
    #else :
        #print(file_option + "is not supported filetype")
        #sys.exit(0)


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

    fig = plt.figure(figsize=(12, 4))#size of graph

    x_values = xArr #The list of values to change 
    offset = xArr[0] #The amount to subtract from each value  
    x_values = list(map(lambda x : x - offset, x_values)) #applies the subtraction x-offset 


    y_values = yArr #The list of values to change 
    offset = yArr[0] #The amount to subtract from each value  
    y_values = list(map(lambda y : y - offset, y_values)) #applies the subtraction x-offset to each value, converts the result back to a list

    z_values = zArr #The list of values to change 
    offset = zArr[0] #the amount to subtract from each value
    z_values = list(map(lambda z : z - offset, z_values)) #applies the subtracti


    
    plt.plot(timeArr,x_values, linewidth = 1, label = "Bx Values")
    plt.plot(timeArr,y_values, linewidth = 1, label = 'By Values')
    plt.plot(timeArr,z_values, linewidth = 1, label = 'Bz Values')
    
    plt.title("Geomagnetic Bx, By and Bz of " + station_name + "   YEARDAY: " + year_day_value +  "   DATE: " + date) 
    plt.ylabel('Bx, By and Bz')
    plt.xlabel("Univeral Time (Hours)")

    plt.legend(loc= 'upper left', prop={'size': 6})

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.axhline(y = 0,color = 'tab:gray', linestyle = '-') #zero axis

    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

    return fig

    #add an if statement for when if they want a pdf or a png
    #file_option = file_option.lower()
    #if(file_option == 'pdf'):
        #fig.savefig('x_y_and_z_plot.pdf', format='pdf', dpi=1200)
    #elif(file_option == 'png'):
        #fig.savefig('x_y_and_z_plot.png', format = 'png', dpi = 1200)
    #else :
        #print(file_option + "is not supported filetype")
        #sys.exit(0)




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


    arrayX, arrayY, arrayZ, timeArr = read_raw_to_list(two_hz_binary_file, start_time, end_time)

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









