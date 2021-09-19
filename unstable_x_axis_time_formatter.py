# x_axis_time_formatter.py
#
# August 2021 -- Created -- Ted Strombeck
#

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

def new_create_time_list( time_arr, delta=(2*3600), default_array=False): # initializing the delta to 2 hours (in seconds)
    x_axis_format = mdates.DateFormatter('%H')
    hours_arr = []
    #current_hour = time_arr[0].hour
    #current_minute = time_arr[0].minute
    #current_second = time_arr[0].second
    x_axis_label = "Universal Time in Hours (HH)"
    time_in_seconds = -1
    
    if default_array:
    	for item in time_arr:
    		if item.hour % 2 != 0:
    			hours_arr.append(item)
    else:
    	for item in time_arr:
    		time_in_seconds = (item.hour * 3600) + (item.minute * 60) + item.second
    		if (time_in_seconds % delta == 0):
    			hours_arr.append(item)
    

    return hours_arr, x_axis_format, x_axis_label

def create_time_list( stime, etime):
    """
    Creates the correct time list for the x-axis labels for plotting within the given start and end times

    Parameters
    ----------
    Datetime.time
        stime: the starting time stamp
        etime: the ending time stamp

    Returns
    -------
    List
        hours_arr: the list of datetime.datetime objects to be plotted

    mdates.DateFormatter
        x_axis_format: the DateFormatter object which specifies how to display the datetime.datetime objects

    String
        x_axis_label: the String value that will be used to label the x_axis
    """
    x_axis_format = mdates.DateFormatter('%H')
    hours_arr = [] # list to use for custom times
    current_hour = stime.hour # setting the hour to start at
    current_minute = stime.minute # setting the minute to start at
    current_second = stime.second # setting the second to start at
    x_axis_label = "Universal Time in Hours (HH)" # The label of the x-axis to use

    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        for i in range(24):
            if (i % 2 != 0):
                hours_arr.append(datetime.datetime(year=1111,
                                                           month=1,
                                                           day=1,
                                                           hour = i,
                                                           minute=current_minute,
                                                           second = current_second))
    else:
        # Going off of the second difference
        second_difference = ((etime.hour * 3600) + (etime.minute * 60) + etime.second) - ((stime.hour * 3600) + (stime.minute * 60) + stime.second)
		
        if ((second_difference / 3600) >= 8): # More than or equal to 8 hour branch
            for second in range(second_difference):
                test_hour = int(second / 3600)
                test_minute = int(second / 60)
                test_second = second - int(test_hour * 3600) - int(test_minute * 60)
                
                #  showing results every 2 hours
                if (test_hour % 2 == 0):
                	hours_arr.append(datetime.datetime(year=1111, month=1, day=1, hour=test_hour, minute=0, second=0))
                	test_hour += 2
                # if (test_hour % 2 == 0) and (test_minute == 0) and (test_second == 0):
#                     hours_arr.append(datetime.datetime(year=1111,
#                                                        month=1,
#                                                        day=1,
#                                                        hour = test_hour + current_hour,
#                                                        minute = test_minute + current_minute,
#                                                        second = test_second))
            # setting the x-axis label
##            x_axis_label = "Universal Time in Hours (HH)"
##
##            # iterating throughout the hours
##            for i in range(int(second_difference / 3600) + 1):
##                factor = int(second_difference / 3600) % 2
##                
##                # Only adding the hour to the hours_arr if it is the same as the factor
##                if (i % 2 == factor):
##                    # Adding to the hours_arr list
##                    hours_arr.append(datetime.datetime(year=1111,
##                                                       month=1,
##                                                       day=1,
##                                                       hour = current_hour,
##                                                       minute= current_minute,
##                                                       second = current_second))
##                    # incrementing current_hour
##                    current_hour += 2

        elif ((second_difference / 3600) >=5): # More than or equal to 5 hour branch
            # setting the x-axis label
            x_axis_label = "Universal Time in Hours (HH)"

            # iterating throughout the hours and adding every hour to the hours_arr list
##            for hour in range(stime.hour, etime.hour+1):
##                hours_arr.append(datetime.datetime(year=1111,
##                                                   month=1,
##                                                   day=1,
##                                                   hour = current_hour,
##                                                   minute= current_minute,
##                                                   second = current_second))
##                # incrementing current_hour
##                current_hour += 1
                    
        elif ((second_difference / 3600) >= 2): # More than or equal to 2 hour branch
            # setting the x-axis label
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            
            # setting the x-axis datetime formatter
            x_axis_format = mdates.DateFormatter('%H:%M')

            
            

            # iterating through the hours
