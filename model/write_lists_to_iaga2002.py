import datetime
import sys
import read_IAGA2002_to_lists

def create_iaga2002_file_from_datetime_lists(x_list, y_list, z_list, time_list):

    x_one = None
    y_one = None
    z_one = None
    x_two = None
    y_two = None
    z_two = None
    time_one = None
    time_two = None
    record_counter = 0
    counter = 0

    while counter < len(time_list):

        x_one = x_list[record_counter]
        x_two = x_list[record_counter + 1]
        y_one = y_list[record_counter]
        y_two = y_list[record_counter + 1]
        z_one = z_list[record_counter]
        z_two = z_list[record_counter + 1]
        time_one = time_list[record_counter]

        record_counter += 2
        counter += 2


def create_record(x1, x2, y1, y2, z1, z2, datetime):

    century = 1
    year = 1
    month = 1
    day = 1
    datestamp = f"{century:02d}{year:02d}-{month:02d}-{day:02d} "
    
    time = datetime.time()
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


file = open("/Users/markortega-ponce/Desktop/ZZZPyside/spacedatapython/testdata/cdr20210602v_l0_half_sec.sec", 'rb')
start = datetime.time.fromisoformat("00:00:00")
end = datetime.time.fromisoformat("23:59:59")
x,y,z,t = read_IAGA2002_to_lists.create_datetime_lists_from_iaga(
                                                file, 
                                                start, 
                                                end)

create_iaga2002_file_from_datetime_lists(x,y,z,t)