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
- start displaying seconds only when we are going to use the seconds (at 3 minutes we display every 30 seconds)
- starting at 2min/90 seconds we display every 15 seconds ---------------------------- |
- need to catch reverse time --------------------------------------------------------- |
- MAIN ALGORITHM --------------------------------------------------------------------- |
	- x-axis time formatter create_time_list function passes in time_arr ------------- |
	- first if statement (changes the label and foramt) ------------------------------ |
	- elif statements reduction ------------------------------------------------------ |
	- pick a delta (10, 15, 20, 1hr) ------------------------------------------------- |
	- walk through every single datetime in the list --------------------------------- |
		- if evenly divisible by delta ----------------------------------------------- |
			- tick_list.add(datetime object) ----------------------------------------- |
--------------------------------------------------------------------------------------------
