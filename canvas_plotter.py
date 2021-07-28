# canvas_plotter.py file
#
# July 2021 -- Created -- Ted Strombeck
#

from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

# Python 3 imports
import sys
import datetime

# Custom file imports
import file_naming
import read_raw_to_lists
import raw_to_plot

def create_figure(xArr, yArr, zArr, timeArr, filename, stime, etime): # Not sure about this function
        # the figure that will contain the plot
        fig = raw_to_plot.plot_arrays(xArr, yArr, zArr, timeArr, filename, stime, etime)

        return fig

def plot(window, file_name_full):
    
        time_interval_string = file_naming.create_time_interval_string_hms(0, 0, 0, 23, 59, 59)
        file_name = file_name_full[0:8] + time_interval_string

        file = open(file_name_full, 'rb')

        start_time_stamp = datetime.time(hour=0, minute=0, second=0)
        end_time_stamp = datetime.time(hour=23, minute=59, second=59)

        xArr, yArr, zArr, timeArr = read_raw_to_lists.create_lists_from_raw(file,
                                                                        start_time_stamp,
                                                                        end_time_stamp)

        fig = create_figure(xArr, yArr, zArr, timeArr, file_name_full[0:8], start_time_stamp, end_time_stamp)

        #window.geometry('1000x500')

        canvas = FigureCanvasTkAgg(fig, master = window)
        canvas.draw()

        canvas.get_tk_widget().grid(column=3, row=2)

def cancel(window):
        window.destroy()

def create_initial_gui(window, file_name_full):
        plot_button = Button(master = window,
                         command = lambda: plot(window, file_name_full),
                         height = 2,
                         width = 10,
                         text='Plot')
        plot_button.grid(column=1, row=1)

        cancel_button = Button(master = window,
                           command = lambda: cancel(window),
                           height = 2,
                           width = 10,
                           text='Cancel')
        cancel_button.grid(column=2, row=1)

def main():
        window = Tk()

        window.title('Plotting MACCS files')

        window.geometry('1400x900')

        file_name_full = 'PG20212.2hz'

        create_initial_gui(window, file_name_full)

        window.mainloop()
    

if __name__ == "__main__":
    main()
