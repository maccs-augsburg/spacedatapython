# cl_plot_stacked.py
#
# 2022 June - Created - Erik Steinmetz
#

""" Command line tool to create a stacked plot.

Creates a stacked plot in either pdf or png format for a given input
file. Start and end times may also be selected.

"""

# Python 3 imports
import sys
import datetime
import numpy as np
import statistics as stats

# MACCS imports
from raw_codecs import decode, time_of_record
import station_names
from plot_stacked_graphs import plot_arrays

# Matplotlib imports
import matplotlib.pyplot as plt
from matplotlib.ticker import(MultipleLocator, AutoMinorLocator)
import matplotlib.dates as mdates

# Plotter program imports
import read_raw_to_lists
import x_axis_time_formatter

import sys
import os


if __name__ == "__main__":
    ### usage message in console
    if len(sys.argv) < 2 :
        print( "Usage: python3 cl_plot_stacked.py filename [starttime [endtime] ]")
        sys.exit(0) # Exiting without an error code
        
    # filename
    filename = sys.argv[1]
    # file option
    file_option = 'pdf' # defaulting with the pdf option

    # try and catch block for bad file name
    try:
        two_hz_binary_file = open(filename, "rb") # attempting to open the file
    except:
        print('Could not open file: ' + filename)
        sys.exit(0) # Exiting without an error code

    ### initializing start and end times
    start_time = datetime.time.fromisoformat( "00:00:00")
    end_time = datetime.time.fromisoformat("23:59:59")

    ### If we get more than 2 items in the console/command line
    if len(sys.argv) == 3 : # if we have 3 items in the command line we assume that it is for specifying file type option
        file_option = sys.argv[2]
    elif len(sys.argv) >= 4 :
        # iso format for a time is HH:MM:SS
        start_time = datetime.time.fromisoformat(sys.argv[2])
        end_time = datetime.time.fromisoformat(sys.argv[3])
    if len(sys.argv) == 5:
        file_option = sys.argv[4]
    if len(sys.argv) >= 6:
        print( "TOO many items entered please try again!" ) # Not sure what else we should do but we should have something to handle if we get toooo many inputs.
        sys.exit(0) # Exiting without an error code


    ### Creating x, y, and z arrays -- NOW INCLUDING START AND END TIMES!!!
    arrayX, arrayY, arrayZ, time_arr = read_raw_to_lists.create_datetime_lists_from_raw(two_hz_binary_file, start_time, end_time, os.path.basename( filename))

    print("Got the arrays, starttime", start_time, " endtime", end_time)
    ### Plotting said arrays -- NOW INCLUDING START AND END TIMES AND FILE OPTION!!!
    # try and catch block to handle error in case file is already open
    try:
        filename = os.path.basename( filename)
        figure = plot_arrays(arrayX, arrayY, arrayZ, time_arr, filename, start_time, end_time, 0, 0, 0, 0, 0, 0)
        print("Got the figure.")
        #plt.show()
        figure.savefig( "thisistest.png", format='png', dpi=1200)
        print("Saved to thisistest.png")
    except:
        print('Could not plot arrays to testgraph.pdf, file is open')
        sys.exit(0) # Exiting without an error code

