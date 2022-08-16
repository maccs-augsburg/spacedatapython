'''
x_axis_time_formatter.py

August 2021 -- Created -- Ted Strombeck

Rewritten 7/x/22 - Mark Ortega-Ponce
'''
# Python 3 imports
import datetime
from this import d
# Matplotlib imports
import matplotlib.dates as mdates
# Constant time values
SEC_PER_HOUR = 3600
SEC_PER_MIN = 60

def create_time_list(stime, etime, time_record):
	"""
	Creates the correct time list for the x-axis labels 
	for plotting within the given start and end times.

	Parameters
	----------
	Datetime.time
		stime: The starting time stamp for plotting the day.
		etime: The ending time stamp for plotting the day.
		datetime: One record from time_arr, returned from create_datetime_from_filetype.
					Used to put the associated date along with time.
	Returns
	-------
	list
		hours_arr: The list of datetime.datetime objects to be plotted.
	mdates.DateFormatter
		x_axis_format: The DateFormatter object which 
				specifies how to display the datetime.datetime objects.
	string
		x_axis_label: the String value that will be used to label the x_axis
	"""	
	year = time_record.year
	month = time_record.month
	day = time_record.day

	# return default ticks if we have default time set in gui
	if (stime == datetime.time.fromisoformat("00:00:00") and etime == datetime.time.fromisoformat("23:59:59")):
		return get_default_ticks(year, month, day)

	hour_step = None
	minute_step = None
	second_step = None
	# Going off of the second difference
	# Subtract total end time in seconds by total start time in seconds
	total_time_diff_seconds = ((etime.hour * SEC_PER_HOUR) + (etime.minute * 60) + etime.second)
	total_time_diff_seconds -= ((stime.hour * SEC_PER_HOUR) + (stime.minute * 60) + stime.second)

	# 1st two cases do step by hour in ticks
	if total_time_diff_seconds / SEC_PER_HOUR >= 8:
		hour_step = 2
	elif total_time_diff_seconds / SEC_PER_HOUR >= 5:
		hour_step = 1

	if hour_step is not None:

		return get_hour_ticks(hour_step, stime, total_time_diff_seconds, year, month, day)

	# Next few cases we step by minute
	if total_time_diff_seconds / SEC_PER_HOUR >= 2:
		minute_step = 30
	elif total_time_diff_seconds / SEC_PER_HOUR >= 1:
		minute_step = 15
	elif total_time_diff_seconds / SEC_PER_MIN >= 30:
		minute_step = 10
	elif total_time_diff_seconds / SEC_PER_MIN >= 20:
		minute_step = 5
	elif total_time_diff_seconds / SEC_PER_MIN >= 10:
		minute_step = 3
	elif total_time_diff_seconds / SEC_PER_MIN >= 7:
		minute_step = 2
	elif total_time_diff_seconds / SEC_PER_MIN >= 2:
		minute_step = 1

	if minute_step is not None:
		return get_minute_ticks(minute_step, stime, total_time_diff_seconds, year, month, day)

	# Last few cases are for ticks with seconds included
	if total_time_diff_seconds >= 60:
		second_step = 20
	elif total_time_diff_seconds >= 45:
		second_step = 15
	elif total_time_diff_seconds >= 25:
		second_step = 10
	elif total_time_diff_seconds >= 10:
		second_step = 3
	elif total_time_diff_seconds >= 6:
		second_step = 2
	else:
		second_step = 1
	
	if second_step is not None:
		return get_second_ticks(second_step, stime, total_time_diff_seconds, year, month, day)


def get_default_ticks(year, month, day):

	x_axis_format = mdates.DateFormatter('%H')
	x_axis_label = "Universal Time in Hours (HH)"
	hours_arr = []

	for i in range(24):
		if (i % 2 != 0):
			hours_arr.append(datetime.datetime(year=year,
											month=month,
											day=day,
											hour = i,
											minute = 0,
											second = 0))

	return hours_arr, x_axis_format, x_axis_label

def get_hour_ticks(hour_step, stime, total_time_diff_seconds, year, month, day):
	# setting the x-axis label
	x_axis_label = "Universal Time in Hours (HH)"
	x_axis_format = mdates.DateFormatter('%H')
	hours_arr = []
	current_hour = stime.hour
	# iterating throughout the hours
	for i in range(int(total_time_diff_seconds / SEC_PER_HOUR) + 1):
		# Assuming we have 9, 32400 total seconds, results in being odd
		odd_or_even = int(total_time_diff_seconds / SEC_PER_HOUR) % hour_step
	
		# Only adding the hour to the hours_arr if it is the same as the odd_or_even
		# This is how Ted had it, if up to me I would taken it out
		# but must be here for some reason
		if (i % hour_step == odd_or_even):
			# Adding to the hours_arr list
			hours_arr.append(datetime.datetime(
									year=year,
									month=month,
									day=day,
									hour = current_hour,
									minute = 0,
									second = 0))
			# incrementing current_hour
			current_hour += hour_step

	return hours_arr, x_axis_format, x_axis_label

def get_minute_ticks(minute_step, stime, total_time_diff_seconds, year, month, day):
	# setting the x-axis label
	x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
	# setting the x-axis datetime formatter
	x_axis_format = mdates.DateFormatter('%H:%M')
	hours_arr = []
	hour = stime.hour
	minute = stime.minute
	counter = minute % minute_step

	# grab initial value if it matches criteria
	# gets skipped in loop
	if minute % minute_step == 0:
		hours_arr.append(datetime.datetime(
							year = year, 
							month = month,
							day = day, 
							hour = hour,
							minute = minute, 
							second = 0))

	for i in range (total_time_diff_seconds + 1):
		# 1800 = 30 min in seconds
		# Append values every 30 mins like previously
		if i % 60 == 0 and i != 0:
			minute += 1
			counter += 1
			if minute == 60:
				minute = 0
				hour += 1

		if counter == minute_step:
			# reset counter
			counter = 0
			# set second value to 0, only care about HH:MM
			hours_arr.append(datetime.datetime(
									year = year,
									month = month,
									day = day,
									hour = hour,
									minute = minute,
									second = 0))

	return hours_arr, x_axis_format, x_axis_label

def get_second_ticks(second_step, stime, total_time_diff_seconds, year, month, day):

	x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
	# setting the x-axis datetime formatter
	x_axis_format = mdates.DateFormatter('%H:%M:%S')
	hours_arr = []

	hour = stime.hour
	minute = stime.minute
	second = stime.second
	counter = second % second_step

	# grab initial value if it matches criteria
	# gets skipped in loop
	if second % second_step == 0:
		hours_arr.append(datetime.datetime(
								year = 1111,
								month = 1,
								day = 1,
								hour = hour,
								minute = minute,
								second = second))

	for i in range (total_time_diff_seconds):
		second += 1
		counter += 1

		if second % 60 == 0 and second != 0:
			second = 0
			minute += 1
			if minute == 60:
				minute = 0
				hour += 1

		if counter == second_step:
			counter = 0
			hours_arr.append(datetime.datetime(
										year = year,
										month = month,
										day = day,
										hour = hour,
										minute = minute,
										second = second))

	return hours_arr, x_axis_format, x_axis_label