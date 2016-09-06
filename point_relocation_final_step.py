import numpy as np
import dead_pixel_region_check

# Write a function that will relocate the points post-clustering to the point with the highest color score within its vicinity for the top and bottom hits (lists of time and three plane hit coordinates)
# The input parameters are the list of points, the three image planes, the dead pixels across each image plane for this event, the range in time and pixel that you're checking for charge, and 'hit_type' 

# FOR BOTH FUNCTIONS:

# NOTE: In this version of the function, I will not worry about issues on the boundary, meaning that I don't think that some of these lists will go out of range
# If that becomes an issue, then I can correct for it

# Also, I do not consider the fact that a pixel adjacent to a dead pixel region could be on the end of a track of charge. I can eliminate this function during tests, because it affects a small minority charge hits 

# Lastly, I do not consider the possibility that both of the matched pixels are located within areas of dead pixels
def charge_vicinity_locator_top_and_bottom(list_of_points, uplane_array, vplane_array, yplane_array, uplane_dead_pixels, vplane_dead_pixels, yplane_dead_pixels, time_range, pixel_range):

    # Define an empty list for the new points that will be located at the ends of tracks
    charge_ends_hits = []

    # Make sure that 'list_of_points' is not an empty list first
    if list_of_points != []:

        # Start a loop over one of the set of points in 'list_of_points' for this top/bottom hit
        for three_plane_hit in list_of_points:

            # Take slices out of the three wire planes for the ranges we're going to search for a maximum amount of charge
            # The 'np.copy' function includes the first point list in the range but NOT the last point, so I have add one to the index on the end of the range
            uplane_range = np.copy(uplane_array[(three_plane_hit[0] - time_range):(three_plane_hit[0] + time_range + 1)][(three_plane_hit[1] - pixel_range):(three_plane_hit[1] + pixel_range + 1)])
            vplane_range = np.copy(vplane_array[(three_plane_hit[0] - time_range):(three_plane_hit[0] + time_range + 1)][(three_plane_hit[2] - pixel_range):(three_plane_hit[2] + pixel_range + 1)])
            yplane_range = np.copy(vplane_array[(three_plane_hit[0] - time_range):(three_plane_hit[0] + time_range + 1)][(three_plane_hit[3] - pixel_range):(three_plane_hit[3] + pixel_range + 1)])

            # I will still enforce three plane matches, so I will only light up three pixels in the same row (or at the same time pixel)
            
            # Set the total ADC value at the three input pixels to be the 'highest_overall_score'
            highest_overall_score = uplane_array[three_plane_hit[0]][three_plane_hit[1]] + vplane_array[three_plane_hit[0]][three_plane_hit[2]] + yplane_array[three_plane_hit[0]][three_plane_hit[3]]

            # Set the 'highest_overall_scoring_pixels' equal to the matched set of pixels
            highest_overall_scoring_pixels = three_plane_hit[:] # MAKE SURE to use the [:] functionality so that the two variables don't have the same address

            # Now, start a loop over the time ticks in this range (to check all of the plane pixels at this time tick value)
            for time_tick in range(three_plane_hit[0] - time_range, three_plane_hit[0] + time_range + 1):

                # Define a quantity for the highest ADC score at this value of 'time_tick', 'highest_score_at_time_tick', that I'll set equal to the central set of pixels in each plane's range (the pixels around which the range is defined)
                highest_score_at_time_tick = uplane_array[time_tick][three_plane_hit[1]] + vplane_array[time_tick][three_plane_hit[2]] + yplane_array[time_tick][three_plane_hit[3]]
                    
                # Define a quantity for the highest scoring set of pixels at this value of 'time_tick', 'highest_scoring_pixels_at_time_tick', that I'll set equal to the first set of pixels in each plane's range
                # I'll do so with member assignment to avoid address issues in Python
                highest_scoring_pixels_at_time_tick = [0, 0, 0, 0]
                
                highest_scoring_pixels_at_time_tick[0] = time_tick # This will stay the same for each new 'highest' set of pixels used
                highest_scoring_pixels_at_time_tick[1] = three_plane_hit[1] 
                highest_scoring_pixels_at_time_tick[2] = three_plane_hit[2] 
                highest_scoring_pixels_at_time_tick[3] = three_plane_hit[3] 

                # Now, start looping over the pixels at this time tick using a python 'range' function
                for uplane_pixel in range(three_plane_hit[1] - pixel_range, three_plane_hit[1] + pixel_range + 1):

                    # Use the 'dead_pixel_region_check' functions to see if this uplane pixel is in, or directly adjacent to, a region of dead pixels on the uplane

                    # If the pixel is adjacent to a dead region, then it is not an end to a charge track.  
                    if dead_pixel_region_check.is_next_to_dead_pixel(uplane_pixel, uplane_dead_pixels) == True:
                        continue

                    # Define a boolean for the output of the 'dead_pixel_region_check', which will help in determining how to extrapolate a value for the pixel's ADC score when this pixel is dead
                    is_upixel_dead = dead_pixel_region_check.is_dead_pixel(uplane_pixel, uplane_dead_pixels)

                    # Start an intermediate loop over the vplane pixels
                    for vplane_pixel in range(three_plane_hit[2] - pixel_range, three_plane_hit[2] + pixel_range + 1):

                        # Use the 'dead_pixel_region_check' functions to see if this vplane pixel is in, or directly adjacent to, a region of dead pixels on the vplane

                        # If the pixel is adjacent to a dead region, then it is not an end to a charge track.
                        if dead_pixel_region_check.is_next_to_dead_pixel(vplane_pixel, vplane_dead_pixels) == True:
                            continue

                        # Define a boolean for the output of the 'dead_pixel_region_check', which will help in determining how to extrapolate a value for the pixel's ADC score when this pixel is dead
                        is_vpixel_dead = dead_pixel_region_check.is_dead_pixel(vplane_pixel, vplane_dead_pixels)

                        # Start a final loop over the yplane pixels
                        for yplane_pixel in range(three_plane_hit[3] - pixel_range, three_plane_hit[3] + pixel_range + 1):

                            # Use the 'dead_pixel_region_check' functions to see if this yplane pixel is in, or directly adjacent to, a region of dead pixels on the yplane

                            # If the pixel is adjacent to a dead region, then it is not an end to a charge track.
                            if dead_pixel_region_check.is_next_to_dead_pixel(yplane_pixel, yplane_dead_pixels) == True:
                                continue

                            # Define a boolean for the output of the 'dead_pixel_region_check', which will help in determining how to extrapolate a value for the pixel's ADC score when this pixel is dead
                            is_ypixel_dead = dead_pixel_region_check.is_dead_pixel(yplane_pixel, yplane_dead_pixels)

                            # Calculate the 'charge score', i.e. the total charge across all three planes for this hit
                            charge_score = uplane_array[time_tick][uplane_pixel] + vplane_array[time_tick][vplane_pixel] + yplane_array[time_tick][yplane_pixel]

                            # See if any of the booleans for dead wires are true (assume that ONLY ONE is true for now; it's unlikely that two track ends would 
                            # // otherwise be located in a region of dead wires)
                            if (is_upixel_dead == True or is_vpixel_dead == True or is_ypixel_dead == True):

                                # Multiply the charge score by 1.5 to reflect that fact
                                # A clumsy extrapolation, but something is necessary
                                charge_score = 1.5 * charge_score

                            # Compare charge score to 'highest_score_at_time_tick' 
                            if charge_score > highest_score_at_time_tick:

                                # Replace 'highest_score_at_time_tick' with 'charge_score'
                                highest_score_at_time_tick = charge_score

                                # Replace the pixel coordinates in 'highest_scoring_pixels_at_time_tick' with this set of pixel coordinates (not the time tick, which stays the same)
                                highest_scoring_pixels_at_time_tick[1] = uplane_pixel
                                highest_scoring_pixels_at_time_tick[2] = vplane_pixel
                                highest_scoring_pixels_at_time_tick[3] = yplane_pixel

                # Compare the current value of 'highest_score_at_time_tick' with 'highest_overall_score'
                if highest_score_at_time_tick > highest_overall_score:

                    # Set 'highest_overall_score' equal to 'highest_score_at_time_tick'
                    highest_overall_score = highest_score_at_time_tick

                    # Replace the time and pixel coordinates in 'highest_overall_scoring_pixels' with this set of time and pixel coordinates
                    highest_overall_scoring_pixels[0] = time_tick
                    highest_overall_scoring_pixels[1] = highest_scoring_pixels_at_time_tick[1]
                    highest_overall_scoring_pixels[2] = highest_scoring_pixels_at_time_tick[2]
                    highest_overall_scoring_pixels[3] = highest_scoring_pixels_at_time_tick[3]

            # *** Place to include an 'if' statement that checks if the highest scoring pixel values are greater than a certain value ****
            # (I'll have to see how the images turn out first)

            # Make sure that this set of time and pixel coordinates was not appended to 'charge_end_hits' previously
            if charge_ends_hits != []:

                # Loop over 'end_hits' in 'charge_end_hits' to see if any iteration of it sets 'end_hits' == 'highest_overall_scoring_pixels'
                for end_hits in charge_ends_hits:

                    if end_hits == highest_overall_scoring_pixels:

                        # Go on to the next 'three_plane_hit' in 'list_of_points'
                        continue

            # A counting number for the next loop                                                                                                                            
            number_of_surrounding_pixels_with_charge = [0, 0, 0]

            # Define an iterator
            list_iterator = 0

            for plane_pixel in [highest_overall_scoring_pixels[1], highest_overall_scoring_pixels[2], highest_overall_scoring_pixels[3]]:

                # Include a print statement for the pixels that you're looping over
                # print "Central Time Pixel: ", highest_overall_scoring_pixels[0]
                # print "Central Plane Pixel: ", plane_pixel

                # Include a newline
                # print "\n"
                
                # Lastly, make sure that their is charge in at least one of the eight pixels surrounding these ones                                                  
                for time_pixel in range(highest_overall_scoring_pixels[0] - 1, highest_overall_scoring_pixels[0] + 2):

                    for neighboring_plane_pixel in range(plane_pixel - 1, plane_pixel + 2):

                        # 'Continue' when you're located on the matched pixel                                                
                        if time_pixel == highest_overall_scoring_pixels[0] and neighboring_plane_pixel == plane_pixel:

                            continue

                        # Separate the 'plane_pixel' cases by plane                                                                                                  
                        if plane_pixel == highest_overall_scoring_pixels[1]:

                            # print "Adjacent Time Pixel: ", time_pixel
                            # print "Adjacent U Plane Pixel: ", neighboring_plane_pixel

                            # print "Score = ", uplane_array[time_pixel][neighboring_plane_pixel]
                            # print "\n"

                            if uplane_array[time_pixel][neighboring_plane_pixel] > 0.50:

                                # Increment 'number_of_surrounding_pixels_with_charge'                                            
                                number_of_surrounding_pixels_with_charge[list_iterator] += 1

                        elif plane_pixel == highest_overall_scoring_pixels[2]:

                            # print "Adjacent Time Pixel: ", time_pixel
                            # print "Adjacent V Plane Pixel: ", neighboring_plane_pixel

                            # print "Score = ", vplane_array[time_pixel][neighboring_plane_pixel]
                            # print "\n"

                            if vplane_array[time_pixel][neighboring_plane_pixel] > 0.50:

                                # Increment 'number_of_surrounding_pixels_with_charge'                                                               
                                number_of_surrounding_pixels_with_charge[list_iterator] += 1

                        elif plane_pixel == highest_overall_scoring_pixels[3]:

                            # print "Adjacent Time Pixel: ", time_pixel
                            # print "Adjacent Y Plane Pixel: ", neighboring_plane_pixel

                            # print "Score = ", yplane_array[time_pixel][neighboring_plane_pixel]
                            # print "\n"

                            if yplane_array[time_pixel][neighboring_plane_pixel] > 0.50:

                                # Increment 'number_of_surrounding_pixels_with_charge'
                                number_of_surrounding_pixels_with_charge[list_iterator] += 1

                list_iterator += 1

                # Include a newline for readable output
                # print "\n"

            # Include a 'print' statement for 'number_of_surrounding_pixels_with_charge'
            # print "Number of Surrounding Pixels with Charge for Each Pixel: ", number_of_surrounding_pixels_with_charge
            # print "\n"

            num_zero_charge_entries = 0

            # Define a boolean that will cause the loop to continue if there is no ADC value in one of the pixels (proper use of the 'continue' statement)
            entry_no_surrounding_charge = False

            # 'Continue' if none of the surrounding pixels have charge                 
            for entry in number_of_surrounding_pixels_with_charge:

                if entry == 0:

                    num_zero_charge_entries += 1

            if num_zero_charge_entries > 0:
                    
                entry_no_surrounding_charge = True

            # 'Continue' if none of the surrounding pixels have charge
            if entry_no_surrounding_charge == True:

                # print "One of the surrounding pixels of one of the matches has no charge.  Continuing!!"
                # print "\n"

                continue

            charge_ends_hits.append(highest_overall_scoring_pixels)

    # Return 'charge_end_hits
    return charge_ends_hits

