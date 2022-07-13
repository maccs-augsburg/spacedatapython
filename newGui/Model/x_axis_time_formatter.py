'''
x_axis_time_formatter.py

August 2021 -- Created -- Ted Strombeck

Updated 7/x/22 - Mark Ortega-Ponce
'''
# Python 3 imports
import datetime

# Matplotlib imports
import matplotlib.dates as mdates
from sympy import sec

SEC_PER_HOUR = 3600

def create_time_list(stime, etime):
	"""
	Creates the correct time list for the x-axis labels 
	for plotting within the given start and end times.

	Parameters
	----------
	Datetime.time
		stime: The starting time stamp.
		etime: The ending time stamp.
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

	x_axis_format = mdates.DateFormatter('%H')
	hours_arr = [] # list to use for custom times
	current_hour = stime.hour # setting the hour to start at
	current_minute = stime.minute # setting the minute to start at
	current_second = stime.second # setting the second to start at
	x_axis_label = "Universal Time in Hours (HH)" # The label of the x-axis to use
	

	# if we have the default starting times
	if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):

		for i in range(24):
			if (i % 2 != 0):
				hours_arr.append(datetime.datetime(year=1111,
												month=1,
												day=1,
												hour = i,
												minute = current_minute,
												second = current_second))
	else:
		# Going off of the second difference
		# Ex: 4 hour range = 14,400
		total_time_diff_seconds = ((etime.hour * SEC_PER_HOUR) + (etime.minute * 60) + etime.second)
		total_time_diff_seconds -= ((stime.hour * SEC_PER_HOUR) + (stime.minute * 60) + stime.second)
		# 14,400 / 3600 
		if ((total_time_diff_seconds / SEC_PER_HOUR) >= 8): # More than or equal to 8 hour branch
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours (HH)"

			# iterating throughout the hours
			for i in range(int(total_time_diff_seconds / SEC_PER_HOUR) + 1):
				# Assuming we have 9, 32400, results in factor being 
				odd_or_even = int(total_time_diff_seconds / SEC_PER_HOUR) % 2
			
				# Only adding the hour to the hours_arr if it is the same as the odd_or_even
				if (i % 2 == odd_or_even):
					# Adding to the hours_arr list
					hours_arr.append(datetime.datetime(year=1111,
													   month=1,
													   day=1,
													   hour = current_hour,
													   minute= current_minute,
													   second = current_second))
					# incrementing current_hour
					current_hour += 2

		# More than or equal to 5 hour branch
		elif ((total_time_diff_seconds / SEC_PER_HOUR) >=5):
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours (HH)"

			# iterating throughout the hours and adding every hour to the hours_arr list
			for hour in range(stime.hour, etime.hour+1):
				hours_arr.append(datetime.datetime(year=1111,
												   month=1,
												   day=1,
												   hour = current_hour,
												   minute= current_minute,
												   second = current_second))
				# incrementing current_hour
				current_hour += 1

		# More than or equal to 2 hour branch
		elif ((total_time_diff_seconds / SEC_PER_HOUR) >= 2):
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
		
			# setting the x-axis datetime formatter
			x_axis_format = mdates.DateFormatter('%H:%M')
			# iterating through the hours
			# get current hour, and start adding ticks from there
			hour = stime.hour
			minute = stime.minute
			second = 0
			counter = minute
			if counter > 30:
				counter -= 30

			for i in range (total_time_diff_seconds):
				# 1800 = 30 min in seconds
				# Append values every 30 mins like previously
				if i % 60 == 0 and i != 0:
					minute += 1
					counter += 1
					if minute == 60:
						minute = 0
						hour += 1

				if counter == 30:
					# reset counter
					counter = 0
					# set second value to 0, only care about HH:MM
					hours_arr.append(datetime.datetime(year = 1111,
													month = 1,
													day = 1,
													hour = hour,
													minute = minute,
													second = 0))

		# More than or equal to 1 hour branch up to 1:59:59 because of last check
		elif ((total_time_diff_seconds / SEC_PER_HOUR) >= 1):
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours and Minutes (HH:MM)"
			# setting the x-axis datetime formatter
			x_axis_format = mdates.DateFormatter('%H:%M')

			hour = stime.hour
			minute = stime.minute
			# counter = current minute, eg. 13, want timestamps in 15 min intervals
			# just keep it the same as it was before
			if minute > 15:
				counter = minute % 15
			else:
				counter = minute
			
			for i in range (total_time_diff_seconds + 1):
				
				if i % 60 == 0 and i != 0:
					minute += 1
					counter += 1
					if minute == 60:
						minute = 0
						hour += 1

				if counter == 15:
					counter = 0
					hours_arr.append(datetime.datetime(
											year = 1111,
											month = 1,
											day = 1,
											hour = hour,
											minute = minute,
											second = 0))
		
		# More than or equal to 30 minutes branch
		elif ((total_time_diff_seconds / 60) >= 30):
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
			# setting the x-axis datetime formatter
			x_axis_format = mdates.DateFormatter('%H:%M:%S')

			hour = stime.hour
			minute = stime.minute
			second = stime.second
			counter = minute % 10

			if minute % 10 == 0:
				hours_arr.append(datetime.datetime(
									year = 1111,
									month = 1,
									day = 1,
									hour = hour,
									minute = minute,
									second = second))
				print(hours_arr)
			
			for i in range (total_time_diff_seconds + 1):
			
				if i % 60 == 0 and i != 0:
					minute += 1
					counter += 1
					if minute == 60:
						minute = 0
						hour += 1
				
				if counter == 10:
					counter = 0
					hours_arr.append(datetime.datetime(
										year = 1111,
										month = 1,
										day = 1,
										hour = hour,
										minute = minute,
										second = second))
			#print(hours_arr)

		# More than or equal to 20 minutes branch
		elif ((total_time_diff_seconds / 60) >= 20):
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
			# setting the x-axis datetime formatter
			x_axis_format = mdates.DateFormatter('%H:%M:%S')

			hour = stime.hour
			minute = stime.minute
			counter = minute % 5

			if minute % 5 == 0:
				hours_arr.append(datetime.datetime(
									year = 1111,
									month = 1,
									day = 1,
									hour = hour,
									minute = minute,
									second = 0))

			for i in range (total_time_diff_seconds + 1):

				if i % 60 == 0 and i != 0:
					minute += 1
					counter += 1
					if minute == 60:
						minute = 0
						hour += 1
				if counter == 5:
					counter = 0
					hours_arr.append(datetime.datetime(
										year = 1111,
										month = 1,
										day = 1,
										hour = hour,
										minute = minute,
										second = 0))

		# More than or equal to 10 minutes branch
		elif ((total_time_diff_seconds / 60) >=10):
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

			# setting the x-axis datetime formatter
			x_axis_format = mdates.DateFormatter('%H:%M:%S')

			# iterating through the minutes
			for minute in range(stime.minute, etime.minute+1):
				# only appending the values for every 3 minutes
				if minute % 3 == 0:
					# appending to the hours_arr list
					hours_arr.append(datetime.datetime(year=1111,
													   month=1,
													   day=1,
													   hour=current_hour,
													   minute=minute,
													   second=current_second))
			
		# More than or equal to 7 minutes branch
		elif ((total_time_diff_seconds / 60) >= 7):
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"
			# setting the x-axis datetime formatter
			x_axis_format = mdates.DateFormatter('%H:%M:%S')
			

			# iterating through the minutes
			for minute in range(stime.minute, etime.minute+1):
				# only appending the values for every 2 minutes
				if minute % 2 == 0:
					# appending to the hours_arr list
					hours_arr.append(datetime.datetime(year=1111,
													   month=1,
													   day=1,
													   hour=current_hour,
													   minute=minute,
													   second=current_second))
		# More than or equal to 2 minutes branch
		elif ((total_time_diff_seconds / 60) >= 2):
			x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

			# setting the x-axis datetime formatter
			x_axis_format = mdates.DateFormatter('%H:%M:%S')

			# iterating through the minutes
			for minute in range(stime.minute, etime.minute+1):
				# appending to the hours_arr list for every minute
				hours_arr.append(datetime.datetime(year=1111,
												   month=1,
												   day=1,
												   hour=current_hour,
												   minute=minute,
												   second=current_second))

		# More than or equal to 1 minute branch
		elif (total_time_diff_seconds >= 60):
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

			# setting the x-axis datetime formatter
			x_axis_format = mdates.DateFormatter('%H:%M:%S')

			# iterating through the minutes
			for minute in range(stime.minute, etime.minute+1):
				# iterating through the seconds
				for second in range(stime.second, etime.second + 1):
					# only appending the values for every 20 seconds
					if second % 20 == 0:
						# appending to the hours_arr list
						hours_arr.append(datetime.datetime(year=1111,
														   month=1,
														   day=1,
														   hour=current_hour,
														   minute=minute,
														   second=second))
		
		elif (total_time_diff_seconds >= 45): # More than or equal to 45 seconds branch
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

			# setting the x-axis datetime formatter
			x_axis_format = mdates.DateFormatter('%H:%M:%S')

			# iterating through the seconds
			for second in range(stime.second, etime.second + 1):
				# only appending the values for every 15 seconds
				if second % 15 == 0:
					# appending to the hours_arr list
					hours_arr.append(datetime.datetime(year=1111,
													   month=1,
													   day=1,
													   hour=current_hour,
													   minute=current_minute,
													   second=second))
				
		elif(total_time_diff_seconds >= 25): # More than or equal to 25 seconds branch
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

			# setting the x-axis datetime formatter
			x_axis_format = mdates.DateFormatter('%H:%M:%S')

			# iterating through the seconds
			for second in range(stime.second, etime.second + 1):
				# only appending the values for every 10 seconds
				if second % 10 == 0:
					# appending to the hours_arr list
					hours_arr.append(datetime.datetime(year=1111,
													   month=1,
													   day=1,
													   hour=current_hour,
													   minute=current_minute,
													   second=second))
		
		# More than or equal to 10 seconds branch
		elif(total_time_diff_seconds >= 10):
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

			# setting the x-axis datetime formatter
			x_axis_format = mdates.DateFormatter('%H:%M:%S')

			# iterating through the seconds
			for second in range(stime.second, etime.second + 1):
				# only appending the values for every 3 seconds
				if second % 3 == 0:
					# appending to the hours_arr list
					hours_arr.append(datetime.datetime(year=1111,
													   month=1,
													   day=1,
													   hour=current_hour,
													   minute=current_minute,
													   second=second))

		 # More than or equal to 5 seconds branch
		elif(total_time_diff_seconds >= 6):
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

			# setting the x-axis datetime formatter
			x_axis_format = mdates.DateFormatter('%H:%M:%S')

			# iterating through the seconds
			for second in range(stime.second, etime.second + 1):
				# only appending the values for every 1 second
				if second % 2 == 0:
					# appending to the hours_arr list
					hours_arr.append(datetime.datetime(year=1111,
													   month=1,
													   day=1,
													   hour=current_hour,
													   minute=current_minute,
													   second=second))
		
		else: # Assuming a gap that is less than 6 seconds
			# setting the x-axis label
			x_axis_label = "Universal Time in Hours, Minutes, and Seconds (HH:MM:SS)"

			# setting the x-axis datetime formatter
			x_axis_format = mdates.DateFormatter('%H:%M:%S')

			# iterating through the seconds
			for second in range(stime.second, etime.second + 1):
				# appending to the hours_arr list for every second
				hours_arr.append(datetime.datetime(year=1111,
												   month=1,
												   day=1,
												   hour=current_hour,
												   minute=current_minute,
												   second=second))
									   
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


def rewrite_helper(stime, etime):

	x_axis_format = mdates.DateFormatter('%H')
	x_axis_label = "Universal Time in Hours (HH)" # The label of the x-axis to use
	hours_arr = [] # list to use for custom times

	hour_step = None
	minute_step = None
	second_step = None

	# Going off of the second difference
	# Ex: 4 hour range = 14,400
	total_time_diff_seconds = ((etime.hour * SEC_PER_HOUR) + (etime.minute * 60) + etime.second)
	total_time_diff_seconds -= ((stime.hour * SEC_PER_HOUR) + (stime.minute * 60) + stime.second)

	# 1st two cases do step by hour in ticks
	if total_time_diff_seconds / SEC_PER_HOUR >= 8:
		hour_step = 2
	elif total_time_diff_seconds / SEC_PER_HOUR >= 5:
		hour_step = 1

	if total_time_diff_seconds / SEC_PER_HOUR >= 2:
		minute_step = 30
	elif total_time_diff_seconds / SEC_PER_HOUR >= 1:
		minute_step = 15
	elif total_time_diff_seconds / 60 >= 30:
		minute_step = 10
	elif total_time_diff_seconds / 60 >= 20:
		minute_step = 5
	elif total_time_diff_seconds / 60 >= 10:
		minute_step = 3
	elif total_time_diff_seconds / 60 >= 7:
		minute_step = 2
	elif total_time_diff_seconds / 60 >= 2:
		minute_step = 1

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