# Script that will perform clustering on the algorithm after taking in the lists of hits of each type for each event ##
import math
import rounding
import time_pixel_proximity_functions 

# Define a function that will add in quadrature the u, v, and y pixels, respectively, with their corresponding time unit
# The two input parameters are 'pixel_hit_dict', the dictionary of pixel hits, and 'dict_entry_len', the number of entries expected in each dictionary entry (to be used if the dictionary is empty)
# This function outputs the quadrature sum of all the different combinations of plane pixel and time, which must be unpacked upon use
def pixel_quadrature_sum(pixel_hit_dict, dict_entry_len):

    # Include different loops for if this (1) an upstream or downstream hit or (2) a top or bottom hit.  Use the length of the zeroth entry to make this determination (doesn't really matter because all of the lists have the same length)

    # First, include the default cases of an empty dictionary for both (1) a dictionary with four-dimensional entries and (2) and a dictionary with three-dimensional entries

    # Return an empty list of the right form so the program won't crash
    if pixel_hit_dict == {} and dict_entry_len == 3:

        return [[], []]

    # Do the same, but for a pixel dictionary in which you are expecting 4 members in each dictionary entry
    if pixel_hit_dict == {} and dict_entry_len == 4:

        return [[], [], []]
    
    # First, the case in which the zeroth entry (and therefore, all of the entries) have a length of three (upstream and downstream hits)
    if len(pixel_hit_dict[0]) == 3:

        # Define two lists: one for the u_pixels added in quadrature and one for the v_pixels added in quadrature
        u_hits_quadrature_sum = []
        v_hits_quadrature_sum = []

        # Loop over each of the hits in pixel_list_hits to unpack each list and compute the quadrature sum
        for i in pixel_hit_dict: # Remember, pixel_list_hits is a dictionary

            # Define the time, the u pixel, and the v pixel from the components of the dictionary at this entry
            time    = pixel_hit_dict[i][0]
            u_pixel = pixel_hit_dict[i][1]
            v_pixel = pixel_hit_dict[i][2]

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

        # Return the list of quadrature sums in a list format
        return [u_hits_quadrature_sum, v_hits_quadrature_sum]

    # Next, the case in which the zeroth entry (and therefore, all of the entries) have a length of four (top and bottom hits)
    if len(pixel_hit_dict[0]) == 4:

        # Define three lists: one for the u_pixels added in quadrature, one for the v_pixels added in quadrature, and one for the y_pixels added in quadrature (the quadrature sum is calculated with the time as well)
        u_hits_quadrature_sum = []
        v_hits_quadrature_sum = []
        y_hits_quadrature_sum = []

        # Loop over each of the hits in pixel_list_hits to unpack each list and compute the quadrature sum                                                                     
        for i in pixel_hit_dict: # Remember, pixel_list_hits is a dictionary                                                                                   

            # Define the time, the u pixel, and the v pixel from the components of the dictionary at this entry                                                                
            time    = pixel_hit_dict[i][0]
            u_pixel = pixel_hit_dict[i][1]
            v_pixel = pixel_hit_dict[i][2]
            y_pixel = pixel_hit_dict[i][3]

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


# Define a function that will define a set of centers for the quadrature sum by distinguishing them based on their distance from the existing centers
# This function will take in a list of coordinates, either in pixel units or in time, and return a list of centers from the list based on how far apart the pixels are from one another

# This function is meant to operate on the list of quadrature sums for each type of hit (ex.: top_u, top_v, upstream_u, etc.) separately, so it must be called multiple times upon total use
def center_list_finder(list, far_dist):

    # Define a list of centers, which here are just members of the list that are far enough away from other members of the list to be considered distinct
    center_list = []

    if list != []: # Append the first member of the input list to center_list, because this will be the first list member that we'll be comparing to the other members
       
        center_list.append(list[0])

        # Loop over the list as the outer loop
        for member in list:

            # Define a variable for the members of 'center_list' that are length = 'far_dist' away from the member of 'list' that is being looped over                   
            centers_far_away = 0

            # Loop over the center_list to compare the distance between the member of the list and each of the centers
            for center in center_list:
               
                if math.fabs(member - center) > far_dist:

                    centers_far_away += 1

                    # If the number of 'centers_far_away' = the length of center_list, then all of the centers are greater than far_dist away and so this member of list is distinct.  Append 'member' to 'center_list' if this is the case.
                    # This really should be at the same scope as the loop over the centers, like just within the loop over the 'list'
            if centers_far_away == len(center_list):
                       
                center_list.append(member)
    
    # Return center_list after all of its members have been added to it
    return center_list

