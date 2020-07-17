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


def encode(a_value) :
    """ 
    Converts an integer value into a 24 bit, two's complement integer.
    This assumes that the value is within the bounds of a 24-bit int,
    so about -8 million to +8 million. The answer is in big-endian byte
    order.
    
    Parameters
    ----------
    a_value : 
        A Python integer value.
        
    Returns
    -------
    bytearray
        The given integer value represented in 24 bits.
    """
    
    if a_value<0:
        a_value+=2**24            # Makes value positive with bit 23 a 1
    answer = bytearray()          # An empty byte array
    answer.append(a_value//65536) # Append the highest-order 8 bits
    a_value = a_value%65536
    answer.append(a_value//256)   # Append the middle 8 bits
    a_value = a_value%256
    answer.append(a_value)        # Append the low-order 8 bits
    return answer


def time_of_record(record) :
    """ Returns the time of the given 2Hz raw record.
    
    Parameters
    ----------
    record :
        A 38 byte raw 2 Hz record
    
    Returns
    -------
    datetime.time
        A time object representing the time encoded in the record
    """
    
    answer = datetime.time(hour=record[4], minute=record[5], second=record[6])
    return answer


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
    
