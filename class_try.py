#Gui implemented with classes
#Annabelle

#Imports from tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


#imports from python 
import sys
import datetime
from PIL import ImageTk, Image

#imports from plotter functions

import file_naming
import read_raw_to_lists
import one_array_plotted 


class ThreeGraphPlotter:
    """
    """
def __init__(self):
    """
    """
    #Creation of the window 
    window = Tk()
    window.geometry('1500x600')
    window.title('X, Y and Z Plotter')

    mainframe = ttk.Frame(window, padding = "3 3 12 12")
    mainframe.grid(column = 0, row = 0, sticky = (N,W,E,S))

    window.columnconfigure(0, weight = 1)
    window.rowconfigure(0, weight = 1)

    #File name values for saving figure
    self.figure = None
    self.file_name = None

    ###Labels###

    #Year day entry box label 
    ttk.label(mainframe, text = "Year Day: ").grid(column = 1, row = 2, sticky = E)
    
    #Start hour entry box label
    ttk.Label(mainframe, text = "Start Hour: ").grid(column = 1, row = 3, sticky = E)

    #Start minute entry box label
    ttk.Label(mainframe, text = "Start Minute: ").grid(column = 1, row = 4,sticky = E)

    #Start second entry box label
    ttk.Label(mainframe, text = "Start Second: ").grid(column = 1, row = 5, sticky = E)

    #End hour entry box label
    ttk.Label(mainframe, text = "End Hour: ").grid(column = 1, row = 6, sticky = E)

    #End minute entry box label
    ttk.Label(mainframe, text = "End Minute: ").grid(column = 1, row = 7, sticky = E)

    #End second entry box label
    ttk.Label(mainframe, text = "End Second: ").grid(column = 1, row = 8, sticky = E)

    #Plot x, y, or z checkbox label
    ttk.Label(mainframe, text = "Plot X, Y or Z: ").grid(column = 1, row = 9, sticky = E)

    #Station code entry box label
    ttk.Label(mainframe, text = "Station Code: ").grid(column = 1, row = 1, pady = (25, 0), sticky = E)

    #File option radiobutton label
    ttk.Label(mainframe, text = "File Option: ").grid(column = 1, row = 14, sticky = E)



    ###Entry Boxes###
    self.year_day = StringVar()
    ttk.Entry(mainframe, width= 5, textvariable = self.year_day).grid(column = 2, row = 2,   sticky = W)

    self.start_hour = IntVar()
    self.start_hour.set(0)
    ttk.Entry(mainframe, width = 5, textvariable = self.start_hour).grid(column = 2, row = 3, sticky = W)

    self.start_minute = IntVar()
    self.start_minute.set(0)
    ttk.Entry(mainframe, width = 5, textvariable = self.start_minute).grid(column = 2, row = 4, sticky = W)

    self.start_second = IntVar()
    self.start_second.set(0)
    ttk.Entry(mainframe, width = 5, textvariable = self.start_second).grid(column = 2, row = 5,sticky = W)

    self.end_hour = IntVar()
    self.end_hour.set(23)
    ttk.Entry(mainframe, width = 5, textvariable = self.end_hour).grid(column = 2, row = 6, sticky = W)

    self.end_minute = IntVar()
    self.end_minute.set(59)
    ttk.Entry(mainframe, width = 5, textvariable = self.end_minute).grid(column = 2, row = 7, sticky = W)

    self.end_second = IntVar()
    self.end_second.set(59)
    ttk.Entry(mainframe, width = 5, textvariable = self.end_second).grid(column = 2, row = 8, sticky = W)

    self.station_names = StringVar()
    ttk.Entry(mainframe, width = 5, textvariable = self.station_names).grid(column = 2, row = 1, pady = (25, 0), sticky = W)

    ###Check Boxes and Radiobuttons###
    self.graph_from_plotter_x = IntVar()
    self.graph_from_plotter_y = IntVar()
    self.graph_from_plotter_z = IntVar()
    
    x_plot = ttk.Checkbutton(mainframe, text = "X Plot", variable = self.graph_from_plotter_x, onvalue = 1).grid(column = 2, row = 10,padx = 25 , sticky = W)
    y_plot = ttk.Checkbutton(mainframe, text = "Y Plot", variable = self.graph_from_plotter_y, onvalue = 2).grid(column = 2, row = 11,padx = 25 , sticky = W) 
    z_plot = ttk.Checkbutton(mainframe, text = "Z Plot", variable = self.graph_from_plotter_z, onvalue = 3).grid(column = 2, row = 12,padx = 25 , sticky = W)

    self.file_selection = StringVar()
    cda_web = Radiobutton(mainframe, text = "CDAWEB:NA", value = 1, variable = self.file_selection).grid(column = 2, row = 15, padx = 25,  sticky = W)
    iaga_00 = Radiobutton(mainframe, text = "IAGA2000:NA", value = 2, variable = self.file_selection).grid(column = 2, row = 16, padx = 25,  sticky = W)
    iaga_02 = Radiobutton(mainframe, text =     "IAGA2002:NA", value = 3, variable = fself.ile_selection).grid(column = 2, row = 17, padx = 25, sticky = W)
    raw_hz_file = Radiobutton(mainframe, text = "Raw 2hz file", value = 4, variable = self.file_selection).grid(column = 2, row = 18, padx = 25,  sticky = W)
    clean_data = Radiobutton(mainframe, text = "Clean Data", value = 5, variable = self.file_selection).grid(column = 2, row = 19, padx = 25, sticky = W)


    ###Buttons###
    
    ttk.Button(mainframe, text = "Plot", command = lambda: self.execute_functions(mainframe)).grid(column = 2, row = 20,  sticky = W)
    ttk.Button(mainframe, text = "Cancel", command = lambda: self.cancel(window)).grid(column =1, row = 20, padx = 25, sticky = W)
    ttk.Button(mainframe, text="Save", command=lambda: self.save(self.figure, self.file_name)).grid(column=2, row=21, sticky=E)
    ttk.Button(mainframe, text="Save As", command=lambda: self.save_as(self.figure, self.file_name)).grid(column=1, row=21, sticky=W)

    #
    for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    #Puts our execute_functions to the return key
    root.bind("<Return>", self.execute_functions)

