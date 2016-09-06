# Define a function that will identify dead wire regions within these images (or, also, regions that have no track of this color at any time)

# The input arguments that the function must take is the array of ADC values across the input three wire planes, which will be checked for any amount of charge above zero (the deconvolved values below zero do not count as an amount of charge above threshold), and 'num_of_plane_pixels', the number of pixels across the plane that could contain charge

def dead_pixel_region_finder(plane_array, num_of_time_pixels, num_of_plane_pixels): 

    # Declare three empty lists that will be filled with lists corresponding to the start and end of the range of dead wires
    plane_dead_pixels = []

    # Before the start of the loop, initialize variables for the start and end of the pixel region
    dead_region_start_pixel = 0
    dead_region_end_pixel   = 0
    
    # Loop over each pixel from (0, num_of_plane_pixels) to see if there are any that do not contain (positive) charge at any time tick
    for j in range(0, num_of_plane_pixels):

        # Define a boolean value for if ANY pixels in this column have charge
        pixels_have_charge = False 

        # Initialize a loop over the time ticks to see if any pixel in the range (0, 756) has a positive ADC value at any time
        for i in range (0, num_of_time_pixels):

            # Check to see if any pixel for this plane in this column has charge
            if plane_array[i][j] > 0:
                
                # If even one pixel in the plane has an ADC value greater than 0, then the boolean declared above will be set equal to 0
                pixels_have_charge = True

          
        # Now, consider the different cases that will "find" regions of dead pixels
        # First, loop over the uplane to find the start and end pixels of the dead regions of pixels, and append these to a list

        # If there is no charge in the plane in this column and 'dead_region_start_pixel' == 0, then change the value of 'dead_region_start_pixel'.  This is the start of a region of dead pixels.

        if pixels_have_charge == False and dead_region_start_pixel == 0:

            # Change the value of 'dead_region_start_pixel'
            dead_region_start_pixel = j

        # If there is charge in the plane and 'dead_region_start_pixel' !=  0, then this is the end of the region of dead pixels.  Set the value of 'dead_region_end_pixel' to this pixel, append a list of 'dead_region_start_pixel' and 'dead_region_end_pixel' to the end of 'plane_dead_pixels', and set 'dead_region_start_pixel' to 0 
        if pixels_have_charge == True and dead_region_start_pixel != 0:

            # Set 'dead_region_end_pixel' equal to the pixel immediately before this one (this pixel has charge, so the last pixel in the 'dead region' is actually the previous one)
            dead_region_end_pixel = j - 1

            # Append 'dead_region_start_pixel' and 'dead_region_end_pixel' onto the 'plane_dead_pixels' list

            # Consider the case that the "dead region" is actually just a single pixel, so I will only append a single pixel to the list
            # In this case, 'dead_region_start_pixel' and 'dead_region_end_pixel' are equal
            if dead_region_start_pixel == dead_region_end_pixel:

                # Append the single pixel as a list so it can be referenced in 'adjacent_pixel_color_scoring.py' as a list and not treated differently from the pixel
                # // range referenced below
                plane_dead_pixels.append([dead_region_start_pixel])

            else:

                plane_dead_pixels.append([dead_region_start_pixel, dead_region_end_pixel])

            # Set 'dead_region_start_pixel' equal to 0
            dead_region_start_pixel = 0

    return plane_dead_pixels
