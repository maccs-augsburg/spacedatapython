#  raw_codecs.py
#
#  Contains conversion code for the various binary parts of MACCS
# raw data files.
#
#  2020 May  -- Created  -- Erik Steinmetz
#

def decode(bytes):
    """ 
    Converts raw bytes into a integer value.
    
    Parameters
    bytes: 3 byte array (24 bits) of 2's complement value
    Returns
    int
        The python integer value represented by the 24 bits.
    """
    value = bytes[0]*65536+bytes[1]*256+bytes[2]
	if value>= 2**23:
		return value - 2**24
	else:
		return value

