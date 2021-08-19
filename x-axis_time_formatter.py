# x-axis_time_formatter.py
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


def create_time_list( stime, etime):
    x_axis_format = mdates.DateFormatter('%H')
    hours_arr = [] # list to use for custom times
    current_hour = stime.hour # setting the hour to start at
    current_minute = stime.minute # setting the minute to start at
    current_second = stime.second # setting the second to start at
    x_axis_label = "Universal Time in Hours (HH)" # The label of the x-axis to use

    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        for i in range(24):
            if (i % 2 != 0):
                hours_arr.append(datetime.datetime(year=year_of_record,
                                                           month=month_of_record,
                                                           day=day_of_record,
                                                           hour = i,
                                                           minute=current_minute,
                                                           second = current_second))
    else:
        hour_difference = etime.hour - stime.hour # Getting the difference in time
        minute_difference = ((etime.hour * 60) + etime.minute) - ((stime.hour * 60) + stime.minute)
        second_difference = ((etime.hour * 3600) + (etime.minute * 60) + etime.second) - ((stime.hour * 3600) + (stime.minute * 60) + stime.second)

        if (hour_difference >= 8): # More than 8 hour branch
            x_axis_label = "Universal Time in Hours (HH)"
            for i in range(hour_difference + 1):
                factor = hour_difference % 2
                if (i % 2 == factor):
                    hours_arr.append(datetime.datetime(year=year_of_record,
                                                       month=month_of_record,
                                                       day=day_of_record,
                                                       hour = current_hour,
                                                       minute= current_minute,
                                                       second = current_second))
                    current_hour += 2

        elif (hour_difference >=5):
            x_axis_label = "Universal Time in Hours (HH)"
            for hour in range(stime.hour, etime.hour+1):
                hours_arr.append(datetime.datetime(year=year_of_record,
                                                   month=month_of_record,
                                                   day=day_of_record,
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
                        hours_arr.append(datetime.datetime(year=year_of_record,
                                                           month=month_of_record,
                                                           day=day_of_record,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))

        elif (hour_difference >= 1):
            x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
            x_axis_format = mdates.DateFormatter('%H:%M')
            for hour in range(stime.hour, etime.hour+1):
                for minute in range(stime.minute, etime.minute+1):
                    if minute % 15 == 0:
                        hours_arr.append(datetime.datetime(year=year_of_record,
                                                           month=month_of_record,
                                                           day=day_of_record,
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
                        hours_arr.append(datetime.datetime(year=year_of_record,
                                                           month=month_of_record,
                                                           day=day_of_record,
                                                           hour=hour,
                                                           minute=minute,
                                                           second=current_second))
        elif (minute_difference >= 20):
            # assuming a 20 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 5 == 0:
                    hours_arr.append(datetime.datetime(year=year_of_record,
                                                       month=month_of_record,
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
                    hours_arr.append(datetime.datetime(year=year_of_record,
                                                       month=month_of_record,
                                                       day=day_of_record,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
                
        elif (minute_difference >= 7):
            # assuming a 7 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                if minute % 2 == 0:
                    hours_arr.append(datetime.datetime(year=year_of_record,
                                                       month=month_of_record,
                                                       day=day_of_record,
                                                       hour=current_hour,
                                                       minute=minute,
                                                       second=current_second))
            
        elif (minute_difference >= 2):
            # assuming a 2 minute or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for minute in range(stime.minute, etime.minute+1):
                hours_arr.append(datetime.datetime(year=year_of_record,
                                                   month=month_of_record,
                                                   day=day_of_record,
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
                        hours_arr.append(datetime.datetime(year=year_of_record,
                                                           month=month_of_record,
                                                           day=day_of_record,
                                                           hour=current_hour,
                                                           minute=minute,
                                                           second=second))
            
        elif (second_difference >= 45):
            # assuming 45 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 15 == 0:
                    hours_arr.append(datetime.datetime(year=year_of_record,
                                                       month=month_of_record,
                                                       day=day_of_record,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 25):
            # assuming 25 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 10 == 0:
                    hours_arr.append(datetime.datetime(year=year_of_record,
                                                       month=month_of_record,
                                                       day=day_of_record,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
        elif(second_difference >= 10):
            # assuming 10 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 3 == 0:
                    hours_arr.append(datetime.datetime(year=year_of_record,
                                                       month=month_of_record,
                                                       day=day_of_record,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))

        elif(second_difference >= 5):
            # assuming 5 second or more gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                if second % 1.5 == 0:
                    hours_arr.append(datetime.datetime(year=year_of_record,
                                                       month=month_of_record,
                                                       day=day_of_record,
                                                       hour=current_hour,
                                                       minute=current_minute,
                                                       second=second))
            
        else:
            # assuming less than a 5 second gap
            x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
            x_axis_format = mdates.DateFormatter('%H:%M:%S')
            for second in range(stime.second, etime.second + 1):
                hours_arr.append(datetime.datetime(year=year_of_record,
                                                   month=month_of_record,
                                                   day=day_of_record,
                                                   hour=current_hour,
                                                   minute=current_minute,
                                                   second=second))

    return hours_arr, x_axis_format, x_axis_label
