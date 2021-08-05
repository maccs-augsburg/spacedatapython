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

        self.execute_functions( *args) : --------------
                                             ---------------
        self.year_day_entry_check( year_day_value) : - test

        self.start_hour_entry_check( self.start_hour.get()) : - not done yet
        
        self.start_minute_entry_check( self.start_minute.get()) : - not done yet
        
        self.start_second_entry_check( self.start_second.get()) : - not done yet

        self.end_hour_entry_check( self.end_hour.get()) : - not done yet
        
        self.end_minute_entry_check( self.end_minute.get()) : - not done yet
        
        self.end_second_entry_check( self.end_second.get()) : - not done yet

        self.station_code_entry_check( station_code_value) : - not done yet

        self.file_format_entry_checker( file_selection_value) : - not done yet

        self.error_message_pop_up( title, message) : - working on

        
        

    """

    def __init__(self):
        root = Tk()
        root.geometry('1400x800')
        root.title("Plot input")
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ######################
        ### Labels Section ###
        ######################
        # year_day label
        ttk.Label(mainframe, text="Year Day:").grid(column=1, row=2, sticky=W)

        # Start time labels
        ttk.Label(mainframe, text="Start Hour:").grid(column=1, row=3, sticky=W)
        ttk.Label(mainframe, text="Start Minute:").grid(column=1, row=4, sticky=W)
        ttk.Label(mainframe, text="Start Second:").grid(column=1, row=5, sticky=W)

        # End time labels
        ttk.Label(mainframe, text="End Hour:").grid(column=1, row=6, sticky=W)
        ttk.Label(mainframe, text="End Minute:").grid(column=1, row=7, sticky=W)
        ttk.Label(mainframe, text="End Second:").grid(column=1, row=8, sticky=W)

        # Plot min and max labels
        # X labels
        ttk.Label(mainframe, text="Plot Min x:").grid(column=1, row=9, sticky=W)
        ttk.Label(mainframe, text="Plot Max x:").grid(column=1, row=10, sticky=W)
        # Y labels
        ttk.Label(mainframe, text="Plot Min y:").grid(column=1, row=11, sticky=W)
        ttk.Label(mainframe, text="Plot Max y:").grid(column=1, row=12, sticky=W)   
        #Z labels
        ttk.Label(mainframe, text="Plot Min z:").grid(column=1, row=13, sticky=W)
        ttk.Label(mainframe, text="Plot Max z:").grid(column=1, row=14, sticky=W)
        
        # Station file label
        ttk.Label(mainframe, text="Station code:").grid(column=1, row=1, sticky=W)

        # File format label
        ttk.Label(mainframe, text="Format of file to Open (pick from list below)").grid(column=1, row=15, sticky=W)

        # setting the image to be the maccs logo
        image=Image.open('maccslogo_870.jpeg')
        image_file = ImageTk.PhotoImage(image)
        image_label = ttk.Label(mainframe, image=image_file)
        image_label.image = image_file
        image_label.grid(column=5,row=1, columnspan=20, rowspan=30)

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
        ### Button Section ###
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
        ttk.Button(mainframe, text="Plot", command=lambda: self.execute_functions(mainframe)).grid(column=1, row = 20, sticky=W)
        ttk.Button(mainframe, text="Quit", command=lambda: self.cancel(root)).grid(column=1, row=20, sticky=E)
        
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        #station_code_entry.focus()

        root.bind("<Return>", self.execute_functions)

        root.mainloop()

    def execute_functions(self, mainframe, *args):

        ############################
        ### Getting User Entries ###
        ############################
        # year_day entry
        year_day_value = self.year_day.get()
        year_day_entry_check(self, year_day_value)

        # Start hour, minute, and second entries
        start_hour_value = start_hour_entry_check(self, self.start_hour.get())
        start_minute_value = start_minute_entry_check(self, self.start_minute.get())
        start_second_value = start_second_entry_check(self, self.start_second.get())

        start_time_stamp = datetime.time(hour=start_hour_value, minute=start_minute_value, second=start_second_value)

        # End hour, minute and second entries
        end_hour_value = end_hour_entry_check(end_hour.get())
        end_minute_value = end_minute_entry_check(end_minute.get())
        end_second_value = end_second_entry_check(end_second.get())

        end_time_stamp = datetime.time(hour=end_hour_value, minute=end_minute_value, second=end_second_value)

        # Plot min and max entries
        plot_min_value_x = self.plot_min_x.get()
        plot_max_value_x = self.plot_max_x.get()
        plot_min_value_y = self.plot_min_y.get()
        plot_max_value_y = self.plot_max_y.get()
        plot_min_value_z = self.plot_min_z.get()
        plot_max_value_z = self.plot_min_z.get()

        # Station code entry
        station_code_value = self.station_code.get()
        station_code_entry_check(station_code_value)

        # File Format entry
        file_selection_value = file_selection.get()
        file_ending_value = file_format_entry_checker(file_selection_value)

        #######################
        ### Making the plot ###
        #######################
        # file name and time interval string creation
        file_name_full = station_code_value + year_day_value + file_ending_value
        time_interval_string = file_naming.create_time_interval_string_hms(start_hour_value, start_minute_value, start_second_value, end_hour_value, end_minute_value, end_second_value)
        file_name = station_code_value + year_day_value + time_interval_string

        # trying to open the file
        try:
            file = open(file_name_full, 'rb')
        except:
            error_message_pop_up("File open error", "couldn't find and open your file")

        # Creating the arrays
        xArr, yArr, zArr, timeArr = read_raw_to_lists.create_datetime_lists_from_raw(file, start_time_stamp,
                                                                                     end_time_stamp, file_name)
        # making the time array into datetime objects

        # plotting the arrays
        fig = raw_to_plot.plot_arrays(xArr, yArr, zArr, timeArr, file_name, start_time_stamp,
                                      end_time_stamp)

        # Putting the arrays into the gui
        canvas_plotter.plot(mainframe, fig)

    def year_day_entry_check(self, year_day_value):
        if (len(year_day_value) == 0):
            self.error_message_pop_up(title='year_day_entry Error', message='There was no input for the year day entry box')
            
    def error_message_pop_up(self, title, message):
        messagebox.showerror(title=title, message = "ERROR: " + message)
        
    def cancel(self, root):
        root.destroy()

def main():
    hopefully_works = SingleGraphPlotter()

if __name__ == "__main__":
    main()
