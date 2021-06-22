#Single Graph GUI
#Annabelle Arns 


#Imports from tkinter to be able to run 
from tkinter import *
from tkinter import ttk

#Import from tkinter to display error messages or warning messages
from tkinter import messagebox


import sys
import datetime

#To be able to import another file to be ran in the GUI 
#import importlib

import oneArrayPlotted


#The code to import the file oneArrayPlotted 
#raw_to_single_plot = importlib.import_module('oneArrayPlotted')


#Function to run the error message pop ups that are created later on in the file
def error_message(title, message):
     """
     This function creates the error message boxes.

     Parameters
     ----------
     title: to be able to create a title for the error messages

     message: to be able to create the actual message to be displayed in the
              error message pop up.

     Returns
     -------

     Exits the program? 
     """
     
     messagebox.showerror(title = title, message = "ERROR: " + message)
     sys.exit(0)


def GUI_labels():
     """
     This funtion is created to be able to label all of our entry boxes in the GUI.

     """

     #Year Day Label
     ttk.Label(mainframe, text = "Year Day: ").grid(column = 1, row = 1, sticky = W)
     #Start Hour Label 
     ttk.Label(mainframe, text = "Start Hour: ").grid(column = 1, row = 2, sticky = W)
     #Start Minute Label 
     ttk.Label(mainframe, text = "Start Minute: ").grid(column = 3, row = 2, sticky = W)
     #Start Second Label 
     ttk.Label(mainframe, text = "Start Second: ").grid(column = 1, row = 3, sticky = W)
     #End Hour Label 
     ttk.Label(mainframe, text = "End Hour: ").grid(column = 1, row = 4, sticky = W)
     #End Minute Label 
     ttk.Label(mainframe, text = "End Minute: ").grid(column = 3, row = 4, sticky = W)
     #End Second Label 
     ttk.Label(mainframe, text = "End Second: ").grid(column = 1, row = 5, sticky = W)
     #Plot x, y, or z Label 
     ttk.Label(mainframe, text = "Plot X, Y or Z: ").grid(column = 1, row = 7, sticky = W)
     #Station Code Label 
     ttk.Label(mainframe, text = "Station Code: ").grid(column = 1, row = 6, sticky = W)


     #Will add png or pdf label (radio buttons)
     #Will add x and y, x and z or y and z label(Radio buttons)

