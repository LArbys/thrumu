import numpy as np

# Define a function that will (1) convert the wire "matches" in MicroBooNE (across two planes or three planes) to pixels, (2) check those pixels and their vicnity for charge above threshold, and (3) return true if there is charge above threshold in the region

# Inputs:
# (1) The pixel that you're checking to see if it contains a threshold amount of charge
# (2) The range around that wire that you're checking for charge above threshold
# (3) The time tick (or "row") in the array that you're iterating over   
# (4) The array that you're checking for charge above threshold  
# (5) The threshold amount of charge that indicates a good chance of a pixel hit
# (6) The maximum pixel that you can check for charge in the image (this is different from the next argument, because no U or V charge will be beyond a certain point in the image)
# (7) The maximum pixel in the image depending on the number of wires and the compression factor of the image

def pixel_charge_check(pixel, pixel_range, time_tick, plane_array, charge_threshold, max_pixel, max_pixel_image):

    # For now, return 'False' if the pixel is greater than 'max_pixel' as an argument
    if pixel > max_pixel:

        return False

    # Now, use an 'if' statement to make sure that the range that we're considering stays within range
    if (pixel - pixel_range) >= 0 and (pixel + pixel_range + 1) <= 864:
    # Take a slice out of 'plane_array' in the row defined by 'time_tick' and in a range from 'pixel - pixel_range' to 'pixel + pixel_range' (you have to add 1 to the upper bound because it is not inclusive)
        slice = np.copy(plane_array[time_tick, (pixel - pixel_range):(pixel + pixel_range + 1)])

    elif (pixel - pixel_range) < 0:

        # Replace 'pixel - pixel_range' with 0 in the copy of the slice
        slice = np.copy(plane_array[time_tick, 0:(pixel + pixel_range + 1)])

    elif (pixel + pixel_range + 1) > max_pixel_image:

        # Replace 'pixel + pixel_range + 1' with 864 in the copy of the slice
        slice = np.copy(plane_array[time_tick, (pixel - pixel_range):864])

    # Set the slice that's greater than 'charge_threshold' to 1.0
    slice[slice > charge_threshold] = 1.0

    # Set the slice that's less than 'charge_threshold' to 0.0
    slice[slice < charge_threshold] = 0.0

    # Use an 'if' statement to determine if the sum of 'slice' is greater than 'charge_threshold'.  If it is, then return True.
    if np.sum(slice) > 0.0:

        return True

    # If that's not true (meaning that the sum is equal to 0.0), then return false
    # Sloppy programming, but I have to check
    if np.sum(slice) <= 0.0:

        return False
