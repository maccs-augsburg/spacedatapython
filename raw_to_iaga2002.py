# raw_to_iaga2002.py
#
# 2020 June - Created - Erik Steinmetz
#

""" Raw to IAGA 2002 format converter

Proceeds through a 2 Hz MACCS raw data file writing the time-stamped
x, y, and z values to a file in the IAGA 2002 format.

"""


# Python 3 imports
import sys
import datetime

# MACCS imports
from raw_codecs import decode, time_of_record


def one_record_to_string( raw_record) :
    """ Creates an IAGA 2002 string for a single raw 2 Hz record.

    Creates a string in IAGA 2002 format for a single second of data.
    The format needs the date, time, day-of-year, x, y, z, and full
    magnetic strength values of a single reading written on each line.
    Each raw record contains two readings, one centered at second.25
    and the other centered at second.75.

    Parameters
    ----------
    raw_record :
        A byte array that is 38 bytes long, containing a single
        record in the SRI 2 Hz format.

    Returns
    -------
    string :
        A string containing both data points (two lines) from the record.
    """

    # Create the datestamp looking like "YYYY-MM-DD "
    century = raw_record[0]
    year = raw_record[1]
    month = raw_record[2]
    day = raw_record[3]
    datestamp = f"{century:02d}{year:02d}-{month:02d}-{day:02d} "

    # Create a timestamp looking like "HH:MM:SS "
    hour = raw_record[4]
    minute = raw_record[5]
    second = raw_record[6]
    timestamp = f"{hour:02d}:{minute:02d}:{second:02d}"

    # Create the day of year like "ddd  "
    the_date = datetime.date( century*100 + year, month, day)
    day_of_year = the_date.strftime("%j")  # %j is the day of year indicator

    # Each axis is a string of nT to the 1/100 accuracy in a 10 char wide field
    x1 = decode( raw_record[18:21]) / 40.0
    x1_str = f"{x1:10.2f}"
    y1 = decode( raw_record[21:24]) / 40.0
    y1_str = f"{y1:10.2f}"
    z1 = decode( raw_record[24:27]) / 40.0
    z1_str = f"{z1:10.2f}"

    x2 = decode( raw_record[27:30]) / 40.0
    x2_str = f"{x2:10.2f}"
    y2 = decode( raw_record[30:33]) / 40.0
    y2_str = f"{y2:10.2f}"
    z2 = decode( raw_record[33:36]) / 40.0
    z2_str = f"{z2:10.2f}"

    first_half = datestamp + timestamp + ".250 " + day_of_year + "  " + x1_str + y1_str + z1_str + "  88888.88\n"
    second_half = datestamp + timestamp + ".750 " + day_of_year + "  " + x2_str + y2_str + z2_str + "  88888.88\n"
    full_data_string = first_half + second_half
    return full_data_string


def print_contents( infile) :
    """ Prints the given file to standard out.

    Prints the records in the file object by reading them one at a time
    until the end of the file.

    Parameters
    ----------
    infile :
        The file object to be read.
    """

    while True :
        one_record = infile.read( 38)
        if not one_record :
            break
        else :
            print( one_record_to_string( one_record))

def print_contents( infile, stime) :
    """ Prints the given file to standard out beginning at the given time.

    Prints the records in the file object by reading them one at a time
    beginning at the given time until the end of the file.

    Parameters
    ----------
    infile :
        The file object to be read.
    stime :
        The datetime.time object from which to begin
    """

    while True :
        one_record = infile.read( 38)
        if not one_record :
            break
        current_time = time_of_record(one_record)
        if current_time >= stime :
            print( one_record_to_string( one_record))

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
            print( one_record_to_string( one_record))
        if current_time >= etime :
            break


if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        print( "Usage: python3 raw_to_iaga2002.py filename [starttime [endtime]]")
        sys.exit(0)   # Exit with no error code
    filename = sys.argv[1]
    two_hz_binary_file = open(filename, "rb")
    if len(sys.argv) == 2 :
        print_contents(two_hz_binary_file)
    elif len(sys.argv) == 3 :
        # iso format for a time is HH:MM:SS
        start_time = datetime.time.fromisoformat(sys.argv[2])
        print_contents(two_hz_binary_file, start_time)
    elif len(sys.argv) == 4 :
        start_time = datetime.time.fromisoformat(sys.argv[2])
        end_time = datetime.time.fromisoformat(sys.argv[3])
        print_contents( two_hz_binary_file, start_time, end_time)
