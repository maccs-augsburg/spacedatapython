# cl_plot_stacked.py
#
# 2022 June - Created - Erik Steinmetz
#

""" Command line tool to create a stacked plot.

Creates a stacked plot in either pdf or png format for a given input
file. Start and end times may also be selected.

"""

# Python 3 imports
import argparse
import datetime
import os
import sys

# MACCS imports
#from newGui.Model.raw_codecs import decode, time_of_record
#import station_names
from newGui.View.plot_stacked_graphs import plot_arrays
# plot_arrays
from newGui.Model.read_raw_to_lists import create_datetime_lists_from_raw
# create_datetime_lists_from_raw
from newGui.Model.read_clean_to_lists import create_datetime_lists_from_clean
# create_datetime_lists_from_clean
from file_naming import create_2hz_plot_file_name


def main():
    """
    Implements a command line tool to create a stacked plot given the
    command line arguments as input parameters.    
    """
    
    ### Retrieve from the command line arguments and store information
    ### or the default values in variables
    
    # Read the command line arguments. They are
    #  optional flag for file type - default to pdf
    #  required filename
    #  optional starttime - default to "00:00:00"
    #  optional endtime - default to "23:59:59"
    parser = argparse.ArgumentParser()
    parser.add_argument('--png', action='store_true', help="output to a png file")
    parser.add_argument('filename', type=str, help="name of the input file")
    parser.add_argument('stime', type=str, nargs='?', 
        default="00:00:00", help="start time for the plot")
    parser.add_argument('etime', type=str, nargs='?',
        default="23:59:59", help="end time for the plot")
    args = parser.parse_args()
    
    # the base_filename has no path included, just the filename
    base_filename = os.path.basename( args.filename)
    extension = os.path.splitext(base_filename)[1]

    # starttime, endtime, and output file type
    start_time = datetime.time.fromisoformat( args.stime)
    end_time = datetime.time.fromisoformat( args.etime)
    output_file_type = 'pdf' # defaulting with the pdf option
    if args.png:
        output_file_type = 'png'

    ### Open the file for reading
    try:
        two_hz_binary_file = open(args.filename, "rb") # attempting to open the file
    except:
        print('Could not open file: ' + args.filename)
        sys.exit(0) # Exiting without an error code

    ### Creating x, y, z, and time arrays 
    if extension == '.2hz' :
        arrayX, arrayY, arrayZ, time_arr = create_datetime_lists_from_raw(
            two_hz_binary_file, start_time, end_time, base_filename)
        level_for_filename = "0"
    elif extension == '.s2' :
        arrayX, arrayY, arrayZ, time_arr, flags_arr = create_datetime_lists_from_clean(
            two_hz_binary_file, start_time, end_time, base_filename)
        level_for_filename = "1"
    else:
        print(f"What kind of file was that?")  # FIXME - better error handling
        sys.exit(0)
        
    ### Create a plot with given arrays
    figure = plot_arrays(
        arrayX, arrayY, arrayZ, time_arr, 
        base_filename, start_time, end_time, 
        0, 0, 0, 0, 0, 0)
    
    ### Write the plot to a file
    try:
        out_filename = create_2hz_plot_file_name( base_filename, args.stime, args.etime)
        out_filename = out_filename + "." + output_file_type
        figure.savefig( out_filename, format=output_file_type, dpi=1200)
        print(f"Saved to {out_filename}")
    except:
        print(f'Could not plot arrays to {out_filename}')



if __name__ == "__main__":
    main()
