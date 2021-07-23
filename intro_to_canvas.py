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
