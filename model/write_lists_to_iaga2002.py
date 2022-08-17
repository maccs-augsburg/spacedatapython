import datetime
import sys
import read_clean_to_lists
import read_raw_to_lists
import argparse
sys.path.append("..")
import raw_to_iaga2002

def create_iaga2002_file_from_datetime_lists(x_list, y_list, z_list, time_list, outfile):

    x_one = None
    y_one = None
    z_one = None
    x_two = None
    y_two = None
    z_two = None
    time_one = None
    time_two = None
    temp_string = None
    record_counter = 0
    counter = 0

    # write records after doing this

    while counter < len(time_list):

        x_one = x_list[record_counter]
        x_two = x_list[record_counter + 1]
        y_one = y_list[record_counter]
        y_two = y_list[record_counter + 1]
        z_one = z_list[record_counter]
        z_two = z_list[record_counter + 1]
        time_one = time_list[record_counter]
        temp_string = create_record_string(
            x_one, x_two,
            y_one, y_two,
            z_one, z_two, time_one
        )
        print(temp_string)
        record_counter += 2
        counter += 2

        outfile.write(temp_string)


def create_record_string(x1, x2, y1, y2, z1, z2, datetime_object):

    century_year = str(datetime_object.year)
    #print(century_year)
    century = int(century_year[0:2])
    #print(century)
    year = int(century_year[2:])
    #print(year)
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
    # get three letter station name for clean or raw file
    # Note: Wouldn't be converting from iaga to iaga
    station_abbrev = args.filename[0:2]

    start = datetime.time.fromisoformat("00:00:00")
    end = datetime.time.fromisoformat("23:59:59")

    file = open(args.filename, 'rb')

    # get filename extension
    extension = args.filename.split('.')[-1]

    if extension == "2hz": 
        x,y,z,t,f = read_clean_to_lists.create_datetime_lists_from_iaga(
            file, start, end
        )
    elif extension == "s2":
        x,y,z,t = read_raw_to_lists.create_datetime_lists_from_raw(
            file, start, end
        )

    file.close()

    outfile_name = raw_to_iaga2002.create_iaga2002_filename(args.filename)
    outfile_name = outfile_name.split('.')[0]
    outfile_name = outfile_name + "_list_to_file_test.sec"
    outfile = open(outfile_name, 'w')
    outfile.write(raw_to_iaga2002.create_header(station_abbrev))
    create_iaga2002_file_from_datetime_lists(x,y,z,t,outfile)    
    

if __name__ == "__main__" :
    main()