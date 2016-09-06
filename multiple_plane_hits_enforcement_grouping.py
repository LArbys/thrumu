import math
import rounding

# Define a function that will take in the two or three lists of pairs of coordinates in [time, pixel], and combine them in the form [time, pixel_one, pixel_two] for the 
# // upstream and downstream hits and [time, pixel_one, pixel_two, pixel_three] for the top and bottom hits

# list_one_pixels, list_two_pixels, and list_three_pixels (for the top and bottom hits) are the three lists of pixels that are input to the function
# 'time_sep_plane_match' is an integer that serves as a threshold for determining if two time components are close enough to one another to consider them part of the same hit and therefore reason to group their average and different plane pixel components together
# 'time_sep_pixel_group' is an integer that serves as a threshold for determining if two pixel components are close enough together to consider them stemming from the same end of a muon
# 'pixel_sep' is an integer that serves as a threshold for determining if two pixel components are close enough to one another to consider them part of the same hit and therefore reason to group them together
# A given pixel's time component and (two or) three pixel components will all have to be within 'time_sep_pixel_group' or 'pixel_sep', respectively, for me to group them with an existing list instead of making a new list within the output
def new_pixel_organization(time_sep_plane_match, time_sep_pixel_group, pixel_sep, list_one_pixels, list_two_pixels, list_three_pixels):

    # Initialize an empty list for the plane pixels that will be have to be filled
    imaging_pixel_list = []

    # First, check to see if 'list_three_pixels' == None to see if it is taking the upstream or downstream coordinate lists as inputs
    if list_three_pixels == None:  

        # Print out a statement when the algorithm enters into this loop
        # print "The algorithm is entering into the outer loop of the upstream/downstream loop for the %dst time." % num_outer_loop
        # print "\n"
        # print "\n"

        # Initialize an outer loop over 'list_one_pixels'
        for list_one_entry in list_one_pixels:

            # Define variables for the time and the pixel in 'list_one_pixels'
            list_one_time  = list_one_entry[0]
            list_one_pixel = list_one_entry[1]

            # Initialize an inner loop over 'list_two_pixels'
            for list_two_entry in list_two_pixels:

                # Define variables for the time and the pixel in 'list_two_pixels'
                list_two_time  = list_two_entry[0]
                list_two_pixel = list_two_entry[1]

                # Insert another print statement
                # print "The algorithm is in the inner loop of the upstream/downstream loop."
                # print "\n"

                # Compare the time components from the two lists to see if they are close enough to be considered part of the same track
                if math.fabs(list_one_time - list_two_time) < time_sep_plane_match:

                    # Append to the list in this case with the average of 'list_one_time' and 'list_two_time'
                    avg_time = (float(list_one_time) + float(list_two_time)) / 2.

                    # Round 'avg_time' the usual way, because it is of type 'float' and the 'int' function conversion has a serious shortcoming of just cutting                  
                    # // off the decimal part of the number                                                                 
                    avg_time = rounding.rounding_function(avg_time)

                    # If 'imaging_pixel_list' is empty, then fill it with the first match (there's nothing to compare this match to, so it must be the start of a list)
                    if imaging_pixel_list == []:

                        # Append an empty list (the first one)
                        imaging_pixel_list.append([])
                        # Append the first match of time and pixels
                        imaging_pixel_list[0].append([avg_time, list_one_pixel, list_two_pixel])

                        # Print out Imaging Pixel List for the case of a new pixel match close to another pixel match                                                            
                        # print "The imaging pixel list after the first set of pixels was appended: ", imaging_pixel_list, "."                                                   
                        # print "\n"

                    else: # This is after the first case, when there are already elements within 'imaging_pixel_list'

                        # Declare an iterator that will tell me at which index value in 'imaging_pixel_list' 'element' is located
                        imaging_pixel_list_index = 0

                        # Start a loop over the existing elements of 'imaging_pixel_list'
                        for element in imaging_pixel_list:

                            # The program will still crash, but print out the element just to see what it looks like 
                            # print "Element before (if/when) the program crashes: ", element, "."
                            # print "\n"

                            # Include an 'if' statement comparing the current values of 'avg_time', 'list_one_pixel', and 'list_two_pixel' to the 
                            # // corresponding components in the 'element' in the current iteration
                            if math.fabs(avg_time - element[0][0]) < time_sep_pixel_group and math.fabs(list_one_pixel - element[0][1]) < pixel_sep and math.fabs(list_two_pixel - element[0][2]) < pixel_sep:

                                # Append the current values of 'avg_time', 'list_one_pixel', and 'list_two_pixel' to 'imaging_pixel_list' if the time component and each of the pixel components are within the correct allowance
                                imaging_pixel_list[imaging_pixel_list_index].append([avg_time, list_one_pixel, list_two_pixel])

                                # Print out Imaging Pixel List for the case of a new pixel match close to another pixel match                                                    
                                # print "The imaging pixel list after a new set of pixels was close to an existing set of pixels is: ", imaging_pixel_list, "."                  
                                # print "\n"

                                # Break the loop at this point; These values should not be appended to more than one list
                                break 
                            
                            # Increment 'imaging_pixel_list_index' 
                            imaging_pixel_list_index += 1

                        # If the 'for' loop never broke, then 'imaging_pixel_list_index' is equal to len(imaging_pixel_list), so I can use an 'if' statement to determine if this is the case and then append a new list onto 'imaging_pixel_list' and fill it with this match of [avg_time, list_one_pixel, list_two_pixel]
                        if imaging_pixel_list_index == len(imaging_pixel_list):

                            # Append a new list onto 'imaging_pixel_list'
                            imaging_pixel_list.append([])

                            # Append this match of [avg_time, list_one_pixel, list_two_pixel]
                            imaging_pixel_list[imaging_pixel_list_index].append([avg_time, list_one_pixel, list_two_pixel])

                            # Print out Imaging Pixel List for the case of a new pixel match close to another pixel match                                                        
                            # print "The imaging pixel list after a new set of pixels was far enough away from every other set of pixels to warrant a new list of pixels: ", imaging_pixel_list, "."
                            # print "\n"

        # Include a statement that the function is ending
        # print "The function is terminating."
        # print "\n"
                    
        # Return the 'imaging_pixel_list' after it is filled with the organized upstream/downstream pixels that need to be filled a certain color
        return imaging_pixel_list

    # Consider the case for hits on the top and the bottom.  This will be the same as the algorithm above, except it will include 'list_three_pixels', a list that does not have 
    # // data type 'None'
    else:

        # Initialize an outer loop over 'list_one_pixels'                                                                                                                      
        for list_one_entry in list_one_pixels:

            # Define variables for the time and the pixel in 'list_one_pixels'                                                                                               
            list_one_time  = list_one_entry[0]
            list_one_pixel = list_one_entry[1]

            # Initialize a middle loop over 'list_two_pixels'                                                                                                                  
            for list_two_entry in list_two_pixels:

                # Define variables for the time and the pixel in 'list_two_pixels'                                                                                             
                list_two_time  = list_two_entry[0]
                list_two_pixel = list_two_entry[1]

                # Insert another print statement                                                                                                                               
                # print "The algorithm is in the inner loop of the top/bottom loop."
                # print "\n"
                
                # Initialize an inner loop over 'list_three_pixels'
                for list_three_entry in list_three_pixels:

                    # Define variables for the time and the pixel in 'list_three_pixels'
                    list_three_time  = list_three_entry[0]
                    list_three_pixel = list_three_entry[1]

                    # Compare the time components from the two lists to see if they are close enough to be considered part of the same track                                      
                    if math.fabs(list_one_time - list_two_time) < time_sep_plane_match and math.fabs(list_one_time - list_three_time) < time_sep_plane_match and math.fabs(list_two_time - list_three_time) < time_sep_plane_match:

                        # Append to the list in this case with the average of 'list_one_time', 'list_two_time', and 'list_three_time                                        
                        avg_time = (float(list_one_time) + float(list_two_time) + float(list_three_time)) / 3.

                        # Round 'avg_time' the usual way, because it is of type 'float' and the 'int' function conversion has a serious shortcoming of just cutting                
                        # // off the decimal part of the number                                                                                                                    
                        avg_time = rounding.rounding_function(avg_time)
                        
                         # If 'imaging_pixel_list' is empty, then fill it with the first match (there's nothing to compare this match to, so it must be the start of a list) 
                        if imaging_pixel_list == []:

                            # Append an empty list (the first one)                                                                                   
                            imaging_pixel_list.append([])
                            # Append the first match of time and pixels
                            imaging_pixel_list[0].append([avg_time, list_one_pixel, list_two_pixel, list_three_pixel])

                            # Print out Imaging Pixel List for the case of a new pixel match close to another pixel match                                                    
                            # print "The imaging pixel list after the first set of pixels was appended: ", imaging_pixel_list, "."
                            # print "\n"

                        else: # This is after the first case, when there are already elements within 'imaging_pixel_list'                                                          
                        
                            # Declare an iterator that will tell me at which index value in 'imaging_pixel_list' 'element' is located                  
                            imaging_pixel_list_index = 0

                            # Start a loop over the existing elements of 'imaging_pixel_list'                                                                       
                            for element in imaging_pixel_list:

                                # The program will still crash, but print out the element just to see what it looks like        
                                # print "Element before (if/when) the program crashes: ", element, "."
                                # print "\n"

                                # Include an 'if' statement comparing the current values of 'avg_time', 'list_one_pixel', and 'list_two_pixel' to the   
                                # // corresponding components in the 'element' in the current iteration            
                                if math.fabs(avg_time - element[0][0]) < time_sep_pixel_group and math.fabs(list_one_pixel - element[0][1]) < pixel_sep and math.fabs(list_two_pixel - element[0][2]) < pixel_sep and math.fabs(list_three_pixel - element[0][3]) < pixel_sep:
                                    
                                    # Append the current values of 'avg_time', 'list_one_pixel', and 'list_two_pixel' to 'imaging_pixel_list' if the time component and each of the pixel components are within the correct allowance                                                                                        
                                    imaging_pixel_list[imaging_pixel_list_index].append([avg_time, list_one_pixel, list_two_pixel, list_three_pixel])

                                    # Print out Imaging Pixel List for the case of a new pixel match close to another pixel match
                                    # print "The imaging pixel list after a new set of pixels was close to an existing set of pixels is: ", imaging_pixel_list, "."
                                    # print "\n"

                                    # Break the loop at this point; These values should not be appended to more than one list 
                                    break

                                # Increment 'imaging_pixel_list_index'                                                      
                                imaging_pixel_list_index += 1

                            # If the 'for' loop never broke, then 'imaging_pixel_list_index' is equal to len(imaging_pixel_list), so I can use an 'if' statement to determine if this is the case and then append a new list onto 'imaging_pixel_list' and fill it with this match of [avg_time, list_one_pixel, list_two_pixel]  
                            if imaging_pixel_list_index == len(imaging_pixel_list):

                                # Append a new list onto 'imaging_pixel_list'                                                                   
                                imaging_pixel_list.append([])

                                # Append this match of [avg_time, list_one_pixel, list_two_pixel]                                           
                                imaging_pixel_list[imaging_pixel_list_index].append([avg_time, list_one_pixel, list_two_pixel, list_three_pixel])
                                
                                # Print out Imaging Pixel List for the case of a new pixel match close to another pixel match                                  
                                # print "The imaging pixel list after a new set of pixels was far enough away from every other set of pixels to warrant a new list of pixels: ", imaging_pixel_list, "."
                                # print "\n"

        # Include a statement that the function is ending                                                                                 
        # print "The function is terminating."
        # print "\n"

        # Return the 'imaging_pixel_list' after it is filled with the organized upstream/downstream pixels that need to be filled a certain color                           
        return imaging_pixel_list

        
                    
        
