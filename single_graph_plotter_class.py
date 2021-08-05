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

        self.station_code : --------
                          ----------
        self.year_day : ------------
                      --------------
        self.start_hour : ----------
                        ------------
        self.start_minute : --------
                          ----------
        self.start_second : --------
                          ----------
        self.end_hour : ------------
                      --------------
        self.end_minute : ----------
                        ------------
        self.end_second : ----------
                        ------------
        self.plot_min_x : ----------
                        ------------
        self.plot_max_x : ----------
                        ------------
        self.plot_min_y : ----------
                        ------------
        self.plot_max_y : ----------
                        ------------
        self.plot_min_z : ----------
                        ------------
        self.plot_max_z : ----------
                        ------------
        self.file_selection : ------
                            --------
        self.plot_button : ---------
                         -----------
        self.quit_button : ---------
                         -----------
        

        Instance methods:

        self.execute_functions(self, *args) : --------------
                                        ---------------
        self.gui_entries(self, mainframe, root) : -----
                                                -------
        self.
        

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

        #station_code_entry.focus()

        root.bind("<Return>", self.execute_functions)

        root.mainloop()

    def gui_labels(self, mainframe):
        pass

    def gui_entries(self, mainframe, root):

        ###########################
        ### Entry Boxes Section ###
        ###########################
        # Station file entries
        self.station_code = StringVar()
        ttk.Entry(mainframe, width=4, textvariable=self.station_code).grid(column=1, row=1)

        # year_day entry
        self.year_day = StringVar()
        ttk.Entry(mainframe, width=6, textvariable=self.year_day).grid(column=1, row=2) 

        # Start Hour entry
        self.start_hour = IntVar()
        self.start_hour.set(0)
        ttk.Entry(mainframe, width=3, textvariable=self.start_hour).grid(column=1, row=3)

        # Start Minute entry
        self.start_minute = IntVar()
        self.start_minute.set(0)
        ttk.Entry(mainframe, width=3, textvariable=self.start_minute).grid(column=1, row=4)

        # Start Second entry
        self.start_second = IntVar()
        ttk.Entry(mainframe, width=3, textvariable=self.start_second).grid(column=1, row=5)

        # End Hour entry
        self.end_hour = IntVar()
        self.end_hour.set(23)
        ttk.Entry(mainframe, width=3, textvariable=self.end_hour).grid(column=1, row=6)

        # End Minute entry
        self.end_minute = IntVar()
        self.end_minute.set(59)
        ttk.Entry(mainframe, width=3, textvariable=self.end_minute).grid(column=1, row=7)

        # End Second entry
        self.end_second = IntVar()
        self.end_second.set(59)
        ttk.Entry(mainframe, width=3, textvariable=self.end_second).grid(column=1, row=8)

        # Plot min and Plot max entries
        # Plot min and max x
        self.plot_min_x = IntVar()
        self.plot_min_x.set(0)
        ttk.Entry(mainframe, width=3, textvariable=self.plot_min_x).grid(column=1, row=9)
        self.plot_max_x = IntVar()
        self.plot_max_x.set(0)
        ttk.Entry(mainframe, width=3, textvariable=self.plot_max_x).grid(column=1, row=10)

        self.plot_min_y = IntVar()
        self.plot_min_y.set(0)
        ttk.Entry(mainframe, width=3, textvariable=self.plot_min_y).grid(column=1, row=11)
        self.plot_max_y = IntVar()
        self.plot_max_y.set(0)
        ttk.Entry(mainframe, width=3, textvariable=self.plot_max_y).grid(column=1, row=12)

        self.plot_min_z = IntVar()
        self.plot_min_z.set(0)
        ttk.Entry(mainframe, width=3, textvariable=self.plot_min_z).grid(column=1, row=13)
        self.plot_max_z = IntVar()
        self.plot_max_z.set(0)
        ttk.Entry(mainframe, width=3, textvariable=self.plot_max_z).grid(column=1, row=14)

        ######################
        ### Button section ###
        ######################
        # Radiobutton section
        # file selection of type of file to open
        self.file_selection = StringVar()
        radio_button_1 = Radiobutton(mainframe, text="CDAWEB -- Not working", value=1, variable=self.file_selection).grid(column=1, row=15, sticky=W)
        radio_button_2 = Radiobutton(mainframe, text="IAGA2000 -- Not working ", value=2, variable=self.file_selection).grid(column=1, row=16, sticky=W)
        radio_button_3 = Radiobutton(mainframe, text="IAGA2002 -- Not working", value=3, variable=self.file_selection).grid(column=1, row=17, sticky=W)
        # Add clean section
        radio_button_4 = Radiobutton(mainframe, text="Raw 2hz file", value=4, variable=self.file_selection).grid(column=1, row=18, sticky=W)
        radio_button_7 = Radiobutton(mainframe, text="other -- Not working", value=7, variable=self.file_selection).grid(column=1, row=19, sticky=W)

        # Management buttons section
        self.plot_button = ttk.Button(mainframe, text="Plot", command=lambda: execute_functions(mainframe)).grid(column=1, row = 20, sticky=W)
        self.quit_button = ttk.Button(mainframe, text="Quit", command=lambda: cancel(root)).grid(column=1, row=20, sticky=E)
        

    def execute_functions(self, *args):
        pass

def main():
    hopefully_works = SingleGraphPlotter()

if __name__ = "__main__":
    main()
