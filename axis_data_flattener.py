'''
axis_data_flattener.py

Axis remover - Given a file, an axis name, and two times, 
    flatten out the data value for the given axis between the two times.

Created - August 2022 - Mark Ortega-Ponce

Test:
python3 axis_data_flattener.py testdata/CH20097.2hz x 15:00:00 20:00:00
python3 axis_data_flattener.py testdata/CH20097.s2 x 15:00:00 20:00:00
Check:
python3 clean_to_screen.py testdata/CH20097_test_flatten_axis.s2
python3 clean_to_screen.py testdata/CH20097_test_flatten_axis.2hz  

'''

import datetime
import sys
import model.raw_codecs

AXIS_FLATENNER_VALUE = 0

def flatten_axis_from_clean(infile, outfile, axis, start_time, end_time):

    axis = axis.lower()

    '''
    One byte = 8bits
    4 bytes = 32 bits, our x,y,z values are signed integers.
    No I did not know that off the top of my head, had to look it up.
    '''

    if axis == "x":
        first_tuple = (4, 7)
        second_tuple = (8, 11)
    elif axis == "y":
        first_tuple = (12, 15)
        second_tuple = (16, 19)
    else:
        first_tuple = (20, 23)
        second_tuple = (24, 27)

    dummy_record = None

    while True:

        one_record = infile.read(first_tuple[0])

        if not one_record:
            break
    
        current_time = datetime.time(hour=one_record[1],minute=one_record[2],second=one_record[3])
        print(current_time)
        outfile.write(one_record)
        
        if current_time >= start_time and current_time <= end_time:
            # read_clean_to_lists for example
            # https://stackoverflow.com/questions/6187699/how-to-convert-integer-value-to-array-of-four-bytes-in-python
            outfile.write(AXIS_FLATENNER_VALUE.to_bytes(4, byteorder='big', signed=True))
            dummy_record = infile.read(4)
            outfile.write(AXIS_FLATENNER_VALUE.to_bytes(4, byteorder='big', signed=True))
            dummy_record = infile.read(4)
            one_record = infile.read(28 - (second_tuple[1] + 1))
            outfile.write(one_record)

        else:
            one_record = infile.read(28 - first_tuple[0])
            outfile.write(one_record)
    

def flatten_axis_from_raw(infile, outfile, axis, start_time, end_time):

    axis = axis.lower()

    '''
    One byte = 8 bits
    3 bytes = 24 bits, our x,y,z values.
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

    dummy_record = None

    while True:
        
        # read up to starting index of first data value
        # Example 'x", read up to first 18 bytes or 0 - 17
        one_record = infile.read(first_tuple[0])

        if not one_record:
            break

        current_time = datetime.time(hour=one_record[4],minute=one_record[5],second=one_record[6])
        outfile.write(one_record)

        if current_time >= start_time and current_time <= end_time:
            # write next three bytes (overwrite with new value)
            outfile.write(model.raw_codecs.encode(AXIS_FLATENNER_VALUE))
            # move up 3 bytes, dont write out to file
            dummy_record = infile.read(3)
            # write out bytes in between first x-value and next
            one_record = infile.read(5)
            outfile.write(one_record)
            # repeat
            outfile.write(model.raw_codecs.encode(AXIS_FLATENNER_VALUE))
            dummy_record = infile.read(3)
            # grab the rest of the records
            one_record = infile.read(38 - second_tuple[1])
            outfile.write(one_record)

        else:
            one_record = infile.read(38 - first_tuple[0])
            outfile.write(one_record)


def flatten_axis_from_iaga(infile, outfile, axis, start_time, end_time):

    axis = axis.lower()

    index = 0

    if axis == "x":
        index = 3
    if axis == "y":
        index = 4
    if axis == "z":
        index = 5
    
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
    
    if len(sys.argv) < 3:
        print("Usage: python3 time_data_remover.py filename axis")
        print("Usage: python3 time_data_remover.py filename axis xx:xx:xx xx:xx:xx")
        sys.exit(0)

    filename = sys.argv[1]
    axis = sys.argv[2]

    if len(sys.argv) == 5:
        start_time = datetime.time.fromisoformat(sys.argv[3])
        end_time = datetime.time.fromisoformat(sys.argv[4])
    else:
        start_time = datetime.time.fromisoformat("10:00:00")
        end_time = datetime.time.fromisoformat("20:00:00")

    tuple_filename = filename.split(".")
    # basefilename without extension
    base_filename = tuple_filename[0]
    filename_extension = tuple_filename[1]

    new_filename = base_filename + "_test_flatten_axis." + filename_extension
    outfile = open(new_filename, "wb")

    if filename_extension == "s2":
        infile = open(filename, "rb")
        flatten_axis_from_clean(infile, outfile, axis, start_time, end_time)
    if filename_extension == "2hz":
        infile = open(filename, "rb")
        flatten_axis_from_raw(infile, outfile, axis, start_time, end_time)
    if filename_extension == "sec":
        infile = open(filename, "r")
        outfile = open(new_filename, "w")
        flatten_axis_from_iaga(infile, outfile, axis,  start_time, end_time)

if __name__ == "__main__":
    main()