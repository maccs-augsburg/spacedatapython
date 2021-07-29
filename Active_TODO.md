# TODO - MACCS Space Data Python #

Here are some ideas for python data processing programs

* Data remover - Given a file and two times, remove all the data records
  between the two times and write out the shortened file.
  
* Axis remover - Given a file, an axis name, and two times, flatten
  out the data value for the given axis between the two times.

-----------
Ted Stuff |
---------------------------------------------------------------------------------------------
- Rename python files in repo -------------------------------------------------------- done |
	git mv oldName.py new_name.py                                                       |
- Remove old unused python files from repo ------------------------------------------- done |
	git rm unused.py
- Canvas test one gui not separate windows ------------------------------------------- done |
- get canvas to plot values from a file ---------------------------------------------- done |
- Canvas GUI refactor to look like original gui -------------------------------------- |
- Get cancel button to close both windows instead of just one ------------------------ done |
- Save as file option buttons? ------------------------------------------------------- |
- x time axis ------------------------------------------------------------------------ almost done|
- try plotting with datetime.datetime objects ---------------------------------------- done |
- more than 8 hours then we use a tick every 2 hours --------------------------------- done |
- more than 3 hours (less than 8) we use a tick every hour (HH:mm) ------------------- done |
- less than 3 hours (HH:mm:ss) ------------------------------------------------------- done |
- implement create_lists_from_clean() function --------------------------------------- done |
- make main work in raw_to_plot.py file ---------------------------------------------- done |
- align the labels in GUI to the right side ------------------------------------------ done |
- fully comment and document everything ---------------------------------------------- |
- default file name and save it where it is running ---------------------------------- |
- default screen size 900 tall and 1400 wide ----------------------------------------- done |
- add starting time and end time entry boxes to canvas GUI --------------------------- |

Not yet required ----------------------------------------------------------------------|
- implment changes that Erik makes (usually when we merge from main)
- get test into one canvas
- missing data should be a blank gap on graph (no line)
- open up save dialogue box?
--------------------------------------------------------------------------------------------

- Any time to save a file, do not override file with the same name
- plot first and then save later 
	- 3 options: quit w/o saving, save and continue, and save and quit