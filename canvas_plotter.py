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
from PIL import ImageTk, Image

# Custom file imports
import file_naming
import read_raw_to_lists
import raw_to_plot

def create_figure(xArr, yArr, zArr, timeArr, filename, stime, etime): # Not sure about this function
        # the figure that will contain the plot
        fig = raw_to_plot.plot_arrays(xArr, yArr, zArr, timeArr, filename, stime, etime)

        return fig

def plot(window, file_name_full):
        # creating the time interval string using the file_naming python file
        time_interval_string = file_naming.create_time_interval_string_hms(0, 0, 0, 23, 59, 59)
        file_name = file_name_full[0:8] + time_interval_string

        # Opening said file
        file = open(file_name_full, 'rb')

        # Setting the start and end time stamps (for testing purposes)
        start_time_stamp = datetime.time(hour=18, minute=0, second=0)
        end_time_stamp = datetime.time(hour=19, minute=59, second=59)

        # Calling the new function in read_raw_to_lists
        #       (create_datetime_lists_from_raw)
        xArr, yArr, zArr, timeArr = read_raw_to_lists.create_datetime_lists_from_raw(file,
                                                                        start_time_stamp,
                                                                        end_time_stamp, file_name_full[0:8])
        # Getting the constructed figure
        fig = create_figure(xArr, yArr, zArr, timeArr, file_name_full[0:8], start_time_stamp, end_time_stamp)

        #window.geometry('1000x500')

        # Storing that figure into a canvas object
        canvas = FigureCanvasTkAgg(fig, master = window)
        canvas.draw()

        # Placing canvas object into the window
        canvas.get_tk_widget().grid(column=3, row=1, columnspan=8, rowspan=20)

def cancel(window):
        window.destroy()

def create_initial_gui(window, file_name_full):
        global plot_min_x, plot_max_x, plot_min_entry_x, plot_max_entry_x
        global plot_min_y, plot_max_y, plot_min_entry_y, plot_max_entry_y
        global plot_min_z, plot_max_z, plot_min_entry_z, plot_max_entry_z

        # setting the image to be the maccs logo
        image=Image.open('maccslogo_870.jpeg')
        image_file = ImageTk.PhotoImage(image)
        image_label = ttk.Label(window, image=image_file)
        image_label.image = image_file
        image_label.grid(column=5,row=1, columnspan=8, rowspan=20)

        
        # plot min x label and entry box
        ttk.Label(window, text="Plot min x:").grid(column=1, row=1)
        plot_min_x = IntVar()
        plot_min_x.set(0)
        plot_min_entry_x = ttk.Entry(window, width=3, textvariable=plot_min_x).grid(column=2, row=1)

        # plot max x label and entry box
        ttk.Label(window, text="Plot max x:").grid(column=1, row=2)
        plot_max_x = IntVar()
        plot_max_x.set(0)
        plot_max_entry_x = ttk.Entry(window, width=3, textvariable=plot_max_x).grid(column=2, row=2)

        # plot min y label and entry box
        ttk.Label(window, text="Plot min y:").grid(column=1, row=3)
        plot_min_y = IntVar()
        plot_min_y.set(0)
        plot_min_entry_y = ttk.Entry(window, width=3, textvariable=plot_min_y).grid(column=2, row=3)

        # plot max y label and entry box
        ttk.Label(window, text="Plot max y:").grid(column=1, row=4)
        plot_max_y = IntVar()
        plot_max_y.set(0)
        plot_max_entry_y = ttk.Entry(window, width=3, textvariable=plot_max_y).grid(column=2, row=4)

        # plot min z label and entry box
        ttk.Label(window, text="Plot min z:").grid(column=1, row=5)
        plot_min_z = IntVar()
        plot_min_z.set(0)
        plot_min_entry_z = ttk.Entry(window, width=3, textvariable=plot_min_z).grid(column=2, row=5)

        # plot max z label and entry box
        ttk.Label(window, text="Plot max z:").grid(column=1, row=6)
        plot_max_z = IntVar()
        plot_max_z.set(0)
        plot_max_entry_z = ttk.Entry(window, width=3, textvariable=plot_max_z).grid(column=2, row=6)

        # plot button creation and placement
        plot_button = Button(master = window,
                         command = lambda: plot(window, file_name_full),
                         height = 2,
                         width = 10,
                         text='Plot')
        plot_button.grid(column=1, row=7)

        # cancel/quit button creation and placement -- Updated text to be "Quit" instead of "Cancel"
        cancel_button = Button(master = window,
                           command = lambda: cancel(window),
                           height = 2,
                           width = 10,
                           text='Quit')
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