##            for hour in range(stime.hour, etime.hour+1):
##                # iterating through the minutes
##                for minute in range(stime.minute, etime.minute+1):
##                    # only appending the values for every 30 minutes
##                    if minute % 30 == 0:
##                        # appending to the hours_arr list
##                        hours_arr.append(datetime.datetime(year=1111,
##                                                           month=1,
##                                                           day=1,
##                                                           hour=current_hour,
##                                                           minute=current_minute,
##                                                           second=current_second))
##                    current_minute += 1
##                current_hour += 1

        elif ((second_difference / 3600) >= 1): # More than or equal to 1 hour branch
            # setting the x-axis label
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"

            # setting the x-axis datetime formatter
            x_axis_format = mdates.DateFormatter('%H:%M')

            # time in seconds for loop that works!!!
            for second in range(second_difference):
                test_hour = int(second / 3600)
                test_minute = int(second / 60)
                test_second = second - (test_hour * 3600) - (test_minute * 60)
                
                #  showing results every 15 minutes
                if (test_minute % 15 == 0) and (test_second == 0):
                    hours_arr.append(datetime.datetime(year=1111,
                                                       month=1,
                                                       day=1,
                                                       hour = test_hour + current_hour,
                                                       minute = test_minute + current_minute,
                                                       second = test_second))
            
            
        elif ((second_difference / 60) >= 30): # More than or equal to 30 minutes branch
            # setting the x-axis label
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

            # setting the x-axis datetime formatter
            x_axis_format = mdates.DateFormatter('%H:%M:%S')

            # iterating through the hours
##            for hour in range(stime.hour, etime.hour+1):
##                # iterating through the minutes
##                for minute in range(stime.minute, etime.minute+1):
##                    # only appending the values for every 10 minutes
##                    if minute % 10 == 0:
##                        # appending to the hours_arr list
##                        hours_arr.append(datetime.datetime(year=1111,
##                                                           month=1,
##                                                           day=1,
##                                                           hour=hour,
##                                                           minute=minute,
##                                                           second=current_second))
##                        
        elif ((second_difference / 60) >= 20): # More than or equal to 20 minutes branch
            # setting the x-axis label
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

            # setting the x-axis datetime formatter
            x_axis_format = mdates.DateFormatter('%H:%M:%S')

            # iterating through the minutes
##            for minute in range(stime.minute, etime.minute+1):
##                # only appending the values for every 5 minutes
##                if minute % 5 == 0:
##                    # appending to the hours_arr list
##                    hours_arr.append(datetime.datetime(year=1111,
##                                                       month=1,
##                                                       day=1,
##                                                       hour=current_hour,
##                                                       minute=minute,
##                                                       second=current_second))

        elif ((second_difference / 60) >=10): # More than or equal to 10 minutes branch
            # setting the x-axis label
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

            # setting the x-axis datetime formatter
            x_axis_format = mdates.DateFormatter('%H:%M:%S')

            # iterating through the minutes
##            for minute in range(stime.minute, etime.minute+1):
##                # only appending the values for every 3 minutes
##                if minute % 3 == 0:
##                    # appending to the hours_arr list
##                    hours_arr.append(datetime.datetime(year=1111,
##                                                       month=1,
##                                                       day=1,
##                                                       hour=current_hour,
##                                                       minute=minute,
##                                                       second=current_second))
                
        elif ((second_difference / 60) >= 7): # More than or equal to 7 minutes branch
            # setting the x-axis label
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

            # setting the x-axis datetime formatter
            x_axis_format = mdates.DateFormatter('%H:%M:%S')

            # iterating through the minutes
##            for minute in range(stime.minute, etime.minute+1):
##                # only appending the values for every 2 minutes
##                if minute % 2 == 0:
##                    # appending to the hours_arr list
##                    hours_arr.append(datetime.datetime(year=1111,
##                                                       month=1,
##                                                       day=1,
##                                                       hour=current_hour,
##                                                       minute=minute,
##                                                       second=current_second))
            
        elif ((second_difference / 60) >= 2): # More than or equal to 2 minutes branch
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

            # setting the x-axis datetime formatter
            x_axis_format = mdates.DateFormatter('%H:%M:%S')

            # iterating through the minutes