def execute_functions(self, mainframe, *args):
    """
    """

    ###Getting the user entries###
    station_names_value = self.station_names.get()
    self.station_names_entry_check(station_names_value)

    year_day_value = self.year_day.get()
    self.year_day_entry_check(year_day_value)

    start_hour_value = self.start_hour_entry_check(self.start_hour.get())
    start_minute_value = self.start_minute_entry_check( self.start_minute.get())
    start_second_value = self.start_second_entry_check( self.start_second.get())

    # creating the start time stamp
    start_time_stamp = datetime.time(hour=start_hour_value, minute=start_minute_value, second=start_second_value)

    
    end_hour_value = self.end_hour_entry_check( self.end_hour.get())
    end_minute_value = self.end_minute_entry_check( self.end_minute.get())
    end_second_value = self.end_second_entry_check( self.end_second.get())

    # creating the end time stamp
    end_time_stamp = datetime.time(hour=end_hour_value, minute=end_minute_value, second=end_second_value)

    file_selcetion_value = self.file_selection.get()
    file_ending_value = self.file_format_entry_check(file_selection_value)


    ###Makeing the Plot###
    file_name_full = station_code_value + year_day_value + file_ending_value
    time_interval_string = file_naming.create_time_interval_string_hms(start_hour_value, start_minute_value, start_second_value, end_hour_value, end_minute_value, end_second_value)
    self.file_name = station_code_value + year_day_value + time_interval_string



    try:
        file = open(file_name_full, 'rb')
    except:
        # popping up an error if we can't open the file
        self.error_message_pop_up("File open error", "couldn't find and open your file")

    xArr, yArr, zArr, timeArr = read_raw_to_lists.create_datetime_lists_from_raw(file, start_time_stamp, end_time_stamp, self.file_name)








