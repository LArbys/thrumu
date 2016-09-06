# Define a function that will score matching pixels according to the amount of charge they have on each of the planes and then compares them to the other pixels that they are grouped with

# Input parameters:
# pixel_list - list of the pixels (grouped together) that are being scored
# uplane_array - the 2D grid of [pixel, time] for plane one, the uplane array
# vplane_array - the 2D grid of [pixel, time] for plane two, the vplane array
# yplane_array - the 2D grid of [pixel, time] for plane three, the yplane array
# uplane_dead_pixels - the dead pixels on the u-plane in list form with each list representing the region of dead pixels along the plane
# vplane_dead_pixels - the dead pixels on the v-plane in list form with each list representing the region of dead pixels along the plane
# yplane_dead_pixels - the dead pixels on the y-plane in list form with each list representing the region of dead pixels along the plane
# hit_type - the type of hit that is being considered here.  Key - 0: top, 1: bottom, 2: upstream, 3: downstream

# This function does not have to discriminate between lists with three elements and those with four elements, because I can check the 0th and 863rd pixels in the arrays

def adjacent_pixels_color_scoring_algo(pixel_list, uplane_array, vplane_array, yplane_array, uplane_dead_pixels, vplane_dead_pixels, yplane_dead_pixels, hit_type):

    # Declare an empty list for the output scored pixels
    output_scored_pixels = []

    # This the loop for top and bottom hits
    if hit_type == 0 or hit_type == 1:

        # The 'pixel_list' will be a list of lists of lists, meaning that there are lists of the time pixels paired with their plane counterparts
        for pixel_collection in pixel_list:

            # Declare the highest scoring set of pixels the first one in 'pixel_collection' (the values will be compared shortly)
            highest_scoring_pixels = pixel_collection[0]

            # Declare the highest score of any of the pixels in the set to be that from the first one in 'pixel_collection'
            highest_score = uplane_array[pixel_collection[0][0]][pixel_collection[0][1]] + vplane_array[pixel_collection[0][0]][pixel_collection[0][2]] + yplane_array[pixel_collection[0][0]][pixel_collection[0][3]]

            # Declare an iterator over the contents of 'pixel_collection'
            pixel_collection_iterator = 0
        
            # Now, loop through 'pixel_collection' calculate the score of each of the sets of pixels
            while pixel_collection_iterator < len(pixel_collection):

                current_score = uplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][1]] + vplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][2]]+ yplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][3]]

                # Now, you have some adjusting to do based on if one of the pixels is in a region of dead pixels on its respective plane
                
                # Define a counter for how many of the pixels for this hit are in a dead region on their respective plane
                num_matched_pixels_in_dead_reg = 0

                # Loop over each collection of 'plane_dead_pixels' to see if any of these pixels are in any of their regions (you'll need two loops each)
                
                # uplane
                for u_plane_list in uplane_dead_pixels:

                    for u_plane_pixel in u_plane_list: # (This is why I had to turn even single pixels into lists in 'dead_pixel_region_classifier_encapsulated')

                        if u_plane_pixel == pixel_collection[pixel_collection_iterator][1]:

                            # Increment 'num_matched_pixels_in_dead_reg'
                            num_matched_pixels_in_dead_reg += 1

                # vplane                                                                                                                  
                for v_plane_list in vplane_dead_pixels:

                    for v_plane_pixel in v_plane_list: # (This is why I had to turn even single pixels into lists in 'dead_pixel_region_classifier_encapsulated') 
                        
                        if v_plane_pixel == pixel_collection[pixel_collection_iterator][2]:

                            # Increment 'num_matched_pixels_in_dead_reg'                                                                                    
                            num_matched_pixels_in_dead_reg += 1

                # yplane
                for y_plane_list in yplane_dead_pixels:

                    for y_plane_pixel in y_plane_list: # (This is why I had to turn even single pixels into lists in 'dead_pixel_region_classifier_encapsulated')

                        if y_plane_pixel == pixel_collection[pixel_collection_iterator][3]:

                            # Increment 'num_matched_pixels_in_dead_reg'
                            num_matched_pixels_in_dead_reg += 1

                # Now, adjust the score based on the value of 'num_matched_pixels_in_dead_reg' 
                if num_matched_pixels_in_dead_reg > 3:

                    # print "Whoa, something is seriously wrong!!"
                    # print "The collection of top or bottom pixels that are 4 or greater in dead pixel number to this is: ", [pixel_collection[pixel_collection_iterator][0], pixel_collection[pixel_collection_iterator][1], pixel_collection[pixel_collection_iterator][2], pixel_collection[pixel_collection_iterator][3]], "."
                    return 0

                if num_matched_pixels_in_dead_reg == 3:

                    # The current score should equal zero, but set it to zero and issue a print statement and the pixels in list form
                    current_score = 0.
                    # print "All of the pixels for this current hit are in a dead region."
                    # print "The collection of top or bottom pixels is: ", [pixel_collection[pixel_collection_iterator][0], pixel_collection[pixel_collection_iterator][1], pixel_collection[pixel_collection_iterator][2], pixel_collection[pixel_collection_iterator][3]], "."
                
                if num_matched_pixels_in_dead_reg == 2:

                    # You have to multiply the current score by 3 to extrapolate what the ADC score would be otherwise
                    # print "Two pixels for this current hit are in a dead region."
                    # print "The collection of top or bottom pixels is: ", [pixel_collection[pixel_collection_iterator][0], pixel_collection[pixel_collection_iterator][1], pixel_collection[pixel_collection_iterator][2], pixel_collection[pixel_collection_iterator][3]], "."
                    current_score = 3.*current_score

                if num_matched_pixels_in_dead_reg == 1:

                    # You have to multiply the current score by 1.5 (= 3/2) to find what the score would be if not for the region of dead wires
                    # print "One pixel for this current hit are in a dead region."
                    # print "The collection of top or bottom pixels is: ", [pixel_collection[pixel_collection_iterator][0], pixel_collection[pixel_collection_iterator][1], pixel_collection[pixel_collection_iterator][2], pixel_collection[pixel_collection_iterator][3]], "."
                    current_score = 1.5*current_score

                # Check to see if the current score is greater than the highest_score
                if current_score > highest_score:
                    
                    # Reset the highest score to the current score
                    highest_score = current_score

                    # Set the highest scoring pixels to the pixels at this iterator in 'pixel_collection'
                    highest_scoring_pixels = pixel_collection[pixel_collection_iterator]

                # Increment the 'pixel_collection_iterator'
                pixel_collection_iterator += 1

            # Print out highest score of the pixels just to see what type of scores I'm considering
            print "The highest score of this collection of top or bottom pixels is: ", highest_score, "."

            # Print out the scores that contribute to this highest score
            print "The scores that contribute to the highest score: "
            print "The U-Plane Score = ", uplane_array[highest_scoring_pixels[0]][highest_scoring_pixels[1]], "."
            print "The V-Plane Score = ", vplane_array[highest_scoring_pixels[0]][highest_scoring_pixels[2]], "."
            print "The Y-Plane Score = ", yplane_array[highest_scoring_pixels[0]][highest_scoring_pixels[3]], "."

            # Continue on with the loop if the highest score is less than or equal to zero
            if highest_score <= 0.1:

                print "This set of pixels, because of a low score, is getting thrown out."
                print "\n"
                continue

            # After this loop, you will know which is the highest scoring set of pixels, and you will append this result into the 'output_scored_pixels' list
            output_scored_pixels.append(highest_scoring_pixels)

            # Print out a blank line
            print "\n"

        # Print out a couple of blank spaces before moving onto the next hit type
        print "\n"
        print "\n"


        # Return 'output_scored_pixels' after the entire list is filled
        return output_scored_pixels
            
    # Begin the loop for upstream hits
    if hit_type == 2:

        # The 'pixel_list' will be a list of lists of lists, meaning that there are lists of the time pixels paired with their plane counterparts 
        for pixel_collection in pixel_list:

            # Declare the highest scoring set of pixels the first one in 'pixel_collection' (the values will be compared shortly)    
            highest_scoring_pixels = pixel_collection[0]

            # Declare the highest score of any of the pixels in the set to be that from the first one in 'pixel_collection'                  
            highest_score = uplane_array[pixel_collection[0][0]][pixel_collection[0][1]] + vplane_array[pixel_collection[0][0]][pixel_collection[0][2]]+ yplane_array[pixel_collection[0][0]][0]

            # Declare an iterator over the contents of 'pixel_collection'
            pixel_collection_iterator = 0

            # Now, loop through 'pixel_collection' calculate the score of each of the sets of pixels                             
            while pixel_collection_iterator < len(pixel_collection):

                # Calculate the current score of the 'plane_matched_pixels' that you're looping over
                current_score = uplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][1]] + vplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][2]]+ yplane_array[pixel_collection[pixel_collection_iterator][0]][0]

                # Now, you have some adjusting to do based on if one of the pixels is in a region of dead pixels on its respective plane
                
                # Define a counter for how many of the pixels for this hit are in a dead region on their respective plane                                              
                num_matched_pixels_in_dead_reg = 0

                # Loop over each collection of 'plane_dead_pixels' to see if any of these pixels are in any of their regions (you'll need two loops each)                
                
                # uplane                                                                                                                                                      
                for u_plane_list in uplane_dead_pixels:

                    for u_plane_pixel in u_plane_list: # (This is why I had to turn even single pixels into lists in 'dead_pixel_region_classifier_encapsulated')      
                        
                        if u_plane_pixel == pixel_collection[pixel_collection_iterator][1]:

                            # Increment 'num_matched_pixels_in_dead_reg'                                                                
                            num_matched_pixels_in_dead_reg += 1

                # vplane                                                                                                                                                       
                for v_plane_list in vplane_dead_pixels:

                    for v_plane_pixel in v_plane_list: # (This is why I had to turn even single pixels into lists in 'dead_pixel_region_classifier_encapsulated')            
                        
                        if v_plane_pixel == pixel_collection[pixel_collection_iterator][2]:

                            # Increment 'num_matched_pixels_in_dead_reg'                                                     
                            num_matched_pixels_in_dead_reg += 1

                # Now, adjust the score based on the value of 'num_matched_pixels_in_dead_reg'                                           
                if num_matched_pixels_in_dead_reg > 2:

                    # print "Whoa, something is seriously wrong!!"
                    # print "The collection of upstream pixels that are 3 or greater in dead pixel number to this is: ", [pixel_collection[pixel_collection_iterator][0], pixel_collection[pixel_collection_iterator][1], pixel_collection[pixel_collection_iterator][2]], "."
                    return 0

                if num_matched_pixels_in_dead_reg == 2:

                    # The current score should equal zero, but set it to zero and issue a print statement and the pixels in list form                        
                    # print "Both of the pixels for this current hit are in a dead region."
                    # print "The collection of upstream pixels is: ", [pixel_collection[pixel_collection_iterator][0], pixel_collection[pixel_collection_iterator][1], pixel_collection[pixel_collection_iterator][2]], "."
                    current_score = 0.

                if num_matched_pixels_in_dead_reg == 1:

                    # You have to multiply the current score by 3 to extrapolate what the ADC score would be otherwise                                                       
                    # print "One pixel for this current hit are in a dead region."
                    # print "The collection of upstream pixels is: ", [pixel_collection[pixel_collection_iterator][0], pixel_collection[pixel_collection_iterator][1], pixel_collection[pixel_collection_iterator][2]], "."
                    current_score = 2.*current_score


                # Check to see if the current score is greater than the highest_score                                                         
                if current_score > highest_score:

                    # Reset the highest score to the current score                                                                                
                    highest_score = current_score

                    # Set the highest scoring pixels to the pixels at this iterator in 'pixel_collection'        
                    highest_scoring_pixels = pixel_collection[pixel_collection_iterator]

                # Increment the 'pixel_collection_iterator'                                 
                pixel_collection_iterator += 1

            # Print out the highest scores of pixels just to see what types of scores I'm considering
            print "The highest score of this collection of upstream pixels is: ", highest_score, "."

            # Print out the scores that contribute to this highest score                                              
            print "The scores that contribute to the highest score: "
            print "The U-Plane Score = ", uplane_array[highest_scoring_pixels[0]][highest_scoring_pixels[1]], "."
            print "The V-Plane Score = ", vplane_array[highest_scoring_pixels[0]][highest_scoring_pixels[2]], "."
            print "The Y-Plane Score = ", yplane_array[highest_scoring_pixels[0]][0], "."

            # If the highest score is <= 0.0, then continue
            if highest_score <= 0.1:

                print "This set of pixels, because of a low score, is getting thrown out."
                print "\n"
                continue

            # Print out a newline first
            print "\n"

            # After this loop, you will know which is the highest scoring set of pixels, and you will append this result into the 'output_scored_pixels' list  
            output_scored_pixels.append(highest_scoring_pixels)

        # Print out a couple of spaces
        print "\n"
        print "\n"
        
        # Return the output scored pixels
        return output_scored_pixels

    # Begin the loop for downstream hits
    if hit_type == 3:

         # The 'pixel_list' will be a list of lists of lists, meaning that there are lists of the time pixels paired with their plane counterparts     
        for pixel_collection in pixel_list:

            # Declare the highest scoring set of pixels the first one in 'pixel_collection' (the values will be compared shortly)           
            highest_scoring_pixels = pixel_collection[0]

            # Declare the highest score of any of the pixels in the set to be that from the first one in 'pixel_collection'                         
            highest_score = uplane_array[pixel_collection[0][0]][pixel_collection[0][1]] + vplane_array[pixel_collection[0][0]][pixel_collection[0][2]]+ yplane_array[pixel_collection[0][0]][863]

            # Declare an iterator over the contents of 'pixel_collection'
            pixel_collection_iterator = 0

            # Now, loop through 'pixel_collection' calculate the score of each of the sets of pixels                                                                                 
            while pixel_collection_iterator < len(pixel_collection):

                current_score = uplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][1]] + vplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][2]]+ yplane_array[pixel_collection[pixel_collection_iterator][0]][863]

                # Now, you have some adjusting to do based on if one of the pixels is in a region of dead pixels on its respective plane
                
                # Define a counter for how many of the pixels for this hit are in a dead region on their respective plane                                                 
                num_matched_pixels_in_dead_reg = 0

                # Loop over each collection of 'plane_dead_pixels' to see if any of these pixels are in any of their regions (you'll need two loops each)           
                
                # uplane                                                                                                                
                for u_plane_list in uplane_dead_pixels:

                    for u_plane_pixel in u_plane_list: # (This is why I had to turn even single pixels into lists in 'dead_pixel_region_classifier_encapsulated')           
                        
                        if u_plane_pixel == pixel_collection[pixel_collection_iterator][1]:

                            # Increment 'num_matched_pixels_in_dead_reg'                                                                                                    
                            num_matched_pixels_in_dead_reg += 1

                # vplane                                                                                                                                                 
                for v_plane_list in vplane_dead_pixels:

                    for v_plane_pixel in v_plane_list: # (This is why I had to turn even single pixels into lists in 'dead_pixel_region_classifier_encapsulated')      
                        
                        if v_plane_pixel == pixel_collection[pixel_collection_iterator][2]:

                            # Increment 'num_matched_pixels_in_dead_reg'                                                                     
                            num_matched_pixels_in_dead_reg += 1

                # Now, adjust the score based on the value of 'num_matched_pixels_in_dead_reg'                                                                              
                if num_matched_pixels_in_dead_reg > 2:

                    # print "Whoa, something is seriously wrong!!"
                    # print "The collection of downstream pixels that are 3 or greater in dead pixel number to this is: ", [pixel_collection[pixel_collection_iterator][0], pixel_collection[pixel_collection_iterator][1], pixel_collection[pixel_collection_iterator][2]], "."
                    return 0

                if num_matched_pixels_in_dead_reg == 2:

                    # The current score should equal zero, but set it to zero and issue a print statement and the pixels in list form                                       
                    # print "Both of the pixels for this current hit are in a dead region."
                    # print "The collection of downstream pixels is: ", [pixel_collection[pixel_collection_iterator][0], pixel_collection[pixel_collection_iterator][1], pixel_collection[pixel_collection_iterator][2]], "."
                    current_score = 0.

                if num_matched_pixels_in_dead_reg == 1:

                    # You have to multiply the current score by 3 to extrapolate what the ADC score would be otherwise                                                      
                    # print "One pixel for this current hit are in a dead region."
                    # print "The collection of upstream pixels is: ", [pixel_collection[pixel_collection_iterator][0], pixel_collection[pixel_collection_iterator][1], pixel_collection[pixel_collection_iterator][2]], "."
                    current_score = 2.*current_score
                
                # Check to see if 'current_score' > 'highest_score'
                if current_score > highest_score:

                    # Reset the highest score to the current score
                    highest_score = current_score

                    # Set the highest scoring pixels to the pixels at this iterator in 'pixel_collection'
                    highest_scoring_pixels = pixel_collection[pixel_collection_iterator]

                # Increment the 'pixel_collection_iterator'
                pixel_collection_iterator += 1

            # Print out the highest scores of pixels just to see what types of scores I'm considering        
            print "The highest score of this collection of downstream pixels is: ", highest_score, "."

            # Print out the scores that contribute to this highest score                                                                                                   
            print "The scores that contribute to the highest score: "
            print "The U-Plane Score = ", uplane_array[highest_scoring_pixels[0]][highest_scoring_pixels[1]], "."
            print "The V-Plane Score = ", vplane_array[highest_scoring_pixels[0]][highest_scoring_pixels[2]], "."
            print "The Y-Plane Score = ", yplane_array[highest_scoring_pixels[0]][863], "."

            # If the highest score is <= 0, then continue (this set of pixels is in the middle of nowhere
            if highest_score <= 0.1:

                print "This set of pixels, because of a low score, is getting thrown out."
                print "\n"
                continue

            # Print out an extra space here
            print "\n"

            # After this loop, you will know which is the highest scoring set of pixels, and you will append this result into the 'output_scored_pixels' list 
            output_scored_pixels.append(highest_scoring_pixels)

        # Print out a couple of newlines
        print "\n"
        print "\n"

        # Return the output list of scored pixels
        return output_scored_pixels
            

                    
    
