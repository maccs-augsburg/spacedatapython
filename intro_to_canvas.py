import matplotlib.pyplot as plt

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

#import matplotlib.pyplot as plt

import sys
import datetime

import one_array_plotted
import read_raw_to_lists
import file_naming


def error_message(title, message) :
    """
     This function creates the error message boxes.

     Parameters
     ----------
     title: to be able to create a title for the error messages

     message: to be able to create the actual message to be displayed in the
              error message pop up.

     """
    messagebox.showerror(title = title, message = "Error: "+ message)


def completed_message(title, message) :
    """
     This function creates the completed message boxes.

     Parameters
     ----------
     title: to be able to create a title for the completed messages

     message: to be able to create the actual message to be displayed in the
              completed message pop up.

     """
    messagebox.showinfo(title, message)

def warning_message(title, message) :
    """
     This function creates the warning message boxes.

     Parameters
     ----------
     title: to be able to create a title for the warning messages

     message: to be able to create the actual message to be displayed in the
              warning message pop up.

     """
    messagebox.showwarning(title = title, message = "Warning: " + message)


def year_day_check(year_day_value):

     """
     This function is set to check if the entry of Year day was inputed. If it was
     not inputed it will send out an error message to let you know.

     Parameters
     ----------
     year_day_value : the integer inputed in the GUI

     Returns
     -------
     error_message : letting you know that there is no input 
     
     """
     if (len(year_day_value) ==  0):
        error_message(title = "yearday Entry Error", message = "There was no input for the yearday entry box")

def start_hour_entry_check(start_hour_value):
     """
     This function checks the start hour entry widget. It checks if the hour
     time is greater then 23 it can not be run. It checks if the time is less then
     zero as well because if it is the program can not run. It also sees if the
     input is set to 1 we have to enter in our own zero in front to run the code.

     Parameter
     ---------
     start_hour_value : the inputed data from the GUI that is an integer between 0 and 23

     Returns
     -------
     start_hour_value : the start hour value as an int
     """
     value = (int)(start_hour_value)
     if(value > 23):
        error_message(title = "Start Hour Entry Error", message = "Start hour cannot be more than 23")

     elif(value < 0):
        error_message(title = "Start Hour Entry Error", message = "Start hour cannot be lower than 0")

     return value

def start_minute_entry_check(start_minute_value):
     """
     This function checks the start minute entry widget. It checks if the minute
     time is greater then 59 it can not be run. It checks if the time is less then
     zero as well because if it is the program can not run. It also sees if the
     input is set to 1 we have to enter in our own zero in front to run the code.

     Parameters
     ----------
     start_minute_value : the inputed value from the GUI that is an integer between 0 and 59. 

     Returns
     -------
     start_minute_value :  the start minute value as an int
     """
     value = (int)(start_minute_value)
     if(value > 59):
        error_message(title = "Start Minute Entry Error", message = "Start minute cannot be greater then 59")

     elif(value < 0):
        error_message(title = "Start Minute Entry Error", message = "Start minute cannot be lower then 0")

     return value

def start_second_entry_check(start_second_value):
     """
     This function checks the start second entry widget. It checks if the second
     time is greater then 59 it can not be run. It checks if the time is less then
     zero as well because if it is the program can not run. It also sees if the
     input is set to 1 we have to enter in our own zero in front to run the code.

     Parameters
     ----------
     start_second_value : the inputed value from the GUI that is an integer between 0 and 59. 

     Returns
     -------
     start_second_value : the start second value as an int
     """
     value = (int)(start_second_value)
     if(value > 59):
        error_message(title = "Start Second Entry Error", message = "Start second cannot be more then 59")

     elif(value < 0):
        error_message(title = "Start Second Entry Error", message = "Start second cannot be negative")

     return value

