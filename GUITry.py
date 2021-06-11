#First GUI Try
#Annabelle 

from tkinter import *
from tkinter import ttk

#Main Application Frame
root = Tk()
root.title("Lineplot INPUT")

#Content Frame
mainframe = ttk.Frame(root, padding= "3 3 12 12")
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
root.columnconfigure(0, weight= 1)
root.rowconfigure(0, weight = 1)


#Creating Entry Widget


ttk.Label(mainframe, text = "Start Hour: ").grid(column = 1, row = 1, sticky = W)
start_Hour = IntVar()
start_Hour_entry = ttk.Entry(mainframe, width = 5, textvariable = start_Hour)
start_Hour_entry.grid(column = 2, row = 1)

ttk.Label(mainframe, text = "Start Minute: ").grid(column = 3, row = 1, sticky = W)
start_Minute = IntVar()
start_Minute_entry = ttk.Entry(mainframe, width = 5, textvariable = start_Minute)
start_Minute_entry.grid(column = 4, row = 1, sticky = (W, E))

ttk.Label(mainframe, text = "Start Second: ").grid(column = 1, row = 2, sticky = W)
start_Second = IntVar()
start_Second_entry = ttk.Entry(mainframe, width = 5, textvariable = start_Second)
start_Second_entry.grid(column = 2, row = 2, sticky = (W, E))

ttk.Label(mainframe, text = "End Hour: ").grid(column = 1, row = 3, sticky = W)
end_Hour = IntVar()
end_Hour_entry = ttk.Entry(mainframe, width = 5, textvariable = end_Hour)
end_Hour_entry.grid(column = 2, row = 3, sticky = (W,E))

ttk.Label(mainframe, text = "End Minute: ").grid(column = 3, row = 3, sticky = W)
end_Minute = IntVar()
end_Minute_entry = ttk.Entry(mainframe, width = 5, textvariable = end_Minute)
end_Minute_entry.grid(column = 4, row = 3, sticky = (W,E))

ttk.Label(mainframe, text = "End Second: ").grid(column = 1, row = 4, sticky = W)
end_Second = IntVar()
end_Second_entry = ttk.Entry(mainframe, width = 5, textvariable = end_Second)
end_Second_entry.grid(column = 2, row = 4, sticky = (W,E))

#Creating the Radio Buttons Widgets

#File Types
ttk.Label(mainframe, text = "File Types").grid(column = 1, row = 5, sticky = W)
file_type = StringVar()
asci = ttk.Radiobutton(mainframe, text = "Asci", variable = file_type, value = "asci").grid(column = 1, row = 6, sticky = W)
raw_Binary = ttk.Radiobutton(mainframe, text = "Raw Binary", variable = file_type, value = "raw binary").grid(column = 1, row = 7, sticky = W) 
clean_Binary =ttk.Radiobutton(mainframe, text = "Clean Binary", variable = file_type, value = "clean binary").grid(column = 1, row = 8, sticky = W)


#Files
ttk.Label(mainframe, text = "Files").grid(column = 3, row = 5, sticky = W)
file = StringVar()
single_File = ttk.Radiobutton(mainframe, text = "Single File", variable = file, value = "single file").grid(column =3, row = 6, sticky = W) 
multiple_Files = ttk.Radiobutton(mainframe, text = "Multiple Files", variable = file, value = "multiple files").grid(column = 3, row = 7, sticky = W)


#Sequential Plots
ttk.Label(mainframe, text = "Sequential Plots").grid(column = 5, row = 5, sticky = W)
sequential_Plots = StringVar()
yes_Plots =ttk.Radiobutton(mainframe, text = "Yes", variable = sequential_Plots, value = "yes plots").grid(column = 5, row = 6, sticky = W)
no_Plots = ttk.Radiobutton(mainframe, text = "No", variable = sequential_Plots, value = "no plots").grid(column = 5, row = 7, sticky = W)


#Postscripts
ttk.Label(mainframe, text = "Postscripts").grid(column = 8, row = 5, sticky = W)
postScripts = StringVar()
yes_Scripts = ttk.Radiobutton(mainframe, text = "Yes", variable = postScripts, value = "yes scripts").grid(column = 8, row = 6, sticky = W)
no_Scripts = ttk.Radiobutton(mainframe, text = "No", variable = postScripts, value = "no scripts").grid(column = 8, row = 7, sticky = W)

#The Okay and Cancel Buttons

okay_button = ttk.Button(mainframe, text = "Okay").grid(column = 5, row = 8, sticky = W)
cancel_button = ttk.Button(mainframe, text = "Cancel").grid(column =8, row = 8, sticky = W) 


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()



