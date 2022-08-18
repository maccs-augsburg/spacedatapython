import datetime
import sys
import model.read_clean_to_lists
import model.read_raw_to_lists
import model.read_IAGA2002_to_lists
import argparse
import raw_to_iaga2002

def create_iaga2002_file_from_datetime_lists(x_list, y_list, z_list, time_list, outfile, station_code):
    '''
    
    '''
    
    outfile.write(raw_to_iaga2002.create_header(station_code))

    record_counter = 0
    # Start writing records from the lists
    while record_counter < len(time_list):

        x_one = x_list[record_counter]
        x_two = x_list[record_counter + 1]
        y_one = y_list[record_counter]
        y_two = y_list[record_counter + 1]
        z_one = z_list[record_counter]
        z_two = z_list[record_counter + 1]
        time = time_list[record_counter]
        temp_string = create_record_string(
            x_one, x_two,
            y_one, y_two,
            z_one, z_two, time
        )
        record_counter += 2
        outfile.write(temp_string)

def create_record_string(x1, x2, y1, y2, z1, z2, datetime_object):

    century_year = str(datetime_object.year)
    century = int(century_year[0:2])
    year = int(century_year[2:])
    month = datetime_object.month
    day = datetime_object.day
    datestamp = f"{century:02d}{year:02d}-{month:02d}-{day:02d} "
    
    time = datetime_object.time()
    hour = time.hour
    minute = time.minute
    second = time.second
    timestamp = f"{hour:02d}:{minute:02d}:{second:02d}"

    # Create the day of year like "ddd  "
    the_date = datetime.date( century*100 + year, month, day)
    day_of_year = the_date.strftime("%j")  # %j is the day of year indicator

    # Each axis is a string of nT to the 1/100 accuracy in a 10 char wide field
    x1_str = f"{x1:10.2f}"
    y1_str = f"{y1:10.2f}"
    z1_str = f"{z1:10.2f}"
    x2_str = f"{x2:10.2f}"
    y2_str = f"{y2:10.2f}"
    z2_str = f"{z2:10.2f}"

    first_half = datestamp + timestamp + ".250 " + day_of_year + "   " + x1_str + y1_str + z1_str + "  88888.88\n"
    second_half = datestamp + timestamp + ".750 " + day_of_year + "   " + x2_str + y2_str + z2_str + "  88888.88\n"
    full_data_string = first_half + second_half

    return full_data_string

def main():

    parser = argparse.ArgumentParser(description="Convert lists to iaga2002 format")
    parser.add_argument('filename', type=str, help="name of the input file")
    args = parser.parse_args()
    start = datetime.time.fromisoformat("00:00:00")
    end = datetime.time.fromisoformat("23:59:59")

    file = open(args.filename, 'rb')

    # get filename extension
    extension = args.filename.split('.')[-1]

    # Used for testing in command line, would most likely integrate 
    # this in the gui somehow for data processing.
    if extension == "2hz": 
        x,y,z,t = model.read_raw_to_lists.create_datetime_lists_from_raw(
            file, start, end
        )
        station_abbrev = args.filename[0:2]

    elif extension == "s2":
        x,y,z,t,f = model.read_clean_to_lists.create_datetime_lists_from_clean(
            file, start, end
        )
        station_abbrev = args.filename[0:2]

    elif extension == "sec":
        x,y,z,t = model.read_IAGA2002_to_lists.create_datetime_lists_from_iaga(
            file, start, end
        )
        station_abbrev = args.filename[0:3]

    file.close()

    outfile_name = raw_to_iaga2002.create_iaga2002_filename(args.filename)
    outfile_name = outfile_name.split('.')[0]
    outfile_name = outfile_name + "_list_to_file_test.sec"
    outfile = open(outfile_name, 'w')
    # Write out the records to the outfile
    create_iaga2002_file_from_datetime_lists(x,y,z,t,outfile, station_abbrev)
    outfile.close()    
    
if __name__ == "__main__" :
    main()