def end_hour_entry_check(end_hour_value):
     """
     This function checks the end hour entry widget. It checks if the hour
     time is greater then 23 it can not be run. It checks if the time is less then
     zero as well because if it is the program can not run. It also sees if the
     input is set to 1 we have to enter in our own zero in front to run the code.

     Parameters
     ----------
     end_hour_value : the inputed value from the GUI that is an integer between 0 and 23. 

     Returns
     -------
     end_hour_value : the end hour value as an int
     """
     
     value = (int)(end_hour_value)
     if(value > 23):
        error_message(title = "End Hour Entry Error", message = "End hour cannot be more then 23")

     elif(value < 0):
        error_message(title = "End Hour Entry Error", message = "End hour cannor be less then 0")

     return value

def end_minute_entry_check(end_minute_value):
     """
     This function checks the end minute entry widget. It checks if the minute
     time is greater then 59 it can not be run. It checks if the time is less then
     zero as well because if it is the program can not run. It also sees if the
     input is set to 1 we have to enter in our own zero in front to run the code.

     Parameters
     ----------
     end_minute_value : the inputed value from the GUI that is an integer between 0 and 59. 

     Returns
     -------
     end_minute_value : the end minute value as an int
     """
     value = (int)(end_minute_value)
     if(value > 59):
        error_message(title = "End Minute Entry Error", message = "End minute cannot be more then 59")

     elif(value < 0):
        error_message(title = "End Minute Entry Error", message = "End minute cannor be less then 0")

     return value

def end_second_entry_check(end_second_value):
     """
     This function checks the end second entry widget. It checks if the second
     time is greater then 59 it can not be run. It checks if the time is less then
     zero as well because if it is the program can not run. It also sees if the
     input is set to 1 we have to enter in our own zero in front to run the code.

     Parameters
     ----------
     end_second_value : the inputed value from the GUI that is an integer between 0 and 59. 

     Returns
     -------
     end_second_value : the end second value as an int
     """
     value = (int)(end_second_value)
        
     if(value > 59):
        error_message(title = "End Second Entry Error", message = "End second cannot be more then 59")

     elif(value< 0):
        error_message(title = "End Minute Entry Error", message = "End second cannor be less then 0")

     return value


def station_names_entry_check(station_names_value):
     """
     Checks to see if there has been a value put into the entry boxs for station name
     if there hasnt been it gives an error message.

     Parameters
     ----------
     station_names_value : the inputed value from the GUI that is a two letter string

     Returns
     -------
     """
     if(len(station_names_value) == 0):
        error_message(title = "Station Code Entry Error", message = "There was no input for the station code entry box")

