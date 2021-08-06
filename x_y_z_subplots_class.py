# x_y_z_subplots_class.py
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

        self.station_code : A StringVar that keeps track of the 2 Letter station code
        
        self.year_day : A StringVar that keeps track of the year and the day of the year in the format: YYDDD
        
        self.start_hour : An IntVar that keeps track of the starting hour
        
        self.start_minute : An IntVar that keeps track of the starting minute
        
        self.start_second : An IntVar that keeps track of the starting second
        
        self.end_hour : An IntVar that keeps track of the ending hour 
        
        self.end_minute : An IntVar that keeps track of the ending minute
        
        self.end_second : An IntVar that keeps track of the ending second
        
        self.plot_min_x : An IntVar that keeps track of the minimum x value to plot (leave 0 for default x values)
        
        self.plot_max_x : An IntVar that keeps track of the maximum x value to plot (leave 0 for default x values)
        
        self.plot_min_y : An IntVar that keeps track of the minimum y value to plot (leave 0 for default y values)
        
        self.plot_max_y : An IntVar that keeps track of the maximum y value to plot (leave 0 for default y values)
        
        self.plot_min_z : An IntVar that keeps track of the minimum z value to plot (leave 0 for default z values)
        
        self.plot_max_z : An IntVar that keeps track of the maximum z value to plot (leave 0 for default z values)
        
        self.file_selection : A StringVar that sets the correct file ending value based on what type of file is being handed over by the user to plot
        

        Instance methods:

        self.execute_functions( mainframe, *args) : reads in user entries in entry boxes in the gui and calls other functions to plot the results based on the user input
        
        self.year_day_entry_check( year_day_value) : reads the inputted year_day_value and checks to see if there was a value inputted in the entry box

        self.start_hour_entry_check( self.start_hour.get()) : reads the inputted hour value, converts it to an integer and checks to see if it is in the correct range
        
        self.start_minute_entry_check( self.start_minute.get()) : reads the inputted minute value, converts it to an integer and checks to see if it is in the correct range
        
        self.start_second_entry_check( self.start_second.get()) : reads the inputted second value, converts it to an integer and checks to see if it is in the correct range

        self.end_hour_entry_check( self.end_hour.get()) : reads the inputted hour value, converts it to an integer and checks to see if it is in the correct range
        
        self.end_minute_entry_check( self.end_minute.get()) : reads the inputted minute value, converts it to an integer and checks to see if it is in the correct range
        
        self.end_second_entry_check( self.end_second.get()) : reads the inputted second value, converts it to an integer and checks to see if it is in the correct range

        self.station_code_entry_check( station_code_value) : reads the inputted station_code_value and checks to see if there was a value inputted in the entry box

        self.file_format_entry_check( file_selection_value) : reads the inputted file_selection_value and sets the correct file_ending_value for the type of file selected 

        self.error_message_pop_up( title, message) : creates an error pop up message box with the given title and message
        
        self.warning_message_pop_up( title, message) : creates a warning pop up message box with the given title and message

        self.convert_hours_list_to_datetime_object( list_to_convert) : - Not yet implemented
    """

    def __init__(self):
        """ Initialization of the gui

        Creates the gui's buttons, labels and displays the MACCS Logo in the window to initialize the gui.
        """
        # Initializing window object and specifying settings
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
        station_code_entry = ttk.Entry(mainframe, width=4, textvariable=self.station_code)
        station_code_entry.grid(column=1, row=1)

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

        # Plot min and max y
        self.plot_min_y = IntVar()
        self.plot_min_y.set(0)
        ttk.Entry(mainframe, width=3, textvariable=self.plot_min_y).grid(column=1, row=11)
        self.plot_max_y = IntVar()
        self.plot_max_y.set(0)
        ttk.Entry(mainframe, width=3, textvariable=self.plot_max_y).grid(column=1, row=12)

        # Plot min and max z
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
        radio_button_1 = Radiobutton(mainframe, text="CDAWEB -- Not working", value=1, variable=self.file_selection).grid(column=1, row=16, sticky=W)
        radio_button_2 = Radiobutton(mainframe, text="IAGA2000 -- Not working ", value=2, variable=self.file_selection).grid(column=1, row=17, sticky=W)
        radio_button_3 = Radiobutton(mainframe, text="IAGA2002 -- Not working", value=3, variable=self.file_selection).grid(column=1, row=18, sticky=W)
        # Add clean section
        radio_button_4 = Radiobutton(mainframe, text="Raw 2hz file", value=4, variable=self.file_selection).grid(column=1, row=19, sticky=W)
        radio_button_7 = Radiobutton(mainframe, text="other -- Not working", value=7, variable=self.file_selection).grid(column=1, row=20, sticky=W)

        # Management buttons section
        ttk.Button(mainframe, text="Plot", command=lambda: self.execute_functions(mainframe)).grid(column=1, row = 21, sticky=W)
        ttk.Button(mainframe, text="Quit", command=lambda: self.cancel(root)).grid(column=1, row=21)
        
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        # starting tab control on the station code entry box
        station_code_entry.focus()

        # Binding the return key to the execute function
        root.bind("<Return>", self.execute_functions)

        # Keeping the program running
        root.mainloop()

    def execute_functions(self, mainframe, *args):
        """
        Obtains the values entered in the GUI and runs the plotting program with the inputted values
        """

        ############################
        ### Getting User Entries ###
        ############################
        # Station code entry
        station_code_value = self.station_code.get()
        self.station_code_entry_check( station_code_value)
        
        # year_day entry
        year_day_value = self.year_day.get()
        self.year_day_entry_check(year_day_value)

        # Start hour, minute, and second entries
        start_hour_value = self.start_hour_entry_check( self.start_hour.get())
        start_minute_value = self.start_minute_entry_check( self.start_minute.get())
        start_second_value = self.start_second_entry_check( self.start_second.get())

        # creating the start time stamp
        start_time_stamp = datetime.time(hour=start_hour_value, minute=start_minute_value, second=start_second_value)

        # End hour, minute and second entries
        end_hour_value = self.end_hour_entry_check( self.end_hour.get())
        end_minute_value = self.end_minute_entry_check( self.end_minute.get())
        end_second_value = self.end_second_entry_check( self.end_second.get())

        # creating the end time stamp
        end_time_stamp = datetime.time(hour=end_hour_value, minute=end_minute_value, second=end_second_value)

        # Plot min and max entries
        plot_min_value_x = self.plot_min_x.get()
        plot_max_value_x = self.plot_max_x.get()
        plot_min_value_y = self.plot_min_y.get()
        plot_max_value_y = self.plot_max_y.get()
        plot_min_value_z = self.plot_min_z.get()
        plot_max_value_z = self.plot_min_z.get()

        # File Format entry
        file_selection_value = self.file_selection.get()
        file_ending_value = self.file_format_entry_check( file_selection_value)

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
            # popping up an error if we can't open the file
            self.error_message_pop_up("File open error", "couldn't find and open your file")

        # Creating the arrays
        xArr, yArr, zArr, timeArr = read_raw_to_lists.create_datetime_lists_from_raw(file, start_time_stamp,
                                                                                     end_time_stamp, file_name)
        # making the time array into datetime objects -- Not done yet
        
        # plotting the arrays
        fig = raw_to_plot.plot_arrays(xArr, yArr, zArr, timeArr, file_name, start_time_stamp,
                                      end_time_stamp)

        # Putting the arrays into the gui
        canvas_plotter.plot(mainframe, fig)

    def convert_hours_list_to_datetime_object(self, list_to_convert):
        converted_list = []
        
        for i in range(len(list_to_convert)):
            total_time = list_to_convert[i]
            hour = int(total_time / 24)

            total_time = total_time - hour
            minute = int(total_time / 59)

            total_time = total_time - minute
            second = total_time

            converted_list.append(datetime.datetime(year=1111, month=1, day=1, hour=hour, minute=minute, second=second))
            
        return converted_list
            
    def year_day_entry_check(self, year_day_value):
        """
        Checks the year day entry value to see if there was a value inputted for the yearday entry box

        Parameters
        ----------
        String
            year_day_value: the value that was inputted into the year_day_entry box
        """
        # Checking to see if any input was put in the yearday entry box
        if (len(year_day_value) == 0):
            self.error_message_pop_up(title='year_day_entry Error', message='There was no input for the year day entry box')

    def station_code_entry_check(self, station_code_value):
        """
        Checks the station_code_entry value and pops up an error message if it isn't a good entry

        Parameters
        ----------
        String
            station_code_value: the value that was inputted into the station_code_entry box
        """
        # Checking to see if no input was put in the station code entry box
        if(len(station_code_value) == 0):
            # show error as no input was received
            self.error_message_pop_up(title="Station code entry error", message="There was no input for the station code entry box")

    def file_format_entry_check(self, file_selection_value):
        """
        Checks the file_selection_entry value and either pops up a message if input was bad or specifies the ending value of the filename which specifies which type of file to use

        Parameters
        ----------
        String
            file_selection_value: the value that was inputted into the file_selection_entry box

        Returns
        -------
        String
            file_ending_value: the value that specifies the type of file to use
            
        """
        # Setting the initial file ending value to an empty string
        file_ending_value = ''

        # Testing to see if user selected CDA-Web branch
        if(file_selection_value == '1'):
            # CDA-Web branch (NOT IMPLEMENTED)
            self.warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

        # Testing to see if user selected IAGA2000 branch
        elif(file_selection_value == '2'):
            #IAGA2000 branch (NOT IMPLEMENTED)
            self.warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

        # Testing to see if user selected IAGA2002 branch
        elif(file_selection_value == '3'):
            #IAGA2002 branch (NOT IMPLEMENTED)
            self.warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

        # Testing to see if user selected Raw 2hz branch
        elif(file_selection_value == '4'):
            #Raw 2hz file branch (TODO: IMPLEMENT SECTION)
            file_ending_value = '.2hz'

        # Testing to see if user selected other branch
        elif(file_selection_value == '7'):
            #Other option branch (NOT IMPLEMENTED YET) -- for now just show warning message and exit
            self.warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

        # Otherwise we can assume that no option had been selected
        else:
            # Message box error when no file format option has been selected
            self.error_message_pop_up(title="File format option error", message="Please select a file format option")

        # Returning the string of the file type to be used
        return file_ending_value
        
    def start_hour_entry_check(self, start_hour_string):
        """
        Checks the start hour entry value and pops up an error message if it isn't a good entry

        Parameters
        ----------
        String
            start_hour_string: the value that was inputted into the start_hour_entry box

        Returns
        -------
        Int
            value: the int version of the inputted value in the start_hour_entry box
        """
        # making sure the inputted value is an int not a float
        value = int(start_hour_string)

        if(value > 23):
            # Have error message box pop up because it can't be more than 23
            self.error_message_pop_up(title="Start Hour Entry Error", message="Start hour cannot be more than 23")
        
        # Testing to see if the inputted value is less than what it can be
        elif(value < 0):
            # Have error message box pop up because it can't be a negative number
            self.error_message_pop_up(title="Start Hour Entry Error", message="Start hour cannot be negative")

        # Returning the start_hour_string so that whatever changes we made to it get returned
        return value

    def start_minute_entry_check(self, start_minute_string):
        """
        Checks the start minute entry value and pops up an error message if it isn't a good entry

        Parameters
        ----------
        String
            start_minute_string: the value that was inputted into the start_minute_entry box

        Returns
        -------
        Int
            value: the inputted value in the start_minute_entry box
        """
        # making sure the inputted value is an int not a float
        value = int(start_minute_string)

        if(value > 59):
            # Have error messsage box pop up becuase it can't be more than 59
            self.error_message_pop_up(title="Start Minute Entry Error", message="Start minute cannot be more than 59")

        # Testing to see if the inputted value is less than what it can be
        elif(value < 0):
            # Have error message box pop up because it can't be a negative number
            self.error_message_pop_up(title="Start Minute Entry Error", message="Start minute cannot be negative")

        # Returning the start_minute_string so whatever changes we made to it get returned
        return value
        
    def start_second_entry_check(self, start_second_string):
        """
        Checks the start second entry value and pops up an error message if it isn't a good entry

        Parameters
        ----------
        String
            start_second_string: the value that was inputted into the start_second_entry box

        Returns
        -------
        Int
            value: the inputted value in the start_second_entry box
        """
        # making sure the inputted value is an int not a float
        value = int(start_second_string)

        if(value > 59):
            # Have error messsage box pop up becuase it can't be more than 59
            self.error_message_pop_up(title="Start Second Entry Error", message="Start second cannot be more than 59")

        # Testing to see if the inputted value is less than what it can be
        elif(value < 0):
            # Have error message box pop up because it can't be a negative number
            self.error_message_pop_up(title="Start Second Entry Error", message="Start second cannot be negative")

        # Returning the start_second_string so whatever changes we made to it get returned
        return value

    def end_hour_entry_check(self, end_hour_string):
        """
        Checks the end hour entry value and pops up an error message if it isn't a good entry

        Parameters
        ----------
        String
            end_hour_string: the value that was inputted into the end_hour_entry box

        Returns
        -------
        Int
            value: the inputted value in the end_hour_entry box
        """
        # making sure the inputted value is an int not a float
        value = int(end_hour_string)

        # Testing to see if the inputted value exceeds what it can be
        if(value > 23):
            # Have error message box pop up because it can't be more than 23
            self.error_message_pop_up(title="End Hour Entry Error", message="End hour cannot be more than 23")

        # Testing to see if the inputted value is less than what it can be
        elif(value < 0):
            # Have error message box pop up because it can't be a negative number
            self.error_message_pop_up(title="End Hour Entry Error", message="End hour cannot be negative")

        # Returning the end_hour_string so whatever changes we made to it get returned
        return value

    def end_minute_entry_check(self, end_minute_string):
        """
        Checks the end minute entry value and pops up an error message if it isn't a good entry

        Parameters
        ----------
        String
            end_minute_string: the value that was inputted into the end_minute_entry box

        Returns
        -------
        Int
            value: the inputted value in the end_hour_entry box
        """
        # making sure the inputted value is an int not a float
        value = int(end_minute_string)

        # Testing to see if the inputted value exceeds what it can be
        if(value > 59):
            #Have error messsage box pop up becuase it can't be more than 59
            self.error_message_pop_up(title="End Minute Entry Error", message="End minute cannot be more than 59")

        # Testing to see if the inputted value is less than what it can be
        elif(value < 0):
            # Have error message box pop up because it can't be a negative number
            self.error_message_pop_up(title="End Minute Entry Error", message="End minute cannot be negative")

        # Returning the end_minute_string so whatever changes we made to it get returned
        return value

    def end_second_entry_check(self, end_second_string):
        """
        Checks the end second entry value and pops up an error message if it isn't a good entry

        Parameters
        ----------
        String
            end_second_string: the value that was inputted into the end_second_entry box

        Returns
        -------
        Int
            end_second_string: the inputted value in the end_second_entry box
        """
        # making sure the inputted value is an int not a float
        value = int(end_second_string)

        # Testing to see if the inputted value exceeds what it can be
        if(value > 59):
            # Have error messsage box pop up becuase it can't be more than 59
            self.error_message_pop_up(title="End Second Entry Error", message="End second cannot be more than 59")

        # Testing to see if the inputted value is less than what it can be
        elif(value < 0):
            # Have error message box pop up because it can't be a negative number
            self.error_message_pop_up(title="End Second Entry Error", message="End second cannot be negative")

        # Returning the end_second_string so whatever changes we made to it get returned
        return value
    
        
    def error_message_pop_up(self, title, message):
        # pops up error message box with the title and message inputted
        messagebox.showerror(title=title, message = "ERROR: " + message)
        sys.exit(0)

    def warning_message_pop_up(self, title, message):
        # pops up warning message box with the title and message inputted
        messagebox.showwarning(title=title, message="WARNING: " + message)
        
    def cancel(self, root):
        # Exits the gui without running any code after
        root.destroy()

def main():
    hopefully_works = SingleGraphPlotter()

if __name__ == "__main__":
    main()