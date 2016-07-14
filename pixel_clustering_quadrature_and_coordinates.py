## Script that will perform clustering on the algorithm after taking in the lists of hits of each type for each event ##
import math

# Define a function that will add in quadrature the u, v, and y pixels, respectively, with their corresponding time unit
def pixel_quadrature_sum(pixel_list_hits):

    # Include different loops for if this (1) an upstream or downstream hit or (2) a top or bottom hit.  Use the length of the zeroth entry to make this determination (doesn't really matter because all of the lists have the same length)
    
    # First, the case in which the zeroth entry (and therefore, all of the entries) have a length of three (upstream and downstream hits)
    if len(pixel_list_hits[0]) == 3:

        # Define two lists: one for the u_pixels added in quadrature and one for the v_pixels added in quadrature
        u_hits_quadrature_sum = []
        v_hits_quadrature_sum = []

        # Include an iterator for the length of the 'quad_sum' list
        quad_sum_list_len = 0

        # Loop over each of the hits in pixel_list_hits to unpack each list and compute the quadrature sum
        for pixel_group_hits in pixel_list_hits: # Remember, pixel_list_hits is a dictionary
            
            # Increment the length of 'quad_sum_list_len'
            quad_sum_list_len += 1

            # Define the time, the u pixel, and the v pixel from the components of the dictionary at this entry
            time    = pixel_list_hits[pixel_group_hits][0]
            u_pixel = pixel_list_hits[pixel_group_hits][1]
            v_pixel = pixel_list_hits[pixel_group_hits][2]

            # Make sure that the time and pixel values get converted to a distance value                                                                                       
            # print "Old Time Value: ", time
            # print "Old U Pixel Value: ", u_pixel
            # print "Old V Pixel Vaue: ", v_pixel

            # Convert each of these variables to a position in cm by using the functions 'plane_pixel_to_distance' and 'time_pixel_to_distance'
            time    = time_pixel_to_distance(time)
            u_pixel = plane_pixel_to_distance(u_pixel)
            v_pixel = plane_pixel_to_distance(v_pixel)

            # Load up on print statements to see how the time values compare to the plane values                                                                               
            # print "Time Value Converted to a Distance Value (in cm): ", time
            # print "U Pixel Value Converted to a Distance Value (in cm): ", u_pixel
            # print "V Pixel Value Converted to a Distance Value (in cm): ", v_pixel
            # print "\n"

            # Append the quadrature sum of these quantities onto the lists defined above
            u_hits_quadrature_sum.append(math.sqrt(math.pow(u_pixel, 2) + math.pow(time, 2)))
            v_hits_quadrature_sum.append(math.sqrt(math.pow(v_pixel, 2) + math.pow(time, 2)))

        # Print out the length of the 'quad_sum' list
        # print "Length of the Quad Sum List: ", quad_sum_list_len
        # print "\n"

        # Return the list of quadrature sums in a list format
        return [u_hits_quadrature_sum, v_hits_quadrature_sum]

    # Next, the case in which the zeroth entry (and therefore, all of the entries) have a length of four (top and bottom hits)
    if len(pixel_list_hits[0]) == 4:

        # Define three lists: one for the u_pixels added in quadrature, one for the v_pixels added in quadrature, and one for the y_pixels added in quadrature (the quadrature sum is calculated with the time as well)
        u_hits_quadrature_sum = []
        v_hits_quadrature_sum = []
        y_hits_quadrature_sum = []

        # Loop over each of the hits in pixel_list_hits to unpack each list and compute the quadrature sum                                                                     
        for pixel_group_hits in pixel_list_hits: # Remember, pixel_list_hits is a dictionary                                                                                    
            
            # Define the time, the u pixel, and the v pixel from the components of the dictionary at this entry                                                                
            time = pixel_list_hits[pixel_group_hits][0]
            u_pixel = pixel_list_hits[pixel_group_hits][1]
            v_pixel = pixel_list_hits[pixel_group_hits][2]
            y_pixel = pixel_list_hits[pixel_group_hits][3]

            # Make sure that the time and pixel values get converted to a distance value
            # print "Old Time Value: ", time
            # print "Old U Pixel Value: ", u_pixel
            # print "Old V Pixel Vaue: ", v_pixel
            # print "Old Y Pixel Value: ", y_pixel

            # Convert each of these variables to a position in cm by using the functions 'plane_pixel_to_distance' and 'time_pixel_to_distance'                                
            time    = time_pixel_to_distance(time)
            u_pixel = plane_pixel_to_distance(u_pixel)
            v_pixel = plane_pixel_to_distance(v_pixel)
            y_pixel = plane_pixel_to_distance(y_pixel)

            # Load up on print statements to see how the time values compare to the plane values
            # print "Time Value Converted to a Distance Value (in cm): ", time
            # print "U Pixel Value Converted to a Distance Value (in cm): ", u_pixel
            # print "V Pixel Value Converted to a Distance Value (in cm): ", v_pixel
            # print "Y Pixel Value Converted to a Distance Value (in cm): ", y_pixel
            # print "\n"
            
            # Append the quadrature sum of these quantities onto the lists defined above               
            u_hits_quadrature_sum.append(math.sqrt(math.pow(u_pixel, 2) + math.pow(time, 2)))
            v_hits_quadrature_sum.append(math.sqrt(math.pow(v_pixel, 2) + math.pow(time, 2)))
            y_hits_quadrature_sum.append(math.sqrt(math.pow(y_pixel, 2) + math.pow(time, 2)))

        # Return the list of quadrature sums in a list format
        return [u_hits_quadrature_sum, v_hits_quadrature_sum, y_hits_quadrature_sum]

