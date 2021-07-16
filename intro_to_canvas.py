from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
#NavigationToolbar2Tk)
import read_raw_to_lists
import sys
import datetime
from raw_codecs import decode, time_of_record
import station_names

# plot function is created for plotting the graph in tkinter window
def plot(xArr, timeArr, filename, stime, etime, file_option):

    
    # the figure that will contain the plot
    #fig = Figure(figsize = (5, 5), dpi = 100)

    # list of squares
    #y = [i**2 for i in range(101)]

    #To split up the file name 
    station = filename[0:2]
    year_day_value = filename[2:7]
    year_value = year_day_value[0:2]
    day_value = year_day_value[2:]
    station_name = station_names.find_full_name(station)


    #List of the hours and finding which ones to use
    default_hours_arr = [1,3,5,7,9,11,13,15,17,19,21,23] # default graph list
    hoursArr = [] # list to use for custom times
    currentTime = stime.hour # setting the time to the start
    default_hours_flag = False # using a flag to better optimize operations


    # setting the flag to true if the stime and etimes are the full 24 hours
    if (stime == datetime.time.fromisoformat( "00:00:00") and etime == datetime.time.fromisoformat('23:59:59')):
        default_hours_flag = True

    # Create a loop that fills out an list with odd numbers from start time to end time
    if not default_hours_flag:
        for i in range(stime.hour, etime.hour, 1): #intial for loop to iterate throughout the given times

            # only adding the odd numbers to the list
            if(currentTime % 2 != 0):
                hoursArr.append(currentTime) # adding the odd numbers to the list
            currentTime += 1

    #Datestamp
    if((int)(year_value) > 50):
        year_value = "19" + year_value
    else:
        year_value = "20" + year_value

    date = datetime.datetime.strptime(year_value + "-" + day_value, "%Y-%j").strftime("%m-%d-%Y")



    #Actual Plot

            

    fig = plt.figure(figsize=(7, 4))
    
    plt.plot(timeArr,xArr, linewidth = 1)
    plt.title("Geomagnetic Bx of " + station_name + "   YEARDAY: " + year_day_value + "   DATE: " + date) 
    plt.ylabel('Bx')

    #Make an if statement about changing the label with the x axis changing 
    plt.xlabel("Universal Time (Hours)")
    

    #plt.gca().axes.xaxis.set_ticklabels([]) # removing x axis numbers
    plt.autoscale(enable=True, axis='x', tight=True) # adjusting x axis scaling
    plt.autoscale(enable=True, axis='y') # adjusting y axis scaling
    plt.gca().tick_params(left=True, right=True) # Putting ticks on both sides of y axis
    plt.gca().tick_params(axis='x', direction='in') # x axis ticks inverted
    plt.gca().tick_params(axis='y', direction='in') # y axis ticks inverted

    

    if (default_hours_flag):
        plt.xticks(default_hours_arr) # setting the xaxis time ticks to 1 to 24 hours
    else:
        plt.xticks(hoursArr)

        

        

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = window)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(column = 1, row = 1, sticky = (N, W, E, S))

    # creating the Matplotlib toolbar
    #toolbar = NavigationToolbar2Tk(canvas, window)
    #toolbar.update()

    # placing the toolbar on the Tkinter window
    #canvas.get_tk_widget().pack()

        
	

	

if __name__ == "__main__" :
    # the main Tkinter window
    window = Tk()
    
    file_option = "pdf"

    # setting the title
    window.title('Plotting in Tkinter')

    # dimensions of the main window
    window.geometry("500x500")

    # button that displays the plot
    plot_button = Button(master = window,
                        command = plot,
                        height = 2,
                        width = 10,
                        text = "Plot")

    # place the button
    # in main window
    plot_button.grid(column = 0, row = 0, sticky = (N, W, E, S))

    # run the gui
    window.mainloop()
