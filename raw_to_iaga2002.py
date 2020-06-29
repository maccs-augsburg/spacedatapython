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

    print(f"start time is {stime}")
    print(f"end time is {etime}")
    while True :
        one_record = infile.read( 38)
        if not one_record :
            break
        current_time = time_of_record(one_record)
        if current_time >= stime :
            print( one_record_to_string( one_record))
        if current_time >= etime :
            break

def create_header( station) :
    """ Creates the header for the given station two letter abbreviation.

    Creates the multi-line IAGA 2002 style header for the station indicated
    by the two letter abbreviation.

    Parameters
    ----------
    station :
        The two letter abbreviation of a station

    Returns
    -------
    string :
        A string containing the header.
    """

    header_string =                 " Format                 IAGA2002                                     |\n"
    header_string = header_string + " Source of Data         Augsburg University                          |\n"
    header_string = header_string + header_beginning_for( station)
#    header_string = header_string + " # Start Time "
#    header_string = header_string + " # Duration In Seconds  "
    header_string = header_string + " Reported               XYZF                                         |\n"
    header_string = header_string + " Sensor Orientation     XYZ                                          |\n"
    header_string = header_string + " Digital Sampling       0.125 seconds                                |\n"
    header_string = header_string + " Data Interval Type     Averaged 0.5-Second (00:00.00 - 00:00.49)    |\n"
    header_string = header_string + " Data Type              Variation                                    |\n"
    header_string = header_string + " # Values are reported in local geomagnetic coordinates.             |\n"
    header_string = header_string + " # Values are collected in local geomagnetic coordinates.            |\n"
    header_string = header_string + " # Time-centered averages at .25 and .75 seconds.                    |\n"
    header_string = header_string + " # F is not detected as an independent observable                    |\n"
    header_string = header_string + " # For more information visit http://space.augsburg.edu              |\n"
# FIXME: Lots more to go here
    return header_string

def header_beginning_for( station) :
    """ Creates the station-specific header information """

    answer = ""
    if station == "CD" :
        answer = answer + " Station Name           Cape Dorset, Nunavut, Canada                 |\n"
        answer = answer + " IAGA CODE              CDR                                          |\n"
        answer = answer + " Geodetic Latitude      64.231                                       |\n"
        answer = answer + " Geodetic Longitude     283.470                                      |\n"
        answer = answer + " Elevation              52                                           |\n"
    elif station == "CH" :
        answer = answer + " Station Name           Coral Harbour, Nunavut, Canada               |\n"
        answer = answer + " IAGA CODE              CHB                                          |\n"
        answer = answer + " Geodetic Latitude      64.188                                       |\n"
        answer = answer + " Geodetic Longitude     276.650                                      |\n"
        answer = answer + " Elevation              50                                           |\n"
    elif station == "CY" :
        answer = answer + " Station Name           Clyde River, Nunavut, Canada                 |\n"
        answer = answer + " IAGA CODE              CRV                                          |\n"
        answer = answer + " Geodetic Latitude      70.486                                       |\n"
        answer = answer + " Geodetic Longitude     291.488                                      |\n"
        answer = answer + " Elevation              73                                           |\n"
    elif station == "GH" :
        answer = answer + " Station Name           Gjoa Haven, Nunavut, Canada                  |\n"
        answer = answer + " IAGA CODE              GJO                                          |\n"
        answer = answer + " Geodetic Latitude      68.633                                       |\n"
        answer = answer + " Geodetic Longitude     264.150                                      |\n"
        answer = answer + " Elevation              20                                           |\n"
    elif station == "IG" :
        answer = answer + " Station Name           Igloolik, Nunavut, Canada                    |\n"
        answer = answer + " IAGA CODE              IGL                                          |\n"
        answer = answer + " Geodetic Latitude      69.375                                       |\n"
        answer = answer + " Geodetic Longitude     278.198                                      |\n"
        answer = answer + " Elevation              20                                           |\n"
    elif station == "NA" :
        answer = answer + " Station Name           Nain, Labrador, Canada                       |\n"
        answer = answer + " IAGA CODE              NAN                                          |\n"
        answer = answer + " Geodetic Latitude      56.541                                       |\n"
        answer = answer + " Geodetic Longitude     298.302                                      |\n"
        answer = answer + " Elevation              7                                            |\n"
    elif station == "PB" :
        answer = answer + " Station Name           Pelly Bay, Nunavut, Canada                   |\n"
        answer = answer + " IAGA CODE              PEB                                          |\n"
        answer = answer + " Geodetic Latitude      68.538                                       |\n"
        answer = answer + " Geodetic Longitude     270.211                                      |\n"
        answer = answer + " Elevation              30                                           |\n"
    elif station == "PG" :
        answer = answer + " Station Name           Pangnirtung, Nunavut, Canada                 |\n"
        answer = answer + " IAGA CODE              PGG                                          |\n"
        answer = answer + " Geodetic Latitude      66.149                                       |\n"
        answer = answer + " Geodetic Longitude     294.324                                      |\n"
        answer = answer + " Elevation              48                                           |\n"
    return answer

# FIXME: the main only prints to the screen right now
if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        print( "Usage: python3 raw_to_iaga2002.py filename [starttime [endtime]]")
        sys.exit(0)   # Exit with no error code
    filename = sys.argv[1]
    station = filename[0:2] # grab the first two letters of the filename, the station abbreviation.
    print( create_header( station))
    two_hz_binary_file = open(filename, "rb")
    start_time = datetime.time.fromisoformat( "00:00:00")
    end_time = datetime.time.fromisoformat("23:59:59")
    if len(sys.argv) >= 3 :
        # iso format for a time is HH:MM:SS
        start_time = datetime.time.fromisoformat(sys.argv[2])
    if len(sys.argv) == 4 :
        end_time = datetime.time.fromisoformat(sys.argv[3])
    print_contents( two_hz_binary_file, start_time, end_time)
