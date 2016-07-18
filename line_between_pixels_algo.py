import math

# Write a script that will draw a line between a list of pixels in two separate lists and check the path between them for charge
# This function will take in two inputs of pixel lists: one list of pixels on one end of the tpc and another list of pixels on the other end of the tpc
# These inputs consist of a list of time pixels paired with their corresponding plane pixels
# The next input is the plane_vector for the plane in question, which contains the deconvoluted ADC values from the plane (for the ccqe.root file, these are dimension 764 * 864) 
# The last argument is the threshold ADC value that determines if a pixel between one point and the other is filled with charge
def line_between_pixels_algo(list_one, list_two, plane_vector, threshold):

    # Loop over the combination of pixels with an outer loop over one list and an inner loop over the other list (the order doesn't really matter)
    for list_one_pair in list_one:

        # Define the time and plane pixel for list_one
        list_one_time  = list_one_pair[0]
        list_one_pixel = list_one_pair[1]

        # Initialize the loop over the second list
        for list_two_pair in list_two:

            # Define the time and plane pixel for list_two
            list_two_time  = list_two_pair[0]
            list_two_pixel = list_two_pair[1]

            print "The first pair of pixels in (time, pixel): ", [list_one_time, list_one_pixel]
            print "The second pair of pixels in (time, pixel): ", [list_two_time, list_two_pixel]

            # Determine the magnitude and direction of the vector between the two points
            # ALWAYS PUT THE LIST ONE COORDINATE IN FRONT FOR CONSISTENCY!!!!! #
            time_diff  = list_one_time - list_two_time
            pixel_diff = list_one_pixel - list_two_pixel

            # This is the ratio of the 'time_diff' and the 'pixel_diff' 
            # Assume that the possibility that math.fabs(time_diff) == math.fabs(pixel_diff) is negligible and ignore the possibilty that time_diff or pixel_diff == 0 for now
            slope = float(math.fabs(time_diff))/float(math.fabs(pixel_diff))

            # Define the following four variables for use in expanding the scope of the this function
            greater_diff               = 0 # This is occupied by either time_diff if slope > 1 or pixel_diff if slope < 1
            lesser_diff                = 0 # This is occupied by either time_diff is slope < 1 or pixel_diff if slope > 1
            greater_diff_higher_value  = 0  # The 'greater_diff' means that the absolute value of its difference is greater according to the slope and the 'higher_value' part implies that this quantity is the higher value in the difference function
            greater_diff_lower_value   = 0 # The 'greater_diff' means that the absolute value of its difference is greater according to the slope and the 'lower_value' part implies that this quantity is the lower value in the difference function
            lesser_diff_higher_value   = 0 # The 'lower_diff' means that the absolute value of its difference is lower according to the slope and the 'higher_value' part implies that this quantity is the higher value in the difference function
            lesser_diff_lower_value    = 0 # The 'lower_diff' means that the absolute value of its difference is lower according to the slope and the 'lower_value' part implies that this quantity is the lower value in the difference function
            
            # Depending on the situation, go about assigning these variables
            if slope > 1: # This means that math.fabs(time_diff) > math.fabs(pixel_diff)

                greater_diff  = time_diff
                lesser_diff   = pixel_diff

                # Initialize the name of "greater_diff" for use later in the function comparing the value of the plane_vector to the threshold
                greater_diff_name = 'time'

                if time_diff > 0 and pixel_diff > 0: # list_one_time > list_two_time and list_one_pixel > list_two_pixel
                    
                    # Define the variables as given by the comparisons above
                    greater_diff_higher_value = list_one_time
                    greater_diff_lower_value  = list_two_time

                    lesser_diff_higher_value   = list_one_pixel
                    lesser_diff_lower_value    = list_two_pixel

                if time_diff > 0 and pixel_diff < 0: # list_one_time > list_two_time and list_one_pixel < list_two_pixel

                    # Define the variables as given by the comparisons above
                    greater_diff_higher_value = list_one_time
                    greater_diff_lower_value  = list_two_time

                    lesser_diff_higher_value   = list_two_pixel
                    lesser_diff_lower_value    = list_one_pixel

                if time_diff < 0 and pixel_diff > 0: # list_one_time < list_two_time and list_one_pixel > list_two_pixel

                    # Define the variables as given by the comparisons above
                    greater_diff_higher_value = list_two_time
                    greater_diff_lower_value  = list_one_time

                    lesser_diff_higher_value   = list_one_pixel
                    lesser_diff_lower_value    = list_two_pixel

                if time_diff < 0 and pixel_diff < 0: # list_one_time < list_two_time and list_one_pixel < list_two_pixel

                    # Define the variables as given by the comparisons above
                    greater_diff_higher_value = list_two_time
                    greater_diff_lower_vaue   = list_one_time

                    lesser_diff_higher_value   = list_two_pixel
                    lesser_diff_lower_value    = list_one_pixel

            if slope < 1: # This means that math.fabs(time_diff) < math.fabs(pixel_diff)

                greater_diff  = pixel_diff
                lesser_diff   = time_diff

                # Initialize the name of "greater_diff" for use later in the function comparing the value of the plane_vector to the threshold                                 
                greater_diff_name = 'pixel'

                # First, invert the value of the slope for use in the functions that follow
                slope = 1/slope

                if time_diff > 0 and pixel_diff > 0: # list_one_time > list_two_time and list_one_pixel > list_two_pixel

                    # Define the variables as given by the comparisons above
                    greater_diff_higher_value = list_one_pixel
                    greater_diff_lower_value  = list_two_pixel

                    lesser_diff_higher_value   = list_one_time
                    lesser_diff_lower_value    = list_two_time

                if time_diff > 0 and pixel_diff < 0: # list_one_time > list_two_time and list_one_pixel < list_two_pixel

                    # Define the variables as given by the comparisons above
                    greater_diff_higher_value = list_two_pixel
                    greater_diff_lower_value  = list_one_pixel

                    lesser_diff_higher_value   = list_one_time
                    lesser_diff_higher_value   = list_two_time

                if time_diff < 0 and pixel_diff > 0: # list_one_time < list_two_time and list_one_pixel > list_two_pixel

                    # Define the variables as given by the comparisons above
                    greater_diff_higher_value = list_one_pixel
                    greater_diff_higher_value = list_two_pixel

                    lesser_diff_higher_value   = list_two_time
                    lesser_diff_lower_value    = list_one_time

                if time_diff < 0 and pixel_diff > 0: # list_one_time < list_two_time and list_one_pixel < list_two_pixel

                    # Define the variables as given by the comparisons above
                    greater_diff_higher_value = list_two_pixel
                    greater_diff_lower_value  = list_one_pixel

                    lesser_diff_higher_value   = list_two_time
                    lesser_diff_lower_value    = list_one_time


            # Now that the variables are set based on the conditions of the input parameters, I can write a generic algorithm to count the number of steps between two points
            # // in (time, pixel) to see how many of them contain an amount of charge above threshold, taking extra care to account for the 'remainder' steps that must be 
            # // taken to reach the end point in the coordinates given

            # Find the number of pixels that are above threshold with the following variable
            # Define another variable, 'steps_not_above_threshold', to keep tabs of the total number of steps (and the ones that are below the threshold value set)
            steps_above_threshold = 0
            steps_not_above_threshold = 0

            # Declare an empty list that will be filled with the other time increments where lesser_diff_unit will have to be incremented                                     
            # Define this here to avoid definition errors later on in the algorithm
            extra_increments = []

            # Declare the variable 'additional_greater_diff_increment' out here just for bookkeeping purposes
            additional_greater_diff_increment = 0

            # Define the integer version of the slope as the 'amount of distance in lesser_diff units before you increment 'lesser_diff_unit''
            # Round the slope in the usual way
            if (slope - int(slope)) >= 0.5:
                        
                # Round the slope up
                slope_integer = int(slope) + 1
                    
            # Use another 'if' statement just to be sure that this one won't get confused with an 'if'...'else' later on in the loop
            if (slope - int(slope)) < 0.5:

                # Use the normal 'int' functionality
                slope_integer = int(slope)

            # Here's where it gets tricky: I have to compare the rounded slope * the number of lesser_diff units to the number of greater_diff units.  If the rounded         
            # // slope * the number of lesser_diff units is greater than the number of higher diff units, then I have to distribute the remainder number of units           
            # over the different iterations                                                                                                                              
            if (slope_integer*math.fabs(lesser_diff)) > math.fabs(greater_diff):

                remainder_num_of_units = math.fabs(lesser_diff) - (math.fabs(greater_diff)/slope_integer) # The quotient involves two 'ints' and so will also be an 'int'

                # Calculate the greater_diff units at which to increment 'lesser_diff_unit' (to be declared several lines later) an additional greater_diff_unit for the case when 
                # // math.fabs(greater_diff) % slope_integer == 0 and for when math.fabs(greater_diff) % slope_integer == 1

                if (math.fabs(greater_diff)/slope_integer) % 2 == 0: # This means that the number of times the slope goes into 'greater_diff' is even (the number of separations between adjacent greater_diff units that lesser_diff_unit is incremented is even)

                    # Consider the case first in which 'remainder_num_of_units' == 1:
                    if remainder_num_of_units == 1:

                        # Just fill this in at the point that is the first incrementing point below the halfway point (which itself is not an incrementing point)
                        extra_increments.append(greater_diff_lower_value + (math.fabs(greater_diff)/2))
                            
                    # Consider the case next in which 'remainder_num_of_units' is even
                    if remainder_num_of_units % 2 == 0:

                        # Fill in an equal number of units on either side of the halfway point (which itself is not an incrementing point)
                        additional_greater_diff_increment = greater_diff_lower_value + (math.fabs(greater_diff)/2) - (remainder_num_of_units * 0.5 * slope_integer) # Explanation: The last term ensures that the same number of units are added above the halfway point as are added below the halfway point

                        # Define an index that will determine if I have added more than 'remainder_num_of_units' greater_diff units to the list of greater_diff units       
                        unit_num = 0

                        while unit_num < remainder_num_of_units:

                            extra_increments.append(additional_greater_diff_increment)

                            unit_num += 1

                            additional_greater_diff_increment += slope_integer
                            
                    if remainder_num_of_units > 1 and remainder_num_of_units % 2 == 1:  # This is if the remainder number of units is greater than 1 and odd

                        additional_greater_diff_increment = greater_diff_lower_value + (math.fabs(greater_diff)/2) - ((remainder_num_of_units - 1) * 0.5 * slope_integer) # Explanation: (remainder_num_of_units - 1) * 0.5 ensures that there will be one more unit ABOVE the middle (remember, the middle is not somewhere that lesser_diff_unit will be incremented).  I can just change that '- 1' to a '+ 1' to ensure that there will be one more unit BELOW the middle (this is the trick with an even number of increments, that there really isn't a middle)

                        # Define an index that will determine if I have added more than 'remainder_num_of_units' lesser_diff_units to the list of lesser_diff_units
                        unit_num = 0

                        # Use a 'while' loop to fill the list
                        while unit_num < remainder_num_of_units:

                            extra_increments.append(additional_greater_unit_increment)
                                    
                            unit_num += 1

                            extra_greater_unit_increment += slope_integer

                # Now, consider the case in which (math.fabs(greater_diff)/slope_integer) % 2 == 1 (meaning that it is odd and there is a center of the incrementing points)
                else:

                    # Consider the case first in which 'remainder_num_of_units' == 1:                                                                              
                    if remainder_num_of_units == 1:

                        # Only fill in the center of the points of incrementing
                        extra_increments.append(greater_diff_lower_value + ((math.fabs(greater_diff)/slope_integer) + 1) * slope_integer)

                    # Consider the case next in which 'remainder_num_of_units' is even                                                                            
                    if remainder_num_of_units % 2 == 0:

                        # Initialize the value of 'additional_greater_unit_increment'
                        additional_greater_diff_increment = greater_diff_lower_value + (((math.fabs(greater_diff)/slope_integer) + 1) * slope_integer) - ((remainder_num_of_units/2) * slope_integer)

                        # Define an index that will determine if I have added more than 'remainder_num_of_units' greater_diff units to the list of greater_diff units              
                        unit_num = 0

                        # Use a 'while' loop to fill the list
                        while unit_num < remainder_num_of_units:

                            if unit_num == (remainder_num_of_units/2) - 1: # This is because I do NOT want to fill the center unit

                                unit_num += 1

                                # Increment 'additional_greater_diff_increment' before continuing
                                additional_greater_diff_increment += slope_integer

                            # Append the 'additional_greater_diff_increment' onto the 'extra_increments' list before incrementing again
                            extra_increments.append(additional_greater_diff_increment)
                                    
                            unit_num += 1

                            additional_greater_diff_increment += slope_integer

                    # Finally, consider the case in which 'remainder_num_of_units' is odd and greater than 1
                    if remainder_num_of_units > 1 and (remainder_num_of_units % 2) == 1:

                        # Initialize the value of additional_greater_diff_increment to be the value of ((remainder_num_of_units - 1)/2) * slope_integer) below the halfway point
                        additional_time_increment = greater_diff_lower_value + (((math.fabs(greater_diff)/slope_integer) + 1) * slope_integer) - ((remainder_num_of_units - 1)/2) * slope_integer

                        # Define an index that will determine if I have added more than 'remainder_num_of_units' greater_diff units to the list of greater_diff units
                        unit_num = 0

                        while unit_num < remainder_num_of_units:

                            extra_increments.append(additional_greater_diff_increment)

                            # Increment 'unit_num'
                            unit_num += 1

                            # Increment 'additional_greater_diff_increment'
                            additional_greater_diff_increment += slope_integer


            # The rest of the algorithm for filling in the remainder_num_of_units will be contained below

            # Initialize the first 'lesser_diff_unit'' as the location of 'lesser_diff_lesser_value', and slowly increment it until it reaches the value 
            # // of lesser_diff_greater_value
            lesser_diff_unit = lesser_diff_lower_value
                   
            # Now, write a loop to venture down this path to the greater_diff_greater_value
            for greater_diff_unit in range(greater_diff_lower_value, greater_diff_higher_value + 1):

                # Increment the value of greater_diff_unit
                greater_diff_unit += 1

                if greater_diff_unit == slope_integer:

                    lesser_diff_unit += 1

                # Invoke the additional lesser_diff_units based on the algorithm above
                # Loop over the list and see if the current lesser_diff_unit is equal to the member of the 'extra_increments' list filled above
                if extra_increments != []:

                    for another_increment in extra_increments:

                        if another_increment == greater_diff_unit:

                            # Increment the 'lesser_diff_unit' again
                            lesser_diff_unit += 1

                # Check to make sure that you have the coordinates right for the event before you check the pixel for an ADC value above threshold

                # First, this is if the greater_diff is the time component
                if greater_diff_name == 'time':

                    if plane_vector[greater_diff_unit][lesser_diff_unit] >= threshold:

                        steps_above_threshold += 1

                    # Sloppy programming again, but include the negative loop of the one immediately above because of extra 'if' statements
                    if plane_vector[greater_diff_unit][lesser_diff_unit] < threshold:

                        steps_not_above_threshold += 1


                # Now, check the plane_vector if the greater_diff is the pixel component
                if greater_diff_name == 'pixel':

                    if plane_vector[lesser_diff_unit][greater_diff_unit] >= threshold:

                        steps_above_threshold += 1

                    # Sloppy programming again, but include the negative loop of the one immediately above because of extra 'if' statements                         
                    if plane_vector[lesser_diff_unit][greater_diff_unit] < threshold:

                        steps_not_above_threshold += 1
                        
            # At the end of the loop, print out the point at which the line terminates
            # This depends on which variable is the 'greater_diff' and which one is the 'lesser_diff', so I have to include an 'if' statement here to make that distinction
            
            if greater_diff_name == 'time':

                print "This line is ending at the point: ", [greater_diff_unit, lesser_diff_unit]

            if greater_diff_name == 'pixel':

                print  "This line is ending at the point: ", [lesser_diff_unit, greater_diff_unit]

            print "The number of steps above threshold is: ", steps_above_threshold
            print "The number of steps below threshold is: ", steps_not_above_threshold
            print "The (float) ratio of these the steps above threshold to the total number of steps is: ", float(steps_above_threshold)/(float(steps_above_threshold) + float(steps_not_above_threshold))
            print "\n"

    return 0 
        

            

                    

                        

                        
                        

                        

                        

                    

        

                

            

    

    
