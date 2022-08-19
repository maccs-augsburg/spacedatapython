# derivatives.py
#
# Contains functions related to processing the derivatives of MACCS
# data.
#
#  2022 August  -- Created  -- Erik Steinmetz
#

def smooth_boxcar( data_array, width) :
    """ Smooths the data using a boxcar average of the given width.
    
    The function depends on the array being 'full' of data. Odd-sized
    windows will have even left and right halves, while even-sized
    windows will have an extra index on the right. For example a window
    size of 3 will average [ * i *] while a window size of 4 will
    average [ * i * *]
    
    The first left-half-size values of the array will be copied in to 
    the answer without alteration as will the last right-half-size
    values in the array.
    
    Parameters
    ----------
    data_array:
        An array of values to be smoothed.
    width:
        The width of the boxcar window
        
    Returns
    -------
    List
        answer_array: a list of smoothed values.
    """
    
    num_of_values = len( data_array)
    answer_array = [None] * num_of_values
    
    left_width = int( (width - 1) / 2)
    right_width = int( (width + 1) / 2)
    if  width % 2 != 0:
        right_width -= 1
    print( f"left_width: {left_width}, right_width:{right_width}")
    left_copy_index = left_width
    right_copy_index = num_of_values - right_width
    
    index = 0
    
    # Copy the first width/2 values into the answer
    while index < left_copy_index :
        answer_array[ index] = data_array[ index]
        index = index + 1
    # Take the average of width values centered on the current index
    while index < right_copy_index:
        answer_array[ index] = sum( data_array[(index-left_width):(index+right_width+1)]) / width
        index = index + 1
    # Copy the last width/2 values into the answer
    while index < num_of_values:
        answer_array[ index] = data_array[index]
        index = index + 1
    
    return answer_array


def create_derivatives( data_array) :
    """
    Creates an array of derivative values from an array of values.
    The derivatives are created for a time t with 
    deriv = ( value(t+1) -  value(t-1) ) / 2
    where the first value is equal to the second value and the last
    value is equal to the next to last value.
    
    Parameters
    ----------
    data_array:
        An array of values from which to take the derivatives
    
    Returns
    -------
    List
        derivatives: an array of derivatives
    """
    
    num_of_values = len( data_array)
    derivatives = [None] * num_of_values
    index = 1
    while index < num_of_values-1 :
        derivatives[ index] = (data_array[index+1] - data_array[index-1]) / 2
        index = index + 1
    derivatives[0] = derivatives[1]
    derivatives[num_of_values-1] = derivatives[num_of_values-2]
    return derivatives

if __name__ == "__main__":
    data = [ 2, 3, 7, 9, 18, None, 21.2, 19, 18.2]
    smoothed = smooth_boxcar( data, 3)
    print( smoothed)
    derivs = create_derivatives( smoothed)
    print( derivs)
