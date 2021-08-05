# single_graph_plotter_class
#
# August 2021 -- Created -- Ted Strombeck
#

# tkinter imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Python 3 imports
import sys
import datetime
from PIL import ImageTk, Image

# Plotter program imports
import raw_to_plot
import file_naming
import read_raw_to_lists
import canvas_plotter

class SingleGraphPlotter:
    """ A class containing a GUI for a single graph, x, y, and z plotter.

        Instance properties:
        

        Instance methods:
            self.calculate( *args): ----------

    """

    def __init__(self):
        root = Tk()
        root.geometry('1400x800')
        root.title("Plot input")
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        gui_labels(self, mainframe)

        gui_entries(self, mainframe, root)
        
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        station_code_entry.focus()

        root.bind("<Return>", self.execute_functions)

        root.mainloop()

    def calculate(self, *args):
        pass

def main():
    pass

if __name__ = "__main__":
    main()