# Define a function that will separate a list of pixel hits, in which each entry is a list with components [time, u_pixel, v_pixel, y_pixel], into a list of three lists of tuples: [[(u_pixel, time)], [(v_pixel, time)], [(y_pixel, time)]]
# The only input is the list of pixel hits
# This method will hinge on placing the tuple of (plane_pixel, time_pixel) in the same location in the tuple list that the quadrature sum of those two quantities is at in the 'plane_hits_quadrature_sum' in the previous function
# Just as in the function above, I have to include two separate 'if' statements to account for the upstream and downstream hits (three components in their 'pixel_list_hits') and, separately, the top and bottom hits (four components in their 'pixel_list_hits')
def pixel_time_list_gen(pixel_list_hits):

    # Identify a list of upstream or downstream hits based on the length of the first list within the input list
    if len(pixel_list_hits[0]) == 3:

        # Define a list of two lists, one for each type of tuple of the (pixel_number on the plane, time_pixel on the plane)
        pixel_time_lists = [[], []]

        # Start a loop over each entry of pixel_list_hits 
        for pixel_group_hits in pixel_list_hits: # Note that pixel_hit_group is an index in a dictionary, not a list of the pixel numbers 

            # Unpack the elements of the pixel_hit at this point in the dictionary
            time    = pixel_list_hits[pixel_group_hits][0]
            u_pixel = pixel_list_hits[pixel_group_hits][1]
            v_pixel = pixel_list_hits[pixel_group_hits][2]
            
            # Append each of these variables onto the appropriate list in pixel_time_list_of_tuples
            # First List: u_pixel and time tuples, Second List: v_pixel and time tuples

            pixel_time_lists[0].append([time, u_pixel])
            pixel_time_lists[1].append([time, v_pixel])

    # Identify a list of top or bottom hits based on the length of the first list within the input list                                                            
    if len(pixel_list_hits[0]) == 4:

        # Define a list of three lists, one for each type of tuple of the (plane_pixel_number, time)                                                                           
        pixel_time_lists = [[], [], []]

        # Start a loop over each entry of pixel_list_hits                                                                                                                   
        for pixel_group_hits in pixel_list_hits: # Note that pixel_hit_group is an index in a dictionary, not a list of the pixel numbers                                     
            
            # Unpack the elements of the pixel_hit at this point in the dictionary                                                                                             
            time    = pixel_list_hits[pixel_group_hits][0]
            u_pixel = pixel_list_hits[pixel_group_hits][1]
            v_pixel = pixel_list_hits[pixel_group_hits][2]
            y_pixel = pixel_list_hits[pixel_group_hits][3]

            # Append each of these variables onto the appropriate list in pixel_time_list_of_tuples                                                                           
            # First List: u_pixel and time tuples, Second List: v_pixel and time tuples, Third List: y_pixel and time tuples                                      
            pixel_time_lists[0].append([time, u_pixel])
            pixel_time_lists[1].append([time, v_pixel])
            pixel_time_lists[2].append([time, y_pixel])
       
    # Return the list that I have created

    # Print out the length of pixel_time_lists (this time for when the upstream function is called)
    # print "Length of the U Upstream Pixel Time Lists: ", len(pixel_time_lists[0])
    # print "\n"
    
    return pixel_time_lists


