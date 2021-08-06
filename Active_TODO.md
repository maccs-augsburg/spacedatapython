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
- x time axis ------------------------------------------------------------------------ just adjust |
- default file name and save it where it is running ---------------------------------- |
- default screen size 900 tall and 1400 wide ----------------------------------------- done |
- Implement it in gui ---------------------------------------------------------------- done |
- No variables for ttk.Label --------------------------------------------------------- done |

- No tilts -------------------------------------------------------------- done | 
- No microsecond -------------------------------------------------------- done |
- Smaller ticks for smaller time periods --------------------------------------------- |
- 5-6 ticks for smaller numbers ------------------------------------------------------ |
- walk through lists of floats, and convert them into datetime objects --------------- working on|


- canvas_plotter.py get main working ------------------------------------------------- done |

- look over Erik's example class code ------------------------------------------------ |
Class stuff ------------------------------------------------ done

New things -------------------------------------------------
- *args - set of optional set of arguments - done
- Background area different color than the control area
------------------------------------------------------------

Not yet required ----------------------------------------------------------------------|
- implment changes that Erik makes (usually when we merge from main)
- get test into one canvas
- missing data should be a blank gap on graph (no line)
- open up save dialogue box?
--------------------------------------------------------------------------------------------

- Any time to save a file, do not override file with the same name
- plot first and then save later 
	- 3 options: quit w/o saving, save and continue, and save and quit