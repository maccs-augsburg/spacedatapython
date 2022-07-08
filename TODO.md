# TODO - MACCS Space Data Python #

Here are some ideas for python data processing programs

* Data remover - Given a file and two times, remove all the data records
  between the two times and write out the shortened file.
  
* Axis remover - Given a file, an axis name, and two times, flatten
  out the data value for the given axis between the two times.

* FIXME - CD21153.s2 file, when testing the guard clause for deleting old figures,
    I found that it would work on most files, and prevent user from replotting the same data
    but found that it wasn't working with CD21153.s2. I also noticed that the min axis
    entries were greater than the max axis entries in some inputs.
