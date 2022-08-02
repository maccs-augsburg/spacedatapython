import datetime
from tarfile import _Bz2ReadableFileobj

from anyio import current_effective_deadline

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

    for i in range(0, 100):
        dummy_record = str(infile.readline())
        dummy_record = dummy_record.split()

        outfile.write(dummy_record)

        if dummy_record[0].__contains__("DATE"):
            outfile.write(dummy_record)
            break

    # Loop until the end of file or end time has been reached
    while True:

        one_record_first_line = infile.readline()
        one_record_first_line = one_record_first_line.split()

        one_record_second_line = infile.readline()
        one_record_second_line = one_record_second_line.split()

        # if we reach the end then we break the loop
        if not one_record_first_line:
            break
        
        time = str(one_record_first_line[1])
        # Grab up to hh:mm:ss ignoring the microseconds
        time = time[2:10]
        datetime_object = datetime.datetime.strptime(time, "%H:%M:%S").time()
        hour = int(datetime_object.strftime("%H"))
        minute = int(datetime_object.strftime("%M"))
        second = int(datetime_object.strftime("%S"))

        #second = one_record[17:23] //second with microsecond
        current_time = datetime.time(hour, minute, second) # getting the current time

        if current_time >= start_time:
            outfile.write(one_record_first_line)
            outfile.write(one_record_second_line)

        if current_time > end_time:
            break
