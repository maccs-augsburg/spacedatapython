import datetime
from tarfile import _Bz2ReadableFileobj

def remove_data_from_clean(infile, outfile, start_time, end_time):

    '''
    Parameters
    ----------
    infile :
        The file object to be read.
    start_time :
        The datetime.time object from which to begin.
    end_time:
        The datetime.time object at which to end.
    '''

    while True:

        one_record = infile.read(28)

        if not one_record:
            break
    
        current_time = datetime.time(hour=one_record[1],minute=one_record[2],second=one_record[3])
        
        if current_time >= start_time:
            outfile.write(one_record)
        if current_time > end_time:
            break

def remove_data_from_raw(infile, outfile, start_time, end_time):

    while True:

        one_record = infile.read(38)

        if not one_record:
            break
            
        current_time = datetime.time(hour=one_record[4],minute=one_record[5],second=one_record[6])

        if current_time >= start_time:
            outfile.write(one_record)
        if end_time > end_time:
            break

def remove_data_from_iaga(infile, outfile, start_time, end_time):
    pass


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
        one_record = infile.read( 28)
        if not one_record :
            break
        current_time = datetime.time(hour=one_record[1], minute=one_record[2], second=one_record[3])
        if current_time >= stime :
            print_one_record( one_record)
        if current_time >= etime :
            break
