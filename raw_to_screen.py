# raw_to_screen.py
#
# Walks through a 2 Hz MACCS data file and prints the 
# time-stamped values to the screen.
#


# Python 3 imports
import sys
import datetime

# MACCS imports
from raw_codecs import decode

def print_one_record( raw_record) :
    hour = raw_record[4]
    minute = raw_record[5]
    second = raw_record[6]
    timestamp = f"{hour:02d}:{minute:02d}:{second:02d}"
    x1 = decode( raw_record[18:21]) / 40.0
    x1_str = f"{x1:12.3f}"# format( x1, "12.3f")
    y1 = decode( raw_record[21:24]) / 40.0
    y1_str = format( y1, "12.3f")
    z1 = decode( raw_record[24:27]) / 40.0
    z1_str = format( z1, "12.3f")
    print( timestamp + x1_str + y1_str + z1_str)

def print_contents( infile) :
    while True :
        one_record = infile.read( 38)
        if not one_record : 
            break
        else :
            print_one_record( one_record)

if __name__ == "__main__" :
    filename = sys.argv[1]
    two_hz_binary_file = open( filename, "rb")
    print_contents( two_hz_binary_file)
    