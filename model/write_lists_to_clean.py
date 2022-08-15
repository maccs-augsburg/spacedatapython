import datetime
import sys
import model.read_clean_to_lists

def create_clean_file_from_datetime_lists(x_list, y_list, z_list, time_list, flag_list):

    pass

def create_clean_record():
    pass

file = open("/Users/markortega-ponce/Desktop/ZZZPyside/spacedatapython/testdata/CH20097.s2", 'rb')
start = datetime.time.fromisoformat("00:00:00")
end = datetime.time.fromisoformat("23:59:59")
x,y,z,t,f = model.read_clean_to_lists.create_datetime_lists_from_clean(
                                                file, 
                                                start, 
                                                end)