# Define a function that will convert the pixel values to distance values (IN CM!!!).  I will choose the center of the pixel to be the point between the 2nd and 3rd wires that the pixel corresponds to.  The position of the pixel in units of 'cm' is = 0 cm for the first wire on the plane
def plane_pixel_to_distance(plane_pixel):

    return (plane_pixel * 1.2) + 0.6 # Plane pixel position in cm

# Define a function that will convert the time pixel values to distance values (IN CM!!!)
# The input variable is the time pixel
def time_pixel_to_distance(time_pixel):

    return ((time_pixel * 3) + 1.5) * 0.11 # Time pixel position in cm (0.11 is in units of cm/us)


# Define a function that will group each term of a list with the center that it is closest too
# 'list' is the list of pixels added in quadrature and 'list_of_centers' are the distinct pixels

# This function is meant to operate on the list of [time_pixel, plane_pixel] for each type of hit (ex.: top_u, top_v, upstream_u, etc.) separately, so it must be called multiple times upon total use
def center_assignment_quadrature_func(plane_pixel_list, quad_sum_list, list_of_centers):

    ### This function is contingent on the fact that the pixel is at the same point in 'plane_pixel_list' as its quadrature sum is at in 'quad_sum_list ###
    ### (Pending a test to be performed momentarily) ###

    # Define variables for the difference that two pixels (one, a candidate for being added to a list and the other, an existing member of that list) 
    time_spread = 10
    pixel_spread = 10

    # Define a minimum percent of [time, pixel] coordinates in the list that must be within the spreads of the [time, pixel] that I'm looping over to add the [time, pixel] to that particular list
    # (Start with 60%)
    min_percentage = 0.50

    # Define an empty list of lists for the contents of the input list organized by their closest center
    output_list = []

    # Define an iterator:
    i = 0

    # Use a loop to fill the output_list with the right number of empty lists (based on the quadrature sums)
    while i < len(list_of_centers):

        # Append an empty list
        output_list.append([])
        
        # Increment the iterator
        i += 1

    # Use a loop over 'quad_sum_list' and attach the member of 'plane_pixel_list' at the same index in 'plane_pixel_list' that 'quad_sum' is at in 'quad_sum_list'

    # Define an index over the elements of 'quad_sum_list' and 'plane_pixel_list'
    index = 0

    for quad_sum in quad_sum_list:

        # Define a variable, closest_center, which will change depending on which center is closest in the end
        # Initialize it to the first center in the list of centers     
        closest_center = list_of_centers[0]

        # Do a loop over the list_of_centers to find which center is the closest
        for center in list_of_centers:

            if math.fabs(quad_sum - center) < math.fabs(quad_sum - closest_center):

                closest_center = center

        # Now, fill the quad_sum into the same spot in output_list that closest_center is at in the center list:
        # Reset the iterator to 0
        i = 0

        # Define a boolean that tells if this iteration of 'index' (meaning this set of pixels)
        index_already_appended = False

        while i < len(list_of_centers):

            # Check to see if 'index_already_appended' is true, and 'break' if it is
            # Don't worry about the value of the index 'i' at this point
            # The index 'index' will still be incremented below, outside of this 'while' loop
            if index_already_appended == True:

                break

            # If 'closest_center' is equal to the entry at that point in 'list_of_centers', then you can consider the cases of where to append this 
            # // this set of coordinates in [time, pixel]
            if list_of_centers[i] == closest_center:

                # Just perform the normal procedure if the list hasn't been filled yet (this pixel will be the benchmark for the rest of the list)
                if output_list[i] == []:

                    # Append the quadrature sum onto the list with this index in 'output_list'
                    output_list[i].append(plane_pixel_list[index])
                    
                    # print "Output List After A Pixel Combo Was Added to an Empty List: ", output_list
                    # print "\n"

                    # Change the boolean value of 'index_already_appended' to 'True'
                    index_already_appended = True

                # This loop is to ensure that the pixel is at about the same time as the other pixels already in the list.  If it isn't, then you have to compare its time 
                # // component to the time components of the other pixels in the list
                else:

                    # *** Do things a little differently from the original 'barnes_pixel_clustering_2D_clustering.py' file by comparing this set of pixels to EVERY pixel within the lists to which it might be added, and then seeing how many of the pixels already in the list are close to the pixel in [time, coordinate] ****
                    
                    # Start off by defining a variable for the number of pixels in the given list that are within 'time_spread' and 'pixel_spread' of the set of pixels at the 'index' entry of 'plane_pixel_list'
                    num_of_pix_within_range = 0

                    # Use a loop over the index of the points in the 'inner_list' of 'output_list' and name it, correctly, 'inner_list'
                    inner_list = 0

                    # Start a loop over the members at this location of 'output_list' to compare this set of pixels with every set of pixel coordinates in this inner_list of 'output_list'
                    while inner_list < len(output_list[i]): 
                    
                    # This is the case when the pair of pixels in [time, pixel] is close in time to the first pixel in the already-partially-filled list and it's already confirmed that their quadrature sums are the closer than the difference between this pixel's quadrature sum and any of the other centers on the list
                        if math.fabs(plane_pixel_list[index][0] - output_list[i][inner_list][0]) < time_spread and math.fabs(plane_pixel_list[index][1] - output_list[i][inner_list][1]) < pixel_spread:

                            # Increment 'num_of_pix_within_range' because this pixel combo in 'output_list[i]' is within range
                            num_of_pix_within_range += 1

                        # Increment 'inner_list' (VERY IMPORTANT!!)
                        inner_list += 1

                    # Check to see if 'num_of_pix_within_range' divided by 'len(output_list[i])' is greater than 'min_percentage'
                    # If it is, then append (plane_pixel_list[index]) to 'output_list[i]'
                    if (float(num_of_pix_within_range)/float(len(output_list[i])) >= min_percentage):

                        output_list[i].append(plane_pixel_list[index])

                        # print "Output List After a Pixel Combo Was Added To A List That Already Has Elements: ", output_list
                        # print "\n"
                        
                        # Change the boolean value of 'index_already_appended' to 'True'                                                                                  
                        index_already_appended = True

                    # If there is not a number of pixels in the list corresponding to the 'quad_sum' that are close enough to the given pixel, then we have to loop through the entire list to perform the same search (skipping over the index in 'output_list' that's equal to 'i', of course)
                    # I'll use an 'elif' so that the loop doesn't enter into this loop after entering the previous one
                    elif (float(num_of_pix_within_range)/float(len(output_list[i])) < min_percentage):

                        # Loop over the other lists to see if, and which, of the other lists within 'output_list' have a higher percentage of close pixel combos than 'output_list[i]'
                        # If I find which of the other lists has the highest percentage of pixel combos, then I will be sure to only add this pixel set to one list
                        
                        # Define a 'highest_percentage_close_pixel_combos' and the index at which this occurs.  I want to see if it is in excess of 'min_percentage'.  The 
                        # // '..index' part will be set to 0 initially
                        highest_percentage_close_pixel_combos_index = 0

                        # I'll declare this up here just in case 'len(output_list[0])' is, indeed, equal to zero.  Then the program will know what function I am referencing. 
                        highest_percentage_close_pixel_combos = 0.
                        
                        # Define a variable for the number of pixels in this list that are close to the pixel at index 'index' in 'plane_pixel_list'
                        num_pix_in_zeroth_index_in_output_list_close_combo = 0

                        # Calculate the percentage of "close_pixel_combos" for the 0th entry in output_list (I think it should already be filled....) and then use this as the 
                        # // standard that the rest of the pixels have to overcome
                        for pixel_set in output_list[0]:

                            if math.fabs(pixel_set[0] - plane_pixel_list[index][0]) < time_spread and math.fabs(pixel_set[1] - plane_pixel_list[index][1]) < pixel_spread:

                                num_pix_in_zeroth_index_in_output_list_close_combo += 1

                        if len(output_list[0]) > 0: # This is my hedge against a crash caused by an empty 'output_list[0]'

                            # Set the value of 'highest_percentage_close_pixel_combos'
                            highest_percentage_close_pixel_combos = float(num_pix_in_zeroth_index_in_output_list_close_combo)/float(len(output_list[0]))
                        
                        # Define an iterator for output list 
                        output_list_iterator = 0

                        # Use a loop over the possible values of 'output_list_iterator' from 0 -> len(output_list) - 1
                        while output_list_iterator < len(output_list):

                            # If 'output_list_iterator' == i, as stated above, then I'll continue with the loop after incrementing the iterator to not repeat what I found above
                            # I also performed the loop once above for the first list in 'output_list' as a benchmark, so I can continue there as well
                            if output_list_iterator == i or output_list_iterator == 0:

                                output_list_iterator += 1

                                continue

                            # If the inner list is empty, then increment 'output_list_iterator' and 'continue'
                            if output_list[output_list_iterator] == []:
                                
                                output_list_iterator += 1

                                continue

                            # Set 'num_of_pix_within_range' to 0
                            num_of_pix_within_range = 0

                            # Set 'inner_list' to 0
                            inner_list = 0

                            # Start a 'while' loop over the values of 'inner_list' in 'output_list[output_list_iterator]'
                            while inner_list < len(output_list[output_list_iterator]):

                                # See if the pixel at this value of 'inner_list' in 'output_list[output_list_iterator]' is within the correct spreads from the pixel we're looping
                                # // over
                                if math.fabs(plane_pixel_list[index][0] - output_list[output_list_iterator][inner_list][0]) < time_spread and math.fabs(plane_pixel_list[index][1] - output_list[output_list_iterator][inner_list][1]) < pixel_spread:

                                    # Increment the value of 'num_of_pix_within_range'
                                    num_of_pix_within_range += 1

                                # Increment 'inner_list'
                                inner_list += 1
                                    
                            # Now, check to see if the percentage of this list's pixel combos close to the given set of pixels is greater than the percentage of the 0th index's list, and change the values of 'highest_percentage_close_pixel_combos_index' and 'highest_percentage_close_pixel_combos' if it is
                            if float(num_of_pix_within_range)/float(len(output_list[output_list_iterator])) > highest_percentage_close_pixel_combos:

                                # Change the value of 'highest_percentage_close_pixel_combos' to the current percentage use just above in the 'if' loop
                                highest_percentage_close_pixel_combos = float(num_of_pix_within_range)/float(len(output_list[output_list_iterator]))

                                # Change the value of 'highest_percentage_close_pixel_combos_index' to 'output_list_iterator'
                                highest_percentage_close_pixel_combos_index = output_list_iterator

                            # Increment 'output_list_iterator'
                            output_list_iterator += 1

                        # Check to see if 'highest_percentage_close_pixel_combos' is > 'min_percentage' and append 'plane_pixel_list[index]' if it is
                        if highest_percentage_close_pixel_combos > min_percentage:

                            output_list[highest_percentage_close_pixel_combos_index].append(plane_pixel_list[index])

                            # print "Output List After A Pixel Combo Was Appended To A Different List Than The One Corresponding To Its Quadrature Sum: ", output_list
                            # print "\n"

                            # Set 'index_already_appended' to 'True'
                            index_already_appended = True

                        # Now cover the final case: the one in which either (1) no percentage of close pixel combos was greater than that at the 0th index and that index's percentage is < 'min_percentage', or the highest percentage of close pixel combos other than the 0th index is less than < 'min_percentage' (both excluded by the previous 'if' statement)
                        else: 

                            # Make a new list and append 'plane_pixel_list[index]'
                            output_list.append([])
                            output_list[len(output_list) - 1].append(plane_pixel_list[index])

                            # print "Output List After A Pixel Combo Was Appended to a New List: ", output_list
                            # print "\n"

                # Print out the output list just to make sure that it is being filled the right way (right now it looks exactly like the averaged list 
                # generated below)
                # print "The output list looks like: ", output_list, "."
                # print "\n"

            # Increment the iterator
            i += 1

        # Increment the index
        index += 1

    # Print out 'output list'
    # print "Output List: "
    
    # print output_list

    # Print out a statement introducing the printing out of the rows of 'output_list'
    # print "Now, printing out the rows of output list...."

    # Use an iterator
    # row_num = 0

    # Print out each row of 'output_list' to see what the output currently looks like
    # for row in output_list:

        # Print out the row index and row
        # print "Row #", row_num, ":", row
        # print "\n" 
        
        # Increment the iterator
        # row_num += 1

    # Call the function that will determine if the coordinates in output list are close or far enough away (determined by the input parameters)
    while time_pixel_proximity_functions.are_all_pixel_lists_distinct(output_list, time_spread, pixel_spread, min_percentage) == False:

        # Combine the coordinates so that they are closer together
        output_list = time_pixel_proximity_functions.lists_of_identical_hit_combo(output_list, time_spread, pixel_spread, min_percentage)

    # Return 'output_list'
    return output_list

