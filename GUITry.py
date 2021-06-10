#First GUI Try
#Annabelle 

from tkinter import *
from tkinter import ttk

#Main Application Frame
root = Tk()
root.title("Lineplot INPUT")

#Content Frame
mainframe = ttk.Frame(root, padding= "200 200 120 120")
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
root.columnconfigure(0, weight= 1)
root.rowconfigure(0, weight = 1)


#Creating Entry Widget

start_Hour = StringVar()
start_Hour_entry = ttk.Entry(mainframe, width = 5, textvariable = "Start Hour")
start_Hour_entry.grid(column = 1, row = 1, sticky = (W, E))

start_Minute =StringVar()
start_Minute_entry = ttk.Entry(mainframe, width = 5, textvariable = "Start Minute")
start_Minute_entry.grid(column = 1, row = 2, sticky = (W, E))


start_Second =StringVar()
start_Second_entry = ttk.Entry(mainframe, width = 5, textvariable = "Start Second")
start_Second_entry.grid(column = 2, row = 1, sticky = (W, E))


end_Hour = StringVar()
end_Hour_entry = ttk.Entry(mainframe, width = 5, textvariable = "End Hour")
end_Hour_entry.grid(column = 3, row = 1, sticky = (W,E))


end_Minute = StringVar()
end_Minute_entry = ttk.Entry(mainframe, width = 5, textvariable = "End Minute")
end_Minute_entry.grid(column = 3, row = 2, sticky = (W,E))

end_Second =StringVar()
end_Second_entry = ttk.Entry(mainframe, width = 5, textvariable = "End Second")
end_Second_entry.grid(column = 4, row = 1, sticky = (W,E))

#Creating the Radio Buttons Widgets

#File Types
file_type = StringVar()
asci = ttk.Radiobutton(mainframe, text = "Asci", variable = file_type, value = "asci")
raw_Binary = ttk.Radiobutton(mainframe, text = "Raw Binary", variable = file_type, value = "raw binary")
clean_Binary =ttk.Radiobutton(mainframe, text = "Clean Binary", variable = file_type, value = "clean binary")


#Files
file = StringVar()
single_File = ttk.Radiobutton(mainframe, text = "Single File", variable = file, value = "single file")
multiple_Files = ttk.Radiobutton(mainframe, text = "Multiple Files", variable = file, value = "multiple files")


#Sequential Plots
sequential_Plots = StringVar()
yes_Plots =ttk.Radiobutton(mainframe, text = "Yes", variable = sequential_Plots, value = "yes plots")
no_Plots = ttk.Radiobutton(mainframe, text = "No", variable = sequential_Plots, value = "no plots")


#Postscripts
postScripts = StringVar()
yes_Scripts = ttk.Radiobutton(mainframe, text = "Yes", variable = postScripts, value = "yes scripts")
no_Scripts = ttk.Radiobutton(mainframe, text = "No", variable = postScripts, value = "no scripts")

#The Okay and Cancel Buttons
#okay_button = ttk.Button(mainframe, text = "Okay", command = submitForm)
#cancel_button = ttk.Button(mainframe, text = "Cancel", command = submitForm)

root.mainloop()



