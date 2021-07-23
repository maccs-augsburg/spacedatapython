from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
#NavigationToolbar2Tk)


import sys
import datetime

import one_array_plotted
import read_raw_to_lists

# plot function is created for plotting the graph in tkinter window
def plot():

    
    # the figure that will contain the plot
    #fig = Figure(figsize = (5, 5), dpi = 100)

    # list of squares
    #y = [i**2 for i in range(101)]

    

        

        

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = window)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(column = 1, row = 1, sticky = (N, W, E, S))

    # creating the Matplotlib toolbar
    #toolbar = NavigationToolbar2Tk(canvas, window)
    #toolbar.update()

    # placing the toolbar on the Tkinter window
    #canvas.get_tk_widget().pack()

def gui_entries(window) :
    """
    """
    #Creation of the Year Day entry widget
    year_day = IntVar()
    year_day_entry = ttk.Entry(window, width = 5, textvariable = year_day)
    year_day_entry.grid(column = 2, row = 2, sticky = (W,E))
    
    #Creation of the Start Hour entry widget 
    start_hour = IntVar()
    start_hour_entry = ttk.Entry(window, width = 5, textvariable = start_hour)
    start_hour_entry.grid(column = 2, row = 3, sticky = (W,E))

    #Creation of the Start Minute entry widget
    start_minute = IntVar()
    start_minute_entry = ttk.Entry(window, width = 5, textvariable = start_minute)
    start_minute_entry.grid(column = 2, row = 4, sticky = (W, E))

    #Creation of the Start Second entry widget 
    start_second = IntVar()
    start_second_entry = ttk.Entry(window, width = 5, textvariable = start_second)
    start_second_entry.grid(column = 2, row = 5, sticky = (W, E))

    #Creation of the end hour entry widget, also has set times for defalut
    end_hour = IntVar()
    end_hour_entry = ttk.Entry(window, width = 5, textvariable = end_hour)
    end_hour_entry.grid(column = 2, row = 6, sticky = (W,E))
    end_hour.set(23)

    #Creation of the end minute entry widget, also has set times for default
    end_minute = IntVar()
    end_minute_entry = ttk.Entry(window, width = 5, textvariable = end_minute)
    end_minute_entry.grid(column = 2, row = 7, sticky = (W,E))
    end_minute.set(59)

    #Creation of the end second widget, also has set times for default
    end_second = IntVar()
    end_second_entry = ttk.Entry(window, width = 3, textvariable = end_second)
    end_second_entry.grid(column = 2, row = 8, sticky = (W,E))
    end_second.set(59)

    #Creation of the station names entry widget
    station_names= StringVar()
    station_names_entry = ttk.Entry(window, width = 3, textvariable = station_names)
    station_names_entry.grid(column = 2, row = 1, sticky = (W,E))

    #Creation of the graph from plotter check button
    graph_from_plotter_x = IntVar()
    graph_from_plotter_y = IntVar()
    graph_from_plotter_z = IntVar()
    x_plot = ttk.Checkbutton(window, text = "X Plot", variable = graph_from_plotter_x, onvalue = 1).grid(column = 1, row = 10, sticky = W)
    y_plot = ttk.Checkbutton(window, text = "Y Plot", variable = graph_from_plotter_y, onvalue = 2).grid(column = 1, row = 11, sticky = W) 
    z_plot = ttk.Checkbutton(window, text = "Z Plot", variable = graph_from_plotter_z, onvalue = 3).grid(column = 1, row = 12, sticky = W)

    #Creation of the Okay and Cancel button that has commands to either run
    #the GUI if you press okay or to "destroy" the GUI if you hit canel
    plot_button = ttk.Button(window, text = "Plot", command = plot).grid(column = 2, row = 14, sticky = W)
    cancel_button = ttk.Button(window, text = "Cancel", command = lambda: cancel(root)).grid(column =1, row = 14, sticky = W)



def gui_labels(window) :
    """
    """
    #Year Day Label
    ttk.Label(window, text = "Year Day: ").grid(column = 1, row = 2, sticky = W)
    #Start Hour Label 
    ttk.Label(window, text = "Start Hour: ").grid(column = 1, row = 3, sticky = W)


def main() :
    """
    """
    # the main Tkinter window
    window = Tk()
    
    file_option = "pdf"

    # setting the title
    window.title('Plotting in Tkinter')

    # dimensions of the main window
    window.geometry("500x500")

    #Call the 
    gui_entries(window)

    gui_labels(window)

    # button that displays the plot
    #plot_button = Button(master = window,
                        #command = plot,
                        #height = 2,
                        #width = 10,
                        #text = "Plot")

    # place the button
    # in main window
    #plot_button.grid(column = 0, row = 0, sticky = (N, W, E, S))

    # run the gui
    window.mainloop()

	

if __name__ == "__main__" :


    main()
    


    
    # the main Tkinter window
    #window = Tk()
    
    #file_option = "pdf"

    # setting the title
    #window.title('Plotting in Tkinter')

    # dimensions of the main window
    #window.geometry("500x500")

    # button that displays the plot
    #plot_button = Button(master = window,
                        #command = plot,
                        #height = 2,
                        #width = 10,
                        #text = "Plot")

    # place the button
    # in main window
    #plot_button.grid(column = 0, row = 0, sticky = (N, W, E, S))

    # run the gui
    #window.mainloop()
