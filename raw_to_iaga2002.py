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
import station_names


def create_iaga2002_filename( raw_filename) :
    """ Creates an IAGA 2002 filename from a raw filename.

    Creates a filename string in IAGA 2002 format given a raw filename.
    The raw filename is in a format that has the pattern STYYDOY.2hz. ST
    is the station name, DOY is the day of year. The IAGA2002 format has the
    pattern STAYYYYMMDDv_l0_half_sec.sec where STA is the station name.

    Parameters
    ----------
    raw_filename :
        A filename string in the raw pattern.

    Returns
    -------
    string :
        A filename string in the IAGA 2002 pattern.
    """

    two_letter_name = raw_filename[0:2]
    three_letter_name = station_names.find_three_letter_name( two_letter_name)
    three_letter_name = three_letter_name.lower()
    century_string = "20"
    year_string = raw_filename[2:4]
    if int(year_string) > 85 :
        century_string = "19"
    doy_string = raw_filename[4:7]
    # use the string parse time functions to create a date object:
    the_date = datetime.datetime.strptime( century_string + year_string + " " + doy_string, "%Y %j")
    # ask the date object for a string of the form YYYYMMDD
    date_string = the_date.strftime("%Y%m%d")
    answer = three_letter_name + date_string + "v_l0_half_sec.sec"
    return answer


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

    first_half = datestamp + timestamp + ".250 " + day_of_year + "   " + x1_str + y1_str + z1_str + "  88888.88\n"
    second_half = datestamp + timestamp + ".750 " + day_of_year + "   " + x2_str + y2_str + z2_str + "  88888.88\n"
    full_data_string = first_half + second_half
    return full_data_string


def write_data_to_file( outfile, infile, stime, etime) :
    """ Write the contents of the raw infile to the outfile as IAGA 2002 text.

    Parameters
    ----------
    outfile :
        The file object in which to write.
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
            outfile.write( one_record_to_string( one_record))
        if current_time >= etime :
            break



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


def column_headers_for( station) :
    """ Creates a column header line for the given station two letter abbreviation."""

    #DATE       TIME         DOY     RBYX      RBYY      RBYZ      RBYF   |
    sta = station_names.find_three_letter_name( station)
    answer = f"DATE       TIME         DOY     {sta}X      {sta}Y      {sta}Z      {sta}F   |\n"
    return answer


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
    header_string = header_string + column_headers_for( station)
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
    elif station == "RB" :
        answer = answer + " Station Name           Repulse Bay, Nunavut, Canada                 |\n"
        answer = answer + " IAGA CODE              RBY                                          |\n"
        answer = answer + " Geodetic Latitude      66.524                                       |\n"
        answer = answer + " Geodetic Longitude     273.769                                      |\n"
        answer = answer + " Elevation              30                                           |\n"
    return answer


# FIXME: No proper header comment for less than 24 hour file.
if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        print( "Usage: python3 raw_to_iaga2002.py filename [starttime [endtime]]")
        sys.exit(0)   # Exit with no error code
    filename = sys.argv[1]
    station = filename[0:2] # grab the first two letters of the filename, the station abbreviation.
    two_hz_binary_file = open(filename, "rb")
    start_time = datetime.time.fromisoformat( "00:00:00")
    end_time = datetime.time.fromisoformat("23:59:59")
    if len(sys.argv) >= 3 :
        # iso format for a time is HH:MM:SS
        start_time = datetime.time.fromisoformat(sys.argv[2])
    if len(sys.argv) == 4 :
        end_time = datetime.time.fromisoformat(sys.argv[3])
    # open a file for writing
    outfile_name = create_iaga2002_filename( filename)
    outfile = open(outfile_name, "w")
    outfile.write( create_header(station))
    write_data_to_file( outfile, two_hz_binary_file, start_time, end_time)
    outfile.close()
    two_hz_binary_file.close()
