## Script that will perform clustering on the algorithm after taking in the lists of hits of each type for each event ##
import math
import rounding

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

    return (plane_pixel*1.2) + 0.6 # Plane pixel position in cm

# Define a function that will convert the time pixel values to distance values (IN CM!!!)
# The input variable is the time pixel
def time_pixel_to_distance(time_pixel):

    return ((time_pixel * 3) + 1.5) * 0.11 # Time pixel position in cm


# Define a function that will group each term of a list with the center that it is closest too
# 'list' is the list of pixels added in quadrature and 'list_of_centers' are the distinct pixels

# This function is meant to operate on the list of [time_pixel, plane_pixel] for each type of hit (ex.: top_u, top_v, upstream_u, etc.) separately, so it must be called multiple times upon total use
def center_assignment_quadrature_func(plane_pixel_list, quad_sum_list, list_of_centers):

    ### This function is contingent on the fact that the pixel is at the same point in 'plane_pixel_list' as its quadrature sum is at in 'quad_sum_list ###
    ### (Pending a test to be performed momentarily) ###

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

        # Now, fill the quad_sum into the same spot in output_list that closest_center is at in teh center list:
        # Reset the iterator to 0
        i = 0

        while i < len(list_of_centers):

            # If 'closest_center' is equal to the entry at that point in 'list_of_centers', then you can consider the cases of where to append this 
            # // this set of coordinates in [time, pixel]
            if list_of_centers[i] == closest_center:

                # Just perform the normal procedure if the list hasn't been filled yet (this pixel will be the benchmark for the rest of the list)
                if output_list[i] == []:

                    # Append the quadrature sum onto the list with this index in 'output_list'
                    output_list[i].append(plane_pixel_list[index])

                # This loop is to ensure that the pixel is at about the same time as the other pixels already in the list.  If it isn't, then you have to compare its time 
                # // component to the time components of the other pixels in the list
                else:

                    # This is the case when the pair of pixels in [time, pixel] is close in time to the first pixel in the already-partially-filled list and it's already confirmed that their quadrature sums are the closer than the difference between this pixel's quadrature sum and any of the other centers on the list
                    if math.fabs(plane_pixel_list[index][0] - output_list[i][0][0]) < 10:

                        output_list[i].append(plane_pixel_list[index])

                    # If this is not the case, then see if ANY of the time components are within ten pixel spots of this pixel. Failing that, append a new list and add this set of pixels onto that
                    else:

                        # Loop through the output list through the ENTIRE length of the output list to see if there is a time component close
                        # (within 10) of 'plane_pixel_list[index][0]' and also closer than any of the other time components
                        closest_time_component = output_list[0][0][0] # This is the time component of the first element of the first element of 'output_list'

                        # Define an iterator
                        output_list_iterator = 0

                        # Define a boolean for if none of the time components of the output_list pixels (at the start of the list) are within 10 of the current value
                        # // plane_pixel_iterator[index][0]
                        are_within_ten = False

                            # See if the current set of pixels is close to any of the ones already appended in 'output_list'
                        while output_list_iterator < len(output_list):

                            # Add print statements to see what the problem is
                            # print "Value of 'output_list_iterator': %d." % output_list_iterator
                            # print "Length of 'output_list': %d." % len(output_list)
                            # print "Value of Index: %d." % index

                            # print "'plane_pixel_list' = ", plane_pixel_list
                            # print "\n"
                            # print "'output_list' = ", output_list
                            # print "\n"

                            if output_list[output_list_iterator] != []:

                                if math.fabs(plane_pixel_list[index][0] - output_list[output_list_iterator][0][0]) < 10: # Only consider time components that are within 10 of 'plane_pixel_list[index][0]
                                    # Change the value of the Boolean to 'true' (there will be one pixel within 10 time component spots of this one, at least)
                                    # Even if the 'if' statement below is not satisfied because only the time component of the first element of the first list of 'output_list' is less than ten, 'are_within_ten' will become True
                                    are_within_ten = True
                                
                                    if math.fabs(output_list[output_list_iterator][0][0] - plane_pixel_list[index][0]) < math.fabs(closest_time_component - plane_pixel_list[index][0]):

                                            closest_time_component = output_list[output_list_iterator][0][0]
                                        
                            # Increment 'output_list_iterator'
                            output_list_iterator += 1

                        # Now, loop through 'output_list' and append 'plane_pixel_list[index]' in the same list as 'closest_time_component'
                        # First, ensure that 'are_within_ten' is True
                        if are_within_ten == True:

                            # Reset 'output_list_iterator'
                            output_list_iterator = 0

                            # Loop through 'output_list_iterator'
                            while output_list_iterator < len(output_list):

                                if output_list[output_list_iterator] != []:

                                    # See which time component of the first member of each list is actually the 'closest_time_component'
                                    if output_list[output_list_iterator][0][0] == closest_time_component:

                                        # Append this set of pixels at this point in 'output_list'
                                        output_list[output_list_iterator].append(plane_pixel_list[index])

                                # Increment the iterator
                                output_list_iterator += 1
                                

                        # This is the case in which there are no time pixels in any of the first entries of 'output_list' that are close (within 10 pixel spots) of 'plane_pixel_list[index][0]'
                        else: 

                            # Make a new list and append 'plane_pixel_list[index]'
                            output_list.append([])
                            output_list[len(output_list) - 1].append(plane_pixel_list[index])

                # Print out the output list just to make sure that it is being filled the right way (right now it looks exactly like the averaged list 
                # generated below)
                # print "The output list looks like: ", output_list, "."
                # print "\n"

            # Increment the iterator
            i += 1

        # Increment the index
        index += 1

    # Print out 'output list'
    print "Output List: "
    
    print output_list

    # Print out a statement introducing the printing out of the rows of 'output_list'
    print "Now, printing out the rows of output list...."

    # Use an iterator
    row_num = 0

    # Print out each row of 'output_list' to see what the output currently looks like
    for row in output_list:

        # Print out the row index and row
        print "Row #", row_num, ":", row
        print "\n" 
        
        # Increment the iterator
        row_num += 1

    print_out_this = True

    if print_out_this == True:

        # Declare a new list for the new output list
        output_list_improved = []
        
        # Declare an empty list for the indices at which to continue in the loop (these lists have already been added)
        list_of_indices_to_continue = []

        # Declare an outer index
        outer_index = 0
        
        # Before returning the output list, you should check to see if each of the lists are close to others in terms of the time coordinates and combine them into the same list (so that there'll be less dots in the middle of nowhere)
        for outer_list in output_list:

            # I'm going to put this break statement in here just to see if this will be a temporary solution to the outer index becoming too large
            if outer_index > len(output_list):

                break

            # Include a boolean that will be set to True when the 'outer_list' has already been added (less output)                                   
            outer_list_added = False

            print "The outer list that I'm looping over is: ", outer_list, " at index #%d." % outer_index

            if outer_index == 2:

                print "WHOOP! WHOOP! WHOOP! This is the print statement that you're looking for.  This is a repeat." 

            # print "I'm entering into the outer list loop with the following outer list: ", outer_list
            # print "\n"
            
            # Declare a boolean that will have to be 'False' to go forward with looping over this iteration of the list
            outer_repeat = False

            # See if you should continue over any of the values in 'list_of_indices_to_continue' 
            for outer_continuing_index in list_of_indices_to_continue:
                
                if outer_index == outer_continuing_index:

                    # print "outer_index: ", outer_index
                    # print "outer_continuing_index: ", outer_continuing_index
                    # print "\n"

                    outer_repeat = True

            # Continue if 'outer_repeat' == True
            if outer_repeat == True:

                # Print out a statement if the function is an outer repeat
                print "OUTER REPEAT! INCREMENTING THE OUTER INDEX."
                # print "\n"
                outer_index += 1

                # print "Outer repeat - continuing!"

                # Continue.  Note that this will continue the OUTER LOOP, not the 'for' loop just above this 'if' statement
                continue

            # Declare an inner index
            inner_index = 0

            # Start another loop over 'output_list' if the loop passed the last loop
            for inner_list in output_list:

                # This will only print out if the 'outer_list' hasn't been added to 'output_list_improved' yet                                                                   
                print "The inner list that I'm looping over is: ", inner_list, " at index #%d." % inner_index

                # I'm going to use a similar 'break' statement as above to end the loop if 'inner_index' becomes too great
                if inner_index > len(output_list):

                    break

                # if 'outer_list_added' == True, then you can just continue.  This will make the program work faster.
                if outer_list_added == True:

                    # You can increment 'inner_index' just for bookeeping purposes, but it doesn't matter because it's reset before the next loop
                    print "THE OUTER LOOP HAS ALREADY BEEN MATCHED.  INCREMENTING THE INNER INDEX!"

                    inner_index += 1

                    # If 'inner_index' is equal to the length of 'output_list', then you should increment the outer index
                    # The loop over the 'inner_list' is going to break over the next iteration, so you have to increment the outer index as well
                    if inner_index == len(output_list):

                        print "LOOP OVER INNER INDEX IS FINISHED! OUTER INDEX INCREMENTED."
                        outer_index += 1

                    continue

                # print "\n"

                # print "I'm entering into the inner list loop with the following inner list: ", inner_list
                # print "\n"

                # Continue immediately if the inner_index is the same as the outer_index
                if inner_index == outer_index:

                    # Increment 'inner_index' and continue
                    # inner_index += 1

                    print "THE INNER INDEX EQUALS THE OUTER INDEX - INNER INDEX INCREMENTED!!"

                    inner_index += 1
                
                    # Continue
                    continue

                # print "The inner list is the same as the outer list.  Continuing!"
                # print "\n"

                # Declare a boolean that will have to be 'False' to go forward with looping over this iteration of the list
                inner_repeat = False

                # Repeat the loop from outside to see if this index has been used before
                for inner_continuing_index in list_of_indices_to_continue:

                    if inner_index == inner_continuing_index:

                        # print "inner_index: ", inner_index
                        # print "inner_continuing_index: ", inner_continuing_index
                        # print "\n"
                        
                        inner_repeat = True
                        
                # Continue if 'inner_repeat' == True
                if inner_repeat == True:
                    
                    # print "The inner list is a repeat.  Continuing!"
                    # print "\n"

                    # Increment the index before continuing!
                    # inner_index += 1

                    # print "INNER REPEAT - CONTINUING!"

                    # Continue (with the inner loop)
                    print "INNER REPEAT! INCREMENTING THE INNER INDEX."

                    inner_index += 1

                    continue

                # print "outer_list[0][0] (before the 'if' statement): ", outer_list[0][0], "."
                # print "inner_list[0][0] (before the 'if' statement): ", inner_list[0][0], "."
                # print "\n"

                # If the loop makes in this far, compare the time coordinates of the first elements of the two lists to see if they are less than 10 time pixel units
                # This means that 'outer_index' != 'inner_index' and the lists have not been concatenated with other lists before
                if math.fabs(outer_list[0][0] - inner_list[0][0]) <= 10 and math.fabs(outer_list[0][1] - inner_list[0][1]) <= 10:

                    # print "The 'output_list_improved' loop is making it this far and is filled (this is inside the 'if' statement)."
                    # print "outer_list[0][0] = ", outer_list[0][0], "."
                    # print "inner_list[0][0] = ", inner_list[0][0], "."
                    # print "\n"

                    print "Hooray!  Two lists are close enough in time and pixel coordinates to be concatenated!"
                    print "The two lists being joined together are: ", inner_list, "and ", outer_list, "."
                    # print "\n"

                    # Add the two lists together and place them into 'output_list_improved'
                    output_list_improved.append(inner_list + outer_list)

                    # print "The outer_index to be appended to the end of the list is: %d." % outer_index
                    # print "The inner_index to be appended to the end of the list is: %d." % inner_index
                    # print "\n" 

                    # Append both of the indices onto 'list_of_indices_to_continue'

                    print "I'm appending", outer_index, "and ", inner_index, "to the list of indices at which to continue."

                    list_of_indices_to_continue.append(outer_index)
                    list_of_indices_to_continue.append(inner_index)

                    # Increment both of the indices
                    # print "Both indices are being incremented.  The output list has been filled."

                    print "INNER AND OUTER INDICES INCREMENTED!!"
                    print "\n"
                    inner_index += 1

                    # Don't increment the 'outer_index' here.....
                    # outer_index += 1

                    if inner_index == len(output_list) + 1:

                        print "WHOOP! WHOOP! WHOOP! The inner index is out of range and was appended to the 'list_of_indices_to_continue'."
                        return 0

                    if outer_index == len(output_list) + 1:

                        print "WHOOP! WHOOP! WHOOP! The outer index is out of range and was appended to the 'list_of_indices_to_continue'."
                        return 0

                    # Set 'outer_list_added' to 'True'
                    outer_list_added = True

                    # Continue in the inner loop
                    continue

                # If the loop makes it this far, then you should increment 'inner_index'.  This list was not looped over or added to the outer index.
                print "INNER INDEX WAS NOT MATCHED TO THIS LIST.  INNER INDEX INCREMENTED!"
     
                inner_index += 1


                # Include a loop inside 'outer_list' that will see if the list is close to any of the existing entries inside 'output_list_improved' (in the event that there are 
                # // three or more lists with a time component that is close)

            # You have to continue with the loop if 'outer_list_added' has already been set to true. Otherwise, you'll enter the loop below without going back to 
            # // the top of the outer loop
            if outer_list_added == True:

                # Continue to the top of the outer loop
                print "THIS OUTER LIST HAS ALREADY BEEN ADDED TO 'output_list_improved'.  CONTINUING!"
                print "The index in the 'outer_list_added' loop is: ", outer_index, "."
                print "\n"
                continue

            # Add an angry return statement if the function reaches this point with index 
        
            # Define an index to do this the easiest way
            extra_index = 0

            # Define a boolean as "False" that will switch to "True" if the list is added to two other lists in the loop
            added_to_existing_output_lists = False

            for added_list in output_list_improved:

                # if extra_index != 0:

                    # extra_index += 1

                if math.fabs(outer_list[0][0] - added_list[0][0]) <= 10 and math.fabs(outer_list[0][1] - added_list[0][1]) <= 10:

                    # Make the new entry of 'output_list_improved' at 'extra_index' equal to 'added_list + outer_list'
                    output_list_improved[extra_index] = added_list + outer_list

                    print "There are three or more lists that are close in time and pixel coordinates!"
                    print "The index of the list being added to the existing lists in 'output_list_improved' is: ", outer_index, "."
                    print "The list being added to the existing list in 'output_list_improved' is: ", outer_list, "."
                    print "The list being added to 'output_list_improved' is ", added_list + outer_list, "."
                    # print "\n"

                    # Put outer index into the 'list_of_indices_to_continue'
                    list_of_indices_to_continue.append(outer_index)

                    if outer_index == len(output_list) + 1:

                        print "WHOOP! WHOOP! WHOOP! The outer index is out of range and was appended to the 'list_of_indices_to_continue'."
                        return 0

                    # Increment 'outer_index' and break

                    # print "OUTER INDEX INCREMENTED!!"
                    # outer_index += 1
                    
                    # This will be used to continue the 'outer_list'
                    added_to_existing_output_lists = True

                    # This will break the loop above, because the list has already been appened to a list
                    break

                # Increment 'extra_index' in the event that the member of 'outer_list' is not appended to other lists in 'outer_list_improved'
                extra_index += 1

            # You want to continue if 'added_to_existing_output_lists' is 'True' (the 'output_list_improved' loop should have already broken by now)
            if added_to_existing_output_lists == True:

                print "This list was added to two other lists."
                print "OUTER INDEX INCREMENTED!!"
                print "\n"

                outer_index += 1

                continue

            # If the loop makes it here to the end, then you should increment 'outer_index'
            print "OUTER INDEX HAS NO MATCHES. OUTER INDEX INCREMENTED!!"
            print "\n"
            outer_index += 1

        # Print the list of indices at which to continue
        # These are the indices of lists that have been added with other lists
        print "The list of indices at which to continue are: ", list_of_indices_to_continue, "."
        print "\n"

        # Use one final loop to set the lists within 'output_list' that are not close in coordinates to one another just so all of the lists are represented 
        # Define an iterator for 'output_list'
        final_iterator = 0

        while final_iterator < len(output_list):

            # print "'final_iterator' = ", final_iterator

            # if final_iterator != 0: # The loop will continue forever because of this if it is stuck on 0

                # final_iterator += 1

            # Make sure that 'final_iterator' is not greater than len(output_list) either
            if final_iterator > len(output_list):

                break

            # Declare a boolean that will tell us whether to loop over a certain index because the list that it corresponds to was added in the previous loop
            loop_over = False

            for indices_to_skip in list_of_indices_to_continue:

                # print "'final_iterator' = ", final_iterator
                # print "'indices_to_skip' = ", indices_to_skip
                # print "\n"

                if final_iterator == indices_to_skip:

                    # Make the boolean True
                    loop_over = True

            # Continue over this loop if 'loop_over' is True
            if loop_over == True:

                # Increment 'final_iterator'

                print "'final_iterator': ", final_iterator
                print "INDEX HAS ALREADY BEEN ADDED TO 'output_list_improved'. FINAL ITERATOR INCREMENTED!"
                print "\n"

                final_iterator += 1

                # Continue on with the loop because this index was added to another list and placed into 'output_list_improved'
                continue

            # Include a print statement for the list within 'output_list' that you're appending (this will be most of the lists from 'output_list')
            # print "I'm appending the following list that was never concatenated with another list: ", output_list[final_iterator], "."
            # print "\n"

            # If the loop has made it this far, then append 'output_list[final_iterator]' onto the 'output_list_improved' 
            output_list_improved.append(output_list[final_iterator])

            print "'final_iterator'", final_iterator
            print "The list being added to the output list that was not added to other lists is: ", output_list[final_iterator], "."
            print "\n"

            # YOU HAVE TO ADD THIS INDEX ONTO 'list_of_indices_to_continue'!!! Otherwise the loop will never stop.
            list_of_indices_to_continue.append(final_iterator)

            # Increment 'final_iterator'

            # print "Final iterator is being incremented!!"
            final_iterator += 1

    # Print out the old list, altogether and in row format
    # print "Old List: ", output_list_improved

    # old_list_row_iterator = 0

    # for row in output_list_improved:

        # print "Row #", old_list_row_iterator, ":", row
        # print "\n"
        # old_list_row_iterator += 1

    # I will add ONE MORE LIST just to clean things up a bit

    # Declare an empty, new list, 'output_list_platinum', that will hold the final version of the list after it's been cleaned up a bit
    output_list_platinum = []

    # Declare an empty list of the coordinates in time and plane pixel that are close to one another
    list_of_close_list_coords = []

    # Declare an index for the outer loop, 'outer_loop_index'
    outer_loop_index = 0

    # I'm going to loop through 'output_list_improved' with an outer list and an inner list, and then add the list numbers that are close in coordinates
    for outer_list in output_list_improved:

        # Print Statement
        print "I'm currently iterating over the outer list ", outer_list, "at index #", outer_loop_index, "."

        # Define a boolean for if the outer list is already added to another list
        outer_list_previously_added = False

        # Include this 'break' statement as a failsafe
        if outer_loop_index > (len(output_list_improved) - 1):

            break

        # I'm going to do as above - define a boolean to see if the index has already been added to 'list_of_close_list_coords' as an inner list
        outer_index_already_added = False

        for already_appended_index in list_of_close_list_coords:

            if already_appended_index == outer_loop_index:

                outer_index_already_added = True

        # Check to see if 'index_already_added' is 'True'.  If it is, increment 'outer_loop_index' and continue
        if outer_index_already_added == True:

            # Increment 'outer_loop_index'
            outer_loop_index += 1

            print "OUTER LOOP ALREADY APPENDED.  CONTINUING!"
            print "\n"

            # Continue
            continue 

        # Define an index for the inner loop
        inner_loop_index = 0

        # Start the inner loop over 'output_list_improved'
        for inner_list in output_list_improved:

            # Print Statement                                            
            print "I'm currently iterating over the inner list ", inner_list, "at index #", inner_loop_index, "."

            # Include a 'break' statement as a failsafe
            if inner_loop_index > (len(output_list_improved) - 1):

                print "INNER LOOP BREAKING!!"
                break

            # See if the outer list has already been added                                                                                              
            if outer_list_previously_added == True:

                inner_loop_index += 1

                if inner_loop_index <= (len(output_list_improved) - 1):

                    print "OUTER LIST PREVIOUSLY APPENDED.  CONTINUING!"
                    # print "\n"
                    
                    # This will continue with the 'inner_list' loop
                    continue

                else:

                    # This will increment the outer_loop_index and then continue so that 'outer_loop_index' gets incremented

                    print "OUTER LIST PREVIOUSLY APPENDED.  CONTINUING onto the next outer loop iteration!"
                    print "Inner Loop Index: ", inner_loop_index, "."
                    # print "\n"
                    outer_loop_index += 1

                    continue

            # First, continue if 'inner_loop_index' is the same as 'outer_loop_index'
            if inner_loop_index == outer_loop_index:

                # Print Statement
                print "THE INNER INDEX EQUALS THE OUTER INDEX.  CONTINUING!!"
                # print "\n"

                # Increment the inner_loop_index first
                inner_loop_index += 1

                # Continue
                continue

            # Do the same as above to see if this index has been added already to the 'list_of_close_list_coords' and therefore to not add it again
            inner_index_already_added = False

            for inner_already_appended_index in list_of_close_list_coords:

                if inner_already_appended_index == inner_loop_index:

                    inner_already_appended_index = True

            # Check to see if 'inner_index_already_added' is 'True'.  If it is, increment 'inner_loop_index' and continue
            if inner_index_already_added == True:

                print "INNER INDEX PREVIOUSLY APPENDED.  CONTINUING ONTO THE NEXT INNER LOOP ITERATION!!"

                # Increment 'inner_loop_index'
                inner_loop_index += 1

                # Continue
                continue

            # If the two lists have passed all of these tests (they have not already been added to the list & they are not the same list), then you can compare their time
            # // and plane pixel coordinates to see if they are within 10 of each other
            # USE THE ABSOLUTE VALUE OF THE QUANTITIES!!!
            if math.fabs(inner_list[0][0] - outer_list[0][0]) <= 5 and math.fabs(inner_list[0][1] - outer_list[0][1]) <= 5:

                # Now you can append an addition of the two lists to 'output_list_platinum'
                output_list_platinum.append(outer_list + inner_list)

                # Print Statement
                print "The following two lists are close in time and pixel coordinates and are being added and appended to the new list: ", outer_list, "and ", inner_list, "."

                print "time coordinate difference between inner list and outer list = ", inner_list[0][0] - outer_list[0][0], "."
                print "plane pixel coordinate difference between inner list and outer list = ", inner_list[0][1] - outer_list[0][1], "."
                
                print "I'm appending the following indices to 'list_of_close_list_coords': ", outer_loop_index, "and ", inner_loop_index, "."

                # Append both of the indices to 'list_of_close_list_coords'
                list_of_close_list_coords.append(outer_loop_index)
                list_of_close_list_coords.append(inner_loop_index)

                # Change 'outer_list_previously_added' to 'True'
                outer_list_previously_added = True

                # Increment 'inner_loop_index' and continue (just for bookkeeping purposes)
                inner_loop_index += 1

                continue

            # Increment the inner index in the event that the inner and outer loops aren't matched
            inner_loop_index += 1

            # Print statement
            print "INNER LIST UNMATCHED WITH THE OUTER LIST.  CONTINUING!!"

        # Increment the outer index in the event that the outer loop isn't matched with any of the loops
        # Check that the outer loop isn't matched with any of the loops by continuing when you come to the 'outer_index_already_added' boolean
        if (outer_list_previously_added == True):

            print "OUTER LIST HAS ALREADY BEEN ADDED, SO IT SHOULDN'T BE INCREMENTED AGAIN.  CONTINUING!!" 
            print "\n"
            continue

        # Incremen at the end of this loop if it makes it this far
        outer_loop_index += 1
        
        # Print statement                                                                                                                                                        
        print "OUTER LIST UNMATCHED WITH ANY INNER LIST.  CONTINUING!!"
        print "\n"

    # Print out the list of coordinates at which to continue
    print "List of coordinates at which to continue with the loop: ", list_of_close_list_coords, "."
    print "\n"

    # Now, fill 'output_list_platinum' with the rest of 'output_list_improved'

    last_output_list_index = 0

    while last_output_list_index < len(output_list_improved):

        # Print statement
        print "I'm looping over the following list in output list improved: ", output_list_improved[last_output_list_index], "at index #", last_output_list_index, "."

        # Include a failsafe break statement (so that the loop is not filled incorrectly)
        if last_output_list_index > (len(output_list_improved) - 1):

            break

        # Define a boolean that will tell if this list in 'output_list_improved' has already been added to another list 
        # // and appended in 'output_list_platinum'
        already_appended = False

        # Do a loop to see if 'last_output_list_index' is the same as one of the indices in 'list_of_close_list_coords'
        for close_list_coord in list_of_close_list_coords:

            if close_list_coord == last_output_list_index:

                already_appended = True

        # Continue with the loop if 'already_appended' is True
        if already_appended == True:

            # Append 'last_output_list_index'
            last_output_list_index += 1

            print "This list has already been appended.  Continuing!"
            print "\n"

            # Continue on to the top of the loop
            continue

        # If the loop has made it this far, then append the entry of 'output_list_improved' at this index to 'output_list_platinum'
        output_list_platinum.append(output_list_improved[last_output_list_index])

        print "This list has not yet been appended to 'output_list_platinum'.  Appending away!"
        print "\n"

        # Increment the 'last_output_list_index'
        last_output_list_index += 1        

    # Return 'output_list_improved'
    return output_list_platinum


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
    

    
        
  
    

    
        
        


  




                


    
    

    
    
    

    
    

    

    

    
