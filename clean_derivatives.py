# clean_derivatives.py
#
# 2020 August - Created - Erik Steinmetz
#

""" Calculates derivatives from cleaned data

Proceeds through a cleaned 2 Hz MACCS data file calculating the
first and second derivatives of the data.

"""


# Python 3 imports
import sys
import math
import datetime
# need to install matplotlib. On Mac $ sudo python3 -mpip install matplotlib
import matplotlib.pyplot as plt

# MACCS imports
from raw_codecs import decode, time_of_record, time_to_second, seconds_to_time_string


def print_one_record( clean_record) :
    """ Prints a single cleaned 2 Hz record to standard out.

    Prints the timestamp, x, y, z, and  values to a single line
    on standard out.

    Parameters
    ----------
    clean_record :
        A byte array that is 28 bytes long, containing a single
        record in the cleaned 2 Hz format.
    """

    hour = clean_record[1]
    minute = clean_record[2]
    second = clean_record[3]
    timestamp = f"{hour:02d}:{minute:02d}:{second:02d}"
    x1 = int.from_bytes(clean_record[4:8], byteorder='big', signed=True) / 1000.0
    x1_str = f"{x1:12.3f}"
    y1 = int.from_bytes(clean_record[12:16], byteorder='big', signed=True)  / 1000.0
    y1_str = f"{y1:12.3f}"
    z1 = int.from_bytes(clean_record[20:24], byteorder='big', signed=True)  / 1000.0
    z1_str = f"{z1:12.3f}"
    flag = clean_record[0]
    flag_str = f"{flag:4d}"
    print( timestamp + x1_str + y1_str + z1_str + flag_str)


def print_contents( derivs, second_derivs, s_sec, e_sec) :
    """ Prints the given derivs to standard out beginning at the given time.

    Prints the derivatives in the array
    beginning at the given time until the end of the file.

    Parameters
    ----------
    derivs :
        The array of derivative values, one for each second of the day.
    s_sec :
        The second from which to begin
    e_sec :
        The second at which to end
    """
    
    current_sec = s_sec
    timestamps = []
    dvals = []
    ddvals = []
    while current_sec <= e_sec :
        sec_str = seconds_to_time_string( current_sec) + "  "
        current_val = derivs[current_sec]
        dvals.append( current_val)         # plotting stuff
        timestamps.append( current_sec)    # plotting stuff
        val_str = f"{current_val:12.3f}"
        second_val = second_derivs[current_sec]
        ddvals.append( second_val)         # plotting stuff
        second_val_str = f"{second_val:12.5f}"
        print( sec_str + val_str + second_val_str)
        current_sec = current_sec + 1

    # Add a plot to it.
    figure = plt.figure( figsize=(12,12)) # width,height
    plt.subplot(211) # 2 plots on one page, this is the first
    plt.plot(timestamps,dvals)
    #plt.scatter(timestamps,dvals,s=0.6,linewidths=0.4)
    plt.ylabel("nT/s")
    plt.subplot(212)
    plt.plot(timestamps,ddvals)
#    plt.scatter(timestamps,ddvals,s=0.6,linewidths=0.4)
    plt.ylabel("nT/(s^2)")
    plt.xlabel("seconds")
    figure.savefig( "testoutplot.png")
    
def calculate_first( infile) :
    """ Calculates the first derivative of the data in the z axis in
        nT/s.
    
    Creates an array filled with first derivative data from the data.
    Ignores the bad data (32,767,000 values for nT*1000), filling in a
    derivative of math.nan instead.
    
    Parameters
    ----------
    infile :
        The file object to be read.
    
    Returns
    -------
    float array
        An array of numbers containing the first derivative of the data.
    """
    
    answer = []
    previous_record = None
    while True :
        current_record = infile.read( 28)
        if not current_record :           # End of file
            break
        if previous_record is not None :
            pz1 = int.from_bytes(previous_record[20:24], byteorder='big', signed=True) / 1000.0
            pz2 = int.from_bytes(previous_record[24:28], byteorder='big', signed=True) / 1000.0
            z1 = int.from_bytes(current_record[20:24], byteorder='big', signed=True) / 1000.0
            z2 = int.from_bytes(current_record[24:28], byteorder='big', signed=True) / 1000.0
            deriv1 = z1 - pz1
            deriv2 = z2 - pz2
            # FIXME: if any of these values are 32,767, throw out the derivatives, replace with ??
            answer.append( (deriv1 + deriv2) / 2.0)
        previous_record = current_record
    return answer

def calculate_second( first_deriv_array) :
    """ Creates an array of second derivatives calculated from first
        derivatives in nT/(s^2)
    
    Creates an array filled with second derivative values.
    
    Parameters
    ----------
    first_deriv_array
        The array of first derivative values.
    
    Returns
    -------
    float array
        An array of nT/(s^2) values
    """
    
    answer = []
    last_index = len( first_deriv_array) - 1
    index = 0
    while index < last_index :
        prev_val = first_deriv_array[ index-1]
        next_val = first_deriv_array[ index+1]
        # FIXME: if any of these values are the bad first deriv value, val is bad 2nd deriv val
        answer.append( (next_val - prev_val) / 2.0)
        index += 1
    return answer
    

if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        print( "Usage: python3 clean_derivatives.py filename [starttime [endtime]]")
        sys.exit(0)   # Exit with no error code
    filename = sys.argv[1]
    two_hz_cleaned_file = open(filename, "rb")
    first_derivatives = calculate_first( two_hz_cleaned_file)
    second_derivatives = calculate_second( first_derivatives)
    start_second = 0
    end_second = 86399
    if len(sys.argv) >= 3 :
        # format for a time is HH:MM:SS
        start_second = time_to_second(sys.argv[2])
    if len(sys.argv) == 4 :
        end_second = time_to_second(sys.argv[3])
    print_contents( first_derivatives, second_derivatives, start_second, end_second)
