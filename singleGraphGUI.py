#Single Graph GUI
#Annabelle Arns 

from tkinter import *
from tkinter import ttk

def GUI_labels():

    ttk.Label(mainframe, text = "Start Hour: ").grid(column = 1, row = 1, sticky = W)

    ttk.Label(mainframe, text = "Start Minute: ").grid(column = 3, row = 1, sticky = W)

    ttk.Label(mainframe, text = "Start Second: ").grid(column = 1, row = 2, sticky = W)

    ttk.Label(mainframe, text = "End Hour: ").grid(column = 1, row = 3, sticky = W)

    ttk.Label(mainframe, text = "End Minute: ").grid(column = 3, row = 3, sticky = W)

    ttk.Label(mainframe, text = "End Second: ").grid(column = 1, row = 4, sticky = W)

    ttk.Label(mainframe, text = "Plot X, Y or Z: ").grid(column = 1, row = 5, sticky = W)  


def GUI_entries():
    



def child_formatting(mainframe):





def main(root, mainframe):

    













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




    
    
    
