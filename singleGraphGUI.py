#Single Graph GUI
#Annabelle Arns 

from tkinter import *
from tkinter import ttk

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




    
    
    
