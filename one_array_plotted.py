#Plotting only one of the arrays
#Created by- Annabelle Arns


#Imports matplotlib library 
import matplotlib.pyplot as plt
from matplotlib.ticker import(MultipleLocator, AutoMinorLocator)
import matplotlib.dates as mdates
 
import sys
import datetime
#Imports from our other previous files 
from raw_codecs import decode, time_of_record
import station_names
import read_raw_to_lists
#import read_to_clean_lists

def plot_axis(axisArr, timeArr, filename, stime, etime, axis):
    """
    Creates a single plot of any axis x, y, z that we want to choose using the axis parameter
    to eliminate the redundancy of code in the file 
    

    Parameters
    ----------
    axisArr : TYPE
        DESCRIPTION.
    timeArr : TYPE
        DESCRIPTION.
    filename : TYPE
        DESCRIPTION.
    stime : TYPE
        DESCRIPTION.
    etime : TYPE
        DESCRIPTION.
    axis : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    #Split up file name and put each piece of info into respective vars
    station = filename[0:2] #name of station 
    year_day_value = filename[2:7] # year and date of file
    year_value = year_day_value[0:2] # year of file 
    day_value = year_day_value[2:] #day of file 
    station_name = station_names.find_full_name(station)#finds respective station name from station_name.py

    #List of the hours and finding which ones to use
    #default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hours_arr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    default_hours_flag = False # using a flag to better optimize operations

    hours_arr = [] # list to use for custom times
    current_hour = stime.hour # setting the hour to start at
    current_minute = stime.minute # setting the minute to start at
    current_second = stime.second # setting the second to start at
    default_hours_flag = False # using a flag to better optimize operations
    x_axis_label = ""
    
    
    #setting the flag to true if the start time and end time is the full 24 hour 
    if (stime == datetime.time.fromisoformat("00:00:00") and etime == datetime.time.fromisoformat("23:59:59")):
        default_hours_flag = True
        x_axis_label = "Universal Time in Hours (HH)"
        # for loop that fills in a list with odd numbers from start time to end 
        for i in range(stime.hour, etime.hour, 1):
            if (currentTime % 2 != 0): #only odd numbers
                hours_arr.append(datetime.datetime(year=1111, month=1, day=1, hour = i, minute=current_minute, second = current_second))
        
    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")

    year_of_record = (int)(date[6:])
    month_of_record = (int)(date[0:2])
    day_of_record = (int)(date[3:5])

    x_axis_format = mdates.DateFormatter('%H')
    
    #if the graph is not going to be in default 24 viewing we have to alter the graph to the respctive time frame 
    if not default_hours_flag:
        hour_difference = etime.hour - stime.hour # Getting the difference in time
        minute_difference = ((etime.hour * 60) + etime.minute) - ((stime.hour * 60) + stime.minute)
        second_difference = ((etime.hour * 3600) + (etime.minute * 60) + etime.second) - ((stime.hour * 3600) + (stime.minute * 60) + stime.second)
        if (hour_difference >= 8): # More than 8 hour branch
            x_axis_label = "Universal Time in Hours (HH)"
            for i in range(hour_difference + 1):
                factor = hour_difference % 2
                if (i % 2 == factor):
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour = current_hour,
                                                       minute= current_minute,
                                                       second = current_second))
                    current_hour += 2

        elif (hour_difference >=5):
            x_axis_label = "Universal Time in Hours (HH)"
            for hour in range(stime.hour, etime.hour+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour = current_hour,
                                                   minute= current_minute,
                                                   second = current_second))
                current_hour += 1
                    
        elif (hour_difference >= 2):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 30 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
                        
        elif (hour_difference >= 1):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 15 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
            
            
        elif (minute_difference >= 30):
            # assuming a 30 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 10 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
                    
        elif (minute_difference >= 20):
            # assuming a 20 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))

        elif (minute_difference >=10):
            # assuming a 10 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
                    
        elif (minute_difference >= 7):
            # assuming a 7 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 2 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
                

            
        elif (minute_difference >= 2):
            # assuming a 2 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=minute,
                                                   second=current_second))
                
        elif (minute_difference >= 1):
            # assuming a 1 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                for second in range(stime.second, etime.second + 1):
                    if second % 20 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=current_hour,
                                                           minute=minute,
                                                           second=second))
            
            
        elif (second_difference >= 45):
            # assuming 45 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 15 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 25):
            # assuming 25 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 10 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
                    
        elif(second_difference >= 10):
            # assuming 10 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))

        elif(second_difference >= 5):
            # assuming 5 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 1.5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
                    
        else:
            # assuming less than a 5 second gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=current_minute,
                                                   second=second))  

    fig = plt.figure(figsize=(12, 4))
    
    plt.plot(timeArr,axisArr, linewidth = 1)
    plt.title("Geomagnetic Bx of " + station_name + "   YEARDAY: " + year_day_value + "   DATE: " + date) 
    plt.ylabel('B' + axis)

    #Make an if statement about changing the label with the x axis changing 
    plt.xlabel(x_axis_label)
def x_plot(xArr, timeArr, filename, stime, etime):
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
    #default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hours_arr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    default_hours_flag = False # using a flag to better optimize operations

    hours_arr = [] # list to use for custom times
    current_hour = stime.hour # setting the hour to start at
    current_minute = stime.minute # setting the minute to start at
    current_second = stime.second # setting the second to start at
    default_hours_flag = False # using a flag to better optimize operations
    x_axis_label = ""


    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True
        x_axis_label = "Universal Time in Hours (HH)"
    # Create a loop that fills out an list with odd numbers from start time to end time
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hours_arr.append(datetime.datetime(year=1111, month=1,day=1,hour = i,minute=current_minute,second = current_second)) # adding the odd numbers to the list
            

    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")

    year_of_record = (int)(date[6:])
    month_of_record = (int)(date[0:2])
    day_of_record = (int)(date[3:5])

    x_axis_format = mdates.DateFormatter('%H')

    #Actual Plot

    if not default_hours_flag:
        hour_difference = etime.hour - stime.hour # Getting the difference in time
        minute_difference = ((etime.hour * 60) + etime.minute) - ((stime.hour * 60) + stime.minute)
        second_difference = ((etime.hour * 3600) + (etime.minute * 60) + etime.second) - ((stime.hour * 3600) + (stime.minute * 60) + stime.second)
        if (hour_difference >= 8): # More than 8 hour branch
            x_axis_label = "Universal Time in Hours (HH)"
            for i in range(hour_difference + 1):
                factor = hour_difference % 2
                if (i % 2 == factor):
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour = current_hour,
                                                       minute= current_minute,
                                                       second = current_second))
                    current_hour += 2

        elif (hour_difference >=5):
            x_axis_label = "Universal Time in Hours (HH)"
            for hour in range(stime.hour, etime.hour+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour = current_hour,
                                                   minute= current_minute,
                                                   second = current_second))
                current_hour += 1
                    
        elif (hour_difference >= 2):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 30 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))

        elif (hour_difference >= 1):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 15 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
            
            
        elif (minute_difference >= 30):
            # assuming a 30 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 10 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
        elif (minute_difference >= 20):
            # assuming a 20 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))

        elif (minute_difference >=10):
            # assuming a 10 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
                
        elif (minute_difference >= 7):
            # assuming a 7 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 2 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
            
        elif (minute_difference >= 2):
            # assuming a 2 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=minute,
                                                   second=current_second))
        elif (minute_difference >= 1):
            # assuming a 1 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                for second in range(stime.second, etime.second + 1):
                    if second % 20 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=current_hour,
                                                           minute=minute,
                                                           second=second))
            
        elif (second_difference >= 45):
            # assuming 45 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 15 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 25):
            # assuming 25 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 10 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 10):
            # assuming 10 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))

        elif(second_difference >= 5):
            # assuming 5 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 1.5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
            
        else:
            # assuming less than a 5 second gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=current_minute,
                                                   second=second))      

    fig = plt.figure(figsize=(12, 4))
    
    plt.plot(timeArr,xArr, linewidth = 1)
    plt.title("Geomagnetic Bx of " + station_name + "   YEARDAY: " + year_day_value + "   DATE: " + date) 
    plt.ylabel('Bx')

    #Make an if statement about changing the label with the x axis changing 
    plt.xlabel(x_axis_label)
    

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.xticks(hours_arr)
    plt.gca().xaxis.set_major_formatter(x_axis_format)
    x_yticks = plt.yticks()


    #if (default_hours_flag):
        #plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    #else:
        #plt.xticks(hoursArr)


    return fig

    

       
def y_plot(yArr, timeArr, filename, stime, etime) :
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
    #default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hours_arr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    #default_hours_flag = False # using a flag to better optimize operations

    current_hour = stime.hour # setting the hour to start at
    current_minute = stime.minute # setting the minute to start at
    current_second = stime.second # setting the second to start at
    default_hours_flag = False # using a flag to better optimize operations
    x_axis_label = ""

    x_axis_format = mdates.DateFormatter('%H')
    
    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hours_arr.append(datetime.datetime(year=1111,month=1,day=1,hour = i,minute=current_minute,second = current_second)) # adding the odd numbers to the list
            


    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")

    year_of_record = (int)(date[6:])
    month_of_record = (int)(date[0:2])
    day_of_record = (int)(date[3:5])

    #Actual Plot



    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True
        x_axis_label = "Universal Time in Hours (HH)"
        for i in range(24):
            if (i % 2 != 0):
                hours_arr.append(datetime.datetime(year=1111,month=1,day=1,hour = i,minute=current_minute,second = current_second))
            

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        hour_difference = etime.hour - stime.hour # Getting the difference in time
        minute_difference = ((etime.hour * 60) + etime.minute) - ((stime.hour * 60) + stime.minute)
        second_difference = ((etime.hour * 3600) + (etime.minute * 60) + etime.second) - ((stime.hour * 3600) + (stime.minute * 60) + stime.second)
        if (hour_difference >= 8): # More than 8 hour branch
            x_axis_label = "Universal Time in Hours (HH)"
            for i in range(hour_difference + 1):
                factor = hour_difference % 2
                if (i % 2 == factor):
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour = current_hour,
                                                       minute= current_minute,
                                                       second = current_second))
                    current_hour += 2

        elif (hour_difference >=5):
            x_axis_label = "Universal Time in Hours (HH)"
            for hour in range(stime.hour, etime.hour+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour = current_hour,
                                                   minute= current_minute,
                                                   second = current_second))
                current_hour += 1
                    
        elif (hour_difference >= 2):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 30 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))

        elif (hour_difference >= 1):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 15 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
            
            
        elif (minute_difference >= 30):
            # assuming a 30 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 10 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
        elif (minute_difference >= 20):
            # assuming a 20 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))

        elif (minute_difference >=10):
            # assuming a 10 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
                
        elif (minute_difference >= 7):
            # assuming a 7 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 2 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
            
        elif (minute_difference >= 2):
            # assuming a 2 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=minute,
                                                   second=current_second))
        elif (minute_difference >= 1):
            # assuming a 1 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                for second in range(stime.second, etime.second + 1):
                    if second % 20 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=current_hour,
                                                           minute=minute,
                                                           second=second))
            
        elif (second_difference >= 45):
            # assuming 45 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 15 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 25):
            # assuming 25 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 10 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 10):
            # assuming 10 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))

        elif(second_difference >= 5):
            # assuming 5 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 1.5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
            
        else:
            # assuming less than a 5 second gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=current_minute,
                                                   second=second))



    fig = plt.figure(figsize=(12, 4))
    
    plt.plot(timeArr,yArr, linewidth = 1)
    plt.title("Geomagnetic By of " + station_name + "   YEARDAY: " + year_day_value +  "   DATE: " + date) 
    plt.ylabel('By')
    plt.xlabel(x_axis_label)

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.xticks(hours_arr) # setting the xaxis time ticks to custom values
    plt.gca().xaxis.set_major_formatter(x_axis_format)

    return fig

   

def z_plot(zArr, timeArr, filename, stime, etime) :
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


    current_hour = stime.hour # setting the hour to start at
    current_minute = stime.minute # setting the minute to start at
    current_second = stime.second # setting the second to start at
    default_hours_flag = False # using a flag to better optimize operations
    x_axis_label = ""
    
    #List of the hours and finding which ones to use
    #default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hours_arr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    #default_hours_flag = False # using a flag to better optimize operations

    

    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hours_arr.append(datetime.datetime(year=1111, month=1,day=1,hour = i,minute=current_minute,second = current_second)) # adding the odd numbers to the list     


    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value


    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")

    year_of_record = (int)(date[6:])
    month_of_record = (int)(date[0:2])
    day_of_record = (int)(date[3:5])

    x_axis_format = mdates.DateFormatter('%H')

    #Actual Plot


    if not default_hours_flag:
        hour_difference = etime.hour - stime.hour # Getting the difference in time
        minute_difference = ((etime.hour * 60) + etime.minute) - ((stime.hour * 60) + stime.minute)
        second_difference = ((etime.hour * 3600) + (etime.minute * 60) + etime.second) - ((stime.hour * 3600) + (stime.minute * 60) + stime.second)
        if (hour_difference >= 8): # More than 8 hour branch
            x_axis_label = "Universal Time in Hours (HH)"
            for i in range(hour_difference + 1):
                factor = hour_difference % 2
                if (i % 2 == factor):
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour = current_hour,
                                                       minute= current_minute,
                                                       second = current_second))
                    current_hour += 2

        elif (hour_difference >=5):
            x_axis_label = "Universal Time in Hours (HH)"
            for hour in range(stime.hour, etime.hour+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour = current_hour,
                                                   minute= current_minute,
                                                   second = current_second))
                current_hour += 1
                    
        elif (hour_difference >= 2):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 30 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))

        elif (hour_difference >= 1):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 15 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
            
            
        elif (minute_difference >= 30):
            # assuming a 30 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 10 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
        elif (minute_difference >= 20):
            # assuming a 20 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))

        elif (minute_difference >=10):
            # assuming a 10 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
                
        elif (minute_difference >= 7):
            # assuming a 7 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 2 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
            
        elif (minute_difference >= 2):
            # assuming a 2 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=minute,
                                                   second=current_second))
        elif (minute_difference >= 1):
            # assuming a 1 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                for second in range(stime.second, etime.second + 1):
                    if second % 20 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=current_hour,
                                                           minute=minute,
                                                           second=second))
            
        elif (second_difference >= 45):
            # assuming 45 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 15 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 25):
            # assuming 25 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 10 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 10):
            # assuming 10 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))

        elif(second_difference >= 5):
            # assuming 5 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 1.5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
            
        else:
            # assuming less than a 5 second gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=current_minute,
                                                   second=second))



    fig = plt.figure(figsize=(12, 4)) #size of graph
    
    plt.plot(timeArr,zArr, linewidth = 1)
    plt.title("Geomagnetic Bz of " + station_name + "   YEARDAY: " + year_day_value+  "   DATE: " + date) 
    plt.ylabel('Bz')
    plt.xlabel(x_axis_label)
    

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.xticks(hours_arr) # setting the xaxis time ticks to custom values
    plt.gca().xaxis.set_major_formatter(x_axis_format)

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

def x_and_y_plot(xArr, yArr, timeArr, filename, stime, etime) :
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
    #default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hours_arr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    #default_hours_flag = False # using a flag to better optimize operations

    current_hour = stime.hour # setting the hour to start at
    current_minute = stime.minute # setting the minute to start at
    current_second = stime.second # setting the second to start at
    default_hours_flag = False # using a flag to better optimize operations
    x_axis_label = ""

    x_axis_format = mdates.DateFormatter('%H')

    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hours_arr.append(datetime.datetime(year=1111,month=1,day=1,hour = i,minute=current_minute,second = current_second)) # adding the odd numbers to the list
            


    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")

    year_of_record = (int)(date[6:])
    month_of_record = (int)(date[0:2])
    day_of_record = (int)(date[3:5])

    #Actual Plot

    if not default_hours_flag:
        hour_difference = etime.hour - stime.hour # Getting the difference in time
        minute_difference = ((etime.hour * 60) + etime.minute) - ((stime.hour * 60) + stime.minute)
        second_difference = ((etime.hour * 3600) + (etime.minute * 60) + etime.second) - ((stime.hour * 3600) + (stime.minute * 60) + stime.second)
        if (hour_difference >= 8): # More than 8 hour branch
            x_axis_label = "Universal Time in Hours (HH)"
            for i in range(hour_difference + 1):
                factor = hour_difference % 2
                if (i % 2 == factor):
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour = current_hour,
                                                       minute= current_minute,
                                                       second = current_second))
                    current_hour += 2

        elif (hour_difference >=5):
            x_axis_label = "Universal Time in Hours (HH)"
            for hour in range(stime.hour, etime.hour+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour = current_hour,
                                                   minute= current_minute,
                                                   second = current_second))
                current_hour += 1
                    
        elif (hour_difference >= 2):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 30 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))

        elif (hour_difference >= 1):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 15 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
            
            
        elif (minute_difference >= 30):
            # assuming a 30 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 10 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
        elif (minute_difference >= 20):
            # assuming a 20 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))

        elif (minute_difference >=10):
            # assuming a 10 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
                
        elif (minute_difference >= 7):
            # assuming a 7 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 2 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
            
        elif (minute_difference >= 2):
            # assuming a 2 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=minute,
                                                   second=current_second))
        elif (minute_difference >= 1):
            # assuming a 1 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                for second in range(stime.second, etime.second + 1):
                    if second % 20 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=current_hour,
                                                           minute=minute,
                                                           second=second))
            
        elif (second_difference >= 45):
            # assuming 45 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 15 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 25):
            # assuming 25 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 10 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 10):
            # assuming 10 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))

        elif(second_difference >= 5):
            # assuming 5 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 1.5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
            
        else:
            # assuming less than a 5 second gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=current_minute,
                                                   second=second))
    

    fig = plt.figure(figsize=(12, 4))#size of graph

    x_values = xArr #The list of values to change 
    offset = xArr[0] #The amount to subtract from each value  
    x_values = list(map(lambda x : x - offset, x_values)) #applies the subtraction x-offset to each value, converts the result back to a list

    y_values = yArr #The list of values to change 
    offset = yArr[0] #the amount to subtract from each value
    y_values = list(map(lambda y : y - offset, y_values))
    
    
    plt.plot(timeArr,x_values, linewidth = 1, label = 'Bx Values')
    plt.plot(timeArr,y_values, linewidth = 1, label = 'By Values')
    
    plt.title("Geomagnetic Bx and By of " + station_name + "   YEARDAY: " + year_day_value +  "   DATE: " + date) 
    plt.ylabel('Bx and By')
    plt.xlabel(x_axis_label)

    plt.legend(loc = 'upper left', prop={'size': 8}, fontsize='medium')

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
    

    #add an if statement for when if they want a pdf or a png
    #file_option = file_option.lower()
    #if(file_option == 'pdf'):
        #fig.savefig('x_and_y_plot.pdf', format='pdf', dpi=1200)
    #elif(file_option == 'png'):
        #fig.savefig('x_and_y_plot.png', format = 'png', dpi = 1200)
    #else :
        #print(file_option + "is not supported filetype")
        #sys.exit(0)

def x_and_z_plot(xArr, zArr, timeArr, filename, stime, etime) :
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
    #default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hours_arr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    #default_hours_flag = False # using a flag to better optimize operations

    current_hour = stime.hour # setting the hour to start at
    current_minute = stime.minute # setting the minute to start at
    current_second = stime.second # setting the second to start at
    default_hours_flag = False # using a flag to better optimize operations
    x_axis_label = ""

    x_axis_format = mdates.DateFormatter('%H')

    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hours_arr.append(datetime.datetime(year=1111, month=1,day=1,hour = i,minute=current_minute,second = current_second)) # adding the odd numbers to the list
            


    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")

    year_of_record = (int)(date[6:])
    month_of_record = (int)(date[0:2])
    day_of_record = (int)(date[3:5])
    #Actual Plot


    if not default_hours_flag:
        hour_difference = etime.hour - stime.hour # Getting the difference in time
        minute_difference = ((etime.hour * 60) + etime.minute) - ((stime.hour * 60) + stime.minute)
        second_difference = ((etime.hour * 3600) + (etime.minute * 60) + etime.second) - ((stime.hour * 3600) + (stime.minute * 60) + stime.second)
        if (hour_difference >= 8): # More than 8 hour branch
            x_axis_label = "Universal Time in Hours (HH)"
            for i in range(hour_difference + 1):
                factor = hour_difference % 2
                if (i % 2 == factor):
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour = current_hour,
                                                       minute= current_minute,
                                                       second = current_second))
                    current_hour += 2

        elif (hour_difference >=5):
            x_axis_label = "Universal Time in Hours (HH)"
            for hour in range(stime.hour, etime.hour+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour = current_hour,
                                                   minute= current_minute,
                                                   second = current_second))
                current_hour += 1
                    
        elif (hour_difference >= 2):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 30 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))

        elif (hour_difference >= 1):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 15 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
            
            
        elif (minute_difference >= 30):
            # assuming a 30 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 10 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
        elif (minute_difference >= 20):
            # assuming a 20 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=day_of_record,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))

        elif (minute_difference >=10):
            # assuming a 10 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
                
        elif (minute_difference >= 7):
            # assuming a 7 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 2 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
            
        elif (minute_difference >= 2):
            # assuming a 2 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=minute,
                                                   second=current_second))
        elif (minute_difference >= 1):
            # assuming a 1 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                for second in range(stime.second, etime.second + 1):
                    if second % 20 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=current_hour,
                                                           minute=minute,
                                                           second=second))
            
        elif (second_difference >= 45):
            # assuming 45 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 15 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 25):
            # assuming 25 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 10 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 10):
            # assuming 10 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=1,
                                                       minute=current_minute,
                                                       second=second))

        elif(second_difference >= 5):
            # assuming 5 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 1.5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
            
        else:
            # assuming less than a 5 second gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=current_minute,
                                                   second=second))

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
    plt.xlabel(x_axis_label)


    plt.legend(loc = 'upper left', prop={'size': 8}, fontsize='medium')
    
    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted
    plt.xticks(hours_arr)
    plt.gca().xaxis.set_major_formatter(x_axis_format)
    plt.axhline(y = 0,color = 'tab:gray', linestyle = '-')

    

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


def y_and_z_plot(yArr, zArr, timeArr, filename, stime, etime) :
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
    #default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hours_arr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    #default_hours_flag = False # using a flag to better optimize operations

    current_hour = stime.hour # setting the hour to start at
    current_minute = stime.minute # setting the minute to start at
    current_second = stime.second # setting the second to start at
    default_hours_flag = False # using a flag to better optimize operations
    x_axis_label = ""

    x_axis_format = mdates.DateFormatter('%H')

    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hours_arr.append(datetime.datetime(year=1111,month=1,day=1,hour = i,minute=current_minute,second = current_second)) # adding the odd numbers to the list
           


    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")

    year_of_record = (int)(date[6:])
    month_of_record = (int)(date[0:2])
    day_of_record = (int)(date[3:5])
    #Actual Plot


    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True
        x_axis_label = "Universal Time in Hours (HH)"
        for i in range(24):
            if (i % 2 != 0):
                hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour = i,
                                                           minute=current_minute,
                                                           second = current_second))
            

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        hour_difference = etime.hour - stime.hour # Getting the difference in time
        minute_difference = ((etime.hour * 60) + etime.minute) - ((stime.hour * 60) + stime.minute)
        second_difference = ((etime.hour * 3600) + (etime.minute * 60) + etime.second) - ((stime.hour * 3600) + (stime.minute * 60) + stime.second)
        if (hour_difference >= 8): # More than 8 hour branch
            x_axis_label = "Universal Time in Hours (HH)"
            for i in range(hour_difference + 1):
                factor = hour_difference % 2
                if (i % 2 == factor):
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour = current_hour,
                                                       minute= current_minute,
                                                       second = current_second))
                    current_hour += 2

        elif (hour_difference >=5):
            x_axis_label = "Universal Time in Hours (HH)"
            for hour in range(stime.hour, etime.hour+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour = current_hour,
                                                   minute= current_minute,
                                                   second = current_second))
                current_hour += 1
                    
        elif (hour_difference >= 2):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 30 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))

        elif (hour_difference >= 1):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 15 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
            
            
        elif (minute_difference >= 30):
            # assuming a 30 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 10 == 0:
                        hours_arr.append(datetime.datetime(year=1,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
        elif (minute_difference >= 20):
            # assuming a 20 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))

        elif (minute_difference >=10):
            # assuming a 10 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
                
        elif (minute_difference >= 7):
            # assuming a 7 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 2 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
            
        elif (minute_difference >= 2):
            # assuming a 2 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=minute,
                                                   second=current_second))
        elif (minute_difference >= 1):
            # assuming a 1 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                for second in range(stime.second, etime.second + 1):
                    if second % 20 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=current_hour,
                                                           minute=minute,
                                                           second=second))
            
        elif (second_difference >= 45):
            # assuming 45 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 15 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 25):
            # assuming 25 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 10 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 10):
            # assuming 10 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))

        elif(second_difference >= 5):
            # assuming 5 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 1.5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
            
        else:
            # assuming less than a 5 second gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=current_minute,
                                                   second=second))

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
    plt.xlabel(x_axis_label)#x label 


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
    

    #add an if statement for when if they want a pdf or a png
    #file_option = file_option.lower()
    #if(file_option == 'pdf'):
        #fig.savefig('y_and_z_plot.pdf', format='pdf', dpi=1200)
    #elif(file_option == 'png'):
        #fig.savefig('y_and_z_plot.png', format = 'png', dpi = 1200)
    #else :
        #print(file_option + "is not supported filetype")
        #sys.exit(0)


def x_y_and_z_plot(xArr, yArr, zArr, timeArr, filename, stime, etime) :
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
    #default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hours_arr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    #default_hours_flag = False # using a flag to better optimize operations

    current_hour = stime.hour # setting the hour to start at
    current_minute = stime.minute # setting the minute to start at
    current_second = stime.second # setting the second to start at
    default_hours_flag = False # using a flag to better optimize operations
    x_axis_label = ""

    x_axis_format = mdates.DateFormatter('%H')

    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hours_arr.append(datetime.datetime(year=1111,month=1,day=1,hour = i,minute=current_minute,second = current_second)) # adding the odd numbers to the list
            


    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")
    
    year_of_record = (int)(date[6:])
    month_of_record = (int)(date[0:2])
    day_of_record = (int)(date[3:5])
    
    #Actual Plot


    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True
        x_axis_label = "Universal Time in Hours (HH)"
        for i in range(24):
            if (i % 2 != 0):
                hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour = i,
                                                           minute=current_minute,
                                                           second = current_second))
            

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        hour_difference = etime.hour - stime.hour # Getting the difference in time
        minute_difference = ((etime.hour * 60) + etime.minute) - ((stime.hour * 60) + stime.minute)
        second_difference = ((etime.hour * 3600) + (etime.minute * 60) + etime.second) - ((stime.hour * 3600) + (stime.minute * 60) + stime.second)
        if (hour_difference >= 8): # More than 8 hour branch
            x_axis_label = "Universal Time in Hours (HH)"
            for i in range(hour_difference + 1):
                factor = hour_difference % 2
                if (i % 2 == factor):
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour = current_hour,
                                                       minute= current_minute,
                                                       second = current_second))
                    current_hour += 2

        elif (hour_difference >=5):
            x_axis_label = "Universal Time in Hours (HH)"
            for hour in range(stime.hour, etime.hour+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour = current_hour,
                                                   minute= current_minute,
                                                   second = current_second))
                current_hour += 1
                    
        elif (hour_difference >= 2):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 30 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))

        elif (hour_difference >= 1):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 15 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
            
            
        elif (minute_difference >= 30):
            # assuming a 30 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 10 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
        elif (minute_difference >= 20):
            # assuming a 20 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))

        elif (minute_difference >=10):
            # assuming a 10 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
                
        elif (minute_difference >= 7):
            # assuming a 7 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 2 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
            
        elif (minute_difference >= 2):
            # assuming a 2 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                hours_arr.append(datetime.datetime(year=1111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=minute,
                                                   second=current_second))
        elif (minute_difference >= 1):
            # assuming a 1 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                for second in range(stime.second, etime.second + 1):
                    if second % 20 == 0:
                        hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour=current_hour,
                                                           minute=minute,
                                                           second=second))
            
        elif (second_difference >= 45):
            # assuming 45 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 15 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 25):
            # assuming 25 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 10 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 10):
            # assuming 10 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 3 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))

        elif(second_difference >= 5):
            # assuming 5 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 1.5 == 0:
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
            
        else:
            # assuming less than a 5 second gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                hours_arr.append(datetime.datetime(year=111,
                                                   month=1,
                                                   day=1,
                                                   hour=current_hour,
                                                   minute=current_minute,
                                                   second=second))

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


    arrayX, arrayY, arrayZ, timeArr = read_raw_to_lists(two_hz_binary_file, start_time, end_time)
    

    X = 'X'
    Y = 'Y'
    Z = 'Z'

    #try:
    #plot_axis(arrayX, timeArr, filename, start_time, end_time, X)
    print("got past plot_axis")
    #plot_axis(arrayY, timeArr, filename, stime, etime, Y)
    #plot_axis(arrayZ, timeArr, filename, stime, etime, Z)
    #x_plot(arrayX, timeArr, filename, start_time, end_time)
#    y_plot(arrayY, timeArr, filename, start_time, end_time)
  #  z_plot(arrayZ, timeArr, filename, start_time, end_time)
   # x_and_y_plot(arrayX, arrayY, timeArr, filename, start_time, end_time)
    #x_and_z_plot(arrayX, arrayZ, timeArr, filename, start_time, end_time)
    #y_and_z_plot(arrayY, arrayZ, timeArr, filename, start_time, end_time)
    #x_y_and_z_plot(arrayX, arrayY, arrayZ, timeArr, filename, start_time, end_time)
    
    
    #except:
        #print('Could not plot arrays to testgraph.pdf')
        #sys.exit(0)









