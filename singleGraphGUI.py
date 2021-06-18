#Single Graph GUI
#Annabelle Arns 

from tkinter import *
from tkinter import ttk
from tkinter import messagebox


def error_message(title, message):
     messagebox.showerror(title = title, message = "ERROR: " + message)
     sys.exit(0)
    




def GUI_labels():
    """
    """

    ttk.Label(mainframe, text = "Year Day: ").grid(column = 1, row = 1, sticky = W)
    
    ttk.Label(mainframe, text = "Start Hour: ").grid(column = 1, row = 2, sticky = W)

    ttk.Label(mainframe, text = "Start Minute: ").grid(column = 3, row = 2, sticky = W)

    ttk.Label(mainframe, text = "Start Second: ").grid(column = 1, row = 3, sticky = W)

    ttk.Label(mainframe, text = "End Hour: ").grid(column = 1, row = 4, sticky = W)

    ttk.Label(mainframe, text = "End Minute: ").grid(column = 3, row = 4, sticky = W)

    ttk.Label(mainframe, text = "End Second: ").grid(column = 1, row = 5, sticky = W)

    ttk.Label(mainframe, text = "Plot X, Y or Z: ").grid(column = 1, row = 6, sticky = W)  

    ttk.Label(mainframe, text = "Okay").grid(column = 3, row = 9, sticky = W)

    ttk.Label(mainframe, text = "Cancel").grid(column = 4, row = 9, sticky = W)

def GUI_entries():
    """
    """

    yearday = IntVar()
    yearday_entry = ttk.Entry(mainframe, width = 5, textvariable = yearday)
    yearday_entry.grid(column = 2, row = 1)

    start_Hour = IntVar()
    start_Hour_entry = ttk.Entry(mainframe, width = 5, textvariable = start_Hour)
    start_Hour_entry.grid(column = 2, row = 2)

    start_Minute = IntVar()
    start_Minute_entry = ttk.Entry(mainframe, width = 5, textvariable = start_Minute)
    start_Minute_entry.grid(column = 4, row = 2, sticky = (W, E))

    start_Second = IntVar()
    start_Second_entry = ttk.Entry(mainframe, width = 5, textvariable = start_Second)
    start_Second_entry.grid(column = 2, row = 3, sticky = (W, E))

    end_Hour = IntVar()
    end_Hour_entry = ttk.Entry(mainframe, width = 5, textvariable = end_Hour)
    end_Hour_entry.grid(column = 2, row = 4, sticky = (W,E))

    end_Minute = IntVar()
    end_Minute_entry = ttk.Entry(mainframe, width = 5, textvariable = end_Minute)
    end_Minute_entry.grid(column = 4, row = 4, sticky = (W,E))

    end_Second = IntVar()
    end_Second_entry = ttk.Entry(mainframe, width = 5, textvariable = end_Second)
    end_Second_entry.grid(column = 2, row = 5, sticky = (W,E))

    graph_from_plotter = StringVar()
    x_plot = ttk.Radiobutton(mainframe, text = "X Plot", variable = graph_from_plotter, value = "x_plot").grid(column = 1, row = 7, sticky = W)
    y_plot = ttk.Radiobutton(mainframe, text = "Y Plot", variable = graph_from_plotter, value = "y_plot").grid(column = 1, row = 8, sticky = W) 
    z_plot =ttk.Radiobutton(mainframe, text = "Z Plot", variable = graph_from_plotter, value = "z_plot").grid(column = 1, row = 9, sticky = W)

def yearday_check(year_day_value):
    """
    """
    if (len(yearday) ==  0):
        error_message(title = "yearday Entry Error", message = "There was no input for the yearday entry box")

def start_hour_entry_check(start_hour_value):
    """
    """
    if(len(start_hour_value) == 1):
        start_hour_value = "0" + start_hour_value

    if((int)(start_hour_value) > 23):
        error_message(title = "Start Hour Entry Error", message = "Start hour cannot be more than 23")

    elif((int)(start_hour_value) < 0):
        error_message(title = "Start Hour Entry Error", message = "Start hour cannot be lower than 0")

    return start_hour_value    
        
