# TODO - MACCS Space Data Python #

Here are some ideas for python data processing programs

* Data remover - Given a file and two times, remove all the data records
  between the two times and write out the shortened file. (Done)
  
* Axis remover - Given a file, an axis name, and two times, flatten
  out the data value for the given axis between the two times. (Done. New: What happens if we use None for AXIS_FLATTENER value? How do we write this out to the file?)
  
* Spec file - Move to only using one .spec file

* Linux Installer

* Improve efficiency of reading IAGA2002 files to lists, on mac there is the rainbow wheel. Not sure about windows.

* Possible use QGroupBox widgets to instead group the different widgets together
  allows for better visual apperances and to keep sections together

* Possible QTabWidget for the graph display widgets and or tab to have multiple plots open?

* Zoom out button / Previous

* (Accessability options) Add user graph display manip such as setting three axis graph to have different style lines  for a color blind person instead of just showing colors

* Get rid of some of the functions in new_gui.py and move them to another file because theres a lot of functions
  and im sure we can better maintain them in differetn smaller files that group together better