##            for minute in range(stime.minute, etime.minute+1):
##                # appending to the hours_arr list for every minute
##                hours_arr.append(datetime.datetime(year=1111,
##                                                   month=1,
##                                                   day=1,
##                                                   hour=current_hour,
##                                                   minute=minute,
##                                                   second=current_second))

                
        elif (second_difference >= 60): # More than or equal to 1 minute branch
            # setting the x-axis label
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

            # setting the x-axis datetime formatter
            x_axis_format = mdates.DateFormatter('%H:%M:%S')

            # iterating through the minutes
##            for minute in range(stime.minute, etime.minute+1):
##                # iterating through the seconds
##                for second in range(stime.second, etime.second + 1):
##                    # only appending the values for every 20 seconds
##                    if second % 20 == 0:
##                        # appending to the hours_arr list
##                        hours_arr.append(datetime.datetime(year=1111,
##                                                           month=1,
##                                                           day=1,
##                                                           hour=current_hour,
##                                                           minute=minute,
##                                                           second=second))
            
        elif (second_difference >= 45): # More than or equal to 45 seconds branch
            # setting the x-axis label
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

            # setting the x-axis datetime formatter
            x_axis_format = mdates.DateFormatter('%H:%M:%S')

            # iterating through the seconds
##            for second in range(stime.second, etime.second + 1):
##                # only appending the values for every 15 seconds
##                if second % 15 == 0:
##                    # appending to the hours_arr list
##                    hours_arr.append(datetime.datetime(year=1111,
##                                                       month=1,
##                                                       day=1,
##                                                       hour=current_hour,
##                                                       minute=current_minute,
##                                                       second=second))
                    
        elif(second_difference >= 25): # More than or equal to 25 seconds branch
            # setting the x-axis label
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

            # setting the x-axis datetime formatter
            x_axis_format = mdates.DateFormatter('%H:%M:%S')

            # iterating through the seconds
##            for second in range(stime.second, etime.second + 1):
##                # only appending the values for every 10 seconds
##                if second % 10 == 0:
##                    # appending to the hours_arr list
##                    hours_arr.append(datetime.datetime(year=1111,
##                                                       month=1,
##                                                       day=1,
##                                                       hour=current_hour,
##                                                       minute=current_minute,
##                                                       second=second))
                    
        elif(second_difference >= 10): # More than or equal to 10 seconds branch
            # setting the x-axis label
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

            # setting the x-axis datetime formatter
            x_axis_format = mdates.DateFormatter('%H:%M:%S')

            # iterating through the seconds
##            for second in range(stime.second, etime.second + 1):
##                # only appending the values for every 3 seconds
##                if second % 3 == 0:
##                    # appending to the hours_arr list
##                    hours_arr.append(datetime.datetime(year=1111,
##                                                       month=1,
##                                                       day=1,
##                                                       hour=current_hour,
##                                                       minute=current_minute,
##                                                       second=second))

        elif(second_difference >= 6): # More than or equal to 5 seconds branch
            # setting the x-axis label
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

            # setting the x-axis datetime formatter
            x_axis_format = mdates.DateFormatter('%H:%M:%S')

            # iterating through the seconds
##            for second in range(stime.second, etime.second + 1):
##                # only appending the values for every 1 second
##                if second % 2 == 0:
##                    # appending to the hours_arr list
##                    hours_arr.append(datetime.datetime(year=1111,
##                                                       month=1,
##                                                       day=1,
##                                                       hour=current_hour,
##                                                       minute=current_minute,
##                                                       second=second))
            
        else: # Assuming a gap that is less than 6 seconds
            # setting the x-axis label
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

            # setting the x-axis datetime formatter
            x_axis_format = mdates.DateFormatter('%H:%M:%S')

            # iterating through the seconds
##            for second in range(stime.second, etime.second + 1):
##                # appending to the hours_arr list for every second
##                hours_arr.append(datetime.datetime(year=1111,
##                                                   month=1,
##                                                   day=1,
##                                                   hour=current_hour,
##                                                   minute=current_minute,
##                                                   second=second))
                                           
    # if we are only showing hours, we need the hours to be aligned in the correct spots
    if (stime.minute != 0) and (x_axis_label == 'Universal Time in Hours (HH)'):
        for i in range(len(hours_arr)):
            hours_arr[i] = datetime.datetime(year=1111,
                                             month=1,
                                             day=1,
                                             hour=hours_arr[i].hour,
                                             minute = 0,
                                             second = hours_arr[i].second)
                                             
                                             
    
            
    

    return hours_arr, x_axis_format, x_axis_label
