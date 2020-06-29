# raw_to_screen.py
#
# 2020 May - Created - Erik Steinmetz
#

""" Raw Data Printer

Proceeds through a 2 Hz MACCS data file printing the time-stamped
x, y, and z values to standard out.

"""


# Python 3 imports
import sys
import datetime

# MACCS imports
from raw_codecs import decode, time_of_record


def print_one_record( raw_record) :
    """ Prints a single 2 Hz record to standard out.

    Prints the timestamp, x, y, and z values to a single line
    on standard out.

    Parameters
    ----------
    raw_record :
        A byte array that is 38 bytes long, containing a single
        record in the SRI 2 Hz format.
    """

    hour = raw_record[4]
    minute = raw_record[5]
    second = raw_record[6]
    timestamp = f"{hour:02d}:{minute:02d}:{second:02d}"
    x1 = decode( raw_record[18:21]) / 40.0
    x1_str = f"{x1:12.3f}"
    y1 = decode( raw_record[21:24]) / 40.0
    y1_str = f"{y1:12.3f}"
    z1 = decode( raw_record[24:27]) / 40.0
    z1_str = f"{z1:12.3f}"
    print( timestamp + x1_str + y1_str + z1_str)


def print_contents( infile, stime, etime) :
    """ Prints the given file to standard out beginning at the given time.

    Prints the records in the file object by reading them one at a time
    beginning at the given time until the end of the file.

    Parameters
    ----------
    infile :
        The file object to be read.
    stime :
        The datetime.time object from which to begin
    etime :
        The datetime.time object at which to end
    """

    while True :
        one_record = infile.read( 38)
        if not one_record :
            break
        current_time = time_of_record(one_record)
        if current_time >= stime :
            print_one_record( one_record)
        if current_time >= etime :
            break


if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        print( "Usage: python3 raw_to_screen.py filename [starttime [endtime]]")
        sys.exit(0)   # Exit with no error code
    filename = sys.argv[1]
    two_hz_binary_file = open(filename, "rb")
    start_time = datetime.time.fromisoformat( "00:00:00")
    end_time = datetime.time.fromisoformat("23:59:59")
    if len(sys.argv) >= 3 :
        # iso format for a time is HH:MM:SS
        start_time = datetime.time.fromisoformat(sys.argv[2])
    if len(sys.argv) == 4 :
        end_time = datetime.time.fromisoformat(sys.argv[3])
    print_contents( two_hz_binary_file, start_time, end_time)
