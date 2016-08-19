# Define a function that will score matching pixels according to the amount of charge they have on each of the planes and then compares them to the other pixels that they are grouped with

# Input parameters:
# pixel_list - list of the pixels (grouped together) that are being scored
# uplane_array - the 2D grid of [pixel, time] for plane one, the uplane array
# vplane_array - the 2D grid of [pixel, time] for plane two, the vplane array
# yplane_array - the 2D grid of [pixel, time] for plane three, the yplane array
# hit_type - the type of hit that is being considered here.  Key - 0: top, 1: bottom, 2: upstream, 3: downstream

# This function does not have to discriminate between lists with three elements and those with four elements, because I can check the 0th and 863rd pixels in the arrays

def adjacent_pixels_color_scoring_algo(pixel_list, uplane_array, vplane_array, yplane_array, hit_type):

    # Declare an empty list for the output scored pixels
    output_scored_pixels = []

    # This the loop for top and bottom hits
    if hit_type == 0 or hit_type == 1:

        # The 'pixel_list' will be a list of lists of lists, meaning that there are lists of the time pixels paired with their plane counterparts
        for pixel_collection in pixel_list:

            # Declare the highest scoring set of pixels the first one in 'pixel_collection' (the values will be compared shortly)
            highest_scoring_pixels = pixel_collection[0]

            # Declare the highest score of any of the pixels in the set to be that from the first one in 'pixel_collection'
            highest_score = uplane_array[pixel_collection[0][0]][pixel_collection[0][1]] + vplane_array[pixel_collection[0][0]][pixel_collection[0][2]] + yplane_array[pixel_collection[0][0]][pixel_collection[0][2]]

            # Declare an iterator over the contents of 'pixel_colletion'
            pixel_collection_iterator = 0
        
            # Now, loop through 'pixel_collection' calculate the score of each of the sets of pixels
            for plane_matched_pixels in pixel_collection:

                current_score = uplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][1]] + vplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][2]]+ yplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][2]]

                # Check to see if the current score is greater than the highest_score
                if current_score > highest_score:
                    
                    # Reset the highest score to the current score
                    highest_score = current_score

                    # Set the highest scoring pixels to the pixels at this iterator in 'pixel_collection'
                    highest_scoring_pixels = pixel_collection[pixel_collection_iterator]

                # Increment the 'pixel_collection_iterator'
                pixel_collection_iterator += 1

            # After this loop, you will know which is the highest scoring set of pixels, and you will append this result into the 'output_scored_pixels' list
            output_scored_pixels.append(highest_scoring_pixels)

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
            for plane_matched_pixels in pixel_collection:

                # Calculate the current score of the 'plane_matched_pixels' that you're looping over
                current_score = uplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][1]] + vplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][2]]+ yplane_array[pixel_collection[pixel_collection_iterator][0]][0]

                # Check to see if the current score is greater than the highest_score                                                         
                if current_score > highest_score:

                    # Reset the highest score to the current score                                                                                
                    highest_score = current_score

                    # Set the highest scoring pixels to the pixels at this iterator in 'pixel_collection'        
                    highest_scoring_pixels = pixel_collection[pixel_collection_iterator]

                # Increment the 'pixel_collection_iterator'                                 
                pixel_collection_iterator += 1

            # After this loop, you will know which is the highest scoring set of pixels, and you will append this result into the 'output_scored_pixels' list  
            output_scored_pixels.append(highest_scoring_pixels)

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
            for plane_matched_pixels in pixel_collection:

                current_score = uplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][1]] + vplane_array[pixel_collection[pixel_collection_iterator][0]][pixel_collection[pixel_collection_iterator][2]]+ yplane_array[pixel_collection[pixel_collection_iterator][0]][863]
                
                # Check to see if 'current_score' > 'highest_score'
                if current_score > highest_score:

                    # Reset the highest score to the current score
                    highest_score = current_score

                    # Set the highest scoring pixels to the pixels at this iterator in 'pixel_collection'
                    highest_scoring_pixels = pixel_collection[pixel_collection_iterator]

                # Increment the 'pixel_collection_iterator'
                pixel_collection_iterator += 1

            # After this loop, you will know which is the highest scoring set of pixels, and you will append this result into the 'output_scored_pixels' list 
            output_scored_pixels.append(highest_scoring_pixels)

        return output_scored_pixels
            

                    
    
