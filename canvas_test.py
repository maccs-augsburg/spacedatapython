from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
#NavigationToolbar2Tk)

# cancel function for closing window
def cancel():
        window.destroy()

def initialize_test_arrays():
        test_arr_1 = [1, 2, 3, 4, 5]
        test_arr_2 = [5, 4, 3, 2, 1]
        test_arr_3 = [1, 3, 2, 4, 5]
        time_arr = [1, 2, 3, 4, 5]

        return test_arr_1, test_arr_2, test_arr_3, time_arr

# plot function is created for plotting the graph in tkinter window
def plot():
        test_arr_1, test_arr_2, test_arr_3, time_arr = initialize_test_arrays()

        # the figure that will contain the plot
        fig = plt.figure(figsize = (12, 7), dpi = 100)
        fig.subplots_adjust(hspace=0.3)

        plt.subplot(311)
        plt.plot(time_arr, test_arr_1)
        plt.title("Canvas initial test")
        plt.ylabel('Bx')
        plt.gca().axes.xaxis.set_ticklabels([])
        plt.autoscale(enable=True, axis='x', tight=True)
        plt.autoscale(enable=True, axis='y')
        plt.gca().tick_params(left=True, right=True) 
        plt.gca().tick_params(axis='x', direction='in') 
        plt.gca().tick_params(axis='y', direction='in')

        plt.subplot(312)
        plt.plot(time_arr, test_arr_2)
        plt.ylabel('By')
        plt.gca().axes.xaxis.set_ticklabels([])
        plt.autoscale(enable=True, axis='x', tight=True)
        plt.autoscale(enable=True, axis='y')
        plt.gca().tick_params(left=True, right=True) 
        plt.gca().tick_params(axis='x', direction='in') 
        plt.gca().tick_params(axis='y', direction='in')

        plt.subplot(313)
        plt.plot(time_arr, test_arr_3)
        plt.ylabel('Bz')
        plt.autoscale(enable=True, axis='x', tight=True)
        plt.autoscale(enable=True, axis='y')
        plt.gca().tick_params(left=True, right=True) 
        plt.gca().tick_params(axis='x', direction='in') 
        plt.gca().tick_params(axis='y', direction='in')

        # list of squares
        #y = [i**2 for i in range(101)]

        # adding the subplot
        #plot1 = fig.add_subplot(111)

        # plotting the graph
        #plot1.plot(y)

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
