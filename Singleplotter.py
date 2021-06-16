#Single graph with x, y and z plotted
#Created by- Annabelle 


import matplotlib.pyplot as plt
from matplotlib.ticker import(MultipleLocator, AutoMinorLocator)
import sys
import datetime

from raw_codecs import decode, time_of_record
import station_names

def create_Arrays (raw_record, stime, etime) :
    """
    Creates x, y, and z
    Places x, y, and z into according lists

    Parameters
    ----------
    raw_recod :

    stime :

    etime :

    Returns
    -------
    List
        xArr:
    List
        yArr:
    List
        zArr
    """
    xArr = []
    yArr = []
    zArr = []
    timeArr = []

    #This while loop is to place the information we are creating into the right arrays
    while True :
        one_record = raw_record.read( 38)
        if not one_record :
            break
        current_time = time_of_record(one_record)
        if current_time >= stime :

            
            x1 = decode( one_record[18:21]) / 40.0
            y1 = decode( one_record[21:24]) / 40.0
            z1 = decode( one_record[24:27]) / 40.0
            xArr.append(x1)
            yArr.append(y1)
            zArr.append(z1)

            hour = one_record[4]
            minute = one_record[5]
            second = one_record[6]
            time = hour + minute /60 + second / 3600
            timeArr.append(time)
            
        if current_time >= etime :
            break
        
    return xArr, yArr, zArr, timeArr


def plot_arrays(xArr, yArr, zArr, timeArr, filename, stime, etime, fileOption) :
    """
    """

























    
