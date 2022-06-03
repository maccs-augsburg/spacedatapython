# -*- coding: utf-8 -*-
"""
Created on Mon May 16 10:31:25 2022

@author: Chris Hance
"""

# numpy
import numpy as np



if __name__ == "__main__":
    arr = np.array([])
    print(arr)
    
    arr = np.append(arr, 5)
    print(arr)
    print(np.amax(arr))
'''
def unused():
    root = Tk()
    root.geometry('1400x800')
    root.title("Plot input")
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
    second_frame = Frame(my_canvas)
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")
    for thing in range(100):
        Button(second_frame, text=f'Button {thing} Yo!').grid(row=thing, column=0, pady=10,padx=10)
        
    root.bind('<MouseWheel>', lambda e: my_canvas.yview_scroll(e.delta//-120, 'units'))
    root.mainloop()
    '''