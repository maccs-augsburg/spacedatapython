'''
time_data_remover.py

Data remover - Given a file and two times, remove all the 
    data records between the two times and write out the shortened file.

Useful reference: documentation/BinaryFormatNotes.txt

Created August 2022 - Mark Ortega-Ponce
'''

import argparse
import datetime
import sys
import model.read_raw_to_lists
import model.read_clean_to_lists
import model.read_iaga2002_to_lists
import write_lists_to_iaga2002

# TODO: Deprecate? Works, but MACCS distributes IAGA files.
def remove_data_from_clean(infile, outfile, start_time, end_time):

    '''
    Parameters
    ----------
    infile : open file object
        The file object to be read.
    outfile : open file object
        The file object to write out to.
    start_time : datetime.time
        The time to start removing records.
    end_time: datetime.time
        The time to stop removing records.
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

# TODO: Deprecate? Works, but MACCS distributes IAGA files.
def remove_data_from_raw(infile, outfile, start_time, end_time):

    '''
    Parameters
    ----------
    infile : open file object
        The file object to be read.
    outfile : open file object
        The file object to write out to.
    start_time : datetime.time
        The time to start removing records.
    end_time: datetime.time
        The time to stop removing records.
    '''

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


def remove_time(x,y,z,t, start_time, end_time, outfile, station):
    '''
    Given datetime lists created from raw/clean/iaga files.
    Remove the time records between start_time and end_time.
    Write the results out to an outfile in iaga2002 format.

    Parameters:
    -----------
    x : list
        List of x values collected from clean/raw/iaga files.
    y : list
        List of y values collected from clean/raw/iaga files.
    z : list
        List of z values collected from clean/raw/iaga files.
    t : list
        List of datetime values collected from clean/raw/iaga files.
    start_time: datetime.time
        Time to start flattening axis.
    end_time : datetime.time
        Time to end flatterning axis.
    outfile : Open file object.
        File to write new values in.
    station_abbrev : str
        Station abbreviation to create header.
    '''

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
        
    new_x = []
    new_y = []
    new_z = []
    new_t = []

    flag = False

    for i in range (len(t)):
        
        if i == start_index:
            flag = True
        if i == end_index:
            flag = False

        if flag == False:
            new_x.append(x[i])
            new_y.append(y[i])
            new_z.append(z[i])
            new_t.append(t[i])

    outfile = open(outfile, 'w')
    write_lists_to_iaga2002.create_iaga2002_file_from_datetime_lists(new_x, new_y, new_z, new_t, outfile, station)

def main():
    
    parser = argparse.ArgumentParser(description="Remove records between start time and end time.")
    parser.add_argument('filename', type=str, help="name of the input file")
    parser.add_argument('stime', type=str, nargs='?',
        default="10:00:00", help="time to start removing records")
    parser.add_argument('etime', type=str, nargs='?',
        default="20:00:00", help="time to stop removing records")
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

    outfile_name = args.filename.split('.')[0] + "_remove_time_test.sec"

    remove_time(x,y,z,t,start_time, end_time, outfile_name, station_code)

if __name__ == "__main__":
    main()