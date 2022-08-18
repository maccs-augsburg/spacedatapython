'''
axis_data_flattener.py

Axis remover - Given a file, an axis name, and two times, 
    flatten out the data value for the given axis between the two times.

Created - August 2022 - Mark Ortega-Ponce

Useful Reference: raw_to_iaga2002.py file, clean_to_screen/raw_to_screen.py

Test:
python3 axis_data_flattener.py testdata/CH20097.2hz x 15:00:00 20:00:00
python3 axis_data_flattener.py testdata/CH20097.s2 x 15:00:00 20:00:00
Check:
python3 clean_to_screen.py testdata/CH20097_test_flatten_axis.s2
python3 clean_to_screen.py testdata/CH20097_test_flatten_axis.2hz  

'''
import argparse
from concurrent.futures.process import _system_limits_checked
import datetime
import model.raw_codecs
import model.read_raw_to_lists
import model.read_clean_to_lists
import model.read_IAGA2002_to_lists
import write_lists_to_iaga2002

# https://matplotlib.org/stable/gallery/lines_bars_and_markers/masked_demo.html
AXIS_FLATTENER_VALUE = "99999.99"

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
        #print(current_time)
        outfile.write(one_record)
        
        if current_time >= start_time and current_time <= end_time:
            # read_clean_to_lists for example
            # https://stackoverflow.com/questions/6187699/how-to-convert-integer-value-to-array-of-four-bytes-in-python
            outfile.write(AXIS_FLATTENER_VALUE.to_bytes(4, byteorder='big', signed=True))
            dummy_record = infile.read(4)
            outfile.write(AXIS_FLATTENER_VALUE.to_bytes(4, byteorder='big', signed=True))
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
            outfile.write(model.raw_codecs.encode(AXIS_FLATTENER_VALUE))
            # move up 3 bytes, dont write out to file
            dummy_record = infile.read(3)
            # write out bytes in between first x-value and next
            one_record = infile.read(5)
            outfile.write(one_record)
            # repeat
            outfile.write(model.raw_codecs.encode(AXIS_FLATTENER_VALUE))
            dummy_record = infile.read(3)
            # grab the rest of the records
            one_record = infile.read(38 - second_tuple[1])
            outfile.write(one_record)

        else:
            one_record = infile.read(38 - first_tuple[0])
            outfile.write(one_record)

def flatten_axis(x,y,z,t, axis, start_time, end_time, outfile, station):

    modify_axis = None
    if axis == 'x':
        modify_axis = x
    elif axis == 'y':
        modify_axis = y
    elif axis == 'z':
        modify_axis = z
    
    start_index = None
    end_index = None

    for i in range (len(t)):
        # convert to time
        current_time = t[i].time()
        # remove microseconds
        current_time = current_time.strftime("%H:%M:%S")
        # can't compare unless both datetime.time. Make shorter?
        current_time = datetime.time.fromisoformat(current_time)

        if start_time == current_time and start_index is None:
            start_index = i
        if end_time == current_time and end_index is None:
            end_index = i
       
    # add one to end_index, because open on end range
    for i in range (start_index, end_index + 1):
        modify_axis[i] = 99999.99

    outfile = open(outfile, 'w')
    write_lists_to_iaga2002.create_iaga2002_file_from_datetime_lists(x,y,z,t, outfile, station)
    outfile.close()

def main():
    
    parser = argparse.ArgumentParser(description="Flatten an axis value's between start time and end time.")
    parser.add_argument('filename', type=str, help="name of the input file")
    parser.add_argument('stime', type=str, nargs='?',
        default="10:00:00", help="time to start flattening an axis")
    parser.add_argument('etime', type=str, nargs='?',
        default="20:00:00", help="time to stop flattening an axis")
    parser.add_argument('axis', type=str, nargs='?',
        default='x', help="the axis to flatten (x, y, z)")
    args = parser.parse_args()

    extension = args.filename.split('.')[-1]
    infile = args.filename
    infile = open(infile, 'rb')
    start = datetime.time.fromisoformat( "00:00:00")
    end = datetime.time.fromisoformat("23:59:59")

    if extension == 's2':
        x,y,z,t,f = model.read_clean_to_lists.create_datetime_lists_from_clean(
            infile, start, end             
        )
        station_code = args.filename[0:2]
        
    elif extension == '2hz':
        x,y,z,t = model.read_raw_to_lists.create_datetime_lists_from_raw(
            infile, start, end
        )
        station_code = args.filename[0:2]
    
    elif extension == 'sec':
        x,y,z,t = model.read_IAGA2002_to_lists.create_datetime_lists_from_iaga(
            infile, start, end
        )
        station_code = args.filename[0:3]

    infile.close()

    start_time = datetime.time.fromisoformat(args.stime)
    end_time = datetime.time.fromisoformat(args.etime)

    outfile_name = args.filename.split('.')[0] + "_flatten_test.sec"

    flatten_axis(x,y,z,t, "x", start_time, end_time, outfile_name, station_code)

if __name__ == "__main__":
    main()