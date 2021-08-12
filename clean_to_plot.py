# clean_to_plot.py
#
# August 2021 -- Created -- Ted Strombeck
#

""" Python Plotter

Code to test and use clean MACCS data files which graphs the time-stamped
x, y, and z values on its' own plot.

"""

#TODO----------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------

# Python 3 import
import sys
import datetime

# MACCS imports
from raw_codecs import decode, time_of_record
import station_names

# Matplotlib imports
import matplotlib.pyplot as plt
from matplotlib.ticker import(MultipleLocator, AutoMinorLocator)
import matplotlib.dates as mdates

# Plotter program imports
import read_clean_to_lists

