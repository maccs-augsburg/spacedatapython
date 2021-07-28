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

        canvas.get_tk_widget().grid(column=3, row=1, columnspan=2, rowspan=12)

def cancel(window):
        window.destroy()

def create_initial_gui(window, file_name_full):
        global plot_min_x, plot_max_x, plot_min_entry_x, plot_max_entry_x
        global plot_min_y, plot_max_y, plot_min_entry_y, plot_max_entry_y
        global plot_min_z, plot_max_z, plot_min_entry_z, plot_max_entry_z
        
        # plot min x
        ttk.Label(window, text="Plot min x:").grid(column=1, row=1)
        plot_min_x = IntVar()
        plot_min_x.set(0)
        plot_min_entry_x = ttk.Entry(window, width=3, textvariable=plot_min_x).grid(column=2, row=1)

        # plot max x
        ttk.Label(window, text="Plot max x:").grid(column=1, row=2)
        plot_max_x = IntVar()
        plot_max_x.set(0)
        plot_max_entry_x = ttk.Entry(window, width=3, textvariable=plot_max_x).grid(column=2, row=2)

        # plot min y
        ttk.Label(window, text="Plot min y:").grid(column=1, row=3)
        plot_min_y = IntVar()
        plot_min_y.set(0)
        plot_min_entry_y = ttk.Entry(window, width=3, textvariable=plot_min_y).grid(column=2, row=3)

        # plot max y
        ttk.Label(window, text="Plot max y:").grid(column=1, row=4)
        plot_max_y = IntVar()
        plot_max_y.set(0)
        plot_max_entry_y = ttk.Entry(window, width=3, textvariable=plot_max_y).grid(column=2, row=4)

        # plot min z
        ttk.Label(window, text="Plot min z:").grid(column=1, row=5)
        plot_min_z = IntVar()
        plot_min_z.set(0)
        plot_min_entry_z = ttk.Entry(window, width=3, textvariable=plot_min_z).grid(column=2, row=5)

        # plot max z
        ttk.Label(window, text="Plot max z:").grid(column=1, row=6)
        plot_max_z = IntVar()
        plot_max_z.set(0)
        plot_max_entry_z = ttk.Entry(window, width=3, textvariable=plot_max_z).grid(column=2, row=6)

        
        plot_button = Button(master = window,
                         command = lambda: plot(window, file_name_full),
                         height = 2,
                         width = 10,
                         text='Plot')
        plot_button.grid(column=1, row=7)

        cancel_button = Button(master = window,
                           command = lambda: cancel(window),
                           height = 2,
                           width = 10,
                           text='Cancel')
        cancel_button.grid(column=2, row=7)

def main():
        window = Tk()

        window.title('Plotting MACCS files')

        window.geometry('1400x900')

        file_name_full = 'PG20212.2hz'

        create_initial_gui(window, file_name_full)

        window.mainloop()
    

if __name__ == "__main__":
    main()