# Write a function that will relocate the points post-clustering to the point with the highest color score within its vicinity for the top and bottom hits (lists of time and three
# // plane hit coordinates)                                                                                                                                                      
# The input parameters are the list of points, the three image planes, the dead pixels across each image plane for this event, the range in time and pixel that you're checking for
# // charge, and 'final_pixel', which refers to the pixel on the edge of the detector that you're checking, which is either indices '0' (for upstream hits) or 'cols - 1' (for downstream hits)
def charge_vicinity_locator_upstream_and_downstream(list_of_points, uplane_array, vplane_array, yplane_array, uplane_dead_pixels, vplane_dead_pixels, yplane_dead_pixels, time_range, pixel_range, final_pixel):

    # Define 'charge_end_hits', the empty list for points that will be located at the end of tracks
    charge_ends_hits = []

    # Make sure that 'list_of_points' is not an empty list first
    if list_of_points != []:

        # Start a loop over one of the set of points in 'list_of_points' for this upstream/downstream hit
        for two_plane_hit in list_of_points:

            # Take slices out of the two wire planes for the ranges we're going to search for a maximum amount of charge                                                      
            # The 'np.copy' function includes the first point list in the range but NOT the last point, so I have add one to the index on the end of the range               
            uplane_range = np.copy(uplane_array[(two_plane_hit[0] - time_range):(two_plane_hit[0] + time_range + 1)][(two_plane_hit[1] - pixel_range):(two_plane_hit[1] + pixel_range + 1)])
            vplane_range = np.copy(vplane_array[(two_plane_hit[0] - time_range):(two_plane_hit[0] + time_range + 1)][(two_plane_hit[2] - pixel_range):(two_plane_hit[2] + pixel_range + 1)])

            # I will still enforce three plane matches, so I will only light up three pixels in the same row (or at the same time pixel, with the last pixel being in the position of 'final_pixel')

            
            highest_overall_score = uplane_array[two_plane_hit[0]][two_plane_hit[1]] + vplane_array[two_plane_hit[0]][two_plane_hit[2]] + yplane_array[two_plane_hit[0]][final_pixel]
            
            highest_overall_scoring_pixels = two_plane_hit[:]

            # Start a loop over the range of time pixel hits
            for time_tick in range(two_plane_hit[0] - time_range, two_plane_hit[0] + time_range + 1):

                # Define a quantity for the highest ADC score at this value of 'time_tick', 'highest_score_at_time_tick', that I'll set equal to the central set of pixels in each plane's range (the pixels around which the range is defined)                                                                                                                  
                highest_score_at_time_tick = uplane_array[time_tick][two_plane_hit[1]] + vplane_array[time_tick][two_plane_hit[2]] + yplane_array[time_tick][final_pixel]

                # Define a quantity for the highest scoring set of pixels at this value of 'time_tick', 'highest_scoring_pixels_at_time_tick', that I'll set equal to the first set of pixels in each plane's range                                                                                                                                              
                # I'll do so with member assignment to avoid address issues in Python                                                                  
                highest_scoring_pixels_at_time_tick = [0, 0, 0]

                highest_scoring_pixels_at_time_tick[0] = time_tick # This will stay the same for each new 'highest' set of pixels used                                        
                highest_scoring_pixels_at_time_tick[1] = two_plane_hit[1]
                highest_scoring_pixels_at_time_tick[2] = two_plane_hit[2]

                # Now, start looping over the pixels at this time tick using a python 'range' function                                                   
                for uplane_pixel in range(two_plane_hit[1] - pixel_range, two_plane_hit[1] + pixel_range + 1):

                    # Use the 'dead_pixel_region_check' functions to see if this uplane pixel is in, or directly adjacent to, a region of dead pixels on the uplane          
                    # If the pixel is adjacent to a dead region, then it is not an end to a charge track.                                                                      
                    if dead_pixel_region_check.is_next_to_dead_pixel(uplane_pixel, uplane_dead_pixels) == True:
                        continue

                    # Define a boolean for the output of the 'dead_pixel_region_check', which will help in determining how to extrapolate a value for the pixel's ADC score when this pixel is dead                                                                                                                                                              
                    is_upixel_dead = dead_pixel_region_check.is_dead_pixel(uplane_pixel, uplane_dead_pixels)

                    # Start an intermediate loop over the vplane pixels                                                                                                        
                    for vplane_pixel in range(two_plane_hit[2] - pixel_range, two_plane_hit[2] + pixel_range + 1):

                        # Use the 'dead_pixel_region_check' functions to see if this vplane pixel is in, or directly adjacent to, a region of dead pixels on the vplane 
                        # If the pixel is adjacent to a dead region, then it is not an end to a charge track.                                                                
                        if dead_pixel_region_check.is_next_to_dead_pixel(vplane_pixel, vplane_dead_pixels) == True:
                            continue

                        # Define a boolean for the output of the 'dead_pixel_region_check', which will help in determining how to extrapolate a value for the pixel's ADC score when this pixel is dead                                                                                                                                                         
                        is_vpixel_dead = dead_pixel_region_check.is_dead_pixel(vplane_pixel, vplane_dead_pixels)

                         # Calculate the 'charge score', i.e. the total charge across all three planes for this hit 
                        charge_score = uplane_array[time_tick][uplane_pixel] + vplane_array[time_tick][vplane_pixel] + yplane_array[time_tick][final_pixel]

                        # See if any of the booleans for dead wires are true (assume that ONLY ONE is true for now; it's unlikely that two track ends would                  
                        # // otherwise be located in a region of dead wires)                                                                                                     
                        if (is_upixel_dead == True or is_vpixel_dead == True):

                            # Multiply the charge score by 1.5 to reflect that fact                                                                                        
                            # A clumsy extrapolation, but something is necessary                                                                                          
                            charge_score = 1.5 * charge_score

                        # Compare charge score to 'highest_score_at_time_tick'                                                                                        
                        if charge_score > highest_score_at_time_tick:

                            # Replace 'highest_score_at_time_tick' with 'charge_score'                                                                           
                            highest_score_at_time_tick = charge_score

                            # Replace the pixel coordinates in 'highest_scoring_pixels_at_time_tick' with this set of pixel coordinates (not the time tick, which stays the same)                                                                                                                                  
                            highest_scoring_pixels_at_time_tick[1] = uplane_pixel
                            highest_scoring_pixels_at_time_tick[2] = vplane_pixel

                if highest_score_at_time_tick > highest_overall_score:

                    # Set "highest_overall_score" to "highest_score_at_time_tick"
                    highest_overall_score = highest_score_at_time_tick

                    # Replace the time and pixel coordinates in 'highest_overall_scoring_pixels' with this set of time and pixel coordinates 
                    highest_overall_scoring_pixels[0] = time_tick
                    highest_overall_scoring_pixels[1] = highest_scoring_pixels_at_time_tick[1]
                    highest_overall_scoring_pixels[2] = highest_scoring_pixels_at_time_tick[2]

            # *** Place to include an 'if' statement that checks if the highest scoring pixel values are greater than a certain value ****                                     
            # (I'll have to see how the images turn out first)

            # Make sure that this set of time and pixel coordinates was not appended to 'charge_end_hits' previously 
            if charge_ends_hits != []:

                # Loop over 'end_hits' in 'charge_end_hits' to see if any iteration of it sets 'end_hits' == 'highest_overall_scoring_pixels'
                for end_hits in charge_ends_hits:
                    
                    # Define a boolean for if 'highest_overall_scoring_pixels' have already been appended to 'end_hits'
                    already_appended = False

                    if end_hits == highest_overall_scoring_pixels:

                        # print "This set of pixels has already been appended to 'charge_hits!'"
                        # print "end hits: ", end_hits
                        # print "highest_overall_scoring_pixels: ", highest_overall_scoring_pixels
                        # print "\n"

                        already_appended = True

                    # if 'already_appended' is True, then you can break the 'for' loop and continue immediately outside in the main loop
                    if already_appended == True:

                        break
                    
                if already_appended == True:

                    continue
                    
            # A counting number for the next loop
            number_of_surrounding_pixels_with_charge = [0, 0, 0]

            # Define an iterator for the list
            list_iterator = 0

            for plane_pixel in [highest_overall_scoring_pixels[1], highest_overall_scoring_pixels[2], final_pixel]: # (I won't worry about the pixel on the boundary)

                 # Include a print statement for the pixels that you're looping over                                                                                                  
                # print "Central Time Pixel: ", highest_overall_scoring_pixels[0]
                # print "Central Plane Pixel: ", plane_pixel

                # Include a newline                                                                                                                                                  
                # print "\n"

                # Lastly, make sure that their is charge in at least one of the eight pixels surrounding these ones
                for time_pixel in range(highest_overall_scoring_pixels[0] - 1, highest_overall_scoring_pixels[0] + 2):

                    for neighboring_plane_pixel in range(plane_pixel - 1, plane_pixel + 2):

                        # 'Continue' when you're located on the matched pixel
                        if time_pixel == highest_overall_scoring_pixels[0] and neighboring_plane_pixel == plane_pixel:
                            
                            continue

                        # Separate the 'plane_pixel' cases by plane
                        if plane_pixel == highest_overall_scoring_pixels[1]:

                            # print "Adjacent Time Pixel: ", time_pixel
                            # print "Adjacent U Plane Pixel: ", neighboring_plane_pixel

                            # print "Score = ", uplane_array[time_pixel][neighboring_plane_pixel]
                            # print "\n"

                            if uplane_array[time_pixel][neighboring_plane_pixel] > 0.50:

                                # Increment 'number_of_surrounding_pixels_with_charge'
                                number_of_surrounding_pixels_with_charge[list_iterator] += 1

                        elif plane_pixel == highest_overall_scoring_pixels[2]:

                            # print "Adjacent Time Pixel: ", time_pixel
                            # print "Adjacent V Plane Pixel: ", neighboring_plane_pixel

                            # print "Score = ", vplane_array[time_pixel][neighboring_plane_pixel]
                            # print "\n"

                            if vplane_array[time_pixel][neighboring_plane_pixel] > 0.50:

                                # Increment 'number_of_surrounding_pixels_with_charge'
                                number_of_surrounding_pixels_with_charge[list_iterator] += 1

                        # Include an 'if' condition for the 
                        elif plane_pixel == final_pixel:

                            # Include a conditional that says that the pixel list cannot be out of range
                            if neighboring_plane_pixel < 0 or neighboring_plane_pixel > 863:
                                
                                continue

                            # Now, consider the pixels that are within range
                            if yplane_array[time_pixel][neighboring_plane_pixel] > 0.20:

                                # Increment 'number_of_surrounding_pixels_with_charge'
                                number_of_surrounding_pixels_with_charge[list_iterator] += 1
                                

                list_iterator += 1
                
                # Include a space for readable output
                # print "\n"

            # Include a 'print' statement for 'number_of_surrounding_pixels_with_charge'                                                                 
            # print "Number of Surrounding Pixels with Charge for Each Pixel: ", number_of_surrounding_pixels_with_charge
            # print "\n"

            num_zero_charge_entries = 0

            # Define a boolean that will cause the entire loop to continue if an entry in 'number_of_surrounding_pixels_with_charge' is 0
            entry_no_surrounding_charge = False

            # 'Continue' if none of the surrounding pixels have charge for any of the pixels
            for entry in number_of_surrounding_pixels_with_charge:

                if entry == 0:

                    num_zero_charge_entries += 1

            if num_zero_charge_entries > 0:
                
                entry_no_surrounding_charge = True

            # Continue if that boolean is 'True'
            if entry_no_surrounding_charge == True:

                # print "One of the surrounding pixels of one of the matches has no charge.  Continuing!!"
                # print "\n"

                continue

            # Append 'highest_overall_scoring_pixels' to charge_end_hits
            charge_ends_hits.append(highest_overall_scoring_pixels)

    # Return 'charge_end_hits'
    return charge_ends_hits
                        
