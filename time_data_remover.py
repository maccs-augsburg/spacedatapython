'''
time_data_remover.py

Data remover - Given a file and two times, remove all the 
    data records between the two times and write out the shortened file.

Usefule reference: documentation/BinaryFormatNotes.txt

Created August 2022 - Mark Ortega-Ponce
'''

import datetime
from hashlib import new
import sys

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
    
    passed_start_time = False

    while True:

        one_record = infile.read(28)

        if not one_record:
            break
    
        current_time = datetime.time(hour=one_record[1],minute=one_record[2],second=one_record[3])
        
        if current_time < start_time and not passed_start_time:
            outfile.write(one_record)
        else:
            passed_start_time = True
        
        if current_time > end_time and passed_start_time:
            outfile.write(one_record)


def remove_data_from_raw(infile, outfile, start_time, end_time):

    passed_start_time = False

    while True:

        one_record = infile.read(38)

        if not one_record:
            break
            
        current_time = datetime.time(hour=one_record[4],minute=one_record[5],second=one_record[6])

        if current_time < start_time and not passed_start_time:
            outfile.write(one_record)
        else:
            passed_start_time = True

        if current_time > end_time and passed_start_time:
            outfile.write(one_record)

def remove_data_from_iaga(infile, outfile, start_time, end_time):

    for i in range(0, 100):

        dummy_record = str(infile.readline())
        dummy_record_list = dummy_record.split()

        if dummy_record_list[0].__contains__("DATE"):
            outfile.write(dummy_record)
            break
        
        outfile.write(dummy_record)
        
    passed_start_time = False

    while True:

        one_record_first_line = str(infile.readline())
        one_record_second_line = str(infile.readline())
        print(one_record_first_line)
        tuple_list_one = one_record_first_line.split()
        print(tuple_list_one)

        # if we reach the end then we break the loop
        if not one_record_first_line:
            break
        
        if len(tuple_list_one) < 6:
            break
        else:
            time = str(tuple_list_one[1])
        # Grab up to hh:mm:ss ignoring the microseconds
        time = time[0:8]
        datetime_object = datetime.datetime.strptime(time, "%H:%M:%S").time()
        hour = int(datetime_object.strftime("%H"))
        minute = int(datetime_object.strftime("%M"))
        second = int(datetime_object.strftime("%S"))

        #second = one_record[17:23] //second with microsecond
        current_time = datetime.time(hour, minute, second) # getting the current time

        if current_time < start_time and not passed_start_time:
            outfile.write(one_record_first_line)
            outfile.write(one_record_second_line)
        else:
            passed_start_time = True

        if current_time > end_time and passed_start_time:
            outfile.write(one_record_first_line)
            outfile.write(one_record_second_line)

def main():
    
    if len(sys.argv) < 2:
        print("Usage: python3 time_data_remover.py filename")
        print("Usage: python3 time_data_remover.py filename xx:xx:xx xx:xx:xx")
        sys.exit(0)

    filename = sys.argv[1]

    if len(sys.argv) == 4:
        start_time = datetime.time.fromisoformat(sys.argv[2])
        end_time = datetime.time.fromisoformat(sys.argv[3])
    else:
        start_time = datetime.time.fromisoformat("10:00:00")
        end_time = datetime.time.fromisoformat("20:00:00")

    tuple_filename = filename.split(".")
    # basefilename without extension
    base_filename = tuple_filename[0]
    filename_extension = tuple_filename[1]
    infile = open(filename, "rb")

    new_filename = base_filename + "_test_data_remover." + filename_extension
    outfile = open(new_filename, "wb")

    if filename_extension == "s2":
        remove_data_from_clean(infile, outfile, start_time, end_time)
    if filename_extension == "2hz":
        remove_data_from_raw(infile, outfile, start_time, end_time)
    if filename_extension == "sec":
        outfile = open(new_filename, "w")
        remove_data_from_iaga(infile, outfile, start_time, end_time)

if __name__ == "__main__":
    main()