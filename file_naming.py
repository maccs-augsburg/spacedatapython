# file_naming.py
#
# 2021 June - Created - Erik Steinmetz
#

""" Utilities for naming files

Functions that help create correct names for MACCS files.

"""

def create_time_interval_string( shour, sminute, ssecond, ehour, eminute, esecond) :
    answer = ""
    if( shour != 0 or sminute != 0 or ssecond != 0 or ehour != 23 or eminute != 59 or esecond != 59) :
        answer = f"_{shour:02}{sminute:02}{ssecond:02}_{ehour:02}{eminute:02}{esecond:02}"
    return answer
    
def create_time_interval_string( ssecond, esecond) :
    shour = ssecond // 3600
    ssecond = ssecond % 3600
    sminute = ssecond // 60
    ssecond = ssecond % 60
    ehour = esecond // 3600
    esecond = esecond % 3600
    eminute = esecond // 60
    esecond = esecond % 60
    return create_time_interval_string( shour, sminute, ssecond, ehour, eminute, esecond)

if __name__ == "__main__" :
    print( create_time_interval_string( 500, 84000))

