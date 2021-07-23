# TODO - MACCS Space Data Python #

Here are some ideas for python data processing programs

* Data remover - Given a file and two times, remove all the data records
  between the two times and write out the shortened file.
  
* Axis remover - Given a file, an axis name, and two times, flatten
  out the data value for the given axis between the two times.

-----------
Ted Stuff |
--------------------------------------------------------------------------------------------
- Rename python files in repo -------------------------------------------------------- done |
	git mv oldName.py new_name.py                                                       |
- Remove old unused python files from repo ------------------------------------------- done |
	git rm unused.py
- Canvas test one gui not separate windows ------------------------------------------- done |
- get canvas to plot values from a file ---------------------------------------------- done |
- Canvas test takes up the left side of the window ----------------------------------- |
- Change pop up screen to show the values of plot min and max's ---------------------- |
- Get cancel button to close both windows instead of just one ------------------------ done |
- Save as file option buttons? ------------------------------------------------------- |
- x time axis ------------------------------------------------------------------------ |
- more than 8 hours then we use a tick every 2 hours --------------------------------- |
- more than 3 hours (less than 8) we use a tick every hour (HH:mm) ------------------- |
- less than 3 hours (HH:mm:ss) ------------------------------------------------------- |
- convert time from 1.5 to 1 hour 30 mins (type of deal) ----------------------------- |

Not yet required ----------------------------------------------------------------------|
- implment changes that Erik makes (usually when we merge from main)
- get test into one canvas
- iaga2002/clean data converter files (to implement when Erik codes it)
- missing data should be a blank gap (no line)
--------------------------------------------------------------------------------------------

- Any time to save a file, do not override file with the same name
- plot first and then save later 
	- 3 options: quit w/o saving, save and continue, and save and quit