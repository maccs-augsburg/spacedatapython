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
- Heavy test x-axis time code -------------------------------------------------------- |
--------------------------------------------------------------------------------------------