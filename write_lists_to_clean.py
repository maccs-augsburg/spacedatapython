import datetime
import sys
import argparse
import clean_to_screen
import model.read_clean_to_lists
import model.read_raw_to_lists
import model.read_iaga2002_to_lists

def create_clean_file_from_datetime_lists(x_list, y_list, z_list, time_list, outfile):
    '''
    Creates a clean file from datetime lists
    created from model/read_clean|raw|iaga2002.create_datetime_list
    calls. Main idea would be to add more data processing, and
    convert to readable format to distribute.

    Parameters:
    -----------
    x_lists : list
        List of x values to write out.
    y_list : list
        List of y values to write out.
    z_list : list
        List of z values to write out.
    time_list : list
        List of time values to write out.
    outfile : open file object
        File to write out to, end result is iaga2002 format.
    '''
    
    # jump by two, getting two values every iteration
    record_counter = 0
    # jump by one, getting one value every iteration
    flag_counter = 0

    while record_counter < len(time_list):
        
        # values from lists are / 1000, multiply by 1000 to write them out
        x_one = int(x_list[record_counter] * 1000)
        x_two = int(x_list[record_counter + 1] * 1000)
        y_one = int(y_list[record_counter] * 1000)
        y_two = int(y_list[record_counter + 1] * 1000)
        z_one = int(z_list[record_counter] * 1000)
        z_two = int(z_list[record_counter + 1] * 1000)

        # get current time of first two records
        datetime_object = time_list[record_counter]
        time = datetime_object.time()
        hour = time.hour
        minute = time.minute
        second = time.second
        
        # set to questionable, not sure what it should be
        # for lists not made from clean file
        flag = 1
        #flag = flag_list[flag_counter]

        # write out hardcoded flag, write out time
        outfile.write(flag.to_bytes(1, byteorder='big', signed=False))
        outfile.write(hour.to_bytes(1, byteorder='big', signed=False))
        outfile.write(minute.to_bytes(1, byteorder='big', signed=False))
        outfile.write(second.to_bytes(1, byteorder='big', signed=False))
        # write out values in the speficied format
        outfile.write(x_one.to_bytes(4, byteorder='big', signed=True))
        outfile.write(x_two.to_bytes(4, byteorder='big', signed=True))
        outfile.write(y_one.to_bytes(4, byteorder='big', signed=True))
        outfile.write(y_two.to_bytes(4, byteorder='big', signed=True))
        outfile.write(z_one.to_bytes(4, byteorder='big', signed=True))
        outfile.write(z_two.to_bytes(4, byteorder='big', signed=True))
        # write newline?
        record_counter += 2
        flag_counter += 1

def main():

    parser = argparse.ArgumentParser(description="Convert lists to iaga2002 format")
    parser.add_argument('filename', type=str, help="name of the input file")
    args = parser.parse_args()
    start = datetime.time.fromisoformat("00:00:00")
    end = datetime.time.fromisoformat("23:59:59")

    file = open(args.filename, 'rb')

    # get filename extension
    name_no_ext = args.filename.split('.')[0]
    extension = args.filename.split('.')[-1]

    # Used for testing in command line, would most likely integrate 
    # this in the gui somehow for data processing.
    if extension == "2hz": 
        x,y,z,t = model.read_raw_to_lists.create_datetime_lists_from_raw(
            file, start, end
        )

    elif extension == "s2":
        x,y,z,t,f = model.read_clean_to_lists.create_datetime_lists_from_clean(
            file, start, end
        )

    elif extension == "sec":
        x,y,z,t = model.read_IAGA2002_to_lists.create_datetime_lists_from_iaga(
            file, start, end
        )

    file.close()

    outfile_name = name_no_ext + "_list_to_clean_file_test.s2"
    outfile = open(outfile_name, 'wb')
    # can only pass the flag array if writing lists from a clean file
    # not sure what to do if not provided. 
    create_clean_file_from_datetime_lists(x,y,z,t,outfile)
    outfile.close()
    # get the filename from open file object
    infile_for_printing_to_screen = open(outfile.name, 'rb')
    # print file out to terminal to check
    clean_to_screen.print_contents(infile_for_printing_to_screen, start, end)

if __name__ == "__main__" :
    main()