def GUI_entries():

     """
     This funtion is to create all of the entry boxes themselves. In this function we had
     to create the variables into global variables to be able to run the GUI in a funtion.  
     """

     global year_day_entry
     global start_hour, start_hour_entry, start_minute, start_minute_entry, start_second, start_second_entry
     global end_hour, end_hour_entry,end_minute,  end_minute_entry, end_second, end_second_entry
     global station_names_entry
     global graph_from_plotter, x_plot, y_plot, z_plot
     global okay_button, cancel_button

     #Creation of the Year Day entry widget 
     year_day = IntVar()
     year_day_entry = ttk.Entry(mainframe, width = 5, textvariable = year_day)
     year_day_entry.grid(column = 2, row = 1)
     #Creation of the Start Hour entry widget 
     start_hour = IntVar()
     start_hour_entry = ttk.Entry(mainframe, width = 5, textvariable = start_hour)
     start_hour_entry.grid(column = 2, row = 2)
     #Creation of the Start Minute entry widget
     start_minute = IntVar()
     start_minute_entry = ttk.Entry(mainframe, width = 5, textvariable = start_minute)
     start_minute_entry.grid(column = 4, row = 2, sticky = (W, E))
     #Creation of the Start Second entry widget 
     start_second = IntVar()
     start_second_entry = ttk.Entry(mainframe, width = 5, textvariable = start_second)
     start_second_entry.grid(column = 2, row = 3, sticky = (W, E))
     #Creation of the end hour entry widget, also has set times for defalut
     end_hour = IntVar()
     end_hour_entry = ttk.Entry(mainframe, width = 5, textvariable = end_hour)
     end_hour_entry.grid(column = 2, row = 4, sticky = (W,E))
     end_hour.set(23)
     #Creation of the end minute entry widget, also has set times for default
     end_minute = IntVar()
     end_minute_entry = ttk.Entry(mainframe, width = 5, textvariable = end_minute)
     end_minute_entry.grid(column = 4, row = 4, sticky = (W,E))
     end_minute.set(59)
     #Creation of the end second widget, also has set times for default
     end_second = IntVar()
     end_second_entry = ttk.Entry(mainframe, width = 5, textvariable = end_second)
     end_second_entry.grid(column = 2, row = 5, sticky = (W,E))
     end_second.set(59)
     #Creation of the station names entry widget
     station_names= StringVar()
     station_names_entry = ttk.Entry(mainframe, width = 5, textvariable = station_names)
     station_names_entry.grid(column = 2, row = 6, sticky = (W,E))
     #Creation of the graph from plotter radio button
     graph_from_plotter = StringVar()
     x_plot = ttk.Radiobutton(mainframe, text = "X Plot", variable = graph_from_plotter, value = "x plot").grid(column = 1, row = 8, sticky = W)
     y_plot = ttk.Radiobutton(mainframe, text = "Y Plot", variable = graph_from_plotter, value = "y plot").grid(column = 1, row = 9, sticky = W) 
     z_plot =ttk.Radiobutton(mainframe, text = "Z Plot", variable = graph_from_plotter, value = "z plot").grid(column = 1, row = 10, sticky = W)
     #Creation of the Okay and Cancel button that has commands to either run
     #the GUI if you press okay or to "destroy" the GUI if you hit canel
     okay_button = ttk.Button(mainframe, text = "Okay", command = run_GUI).grid(column = 3, row = 10, sticky = W)
     cancel_button = ttk.Button(mainframe, text = "Cancel", command = cancel).grid(column =4, row = 10, sticky = W)

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
     

     start_hour_value :      
     """
     if(len(start_hour_value) == 1):
        start_hour_value = "0" + start_hour_value

     if((int)(start_hour_value) > 23):
        error_message(title = "Start Hour Entry Error", message = "Start hour cannot be more than 23")

     elif((int)(start_hour_value) < 0):
        error_message(title = "Start Hour Entry Error", message = "Start hour cannot be lower than 0")

     return start_hour_value    
        
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
     start_minute_value : 
     """
     if(len(start_minute_value) == 1):
        start_minute_value = "0" + start_minute_value

     if((int)(start_minute_value) > 59):
        error_message(title = "Start Minute Entry Error", message = "Start minute cannot be greater then 59")

     elif((int)(start_minute_value) < 0):
        error_message(title = "Start Minute Entry Error", message = "Start minute cannot be lower then 0")

     return start_minute_value


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
     start_second_value : 
     """

     if(len(start_second_value) == 1):
        start_second_value = "0" + start_second_value

     if((int)(start_second_value) > 59):
        error_message(title = "Start Second Entry Error", message = "Start second cannot be more then 59")

     elif((int)(start_second_value) < 0):
        error_message(title = "Start Second Entry Error", message = "Start second cannot be negative")

     return start_second_value

def start_time_entry_check(start_hour_value, start_minute_value, start_second_value):
     """
     """

     start_hour_value = start_hour_entry_check(start_hour_value)
     start_minute_value = start_minute_entry_check(start_minute_value)
     start_second_value = start_second_entry_check(start_second_value)

     return start_hour_value, start_minute_value, start_second_value


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
     end_hour_value : 
     """
     
     if(len(end_hour_value) == 1):
        end_hour_value = "0" + end_hour_value

     if((int)(end_hour_value) > 23):
        error_message(title = "End Hour Entry Error", message = "End hour cannot be more then 23")

     elif((int)(end_hour_value)< 0):
        error_message(title = "End Hour Entry Error", message = "End hour cannor be less then 0")

     return end_hour_value


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
     end_minute_value : 
     """
     if(len(end_minute_value) == 1):
        end_minute_value = "0" + end_minute_value
        
     if((int)(end_minute_value) > 59):
        error_message(title = "End Minute Entry Error", message = "End minute cannot be more then 59")

     elif((int)(end_minute_value)< 0):
        error_message(title = "End Minute Entry Error", message = "End minute cannor be less then 0")

     return end_minute_value

        
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
     end_second_value : 
     """
     if(len(end_second_value) == 1):
        end_second_value = "0" + end_second_value
        
     if((int)(end_second_value) > 59):
        error_message(title = "End Second Entry Error", message = "End second cannot be more then 59")

     elif((int)(end_second_value)< 0):
        error_message(title = "End Minute Entry Error", message = "End second cannor be less then 0")

     return end_second_value
 
