# TODO - MACCS Space Data Python #

Here are some ideas for python data processing programs

* Data remover - Given a file and two times, remove all the data records
  between the two times and write out the shortened file.
  
* Axis remover - Given a file, an axis name, and two times, flatten
  out the data value for the given axis between the two times.

-----------
Ted's Stuff |
---------------------------------------------------------------------------------------------
- Rename python files in repo -------------------------------------------------------- done |
	git mv oldName.py new_name.py                                                       |
- Remove old unused python files from repo ------------------------------------------- done |
	git rm unused.py
- Unexpected crashing -- due to plt.close() ------------------------------------------ done |
- save as not saving any information to file ----------------------------------------- done |
- Fixing clean files ----------------------------------------------------------------- done |
- get plot min and max to work for x, y, and z --------------------------------------- done |
- x-axis time go off of the second difference ---------------------------------------- done |
- x-axis 1 hour time slot ------------------------------------------------------------ done |
- Format time to display 24:00:00 ---------------------------------------------------- done |
- start time and end time functions that hands back a time stamp --------------------- done |
- see if we can lower where the x-ticks are located ---------------------------------- done |
- plot time both all the way on the left and all the way on the right ---------------- done |
- Erik's converting the list reading into seconds instead of hours ------------------- |
- Implement Erik's changes ----------------------------------------------------------- |
--------------------------------------------------------------------------------------------

New things to implement
- rename main file to be "line_X.py" -- done
- start displaying seconds only when we are going to use the seconds (at 3 minutes we display every 30 seconds)
- starting at 2 mins/90 seconds (we display every 15 seconds)
- need to catch reverse time
- 

Algorithm
- x-axis time formatter create_time_list function passes in time_arr
- first if statement (changes the label and the format)
- elif statements reduction
- pick a delta (10, 15, 20, 1hr)
- walk through every single datetime in the list
  	- if evenly divisible by delta
		- tick_list.add(datetime object)
- 