# Define a function that will take in a list of the quadrature sum of the pixels, a list of the tuples of the time and the pixel on this plane, and 'far_dist', the distance between two pixel quadrature sums that is far enough to consider them unique
# This function will group the pixels according to their quadrature sum and return an average of the pixel value and time in the tuple 
# Note that this only takes the list of tuples for ONE pixel and the quadrature list for ONE type of pixel.  I'll have to unpack the output from the previous two functions in order to use this one
def pixel_time_clustering(pixel_quad_sum_list, list_of_pixels_and_times, far_dist):

    # Define a list of centers, which here are just members of the list that are far enough away from other members of the list to be considered distinct
    pixel_quad_sum_center_list = []

    # Append the first member of the input list to 'pixel_quad_sum_center_list', because this will be the first list member that we'll be comparing to the other members
    pixel_quad_sum_center_list.append(pixel_quad_sum_list[0])

    # Loop over the list as the outer loop
    for member in pixel_quad_sum_list:

        # Define a variable for the members of 'pixel_quad_sum_center_list' that are length = far_dist away from the member of 'pixel_quad_sum_list' that is being looped over  
        centers_far_away = 0

        # Loop over 'pixel_quad_sum_center_list' to compare the distance between the member of the list and each of the centers
        for center in pixel_quad_sum_center_list:

            if math.fabs(member - center) > far_dist:

                centers_far_away += 1

            # If the number of 'centers_far_away' = the length of 'pixel_quad_sum_center_list', then all of the centers are greater than far_dist away and so this member of list is distinct.  Append 'member' to 'center_list' if this is the case.
            if centers_far_away == len(pixel_quad_sum_center_list):

                pixel_quad_sum_center_list.append(member)

    # Now, using the length of the pixel_quad_sum_center_list, make one new list in which to sort the pixel_quad_sum_centers and another in which to return the average of the tuples of plane pixels and time pixels that are assigned to that center
    pixel_quad_centers_organized = []
    time_and_pixel_list_avgs     = []

    # Fill the 'pixel_quad_centers_organized' list with the correct number of empty lists depending on the length of 'pixel_quad_sum_center_list'
    # Fill the 'time_and_pixel_tuple_avgs' with tuples of 0s that can later be replaced with the tuple of the average pixel number and average time that correspond to that pixel_quad_center
    # Use an index to loop over the entries of 'pixel_quad_sum_center_list' 
    j = 0

    # Begin the loop
    while j < len(pixel_quad_sum_center_list):

        # Fill both of the lists
        pixel_quad_centers_organized.append([])
        time_and_pixel_list_avgs.append([0, 0])

        # Increment the iterator
        j += 1

    # Use an index to tell which value of 'pixel_quad_sum_list' we're on                                                                                                         
    i = 0

    # Now that both of the lists are initialized, fill them with the pixel_quad_centers_organized and change the average pixel and time in the tuple at that point on the list
    for pixel_quad in pixel_quad_sum_list: # This is a loop over a list, so the elements are the components of pixel_quad_sum_list

        # Initialize a variable for the closest center to the pixel_quad that the loop is going over.  Start the loop at the first center in the list.
        closest_center = pixel_quad_sum_center_list[0]

        # Initialize a loop over the centers
        for center in pixel_quad_sum_center_list:

            # Compare the distance from this center to pixel_quad with the distance from 'closest_center' to 'pixel_quad'
            if math.fabs(pixel_quad - center) < math.fabs(pixel_quad - closest_center):

                # Change 'closest_center' so that it's equal to the new center if the loop passes this 'if' statement
                closest_center = center

        # At the end of this loop, the value of 'closest_center' is equal to the center that is closest to this pixel_quad
        # Now, the fact that the the pixels & time in the tuple are in the same position as the quadrature sum of their centers and their time will be taken advantage
        # of here

        # Use a loop to find out which center 'closest_center' ended up being, and append this center to that position in the 'pixel_quad_centers_organized' list
        # Declare an index
        j = 0

        while j < len(pixel_quad_sum_center_list):

            if closest_center == pixel_quad_sum_center_list[j]:

                # Assign the pixel_quad sum to the same spot in 'pixel_quad_centers_organized' that 'closest_center' is at in 'pixel_quad_sum_center_list'
                pixel_quad_centers_organized[j].append(pixel_quad)

                # Recalculate the average of the time and plane pixel values for this center's cluster in 'time_and_pixel_tuple_avgs'
                # Initially use variables for the time and the pixels, but then put them into the 'time_and_pixel_list_avgs' list after rounding them correctly

                # To calculate this average correctly, convert all of the quantities involved to floats

                # This first line will recalculate the average time for this collection of pixels using the time corresponding to this quadrature_sum_center
                time  = (((float(len(pixel_quad_centers_organized[j])) - 1.0) * float(time_and_pixel_list_avgs[j][0])) + float(list_of_pixels_and_times[i][0])) / float(len(pixel_quad_centers_organized[j]))

                # This second line will recalculate the average time for this collection of pixels using the pixel corresponding to this quadrature_sum_center
                pixel = (((float(len(pixel_quad_centers_organized[j])) - 1.0) * float(time_and_pixel_list_avgs[j][1])) + float(list_of_pixels_and_times[i][1])) / float(len(pixel_quad_centers_organized[j]))

                # Now check to see if the decimal parts of time and pixel are greater than 0.5 for the rounding to overcome the nature of the python 'int' function

                # Round up to the next integer if the decimal part of 'time' is greater than 0.5
                if (time - int(time)) >= 0.5:

                    time = int(time) + 1

                # Otherwise, the 'int' function will just round the function down to the next lowest integer (sloppy programming, but I have to include another 'if' statement
                # // instead of an 'else' because there will be a loop right afterward for the 'pixel' quantity)
                if (time - int(time)) < 0.5:

                    time = int(time)

                # Round up to the next integer if the decimal part of 'pixel' is greater than 0.5                                                                           
                if (pixel - int(pixel)) >= 0.5:

                    pixel = int(pixel) + 1
    
                # Otherwise, the 'int' function will just round the function down to the next lowest integer
                if (pixel - int(pixel)) < 0.5:

                    pixel = int(pixel)

                # Now, set the appropriate entries in 'time_and_pixel_list_avgs' equal to 'time' and 'pixel' before continuing with the loop
                time_and_pixel_list_avgs[j] = [time, pixel]
                
            # Increment the j iterator
            j += 1

        # Increment the i iterator
        i += 1

    # Define an index for use in this next function
    k = 0

    # Now, combine the centers in 'pixel_quad_centers_organized' into an average 
    for center_list in pixel_quad_centers_organized:

        # Define the sum and average of the centers here
        sum = 0
        avg = 0

        # Loop over the components of 'center_list' to sum them
        for center in center_list:

            sum += center
            
        # Calculate the average of the components of 'center_list'
        avg = sum/len(center_list)

        # Set the value of the 'pixel_quad_centers_organized' at this point to 'avg', replacing the list
        pixel_quad_centers_organized[k] = avg

        # Increment the iterator
        k += 1

    # Return the averaged list of centers and time_and_pixel_list_avgs
    return [pixel_quad_centers_organized, time_and_pixel_list_avgs]


# Define a function that will convert the pixel values to distance values (IN CM!!!).  I will choose the center of the pixel to be the point between the 2nd and 3rd wires that the pixel corresponds to.  The position of the pixel in units of 'mm' is = 0 mm for the first wire on the plane
def plane_pixel_to_distance(plane_pixel):

    return (plane_pixel*1.2) + 0.6 # Plane pixel position in cm

# Define a function that will convert the time pixel values to distance values (IN CM!!!)
# The input variable is the time pixel
def time_pixel_to_distance(time_pixel):

    return ((time_pixel * 3) + 1.5) * 0.11 # Time pixel position in cm



    

    
        
  
    

    
        
        


  




                


    
    

    
    
    

    
    

    

    

    
