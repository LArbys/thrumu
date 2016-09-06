# Define a function that will fill the correct channels with the right amount of color depending on what type of list they are:
# Top: Cyan
# Bottom: Magenta
# Upstream: Yellow
# Downstream: Orange

# The inputs to this function will be the following:
# 'hit_string' - this is a string with the name of what type of list this ('top', 'bottom', 'upstream', 'downstream')
# pixel_list   - this is the list of pixels in the order [time, u_pixel, y_pixel, and y_pixel] that need to be filled with color
# uplane_array - array of ADC values on the uplane (Plane 1), which is of dimensions of 756 * 864
# vplane_array - array of ADC values on the vplane (Plane 2), which is of dimensions of 756 * 864
# uplane_array - array of ADC values on the yplane (Plane 3), which is of dimensions of 756 * 864

def pixel_color_adding_algo(top_pixel_list, bottom_pixel_list, upstream_pixel_list, downstream_pixel_list, uplane_array, vplane_array, yplane_array):

    # print "The code is entering the pixel_color_addition_algo!"
    # print "\n"

    # print "Top Pixel Hit List: ", top_pixel_list
    # print "\n"

    # Cheat them an intialize all of the 'pixel_time' variables to 0.  Take that, python interpreter!
    top_pixel_time        = 0
    bottom_pixel_time     = 0
    upstream_pixel_time   = 0
    downstream_pixel_time = 0
    
    # Include this statement to ensure that the list of hits on the top is not empty
    if top_pixel_list != []:

        # See what 'top_pixel_list' looks like
        # It's not getting this far...
        # print "Top Pixel Hit List: ", top_pixel_list
        # print "\n"

        # Start a loop over 'top_pixel_list'
        for top_pixel_coord_group in top_pixel_list:

            # Define 'top_pixel_time', the time coordinate of the group of coordinates here
            top_pixel_time = top_pixel_coord_group[0]

            # Include an 'if' statement for the possibility of the time component being equal to 0, in which case this time has already been found
            if top_pixel_time == 0:

                # Continue onto the next 'top_pixel_coord_group' in 'top_pixel_list'
                continue

            if top_pixel_time == None:  # This is for the possibility that the empty list is entering the loop

                continue

            # Start a loop for coloring the matches cyan by using the uplane and vplane arrays
            for pixel in [top_pixel_coord_group[1], top_pixel_coord_group[2], top_pixel_coord_group[3]]:

                uplane_array[top_pixel_time][pixel] += 255
                vplane_array[top_pixel_time][pixel] += 255

     # Include this statement to ensure that the list of hits on the top is not empty                                                              
    if bottom_pixel_list != []:
    
        # Start a loop over 'bottom_pixel_list'
        for bottom_pixel_coord_group in bottom_pixel_list:

            # Define 'bottom_pixel_time', the time coordinate of the group of coordinates here
            bottom_pixel_time = bottom_pixel_coord_group[0]

            # Include an 'if' statement for the possibility of the time component being equal to 0, in which case this time has already been found
            if bottom_pixel_time == 0:

                # Continue onto the next 'bottom_pixel_coord_group' in 'bottom_pixel_list'
                continue
        
            if bottom_pixel_time == None:  # This is for the possibility that the empty list is entering the loop                                                                 
            
                continue
        
            # Start a loop for coloring the matches magenta by using the uplane and yplane arrays
            for pixel in [bottom_pixel_coord_group[1], bottom_pixel_coord_group[2], bottom_pixel_coord_group[3]]:
            
                uplane_array[bottom_pixel_time][pixel] += 127
                yplane_array[bottom_pixel_time][pixel] += 255

     # Include this statement to ensure that the list of hits on the top is not empty                                                          
    if upstream_pixel_list != []:
    
        # Start a loop over 'upstream_pixel_list'
        for upstream_pixel_coord_group in upstream_pixel_list:

            # Define 'upstream_pixel_time', the time coordinate of the group of coordinates here
            upstream_pixel_time = upstream_pixel_coord_group[0]

            # Include an 'if' statement for the possibility of the time component being equal to 0, in which case this time has already been found
            if upstream_pixel_time == 0:

                # Continue onto the next 'upstream_pixel_coord_group' in 'upstream_pixel_list'
                continue

            if upstream_pixel_time == None:  # This is for the possibility that the empty list is entering the loop                                                           

                continue

            # Start a loop for coloring the matches yellow by using the vplane and yplane arrays
            for pixel in [upstream_pixel_coord_group[1], upstream_pixel_coord_group[2], 0]:

                vplane_array[upstream_pixel_time][pixel] += 255
                yplane_array[upstream_pixel_time][pixel] += 255

    # Include this statement to ensure that the list of downstream hits is not empty

    if downstream_pixel_list != []:

        # Start a loop over 'downstream_pixel_list'
        for downstream_pixel_coord_group in downstream_pixel_list:

            # Define 'downstream_pixel_time', the time coordinate of the group of coordinates here
            downstream_pixel_time = downstream_pixel_coord_group[0]

            # Include an 'if' statement for the possibility of the time component being equal to 0, in which case this time has already been found
            if downstream_pixel_time == 0:

                # Continue onto the next 'downstream_pixel_coord_group' in 'downstream_pixel_list'
                continue

            if downstream_pixel_time == None:  # This is for the possibility that the empty list is entering the loop                                                            

                continue

            # Start a loop for coloring the pixels orange by using the vplane and yplane arrays
            for pixel in [downstream_pixel_coord_group[1], downstream_pixel_coord_group[2], 863]:

                uplane_array[downstream_pixel_time][pixel] += 100000
                vplane_array[downstream_pixel_time][pixel] += 100000
                yplane_array[downstream_pixel_time][pixel] += 100000


    # Return the three plane arrays of ADC values
    return [uplane_array, vplane_array, yplane_array]