# Define a function that will average the lists in each of the entries of the list organized by the closest entry
# 'organized_list' - the list of pixels that are organized by the center that they are closest too
# 'plane_ADC_array' - the array of ADC values for each time and pixel of this event (for either the U, V, or Y plane)
def center_average_calculator(organized_list, plane_ADC_array):

    # Use an index to set the element of organized_list to the average of the contents of the list at the end
    i = 0

    # Use an outer loop over the lists within 'organized_list'
    # This will just return the original empty list if there is no 
    for inner_list in organized_list:

        # Include a failsafe against an empty 'inner_list' by just setting this point in 'organized_list' equal to [0, 0] (which won't be filled) and will prevent
        # that entry of the list from being 'NAN

        # This shouldn't be necessary....

        # if inner_list == []:

            # organized_list[i] = [0, 0]
            
            # This will allow the loop to continue without using any of the functions below
            # continue

        # Define a variable for the sum of the pixel ADC values corresponding to the [time, pixel] coordinates in 'organized_list'
        pixel_ADC_sum = 0

        # Define variables for the sums of the time and pixel components separately
        sum_time_times_ADC_value_inner_list  = 0
        sum_pixel_times_ADC_value_inner_list = 0

        # I should define the ADC weighted averages out here so that the function won't have problems with it
        ADC_weighted_average_time_inner_list  = 0
        ADC_weighted_average_pixel_inner_list = 0

        # Multiply each time and pixel element in 'inner_list' by the corresponding ADC value in 'plane_ADC_array' and take the sum
        # In the same loop, find the sum of the plane ADC values
        for elem in inner_list:

            pixel_ADC_sum += plane_ADC_array[elem[0]][elem[1]]

            # Print the pixel ADC sum as it is being filled
            # print "The pixel ADC value = %d." % plane_ADC_array[elem[0]][elem[1]]
            # print "The pixel ADC sum = %d." % pixel_ADC_sum
            # print "\n"

            # Add the first element of each list multiplied by the corresponding ADC plane array value, the time pixel * plane_ADC_array[elem[0]][elem[1]], to 'sum_time_inner_list' 
            sum_time_times_ADC_value_inner_list  += elem[0]*plane_ADC_array[elem[0]][elem[1]]

            # Add the second element of each list multiplied by the corresponding ADC plane array value, the plane pixel * plane_ADC_array[elem[0]][elem[1]], to 'sum_pixel_inner_list'
            sum_pixel_times_ADC_value_inner_list += elem[1]*plane_ADC_array[elem[0]][elem[1]]
        
        # If 'pixel_ADC_sum' == 0, then I'll reset the quantities above in a loop that will just take the normal average 
        # These pixels were all included in the input list because of the space charge effect, though none of them have charge themselves
        if pixel_ADC_sum == 0:

            # The two weighted sums are definitely 0 in this case, but as a sanity check I will set them both to zero again
            sum_time_times_ADC_value_inner_list  = 0
            sum_pixel_times_ADC_value_inner_list = 0

            for elem in inner_list:

                # Add the first element of each pair in a sum (this one is not weighted, because all of the ADC values are 0)
                sum_time_times_ADC_value_inner_list  += elem[0]

                # Add the second element of each pair in a sum (this one is not weighted, because all of the ADC values are 0)
                sum_pixel_times_ADC_value_inner_list += elem[1] 

        # Use print statements to see what the values of these quantities are before you calculated the weighted averages below
        # The next step is just to fill these pixels with 0s so the program won't crash
        # print "The sum of the pixel ADC values is: %d." % pixel_ADC_sum
        # print "The sum of the time pixels times the ADC value is: %d." % sum_time_times_ADC_value_inner_list
        # print "The sum of the plane pixels times the ADC value is: %d." % sum_pixel_times_ADC_value_inner_list
        # print "\n"

        # Calculate the time average with 'sum_time_times_ADC_value_inner_list' and 'pixel_ADC_sum' (if the pixel_ADC_value isn't 0)
        if pixel_ADC_sum != 0:

            # Calculate the weighted average of the times by dividing the wighted sum of the times by the ADC sum
            ADC_weighted_average_time_inner_list  = sum_time_times_ADC_value_inner_list  / pixel_ADC_sum 

            # Calculate the weighted average of the pixels by dividing the wighted sum of the pixels by the ADC sum
            ADC_weighted_average_pixel_inner_list = sum_pixel_times_ADC_value_inner_list / pixel_ADC_sum

        # Sloppy programming, but I have more than one 'if' statements above
        if pixel_ADC_sum == 0:

            # Calculate the NORMAL average, but still call the variable by the same name
            ADC_weighted_average_time_inner_list  = float(sum_time_times_ADC_value_inner_list) / float(len(inner_list))

            ADC_weighted_average_pixel_inner_list = float(sum_pixel_times_ADC_value_inner_list) / float(len(inner_list))

        # Now, set the entry previously occupied by 'inner_list' to the averages of the time components and pixel components of 'inner_list' just calculated                     
        # Convert this to an by rounding using the new rounding function, because it is a pixel value                                                                            
        organized_list[i] = [rounding.rounding_function(ADC_weighted_average_time_inner_list), rounding.rounding_function(ADC_weighted_average_pixel_inner_list)]

        # Increment the index to fill the appropriate position in 'organized_list' on the next iteration
        i += 1
        
    # After operating on 'organized_list', return it from this function
    return organized_list


        
    # print "Upstream Time Hits Averaged: ", up_time_hits_center_organized
    # print "Upstream U Hits Averaged: ", up_u_hits_center_organized
    # print "Upstream V Hits Averaged: ", up_v_hits_center_organized
    # print "\n"

    # print "Downstream Time Hits Averaged: ", down_time_hits_center_organized
    # print "Downstream U Hits Averaged: ", down_u_hits_center_organized
    # print "Downstream V Hits Averaged: ", down_v_hits_center_organized
    # print "\n"

    # print "Top Time Hits Averaged: ", top_time_hits_center_organized
    # print "Top U Hits Averaged: ", top_u_hits_center_organized
    # print "Top V Hits Averaged: ", top_v_hits_center_organized
    # print "Top Y Hits Averaged: ", top_y_hits_center_organized
    # print "\n"

    # print "Bottom Time Hits Averaged: ", bottom_time_hits_center_organized
    # print "Bottom U Hits Averaged: ", bottom_u_hits_center_organized
    # print "Bottom V Hits Averaged: ", bottom_v_hits_center_organized
    # print "Bottom Y Hits Averaged: ", bottom_y_hits_center_organized
    # print "\n"

    # return [up_time_hits_center_organized, up_u_hits_center_organized, up_v_hits_center_organized, down_time_hits_center_organized, down_u_hits_center_organized, down_v_hits_center_organized, top_time_hits_center_organized, top_u_hits_center_organized, top_v_hits_center_organized, top_y_hits_center_organized, bottom_time_hits_center_organized, bottom_u_hits_center_organized, bottom_v_hits_center_organized, bottom_y_hits_center_organized]
    

    
        
  
    

    
        
        


  




                


    
    

    
    
    

    
    

    

    

    
