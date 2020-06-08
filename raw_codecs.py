#  raw_codecs.py
#
#  Contains conversion code for the various binary parts of MACCS
# raw data files.
#
#  2020 May  -- Created  -- Erik Steinmetz
#

import datetime

def decode(bytes) :
    """ 
    Converts 24 bit integer into a integer value.
    
    Parameters
    ----------
    bytes : 
        A 3 byte array (24 bits) of 2's complement value
        
    Returns
    -------
    int
        The python integer value represented by the 24 bits.
    """
    
    value = bytes[0] * 65536 + bytes[1] * 256 + bytes[2]
    if value >= 2**23 :
        return value - 2**24
    else :
        return value


def time_to_second(time_string) :
    """ Converts an HH:MM:SS string into an ordinal second of the day
        number from 0 to 85399.
    
    Parameters
    ----------
    time_string :
        A string of the form HH:MM:SS
    
    Returns
    -------
    int
        An integer from 0 up to 85,399
    """
    
    the_time = datetime.time.fromisoformat(time_string)
    seconds = the_time.hour * 3600
    seconds = seconds + the_time.minute * 60
    seconds = seconds + the_time.second
    return seconds
    
