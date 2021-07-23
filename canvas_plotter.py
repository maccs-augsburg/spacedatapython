# canvas_plotter.py file
#
# July 2021 -- Created -- Ted Strombeck
#

from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkaggg import (FigureCanvasTkAgg)

def cancel():
    window.destroy()

def plot():
    print('Plotted portion of code')

def create_initial_gui(window):
    plot_button = Button(master = window,
                         command = plot,
                         height = 2,
                         width = 10,
                         text='Plot')
    plot_button.grid(column=1, row=1)
    
    cancel_button = Button(master = window,
                           command = cancel,
                           height = 2,
                           width = 10,
                           text='Cancel')
    cancel_button.grid(column=2, row=1)

def main():
    window = Tk()

    window.title('Plotting MACCS files')

    window.geometry('200x100')

    create_initial_gui(window)

    window.mainloop()
    

if __name__ == "__main__":
    main()
