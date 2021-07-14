from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
#NavigationToolbar2Tk)

def cancel():
        window.destroy()

# plot function is created for plotting the graph in tkinter window
def plot():

	# the figure that will contain the plot
	fig = Figure(figsize = (5, 5), dpi = 100)

	# list of squares
	y = [i**2 for i in range(101)]

	# adding the subplot
	plot1 = fig.add_subplot(111)

	# plotting the graph
	plot1.plot(y)

	# creating the Tkinter canvas
	# containing the Matplotlib figure
	canvas = FigureCanvasTkAgg(fig, master = window)
	canvas.draw()

	# placing the canvas on the Tkinter window
	canvas.get_tk_widget().grid(column=3, row=2)

	# creating the Matplotlib toolbar
	#toolbar = NavigationToolbar2Tk(canvas, window)
	#toolbar.update()

	# placing the toolbar on the Tkinter window
	#canvas.get_tk_widget().pack()

if __name__ == "__main__" :
    # the main Tkinter window
    window = Tk()

    # setting the title
    window.title('Plotting in Tkinter')

    # dimensions of the main window
    window.geometry("675x550")

    # button that displays the plot
    plot_button = Button(master = window,
                        command = plot,
                        height = 2,
                        width = 10,
                        text = "Plot")
    cancel_button = Button(master=window,
                           command=cancel,
                           height=2,
                           width=10,
                           text="Cancel")
    

    # place the button
    # in main window
    plot_button.grid(column=1, row=1)
    cancel_button.grid(column=2, row=1)

    # run the gui
    window.mainloop()