def file_format_entry_check(file_selection_value):
    """
    sets the correct file ending value based on the file selection value

    Parameters
    ----------
    file_selection_value : the value of the type of file to select

    Returns
    -------
    file_ending_value : the value of the ending value of the file
    """
    if(file_selection_value == '1'):
        # CDA-Web branch (NOT IMPLEMENTED)
        warning_message(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

    # Testing to see if user selected IAGA2000 branch
    elif(file_selection_value == '2'):
        #IAGA2000 branch (NOT IMPLEMENTED)
        warning_message(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

    # Testing to see if user selected IAGA2002 branch
    elif(file_selection_value == '3'):
        #IAGA2002 branch (NOT IMPLEMENTED)
        warning_message(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

    # Testing to see if user selected Raw 2hz branch
    elif(file_selection_value == '4'):
        #Raw 2hz file branch (TODO: IMPLEMENT SECTION)
        file_ending_value = '.2hz'

    elif(file_selection_value == '5'):
        #Raw 2hz file branch (TODO: IMPLEMENT SECTION)
        file_ending_value = '.s2'

    # Otherwise we can assume that no option had been selected
    else:
        # Message box error when no file format option has been selected
        error_message(title="File format option error", message="Please select a file format option")

    # Returning the string of the file type to be used
    return file_ending_value






def graph_from_plotter_entry_check(graph_from_plotter_value_x,graph_from_plotter_value_y, graph_from_plotter_value_z, xArr, yArr, zArr, timeArr, one_array_plotted, filename, stime, etime, file_option):

     """
     Checks the radio button input to then produce either the X, Y or Z graph.

     Parameters
     ----------
     graph_from_plotter_value :

     xArr :

     yArr :

     zArr :

     timeArr :

     stime :

     etime :

     filename :

     file_option :

     raw_to_single_plot

     Returns
     -------
     graph_from_plotter_value : 

     
     """
     #If statement to decided if we want X, Y or Z plot
     
     #X,Y and Z Plot
     if(graph_from_plotter_value_x == 1 and graph_from_plotter_value_y ==2 and graph_from_plotter_value_z == 3):
         fig = one_array_plotted.x_y_and_z_plot(xArr, yArr, zArr, timeArr, filename, stime, etime, file_option)
    #Y and Z plot
     elif(graph_from_plotter_value_y == 2 and graph_from_plotter_value_z == 3):
         fig = one_array_plotted.y_and_z_plot(yArr, zArr, timeArr, filename, stime, etime, file_option)
    #X and Z plot 
     elif(graph_from_plotter_value_x == 1 and graph_from_plotter_value_z == 3):
         fig = one_array_plotted.x_and_z_plot(xArr,zArr, timeArr, filename, stime, etime, file_option)
    #X and Y plot
     elif(graph_from_plotter_value_x == 1 and graph_from_plotter_value_y == 2):
         fig = one_array_plotted.x_and_y_plot(xArr, yArr, timeArr, filename, stime, etime, file_option)
    #Z plot
     elif(graph_from_plotter_value_z == 3):
         fig = one_array_plotted.z_plot(zArr, timeArr, filename, stime, etime, file_option)     
    #Y plot
     elif(graph_from_plotter_value_y == 2):
         fig = one_array_plotted.y_plot(yArr, timeArr, filename, stime, etime, file_option)
    #X plot
     elif(graph_from_plotter_value_x == 1):
         fig = one_array_plotted.x_plot(xArr, timeArr, filename, stime, etime, file_option)
                  
    #Warning Message
     else:
         warning_message(title = "File Format Option Error", message = "Please select a file format option")

    #eturn graph_from_plotter_value_x, graph_from_plotter_value_y, graph_from_plotter_value_z, fig
     return fig    






# plot function is created for plotting the graph in tkinter window
def plot():

    
    # the figure that will contain the plot
    #fig = plt.figure(figsize = (5, 5), dpi = 100)

    # list of squares
    #y = [i**2 for i in range(101)]

    #Here we call for out input and then runs through our year day check 
    year_day_value = year_day_entry.get()
    year_day_check(year_day_value)

    #here we call for our input and then runs through our start hour, start minut and start second check
    start_hour_value = start_hour_entry_check(start_hour_entry.get())
    #start_hour_value = date_time_object_check(start_hour_value)

    start_minute_value = start_minute_entry_check(start_minute_entry.get())
    #start_minute_value = date_time_object_check(start_minute_value)
     
    start_second_value = start_second_entry_check(start_second_entry.get())
    #start_second_value = date_time_object_check(start_second_value)

     
    start_time_stamp = datetime.time(hour = start_hour_value, minute = start_minute_value, second =  start_second_value)

    #Here we call for our input and then run it through our end hour, end minute and end second check
    end_hour_value = end_hour_entry_check(end_hour_entry.get())
    #end_hour_value = date_time_object_check(end_hour_value)
     
    end_minute_value = end_minute_entry_check(end_minute_entry.get())
    #end_minute_value = date_time_object_check(end_minute_value)
     
    end_second_value = end_second_entry_check(end_second_entry.get())
    #end_second_value = date_time_object_check(end_second_value)

     
    end_time_stamp = datetime.time(hour = end_hour_value, minute = end_minute_value, second = end_second_value)
    #Here we call for our input and then run it through our station names check. 
    station_names_value = station_names_entry.get()
    station_names_entry_check(station_names_value)

    file_selection_value = file_selection.get()
    file_ending_value = file_format_entry_check(file_selection_value)

    file_name_full = station_names_value + year_day_value + file_ending_value
    time_interval_string = file_naming.create_time_interval_string_hms(start_hour_value,start_minute_value, start_second_value, end_hour_value, end_minute_value, end_second_value) 
    file_name = station_names_value + year_day_value + time_interval_string 

    #This opens our said file
    try:
        file = open(file_name_full, 'rb')
    except:
        error_message("File open error", "Couldn't find and open filename")
        sys.exit(0)
    

    file_option = "pdf"
     
    #Creates our arrays
    xArr, yArr, zArr, timeArr = read_raw_to_lists.create_lists_from_raw(file, start_time_stamp, end_time_stamp)   
    #This calls our graph plotter function to plot the chose graph
    graph_from_plotter_value_x = graph_from_plotter_x.get()
    graph_from_plotter_value_y = graph_from_plotter_y.get()
    graph_from_plotter_value_z = graph_from_plotter_z.get() 

    fig = graph_from_plotter_entry_check(graph_from_plotter_value_x,graph_from_plotter_value_y, graph_from_plotter_value_z, xArr, yArr, zArr, timeArr, one_array_plotted, file_name, start_time_stamp, end_time_stamp, file_option) #update params


    


    
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = window)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(column = 5, row = 5, columnspan = 5, rowspan = 20, padx = 15, pady = 10, sticky = (N, W, E, S))
    

    
    # creating the Matplotlib toolbar
    toolbar_frame = Frame(window)
    toolbar_frame.grid(row = 25, column = 1, sticky = (W))
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    #toolbar.update()

    # placing the toolbar on the Tkinter window
    #canvas.get_tk_widget().grid(column = 3, row = 22, sticky = (N, W, E, S))

def gui_entries(window) :
    """
    """

    global year_day_entry
    global start_hour, start_hour_entry, start_minute, start_minute_entry, start_second, start_second_entry
    global end_hour, end_hour_entry,end_minute,  end_minute_entry, end_second, end_second_entry
    global station_names_entry
    global graph_from_plotter_x,graph_from_plotter_y,graph_from_plotter_z, x_plot, y_plot, z_plot
    global okay_button, cancel_button
    global file_selection, cda_web, iaga_00, iaga_02, raw_hz_file
    
    #Creation of the Year Day entry widget
    year_day = IntVar()
    year_day_entry = ttk.Entry(window, width= 5, textvariable = year_day)
    year_day_entry.grid(column = 2, row = 2,   sticky = W)
    
    #Creation of the Start Hour entry widget 
    start_hour = IntVar()
    start_hour_entry = ttk.Entry(window, width = 5, textvariable = start_hour)
    start_hour_entry.grid(column = 2, row = 3, sticky = W)

    #Creation of the Start Minute entry widget
    start_minute = IntVar()
    start_minute_entry = ttk.Entry(window, width = 5, textvariable = start_minute)
    start_minute_entry.grid(column = 2, row = 4, sticky = W)

    #Creation of the Start Second entry widget 
    start_second = IntVar()
    start_second_entry = ttk.Entry(window, width = 5, textvariable = start_second)
    start_second_entry.grid(column = 2, row = 5,sticky = W)

    #Creation of the end hour entry widget, also has set times for defalut
    end_hour = IntVar()
    end_hour_entry = ttk.Entry(window, width = 5, textvariable = end_hour)
    end_hour_entry.grid(column = 2, row = 6, sticky = W)
    end_hour.set(23)

    #Creation of the end minute entry widget, also has set times for default
    end_minute = IntVar()
    end_minute_entry = ttk.Entry(window, width = 5, textvariable = end_minute)
    end_minute_entry.grid(column = 2, row = 7, sticky = W)
    end_minute.set(59)

    #Creation of the end second widget, also has set times for default
    end_second = IntVar()
    end_second_entry = ttk.Entry(window, width = 5, textvariable = end_second)
    end_second_entry.grid(column = 2, row = 8, sticky = W)
    end_second.set(59)

    #Creation of the station names entry widget
    station_names= StringVar()
    station_names_entry = ttk.Entry(window, width = 5, textvariable = station_names)
    station_names_entry.grid(column = 2, row = 1, pady = (25, 0), sticky = W)

    #Creation of the graph from plotter check button
    graph_from_plotter_x = IntVar()
    graph_from_plotter_y = IntVar()
    graph_from_plotter_z = IntVar()
    x_plot = ttk.Checkbutton(window, text = "X Plot", variable = graph_from_plotter_x, onvalue = 1).grid(column = 2, row = 10,padx = 25 , sticky = W)
    y_plot = ttk.Checkbutton(window, text = "Y Plot", variable = graph_from_plotter_y, onvalue = 2).grid(column = 2, row = 11,padx = 25 , sticky = W) 
    z_plot = ttk.Checkbutton(window, text = "Z Plot", variable = graph_from_plotter_z, onvalue = 3).grid(column = 2, row = 12,padx = 25 , sticky = W)

    #Creation of the File options of the data being graphed
    file_selection = StringVar()
    cda_web = Radiobutton(window, text = "CDAWEB:NA", value = 1, variable = file_selection).grid(column = 2, row = 15, padx = 25,  sticky = W)
    iaga_00 = Radiobutton(window, text = "IAGA2000:NA", value = 2, variable = file_selection).grid(column = 2, row = 16, padx = 25,  sticky = W)
    iaga_02 = Radiobutton(window, text =     "IAGA2002:NA", value = 3, variable = file_selection).grid(column = 2, row = 17, padx = 25, sticky = W)
    raw_hz_file = Radiobutton(window, text = "Raw 2hz file", value = 4, variable = file_selection).grid(column = 2, row = 18, padx = 25,  sticky = W)
    clean_data = Radiobutton(window, text = "Clean Data", value = 5, variable = file_selection).grid(column = 2, row = 19, padx = 25, sticky = W)


    
    #Creation of the Okay and Cancel button that has commands to either run
    #the GUI if you press okay or to "destroy" the GUI if you hit canel
    plot_button = ttk.Button(window, text = "Plot", command = plot).grid(column = 2, row = 20,  sticky = W)
    cancel_button = ttk.Button(window, text = "Cancel", command = lambda: cancel(window)).grid(column =1, row = 20, padx = 25, sticky = W)



def gui_labels(window) :
    """
    """
    #Year Day Label
    ttk.Label(window, text = "Year Day: ").grid(column = 1, row = 2,  sticky = E)
    #Start Hour Label 
    ttk.Label(window, text = "Start Hour: ").grid(column = 1, row = 3, sticky = E)
    #Start Minute Label 
    ttk.Label(window, text = "Start Minute: ").grid(column = 1, row = 4,sticky = E)
    #Start Second Label 
    ttk.Label(window, text = "Start Second: ").grid(column = 1, row = 5, sticky = E)
    #End Hour Label 
    ttk.Label(window, text = "End Hour: ").grid(column = 1, row = 6, sticky = E)
    #End Minute Label 
    ttk.Label(window, text = "End Minute: ").grid(column = 1, row = 7, sticky = E)
    #End Second Label 
    ttk.Label(window, text = "End Second: ").grid(column = 1, row = 8, sticky = E)
    #Plot x, y, or z Label 
    ttk.Label(window, text = "Plot X, Y or Z: ").grid(column = 1, row = 9, sticky = E)
    #Station Code Label 
    ttk.Label(window, text = "Station Code: ").grid(column = 1, row = 1, pady = (25, 0), sticky = E)
    #File Option Label
    ttk.Label(window, text = "File Option: ").grid(column = 1, row = 14, sticky = E)
    
def cancel(window):
    
    """

    Parameters
    ----------
    *args : 
    """
    window.destroy()


def main() :
    """
    """
    # the main Tkinter window
    global window
    window = Tk()
    
    file_option = "pdf"

    # setting the title
    window.title('Single Graph Plotter')

    # dimensions of the main window
    window.geometry("1500x600")

    #Color the window so all systems are the same
    window.configure(bg = 'grey95')

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