def start_minute_entry_check(start_minute_value):
    if(len(start_minute_value) == 1):
        start_minute_value = "0" + start_minute_value

    if((int)(start_minute_value) > 59):
        error_message(title = "Start Minute Entry Error", message = "Start minute cannot be greater then 59")

    elif((int)(start_minute_value) < 0):
        error_message(title = "Start Minute Entry Error", message = "Start minute cannot be lower then 0")

    return start_minute_value


def start_second_entry_check(start_second_value):

    if(len(start_second_value) == 1):
        start_second_value = "0" + start_second_value

    if((int)(start_second_value) > 59):
        error_message(title = "Start Second Entry Error", message = "Start second cannot be more then 59")

    elif((int)(start_second_value) < 0):
        error_message(title = "Start Second Entry Error", message = "Start second cannot be negative")

    return start_second_value

def start_time_entry_check(start_hour_value, start_minute_value, start_second_value):


    start_hour_value = start_hour_entry_check(start_hour_value)
    start_minute_value = start_minute_entry_check(start_minute_value)
    start_second_value = start_second_entry_check(start_second_value)

    return start_hour_value, start_minute_value, start_second_value


def end_hour_entry_check(end_hour_value):
    if(len(end_hour_value) == 1):
        end_hour_value = "0" + end_hour_value

    if((int)(end_hour_value) > 23):
        error_message(title = "End Hour Entry Error", message = "End hour cannot be more then 23")

    elif((int)(end_hour_value)< 0):
        error_message(title = "End Hour Entry Error", message = "End hour cannor be less then 0")

    return end_hour_value


def end_minute_entry_check(end_minute_value):
    if(len(end_minute_value) == 1):
        end_minute_value = "0" + end_minute_value
        
    if((int)(end_minute_value) > 59):
        error_message(title = "End Minute Entry Error", message = "End minute cannot be more then 59")

    elif((int)(end_minute_value)< 0):
        error_message(title = "End Minute Entry Error", message = "End minute cannor be less then 0")

    return end_minute_value

        
def end_second_entry_check(end_second_value):
    if(len(end_second_value) == 1):
        end_minute_value = "0" + end_minute_value
        
    if((int)(end_second_value) > 59):
        error_message(title = "End Second Entry Error", message = "End second cannot be more then 59")

    elif((int)(end_second_value)< 0):
        error_message(title = "End Minute Entry Error", message = "End second cannor be less then 0")

    return end_second_value

def end_time_entry_check(end_hour_value, end_minute_value, end_second_value):


    end_hour_value = end_hour_entry_check(end_hour_value)
    end_minute_value = end_minute_entry_check(end_minute_value)
    end_second_value = end_second_entry_check(end_second_value)

    return end_hour_value, end_minute_value, end_second_value


def run_GUI(*args):
    year_day_value = yearday_entry.get()
    yearday_check(yearday_day_value)

    start_hour_value = start_Hour_entry.get()
    start_minute_value = start_Minute_entry.get()
    start_second_value = start_Second_entry.get()

    start_hour_value, start_minute_value, start_second_value = start_time_entry_check(start_hour_vale, start_minute_value, start_second_value)
    start_time_stamp = datetime.timefromisoformat(start_hour_value + ":" + start_minute_value + ":" + start_second_value)

    end_hour_value = end_hour_entry.get()
    end_minute_value = end_minute_entry.get()
    end_second_value = end_second_entry.get()

    
    end_hour_value, end_minute_value, end_second_value = end_time_entry_check(end_hour_value, end_minute_value, end_second_value)
    end_time_stamp = datetime.time.fromisoformat(end_hour_value + ":" + end_minute_value + ":" + end_second_value)




def child_formatting(mainframe):
    """
    """

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)



def main(root, mainframe):

    GUI_labels()
    
    
    GUI_entries()
    
    
    child_formatting(mainframe)

    #year_day_entry.focus() 
    #root.bind("<Return>", run_GUI)













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




    
    
    
