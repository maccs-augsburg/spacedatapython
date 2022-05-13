#Gui implemented with classes
#Annabelle

#Imports from tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename


#imports from python 
import sys
import datetime
from PIL import ImageTk, Image

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import subprocess
import os
#imports from plotter functions

import file_naming
import read_raw_to_lists
import one_array_plotted
import read_clean_to_lists
import clean_one_array_plotted


class ThreeGraphPlotter:
    def __init__(self):
        #Creation of the window 
        window = Tk()
        window.geometry('1500x700')
        window.title('X, Y and Z Plotter')

        mainframe = ttk.Frame(window, padding = "3 3 12 12")
        mainframe.grid(column = 0, row = 0, sticky = (N,W,E,S))

        window.columnconfigure(0, weight = 1)
        window.rowconfigure(0, weight = 1)

        #File name values for saving figure
        self.figure = None
        self.file_name = None

        ###Labels###

        #Year day entry box label 
        ttk.Label(mainframe, text = "Year Day: ").grid(column = 1, row = 2, sticky = E)

        #Start hour entry box label
        ttk.Label(mainframe, text = "Start Hour: ").grid(column = 1, row = 3, sticky = E)

        #Start minute entry box label
        ttk.Label(mainframe, text = "Start Minute: ").grid(column = 1, row = 4,sticky = E)

        #Start second entry box label
        ttk.Label(mainframe, text = "Start Second: ").grid(column = 1, row = 5, sticky = E)

        #End hour entry box label
        ttk.Label(mainframe, text = "End Hour: ").grid(column = 1, row = 6, sticky = E)

        #End minute entry box label
        ttk.Label(mainframe, text = "End Minute: ").grid(column = 1, row = 7, sticky = E)

        #End second entry box label
        ttk.Label(mainframe, text = "End Second: ").grid(column = 1, row = 8, sticky = E)

        #Plot x, y, or z checkbox label
        ttk.Label(mainframe, text = "Plot X, Y or Z: ").grid(column = 1, row = 9, sticky = E)

        #Station code entry box label
        ttk.Label(mainframe, text = "Station Code: ").grid(column = 1, row = 1, pady = (25, 0), sticky = E)

        #File option radiobutton label
        ttk.Label(mainframe, text = "File Option: ").grid(column = 1, row = 14, sticky = E)



        ###Entry Boxes###
        self.year_day = StringVar()
        ttk.Entry(mainframe, width= 5, textvariable = self.year_day).grid(column = 2, row = 2,   sticky = W)

        self.start_hour = IntVar()
        self.start_hour.set(0)
        ttk.Entry(mainframe, width = 5, textvariable = self.start_hour).grid(column = 2, row = 3, sticky = W)

        self.start_minute = IntVar()
        self.start_minute.set(0)
        ttk.Entry(mainframe, width = 5, textvariable = self.start_minute).grid(column = 2, row = 4, sticky = W)

        self.start_second = IntVar()
        self.start_second.set(0)
        ttk.Entry(mainframe, width = 5, textvariable = self.start_second).grid(column = 2, row = 5,sticky = W)

        self.end_hour = IntVar()
        self.end_hour.set(23)
        ttk.Entry(mainframe, width = 5, textvariable = self.end_hour).grid(column = 2, row = 6, sticky = W)

        self.end_minute = IntVar()
        self.end_minute.set(59)
        ttk.Entry(mainframe, width = 5, textvariable = self.end_minute).grid(column = 2, row = 7, sticky = W)

        self.end_second = IntVar()
        self.end_second.set(59)
        ttk.Entry(mainframe, width = 5, textvariable = self.end_second).grid(column = 2, row = 8, sticky = W)

        self.station_names = StringVar()
        ttk.Entry(mainframe, width = 5, textvariable = self.station_names).grid(column = 2, row = 1, pady = (25, 0), sticky = W)

        ###Check Boxes and Radiobuttons###
        self.graph_from_plotter_x = IntVar()
        self.graph_from_plotter_y = IntVar()
        self.graph_from_plotter_z = IntVar()
        
        # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Checkbutton.html
        # onvalue = 1 when checked inside gui by default, can also change onvalue to something we specify
        x_plot = ttk.Checkbutton(mainframe, text = "X Plot", variable = self.graph_from_plotter_x, onvalue = 1).grid(column = 2, row = 10,padx = 25 , sticky = W)
        y_plot = ttk.Checkbutton(mainframe, text = "Y Plot", variable = self.graph_from_plotter_y, onvalue = 2).grid(column = 2, row = 11,padx = 25 , sticky = W) 
        z_plot = ttk.Checkbutton(mainframe, text = "Z Plot", variable = self.graph_from_plotter_z, onvalue = 3).grid(column = 2, row = 12,padx = 25 , sticky = W)

        self.selection_file = StringVar()
        cda_web = Radiobutton(mainframe, text = "CDAWEB:NA", value = 1, variable = self.selection_file).grid(column = 2, row = 15, padx = 25,  sticky = W)
        iaga_00 = Radiobutton(mainframe, text = "IAGA2000:NA", value = 2, variable = self.selection_file).grid(column = 2, row = 16, padx = 25,  sticky = W)
        iaga_02 = Radiobutton(mainframe, text = "IAGA2002:NA", value = 3, variable = self.selection_file).grid(column = 2, row = 17, padx = 25, sticky = W)
        raw_hz_file = Radiobutton(mainframe, text = "Raw 2hz file", value = 4, variable = self.selection_file).grid(column = 2, row = 18, padx = 25,  sticky = W)
        clean_data = Radiobutton(mainframe, text = "Clean Data", value = 5, variable = self.selection_file).grid(column = 2, row = 19, padx = 25, sticky = W)


        ###Buttons###

        ttk.Button(mainframe, text = "Plot", command = lambda: self.execute_functions(mainframe)).grid(column = 2, row = 20,  sticky = W)
        ttk.Button(mainframe, text = "Quit", command = lambda: self.cancel(window)).grid(column =1, row = 22,columnspan = 2,  padx = 25, sticky = W)
        ttk.Button(mainframe, text="Save", command=lambda: self.save(self.figure, self.file_name)).grid(column=2, row=21, sticky=W)
        ttk.Button(mainframe, text="Save As...", command=lambda: self.save_as(self.figure, self.file_name)).grid(column=1, row=21, sticky=W)
        ttk.Button(mainframe, text="Open File...", command=lambda: self.open_file()).grid(column=1, row=20, sticky=W)
        #

        image=Image.open('maccslogo_870.jpeg')
        image_file = ImageTk.PhotoImage(image)
        image_label = ttk.Label(mainframe, image=image_file)
        image_label.image = image_file
        image_label.grid(column=7,row=1, columnspan=8, rowspan=24)

        
        for child in mainframe.winfo_children(): 
                child.grid_configure(padx=5, pady=5)

        #Puts our execute_functions to the return key
        window.bind("<Return>", self.execute_functions)

        window.mainloop()    

    def execute_functions(self, mainframe, *args):
        """
        executes the functions that are in the gui

        Parameters
        ----------
        mainframe : the main frame that the gui is placed in
        """

        ###Getting the user entries###
        station_names_value = self.station_names.get()
        self.station_names_entry_check(station_names_value)

        year_day_value = self.year_day.get()
        self.year_day_entry_check(year_day_value)

        start_hour_value = self.start_hour_entry_check(self.start_hour.get())
        start_minute_value = self.start_minute_entry_check( self.start_minute.get())
        start_second_value = self.start_second_entry_check( self.start_second.get())

        # creating the start time stamp
        start_time_stamp = datetime.time(hour=start_hour_value, minute=start_minute_value, second=start_second_value)


        end_hour_value = self.end_hour_entry_check( self.end_hour.get())
        end_minute_value = self.end_minute_entry_check( self.end_minute.get())
        end_second_value = self.end_second_entry_check( self.end_second.get())

        # creating the end time stamp
        end_time_stamp = datetime.time(hour=end_hour_value, minute=end_minute_value, second=end_second_value)

        selection_file_value = self.selection_file.get()
        file_ending_value = self.file_format_entry_check(selection_file_value)


        # Making the Plot
        file_name_full = station_names_value + year_day_value + file_ending_value
        time_interval_string = file_naming.create_time_interval_string_hms(start_hour_value, start_minute_value, start_second_value, end_hour_value, end_minute_value, end_second_value)
        self.file_name = station_names_value + year_day_value + time_interval_string
        
        # Get associated values to GUI, if x,y,z checked, then they are set to some value, respectively 1, 2, 3
        graph_from_plotter_value_x = self.graph_from_plotter_x.get()
        graph_from_plotter_value_y = self.graph_from_plotter_y.get()
        graph_from_plotter_value_z = self.graph_from_plotter_z.get()


        try:
            file = open(file_name_full, 'rb')
        except:
            # popping up an error if we can't open the file
            self.error_message_pop_up("File open error", "couldn't find and open your file")

        if (selection_file_value == '4'):
            
            xArr, yArr, zArr, timeArr = read_raw_to_lists.create_datetime_lists_from_raw(file, start_time_stamp,end_time_stamp, self.file_name)
            # plotting the arrays
            self.figure = self.graph_from_plotter_entry_check(graph_from_plotter_value_x,
                                                              graph_from_plotter_value_y, 
                                                              graph_from_plotter_value_z, 
                                                              xArr, 
                                                              yArr, 
                                                              zArr,
                                                              timeArr, 
                                                              self.file_name, start_time_stamp, end_time_stamp, selection_file_value)

        elif (selection_file_value == '5'):
            
            xArr, yArr, zArr, timeArr, flag_arr = read_clean_to_lists.create_datetime_lists_from_clean(file, start_time_stamp, end_time_stamp, self.file_name)
            # plotting the arrays
            self.figure = self.graph_from_plotter_entry_check(graph_from_plotter_value_x,
                                                              graph_from_plotter_value_y, 
                                                              graph_from_plotter_value_z, 
                                                              xArr, 
                                                              yArr, 
                                                              zArr,
                                                              timeArr, 
                                                              self.file_name, start_time_stamp, end_time_stamp, selection_file_value)
                                          
        
        canvas = FigureCanvasTkAgg(self.figure, master = mainframe)
        canvas.draw()

        canvas.get_tk_widget().grid(column=4, row=1, columnspan=8, rowspan=24)


    def convert_hours_list_to_datetime_object(self, list_to_convert):
        """
        converts the hours list into datetime objects

        Parameters
        ----------
        list_to_convert : the list of items to convert

        Returns
        -------
        converted_list : the list of converted items
        """
        converted_list = []
            
        for i in range(len(list_to_convert)):
            total_time = list_to_convert[i]
            hour = int(total_time / 24)

            total_time = total_time - hour
            minute = int(total_time / 59)

            total_time = total_time - minute
            second = total_time

            converted_list.append(datetime.datetime(year=1111, month=1, day=1, hour=hour, minute=minute, second=second))

        return converted_list

    def save(self, fig, file_name):
         
        """
        saves the file as a pdf document

        Parameters
        ----------
        fig : the plotted figure

        file_name : the name of the file to be saved as
        """
        # Saving the file as a defualt pdf
        fig.savefig(file_name + '.pdf', format='pdf', dpi=1200)
        # Opening the file after saving so the user knows it has been saved and can see it
        subprocess.Popen(file_name + '.pdf', shell=True)

    def save_as(self, fig, file_name):
         
        """
        saves the file as either a pdf or png

        Parameters
        ----------
        fig : the plotted figure

        file_name : the name of the file to be saved as
        """
        
        # Specifying the supported file types that can be saved
        
        files = [('PDF Files', '*.pdf'), ('PNG Files', '*.png'), ('All Files', '*.*')]
        # Popping up the save as file dialog box
        save_as_file = asksaveasfile(filetypes = files, defaultextension = files, initialfile=(file_name + '.pdf'))

        if save_as_file is None:
            return
        else:
            file_ending = save_as_file.name.split('/')[-1][-4:]
            if file_ending == ".pdf":
                fig.savefig(file_name + file_ending, format = "pdf", dpi = 1200)
            elif file_ending == ".png":
                fig.savefig(file_name + file_ending, format = "png", dpi = 1200)

                

    def open_file(self):
        """
        Opens a open file dialog box where the user picks the appropriate file type. Once that is
        selected, it inputs the data into the boxes automatically based on the filename.
        """
        # listing the types of file types we currently support
        filetypes = (
            ('Raw files', '*.2hz'),
            ('Clean files', '*.s2')
        )

        # opening the dialog box
        file_name = askopenfilename(title='test', filetypes = filetypes)

        # splitting up the path and selecting the filename
        self.file_name = file_name.split('/')[-1]

        # setting the station code from the filename
        self.station_names.set(self.file_name[0:2])

        # setting the yearday from the filename
        self.year_day.set(self.file_name[2:7])

        # resetting the start times and end times
        self.start_hour.set(0)
        self.start_minute.set(0)
        self.start_second.set(0)
        self.end_hour.set(23)
        self.end_minute.set(59)
        self.end_second.set(59)

        # raw file selection branch
        if (self.file_name[7:] == '.2hz'):
            self.selection_file.set(4)
            
        # clean file selection branch
        elif (self.file_name[7:] == '.s2'):
            self.selection_file.set(5)

        # else
        else:
            print('Option not available yet :(')

    def year_day_entry_check(self, year_day_value):

        """
        Checks the year day entry value to see if there was a value inputted for the yearday entry box
        Parameters
        ----------
        year_day_value: the value that was inputted into the year_day_entry box
        """
        # Checking to see if any input was put in the yearday entry box
        if (len(year_day_value) == 0):
            self.error_message_pop_up(title='year_day_entry Error', message='There was no input for the year day entry box')


    def station_names_entry_check(self, station_names_value):

        """
        Checks the station_code_entry value and pops up an error message if it isn't a good entry
        Parameters
        ----------
        station_code_value: the value that was inputted into the station_code_entry box
        """
        # Checking to see if no input was put in the station code entry box
        if(len(station_names_value) == 0):
            # show error as no input was received
            self.error_message_pop_up(title="Station code entry error", message="There was no input for the station code entry box")




    def file_format_entry_check(self, selection_file_value):
        """
        checks the file selection value and sets the ending value to match it

        Parameters
        ----------
        selection_file_value : the value of the file selection

        Returns
        -------
        file_ending_value : the ending value of the file
        """
        if(selection_file_value == '1'):
            # CDA-Web branch (NOT IMPLEMENTED)
            self.warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

        # Testing to see if user selected IAGA2000 branch
        elif(selection_file_value == '2'):
            #IAGA2000 branch (NOT IMPLEMENTED)
            self.warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

        # Testing to see if user selected IAGA2002 branch
        elif(selection_file_value == '3'):
            #IAGA2002 branch (NOT IMPLEMENTED)
            self.warning_message_pop_up(title="File format option error", message="Sorry! But we don't have this option available yet, please try picking a different option")

        # Testing to see if user selected Raw 2hz branch
        elif(selection_file_value == '4'):
            #Raw 2hz file branch (TODO: IMPLEMENT SECTION)
            file_ending_value = '.2hz'

        elif(selection_file_value == '5'):
            #Raw 2hz file branch (TODO: IMPLEMENT SECTION)
            file_ending_value = '.s2'

        # Otherwise we can assume that no option had been selected
        else:
            # Message box error when no file format option has been selected
            self.error_message_pop_up(title="File format option error", message="Please select a file format option")

        # Returning the string of the file type to be used
        return file_ending_value

    def graph_from_plotter_entry_check(self, graph_from_plotter_value_x,graph_from_plotter_value_y, graph_from_plotter_value_z, xArr, yArr, zArr, timeArr, filename, stime, etime, selection_file):

        """
        Checks the gui entries

        Parameters
        ----------
        graph_from_plotter_value_x : the value from the gui to see if we need to plot x

        graph_from_plotter_value_y : the value from the gui to see if we need to plot y

        graph_from_plotter_value_z : the value from the gui to see if we need to plot z

        xArr : the x array values

        yArr : the y array values

        zArr : the z array values

        timeArr : the time array values

        filename : the name of the file

        stime : the start time stamp

        etime : the end time stamp

        selection_file : the selection file value

        Returns
        -------
        fig : the plotted figure
        """

        '''
        -- can get rid of inside elif check once we know there is no difference between one_array and clean_one_array
        -- can also get rid of file_state check if were only doing raw and clean, since arrays are going to contain the same vals.
        
        create an alias from plotter values
        these values correspond to the checkbox state in GUI
        x == 1, y == 2, z ==3 when checked
        file_state either 4 or 5, raw = 4, clean = 5, others will throw error because not supported yet
        '''
        x_state = graph_from_plotter_value_x
        y_state = graph_from_plotter_value_y
        z_state = graph_from_plotter_value_z
        file_state = int(selection_file)
        any_plot_state = x_state + y_state + file_state
        
        #If statement to decided if we want X, Y or Z plot
        # X, Y, Z plot, clean or raw
        # first check if all on, then two the two_plot checks, last should be one_axis
        if (x_state == 1 and y_state == 2 and z_state == 3):
    
            if (file_state >= 4):
                fig = one_array_plotted.x_y_and_z_plot (xArr, yArr, zArr, timeArr, filename, stime, etime)
            
                
        # Y, Z plot, clean or raw
        elif (y_state == 2 and z_state == 3):
            
            if (file_state >= 4):
                fig = one_array_plotted.plot_two_axis(yArr, zArr, timeArr, filename, stime, etime, 'Y', 'Z')
            
                
        elif (x_state == 1 and z_state == 3):
            
            if (file_state >= 4):
                fig = one_array_plotted.plot_two_axis(xArr, zArr, timeArr, filename, stime, etime, 'X', 'Z')
            
        
        elif (x_state == 1 and y_state == 2):
            
            if (file_state >= 4):
                fig = one_array_plotted.plot_two_axis(xArr, yArr, timeArr, filename, stime, etime, 'X', 'Y')
            
        
        elif ( any_plot_state > 0 and file_state > 0):
            
            if (x_state == 1):
                fig = one_array_plotted.plot_axis(xArr, timeArr, filename, stime, etime, 'X')
            
            if(y_state == 2):
                fig = one_array_plotted.plot_axis(yArr, timeArr, filename, stime, etime, 'Y')
            
            if(z_state == 3):
                fig = one_array_plotted.plot_axis(zArr, timeArr, filename, stime, etime, 'Z')
                
        #Warning Message
        else:
            self.warning_message_pop_up(title = "File Format Option Error", message = "Please select a file format option")

        #return graph_from_plotter_value_x, graph_from_plotter_value_y, graph_from_plotter_value_z, fig
        return fig
        
                
        '''START COMMENT
        
        #Raw X,Y and Z Plot
        # start cutting down on redundant code DONE
        if(graph_from_plotter_value_x == 1 and graph_from_plotter_value_y == 2 and graph_from_plotter_value_z == 3 and selection_file == '4'):
            fig = one_array_plotted.x_y_and_z_plot(xArr, yArr, zArr, timeArr, filename, stime, etime)
             
        #Clean X,Y, and Z plot    DONE
        elif(graph_from_plotter_value_x == 1 and graph_from_plotter_value_y ==2 and graph_from_plotter_value_z == 3 and selection_file == '5'):
            fig = clean_one_array_plotted.x_y_and_z_plot(xArr, yArr, zArr, timeArr, filename, stime, etime)

             
        #Raw Y and Z plot         DONE
        elif(graph_from_plotter_value_y == 2 and graph_from_plotter_value_z == 3 and selection_file == '4'):
            fig = one_array_plotted.plot_two_axis(yArr, zArr, timeArr, filename, stime, etime, 'Y', 'Z')

        #Clean Y and Z plot       DONE
        elif(graph_from_plotter_value_y == 2 and graph_from_plotter_value_z == 3 and selection_file == '5'):
            fig = clean_one_array_plotted.y_and_z_plot(yArr, zArr, timeArr, filename, stime, etime)
             
        #Raw X and Z plot         DONE
        elif(graph_from_plotter_value_x == 1 and graph_from_plotter_value_z == 3 and selection_file == '4'):
            fig = one_array_plotted.plot_two_axis(xArr, zArr, timeArr, filename, stime, etime, 'X', 'Z')

         #Clean X and Z plo       DONE 
        elif(graph_from_plotter_value_x == 1 and graph_from_plotter_value_z == 3 and selection_file == '5'):
            fig = clean_one_array_plotted.x_and_z_plot(xArr,zArr, timeArr, filename, stime, etime)

        #Raw X and Y plot         DONE
        elif(graph_from_plotter_value_x == 1 and graph_from_plotter_value_y == 2 and selection_file == '4'):
            fig = one_array_plotted.plot_two_axis(xArr, yArr, timeArr, filename, stime, etime, 'X', 'Y')

        #Clean X and Y plot       DONE
        elif(graph_from_plotter_value_x == 1 and graph_from_plotter_value_y == 2 and selection_file == '5'):
            fig = clean_one_array_plotted.x_and_y_plot(xArr, yArr, timeArr, filename, stime, etime)

        #Raw Z plot               DONE
        elif(graph_from_plotter_value_z == 3 and selection_file == '4'):
            fig = one_array_plotted.plot_axis(zArr, timeArr, filename, stime, etime, 'Z')

        #Clean Z plot             DONE
        elif(graph_from_plotter_value_z == 3 and selection_file == '5'):
            fig = clean_one_array_plotted.z_plot(zArr, timeArr, filename, stime, etime)

        #Raw Y plot               DONE
        elif(graph_from_plotter_value_y == 2 and selection_file == '4'):
            fig = one_array_plotted.plot_axis(yArr, timeArr, filename, stime, etime, 'Y')

        #Clean Y plot             DONE
        elif(graph_from_plotter_value_y == 2 and selection_file == '5'):
            fig = clean_one_array_plotted.y_plot(yArr, timeArr, filename, stime, etime)
             
        #Raw X plot               DONE
        elif(graph_from_plotter_value_x == 1 and selection_file == '4'):
            fig = one_array_plotted.plot_axis(xArr, timeArr, filename, stime, etime, 'X')

        #Clean X plot             DONE
        elif(graph_from_plotter_value_x == 1 and selection_file == '5'):
            fig = clean_one_array_plotted.x_plot(xArr, timeArr, filename, stime, etime)
                      
        #Warning Message
        else:
            self.warning_message_pop_up(title = "File Format Option Error", message = "Please select a file format option")

        #return graph_from_plotter_value_x, graph_from_plotter_value_y, graph_from_plotter_value_z, fig
        return fig
    
        END COMMENT''' 




    def start_hour_entry_check(self, start_hour_string):
         
        """
        Checks the start hour entry value and pops up an error message if it isn't a good entry
        Parameters
        ----------
        String
        start_hour_string: the value that was inputted into the start_hour_entry box
        Returns
        -------
        Int
        value: the int version of the inputted value in the start_hour_entry box
        """
        # making sure the inputted value is an int not a float
        value = int(start_hour_string)

        if(value > 23):
            # Have error message box pop up because it can't be more than 23
            self.error_message_pop_up(title="Start Hour Entry Error", message="Start hour cannot be more than 23")
            
        # Testing to see if the inputted value is less than what it can be
        elif(value < 0):
            # Have error message box pop up because it can't be a negative number
            self.error_message_pop_up(title="Start Hour Entry Error", message="Start hour cannot be negative")

        # Returning the start_hour_string so that whatever changes we made to it get returned
        return value


    def start_minute_entry_check(self, start_minute_string):

        """
        Checks the start minute entry value and pops up an error message if it isn't a good entry
        Parameters
        ----------
        String
        start_minute_string: the value that was inputted into the start_minute_entry box
        Returns
        -------
        Int
        value: the inputted value in the start_minute_entry box
        """
        # making sure the inputted value is an int not a float
        value = int(start_minute_string)

        if(value > 59):
            # Have error messsage box pop up becuase it can't be more than 59
            self.error_message_pop_up(title="Start Minute Entry Error", message="Start minute cannot be more than 59")

        # Testing to see if the inputted value is less than what it can be
        elif(value < 0):
            # Have error message box pop up because it can't be a negative number
            self.error_message_pop_up(title="Start Minute Entry Error", message="Start minute cannot be negative")

        # Returning the start_minute_string so whatever changes we made to it get returned
        return value



    def start_second_entry_check(self, start_second_string):

        """
        Checks the start second entry value and pops up an error message if it isn't a good entry
        Parameters
        ----------
        String
        start_second_string: the value that was inputted into the start_second_entry box
        Returns
        -------
        Int
        value: the inputted value in the start_second_entry box
        """
        # making sure the inputted value is an int not a float
        value = int(start_second_string)

        if(value > 59):
            # Have error messsage box pop up becuase it can't be more than 59
            self.error_message_pop_up(title="Start Second Entry Error", message="Start second cannot be more than 59")

        # Testing to see if the inputted value is less than what it can be
        elif(value < 0):
            # Have error message box pop up because it can't be a negative number
            self.error_message_pop_up(title="Start Second Entry Error", message="Start second cannot be negative")

        # Returning the start_second_string so whatever changes we made to it get returned
        return value





    def end_hour_entry_check(self, end_hour_string):

        """
        Checks the end hour entry value and pops up an error message if it isn't a good entry
        Parameters
        ----------
        String
            end_hour_string: the value that was inputted into the end_hour_entry box
        Returns
        -------
        Int
            value: the inputted value in the end_hour_entry box
        """
        # making sure the inputted value is an int not a float
        value = int(end_hour_string)

        # Testing to see if the inputted value exceeds what it can be
        if(value > 23):
            # Have error message box pop up because it can't be more than 23
            self.error_message_pop_up(title="End Hour Entry Error", message="End hour cannot be more than 23")

         # Testing to see if the inputted value is less than what it can be
        elif(value < 0):
            # Have error message box pop up because it can't be a negative number
            self.error_message_pop_up(title="End Hour Entry Error", message="End hour cannot be negative")

        # Returning the end_hour_string so whatever changes we made to it get returned
        return value



    def end_minute_entry_check(self, end_minute_string):

        """
        Checks the end minute entry value and pops up an error message if it isn't a good entry
        Parameters
        ----------
        String
        end_minute_string: the value that was inputted into the end_minute_entry box
        Returns
        -------
        Int
        value: the inputted value in the end_hour_entry box
        """
        # making sure the inputted value is an int not a float
        value = int(end_minute_string)

        # Testing to see if the inputted value exceeds what it can be
        if(value > 59):
            #Have error messsage box pop up becuase it can't be more than 59
            self.error_message_pop_up(title="End Minute Entry Error", message="End minute cannot be more than 59")

        # Testing to see if the inputted value is less than what it can be
        elif(value < 0):
            # Have error message box pop up because it can't be a negative number
            self.error_message_pop_up(title="End Minute Entry Error", message="End minute cannot be negative")

        # Returning the end_minute_string so whatever changes we made to it get returned
        return value



    def end_second_entry_check(self, end_second_string):
        """
        Checks the end second entry value and pops up an error message if it isn't a good entry
        Parameters
        ----------
        String
        end_second_string: the value that was inputted into the end_second_entry box
        Returns
        -------
        Int
        end_second_string: the inputted value in the end_second_entry box
        """
        # making sure the inputted value is an int not a float
        value = int(end_second_string)

        # Testing to see if the inputted value exceeds what it can be
        if(value > 59):
            # Have error messsage box pop up becuase it can't be more than 59
            self.error_message_pop_up(title="End Second Entry Error", message="End second cannot be more than 59")

        # Testing to see if the inputted value is less than what it can be
        elif(value < 0):
            # Have error message box pop up because it can't be a negative number
            self.error_message_pop_up(title="End Second Entry Error", message="End second cannot be negative")

        # Returning the end_second_string so whatever changes we made to it get returned
        return value


    def error_message_pop_up(self, title, message):
         
        # pops up error message box with the title and message inputted
        messagebox.showerror(title=title, message = "ERROR: " + message)
        sys.exit(0)

    def warning_message_pop_up(self, title, message):
        # pops up warning message box with the title and message inputted
        messagebox.showwarning(title=title, message="WARNING: " + message)
            
    def cancel(self, window):
        # Exits the gui without running any code after
        window.destroy()


def main():
    x_y_z_plotter = ThreeGraphPlotter()

if __name__ == "__main__":
    main()



