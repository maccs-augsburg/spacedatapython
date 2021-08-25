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
- break out x time axis into separate file ------------------------------------------- done |
- Dump the leftmost label on x-time axis if it goes over the origin ------------------ done |
- x-time axis when the minutes != 0, labels are in incorrect spots ------------------- done |
- 3 rows for options (Plot, \n Save, Save As... \n Quit) ----------------------------- done |
- Add the unicode character for elipses on the Save As ------------------------------- done |
- Put the 4:30 label at 4 ------------------------------------------------------------ done |
- Get the centers of the two subplots and fix y-axis --------------------------------- done |
- make end time defaulted to 24:00:00 ---------------- datetime objects only go to 23:59:59 |
- "Open..." button to autofill in station code and yearday --------------------------- done |
- Cancel button to cancel that file selection ------------------------- Not sure if needed? |
- Zoom w Erik about y-axis ----------------------------------------------------------- done |
- find the overall center point of the day in terms of y ----------------------------- done |
- create function that finds the max and min of a list y axis ------------------------ done |
- x diff, y diff, z diff ------------------------------------------------------------- done |
- mid x , mid y, and mid z ----------------------------------------------------------- done |
- find biggest difference + 5% ------------------------------------------------------- done |
- halfway up the biggest diff + 5% --------------------------------------------------- done |
- clean data file implemenation ------------------------------------------------------ done |
- Heavy test x-axis time code -------------------------------------------------------- done |
- Reset counters when selecting a new file ------------------------------------------- done |
--------------------------------------------------------------------------------------------


New things!-----------------------------------
- Unexpected crashing? -- due to plt.close() change it and commit - done
- save as not saving any information to file - done (still should test)
- Clean files ---- done
	- plotting extreme values (32767000)
		- if we read in fake data don't plot it
		- if test_for_nodata = 32767000:
			continue
- get plot min and max to work for x, y, and z
- x-axis 1 hour time slot
- see if we can lower where the x-ticks are located
- plot time both all the way on the left and all the way on the right
- x-time axis go off of the second difference
- Format time to display 24:00:00 when in reality
- start time and end time functions that hands back a time stamp

- Erik's converting the list reading into seconds instead of hours
----------------------------------------------

