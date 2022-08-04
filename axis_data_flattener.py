'''
axis_data_flattener.py

Axis remover - Given a file, an axis name, and two times, 
    flatten out the data value for the given axis between the two times.

Created - August 2022 - Mark Ortega-Ponce
'''

import datetime
import sys
import model.raw_codecs

AXIS_FLATENNER_VALUE = 0

def flatten_axis_from_clean(infile, outfile, axis, start_time, end_time):

    axis = axis.lower()

    if axis == "x":
        first_tuple = (4, 7)
        second_tuple = (8, 11)
    elif axis == "y":
        first_tuple = (12, 15)
        second_tuple = (16, 19)
    else:
        first_tuple = (20, 23)
        second_tuple = (24, 27)

    passed_start_time = False

    while True:

        one_record = infile.read(28)

        if not one_record:
            break

        one_record[first_tuple[0]:first_tuple[1]] = AXIS_FLATENNER_VALUE
        one_record[second_tuple[0]:second_tuple[1]] = AXIS_FLATENNER_VALUE
    
        current_time = datetime.time(hour=one_record[1],minute=one_record[2],second=one_record[3])
        
        if current_time < start_time and not passed_start_time:
            outfile.write(one_record)
        else:
            passed_start_time = True
        
        if current_time > end_time and passed_start_time:
            outfile.write(one_record)


def flatten_axis_from_raw(infile, outfile, axis, start_time, end_time):

    axis = axis.lower()

    '''
    18:20  24 bit 2's comp  x1        Value in nanotesla*40 of the x axis for the 1st half of the second.
    21:23  24 bit 2's comp  y1
    24:26  24 bit 2's comp  z1
    27:29  24 bit 2's comp  x2        Value in nanotesla*40 of the x axis for the 2nd half of the second.
    30:32  24 bit 2's comp  y2
    33:35  24 bit 2's comp  z2
    '''

    if axis == "x":
        first_tuple = (18, 20)
        second_tuple = (27, 29)
    
    elif axis == "y":
        first_tuple = (21, 23)
        second_tuple = (30, 32)

    else:
        first_tuple = (24, 26)
        second_tuple = (33, 35)

    passed_start_time = False

    while True:
        
        one_record = infile.read(38)

        if not one_record:
            break

        # Encode our value into binary format 
        # and splice that value into first and second axis value.
        one_record[first_tuple[0]:first_tuple[1]] = model.raw_codecs.encode(AXIS_FLATENNER_VALUE)
        one_record[second_tuple[0]:second_tuple[1]] = model.raw_codecs.encode(AXIS_FLATENNER_VALUE)

        current_time = datetime.time(hour=one_record[4],minute=one_record[5],second=one_record[6])

        if current_time < start_time and not passed_start_time:
            outfile.write(one_record)
        else:
            passed_start_time = True

        if current_time > end_time and passed_start_time:
            outfile.write(one_record)

def remove_data_from_iaga(infile, outfile, axis, start_time, end_time):

    for i in range(0, 100):

        dummy_record = str(infile.readline())
        dummy_record_list = dummy_record.split()

        if dummy_record_list[0].__contains__("DATE"):
            outfile.write(dummy_record)
            break
        
        outfile.write(dummy_record)
        
    passed_start_time = False

    while True:

        one_record_first_line = infile.readline()
        one_record_second_line = infile.readline()
        tuple_list_one = one_record_first_line.split()

        # if we reach the end then we break the loop
        if not one_record_first_line:
            break
        
        time = tuple_list_one[1]
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

    new_filename = base_filename + "_test_data_remover." + filename_extension
    outfile = open(new_filename, "wb")

    if filename_extension == "s2":
        infile = open(filename, "rb")
        remove_data_from_clean(infile, outfile, start_time, end_time)
    if filename_extension == "2hz":
        infile = open(filename, "rb")
        remove_data_from_raw(infile, outfile, start_time, end_time)
    if filename_extension == "sec":
        infile = open(filename, "r")
        outfile = open(new_filename, "w")
        remove_data_from_iaga(infile, outfile, start_time, end_time)

if __name__ == "__main__":
    main()