def end_time_entry_check(end_hour_value, end_minute_value, end_second_value):
     """
     """
     end_hour_value = end_hour_entry_check(end_hour_value)
     end_minute_value = end_minute_entry_check(end_minute_value)
     end_second_value = end_second_entry_check(end_second_value)

     return end_hour_value, end_minute_value, end_second_value

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

def graph_from_plotter_entry_check(graph_from_plotter_value, xArr, yArr, zArr, timeArr, oneArrayPlotted, filename, stime, etime, file_option):
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
     if(graph_from_plotter_value == "x plot"):
          oneArrayPlotted.x_plot(xArr, timeArr, filename, stime, etime, file_option)
     elif(graph_from_plotter_value == "y plot"):
          oneArrayPlotted.y_plot(yArr, timeArr, filename, stime, etime, file_option)
     elif(graph_from_plotter_value == "z plot"):
          oneArrayPlotted.z_plot(zArr, timeArr, filename, stime, etime, file_option)
     else:
          warning_message(title = "File Format Option Error", message = "Please select a file format option")

     return graph_from_plotter_value 

def run_GUI(*args):
     """
     This funtion is esentially our main. We run everything we have created above
     into this function to implement it.

     Parameters
     ----------
     *args :

     Returns :
     
     """

     #Here we call for out input and then runs through our year day check 
     year_day_value = year_day_entry.get()
     year_day_check(year_day_value)
     #here we call for our input and then runs through our start hour, start minut and start second check
     start_hour_value = start_hour_entry.get()
     start_minute_value = start_minute_entry.get()
     start_second_value = start_second_entry.get()

     start_hour_value, start_minute_value, start_second_value = start_time_entry_check(start_hour_value, start_minute_value, start_second_value)
     start_time_stamp = datetime.time.fromisoformat(start_hour_value + ":" + start_minute_value + ":" + start_second_value)
     #Here we call for our input and then run it through our end hour, end minute and end second check
     end_hour_value = end_hour_entry.get()
     end_minute_value = end_minute_entry.get()
     end_second_value = end_second_entry.get()


     end_hour_value, end_minute_value, end_second_value = end_time_entry_check(end_hour_value, end_minute_value, end_second_value)
     end_time_stamp = datetime.time.fromisoformat(end_hour_value + ":" + end_minute_value + ":" + end_second_value)
     #Here we call for our input and then run it through our station names check. 
     station_names_value = station_names_entry.get()
     station_names_entry_check(station_names_value)

     #Creating a file name to be found in our file explorer to run through our plotter
     file_name = station_names_value + year_day_value + '.2hz'
     #The out put of our file as of right now is just a pdf
     file_option = 'pdf' # Update later
     #This opens our said file
     file = open(file_name, 'rb')
     #Creates our arrays
     xArr, yArr, zArr, timeArr = oneArrayPlotted.create_Arrays(file, start_time_stamp, end_time_stamp)
     #This calls our graph plotter function to plot the chose graph
     graph_from_plotter_value = graph_from_plotter.get()
     graph_from_plotter_value = graph_from_plotter_entry_check(graph_from_plotter_value,  xArr, yArr, zArr, timeArr, oneArrayPlotted, file_name, start_time_stamp, end_time_stamp, file_option) #update params



def cancel(*args):
     """
     For the cancel button to shut down the GUI and plotter when pressed.

     Parameters
     ----------
     *args : 
     """
     root.destroy()

def child_formatting(mainframe):
     """
     """

     for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)



def main(root, mainframe):
     """
     Calls all our our GUI functions to create the gui that is presented.

     Parameters
     ----------
     root :

     mainframe :
     
     """

     GUI_labels()


     GUI_entries()


     child_formatting(mainframe)

     year_day_entry.focus() 
     













if __name__ == "__main__" :

     #Sets up GUI Function 
     root = Tk()
     root.title("Single Graph Plotter")


     mainframe = ttk.Frame(root, padding= "3 3 12 12")
     mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
     root.columnconfigure(0, weight= 1)
     root.rowconfigure(0, weight = 1)

     main(root, mainframe)

     root.mainloop()




    
    
    
