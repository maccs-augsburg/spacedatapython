from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
#NavigationToolbar2Tk)

# cancel function for closing window
def cancel():
        window.destroy()

# function to create test arrays for 3 subplots displays
def initialize_test_arrays():
        test_arr_1 = [1, 2, 3, 4, 5]
        test_arr_2 = [5, 4, 3, 2, 1]
        test_arr_3 = [1, 3, 2, 4, 5]
        time_arr = [1, 2, 3, 4, 5]

        return test_arr_1, test_arr_2, test_arr_3, time_arr

def create_toolbar():
        # Creating new tk window for the toolbar
        toolbar = Tk()
        toolbar.title("Toolbar")
        toolbar.geometry("200x200")

        # Calling other functions to set up the toolbar object
        toolbar_gui_entries(toolbar)
        toolbar_gui_entry_boxes(toolbar)

def toolbar_gui_entry_boxes(toolbar):
        # plot min x section
        plot_min_x = IntVar()
        plot_min_x.set(0)
        plot_min_entry_x = ttk.Entry(toolbar, width=3, textvariable=plot_min_x)
        plot_min_entry_x.grid(column=2, row=2)

        # plot max x section
        plot_max_x = IntVar()
        plot_max_x.set(0)
        plot_max_entry_x = ttk.Entry(toolbar, width=3, textvariable=plot_max_x)
        plot_max_entry_x.grid(column=2, row=3)

        # plot min y section
        plot_min_y = IntVar()
        plot_min_y.set(0)
        plot_min_entry_y = ttk.Entry(toolbar, width=3, textvariable=plot_min_y)
        plot_min_entry_y.grid(column=2, row=4)

        # plot max y section
        plot_max_y = IntVar()
        plot_max_y.set(0)
        plot_max_entry_y = ttk.Entry(toolbar, width=3, textvariable=plot_max_y)
        plot_max_entry_y.grid(column=2, row=5)

        # plot min z section
        plot_min_z = IntVar()
        plot_min_z.set(0)
        plot_min_entry_z = ttk.Entry(toolbar, width=3, textvariable=plot_min_z)
        plot_min_entry_z.grid(column=2, row=6)

        # plot max z section
        plot_max_z = IntVar()
        plot_max_z.set(0)
        plot_max_entry_z = ttk.Entry(toolbar, width=3, textvariable=plot_max_z)
        plot_max_entry_z.grid(column=2, row=7)
        
        ### All sections above don't display 0 in the box for some reason ###

def toolbar_gui_entries(toolbar):
        # Title -- Not sure if I should keep
        ttk.Label(toolbar, text="Toolbar Entry Form").grid(column=1, row=1, sticky=(W,E))

        # min and max labels
        ttk.Label(toolbar, text="Plot min x:").grid(column=1, row=2)
        ttk.Label(toolbar, text="Plot max x:").grid(column=1, row=3)
        ttk.Label(toolbar, text="Plot min y:").grid(column=1, row=4)
        ttk.Label(toolbar, text="Plot max y:").grid(column=1, row=5)
        ttk.Label(toolbar, text="Plot min z:").grid(column=1, row=6)
        ttk.Label(toolbar, text="Plot max z:").grid(column=1, row=7)

# plot function is created for plotting the graph in tkinter window
def plot():
        test_arr_1, test_arr_2, test_arr_3, time_arr = initialize_test_arrays()

        # the figure that will contain the plot
        fig = plt.figure(figsize = (5, 7), dpi = 100)
        fig.subplots_adjust(hspace=0.3)

        # First subplot
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

        # Second subplot
        plt.subplot(312)
        plt.plot(time_arr, test_arr_2)
        plt.ylabel('By')
        plt.gca().axes.xaxis.set_ticklabels([])
        plt.autoscale(enable=True, axis='x', tight=True)
        plt.autoscale(enable=True, axis='y')
        plt.gca().tick_params(left=True, right=True) 
        plt.gca().tick_params(axis='x', direction='in') 
        plt.gca().tick_params(axis='y', direction='in')

        # Third subplot
        plt.subplot(313)
        plt.plot(time_arr, test_arr_3)
        plt.ylabel('Bz')
        plt.autoscale(enable=True, axis='x', tight=True)
        plt.autoscale(enable=True, axis='y')
        plt.gca().tick_params(left=True, right=True) 
        plt.gca().tick_params(axis='x', direction='in') 
        plt.gca().tick_params(axis='y', direction='in')

        # Adjusting window geometry
        window.geometry("670x750")
        
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master = window)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().grid(column=3, row=2)

        # creating the Matplotlib toolbar
        create_toolbar()
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
        window.geometry("200x100")

        # button that displays the plot
        plot_button = Button(master = window,
                             command = plot,
                             height = 2,
                             width = 10,
                             text = "Plot")
        # button that closes the window
        cancel_button = Button(master=window,
                               command=cancel,
                               height=2,
                               width=10,
                               text="Cancel")

        # place the buttons in the main window
        plot_button.grid(column=1, row=1)
        cancel_button.grid(column=2, row=1)

        # running the gui
        window.mainloop()
