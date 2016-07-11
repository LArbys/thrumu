## Script that will perform clustering on the algorithm after taking in the lists of hits of each type for each event ##

import numpy as np
import math

def pixel_clustering_centers_algo(upstream_pixel_hits, downstream_pixel_hits, top_pixel_hits, bottom_pixel_hits):

    # Make sure that each of the dicts inherited by the function have contents, i.e., that they are not equal to {}
    # If they are equal to {}, set them equal to a default value so that the program won't crash
    if upstream_pixel_hits == {}:

        upstream_pixel_hits[0] = [0, 0, 0]

    if downstream_pixel_hits == {}:

        downstream_pixel_hits[0] = [0, 0, 0]

    if top_pixel_hits == {}:

        top_pixel_hits[0] = [0, 0, 0, 0]

    if bottom_pixel_hits == {}:

        bottom_pixel_hits[0] = [0, 0, 0, 0]

    # Initialize arrays for the centers of the clusters of the groups of pixels on each plane for each type of hit here

    upstream_pixel_u_center_list = []
    upstream_pixel_v_center_list = []

    downstream_pixel_u_center_list = []
    downstream_pixel_v_center_list = []

    top_pixel_u_center_list = []
    top_pixel_v_center_list = []
    top_pixel_y_center_list = []

    bottom_pixel_u_center_list = []
    bottom_pixel_v_center_list = []
    bottom_pixel_y_center_list = []
    
    # Append the first member of each list of hits to the list of centers to have some reference off which to base the rest of the centers (i.e., loop over them if they are within a certain pixel distance from this one)

    # The upstream and downstream hits don't have "hit" pixels on the y plane!
    upstream_pixel_u_center_list.append(upstream_pixel_hits[0][1])
    upstream_pixel_v_center_list.append(upstream_pixel_hits[0][2])
    
    downstream_pixel_u_center_list.append(downstream_pixel_hits[0][1])
    downstream_pixel_v_center_list.append(downstream_pixel_hits[0][2])

    # The top and bottom hits DO have "hit" pixels on the y plane!

    top_pixel_u_center_list.append(top_pixel_hits[0][1])
    top_pixel_v_center_list.append(top_pixel_hits[0][2])
    top_pixel_y_center_list.append(top_pixel_hits[0][3])

    bottom_pixel_u_center_list.append(bottom_pixel_hits[0][1])
    bottom_pixel_v_center_list.append(bottom_pixel_hits[0][2])
    bottom_pixel_y_center_list.append(bottom_pixel_hits[0][3])
    
    # Find the groups of pixels that can be used to differentiate the clusters of pixels from one another (the next step will be assigning them to a group)
    # First, the group of upstream pixels
    for upstream_pixel_hit_group in upstream_pixel_hits:

        # Create a variable that will be incremented each time there is a center that is greater than 5 pixel units away from the given hit in the center_list (for each of the planes)
        u_centers_far_away = 0
        v_centers_far_away = 0

        for upstream_u_center in upstream_pixel_u_center_list:

            if math.fabs(upstream_u_center - upstream_pixel_hits[upstream_pixel_hit_group][1]) > 5:

                u_centers_far_away += 1

        for upstream_v_center in upstream_pixel_v_center_list:

            if math.fabs(upstream_v_center - upstream_pixel_hits[upstream_pixel_hit_group][2]) > 5:

                v_centers_far_away += 1
        
        # If the number of centers far away is equal to the length of the list, then this new center is far enough away that I can declare it a new center
        if u_centers_far_away == len(upstream_pixel_u_center_list):

            upstream_pixel_u_center_list.append(upstream_pixel_hits[upstream_pixel_hit_group][1])

        if v_centers_far_away == len(upstream_pixel_v_center_list):
            
            upstream_pixel_v_center_list.append(upstream_pixel_hits[upstream_pixel_hit_group][2])

    
    # Next, the group of downstream pixel hits
    for downstream_pixel_hit_group in downstream_pixel_hits:

        # Create a variable that will be incremented each time there is a center that is greater than 5 pixel units away from the given hit in the center_list (for each of the planes)                                                                                                                                                                            
        u_centers_far_away = 0
        v_centers_far_away = 0

        # Check to see if the distance between every member of the centers vector and the member of the pixel hits is greater than 5 pixel units                              
        for downstream_u_center in downstream_pixel_u_center_list:

            if math.fabs(downstream_u_center - downstream_pixel_hits[downstream_pixel_hit_group][1]) > 5:

                u_centers_far_away += 1

        for downstream_v_center in downstream_pixel_v_center_list:

            if math.fabs(downstream_v_center - downstream_pixel_hits[downstream_pixel_hit_group][2]) > 5:

                v_centers_far_away += 1

        # Now, for this hit group, see if this pixel's coordinates are greater than every member of the group based on the values of u_centers_far_away, v_centers_far_away, and y_centers_far_away                                                                                                                                                                   
        if u_centers_far_away == len(downstream_pixel_u_center_list):

            downstream_pixel_u_center_list.append(downstream_pixel_hits[downstream_pixel_hit_group][1])

        if v_centers_far_away == len(downstream_pixel_v_center_list):

            downstream_pixel_v_center_list.append(downstream_pixel_hits[downstream_pixel_hit_group][2])

    # Next, the group of top pixel hits
    for top_pixel_hit_group in top_pixel_hits:

        # Create a variable that will be incremented each time there is a center that is greater than 5 pixel units away from the given hit in the center_list (for each of the planes) (10 for the y plane, the induction plane)
        u_centers_far_away = 0
        v_centers_far_away = 0
        y_centers_far_away = 0

        # Check to see if the distance between every member of the centers vector and the member of the pixel hits is greater than 5 pixel units (10 for the y plane)             
        for top_u_center in top_pixel_u_center_list:

            if math.fabs(top_u_center - top_pixel_hits[top_pixel_hit_group][1]) > 5:

                u_centers_far_away += 1

        for top_v_center in top_pixel_v_center_list:

            if math.fabs(top_v_center - top_pixel_hits[top_pixel_hit_group][2]) > 5:

                v_centers_far_away += 1

        for top_y_center in top_pixel_y_center_list:

            if math.fabs(top_y_center - top_pixel_hits[top_pixel_hit_group][3]) > 10:

                y_centers_far_away += 1

        # Now, for this hit group, see if this pixel's coordinates are greater than every member of the group based on the values of time_centers_far_away, u_centers_far_away, v_centers_far_away, and y_centers_far_away                                                                                                                                             
        if u_centers_far_away == len(top_pixel_u_center_list):

            top_pixel_u_center_list.append(top_pixel_hits[top_pixel_hit_group][1])

        if v_centers_far_away == len(top_pixel_v_center_list):

            top_pixel_v_center_list.append(top_pixel_hits[top_pixel_hit_group][2])

        if y_centers_far_away == len(top_pixel_y_center_list):

            top_pixel_y_center_list.append(top_pixel_hits[top_pixel_hit_group][3])

    # Next, the group of bottom pixel hits                                                                                                                                         
    for bottom_pixel_hit_group in bottom_pixel_hits:

        # Create a variable that will be incremented each time there is a center that is greater than 5 pixel units away from the given hit in the center_list (for each of the planes) (10 for the y plane)
        u_centers_far_away = 0
        v_centers_far_away = 0
        y_centers_far_away = 0

        # Check to see if the distance between every member of the centers vector and the member of the pixel hits is greater than 5 pixel units (10 for time)                 
        for bottom_u_center in bottom_pixel_u_center_list:

            if math.fabs(bottom_u_center - bottom_pixel_hits[bottom_pixel_hit_group][1]) > 5:

                u_centers_far_away += 1

        for bottom_v_center in bottom_pixel_v_center_list:

            if math.fabs(bottom_v_center - bottom_pixel_hits[bottom_pixel_hit_group][2]) > 5:

                v_centers_far_away += 1

        for bottom_y_center in bottom_pixel_y_center_list:

            if math.fabs(bottom_y_center - bottom_pixel_hits[bottom_pixel_hit_group][3]) > 10:

                y_centers_far_away += 1

        # Now, for this hit group, see if this pixel's coordinates are greater than every member of the group based on the values of u_centers_far_away, v_centers_far_away, and y_centers_far_away                                                                                                                                                       
        if u_centers_far_away == len(bottom_pixel_u_center_list):

            bottom_pixel_u_center_list.append(bottom_pixel_hits[bottom_pixel_hit_group][1])

        if v_centers_far_away == len(bottom_pixel_v_center_list):

            bottom_pixel_v_center_list.append(bottom_pixel_hits[bottom_pixel_hit_group][2])

        if y_centers_far_away == len(bottom_pixel_y_center_list):

            bottom_pixel_y_center_list.append(bottom_pixel_hits[bottom_pixel_hit_group][3])

        return [upstream_pixel_u_center_list, upstream_pixel_v_center_list, downstream_pixel_u_center_list, downstream_pixel_v_center_list, top_pixel_u_center_list, top_pixel_v_center_list, top_pixel_y_center_list, bottom_pixel_u_center_list, bottom_pixel_v_center_list, bottom_pixel_y_center_list]


# Define a function to assign each of the points within the hit functions to a center that it is closest to and organize these points into a list
def pixel_cluster_assignment_algo(upstream_pixel_hits, downstream_pixel_hits, top_pixel_hits, bottom_pixel_hits):

    # Unpack the output from the previous function to acquire the lists of centers for each type of hits
    [up_u_center_list, up_v_center_list, down_u_center_list, down_v_center_list, top_u_center_list, top_v_center_list, top_y_center_list, bottom_u_center_list, bottom_v_center_list, bottom_y_center_list] = pixel_clustering_centers_algo(upstream_pixel_hits, downstream_pixel_hits, top_pixel_hits, bottom_pixel_hits)

    # Declare lists of lists of all the u, v, and y pixel values that correspond to the center at the same list position in the center lists
    # The next step will be to append them with the same number of entries (for now, empty lists) as the center lists above

    # Declare this list separately from the others. See if initializing the list this way is better... (news flash: it is)

    # Later, these will be averaged and combined into a single list
    up_u_time_hits_organized = []
    up_v_time_hits_organized = []

    up_u_hits_organized = []
    up_v_hits_organized = []

    # Later, these will be averaged and combined into a single list
    down_u_time_hits_organized = []
    down_v_time_hits_organized = []

    down_u_hits_organized = []
    down_v_hits_organized = []

    # Later, these will be averaged and combined into a single list
    top_u_time_hits_organized = []
    top_v_time_hits_organized = []
    top_y_time_hits_organized = []

    top_u_hits_organized = []
    top_v_hits_organized = []
    top_y_hits_organized = []
    
    # Later, these will be averaged and combined into a single list
    bottom_u_time_hits_organized = []
    bottom_v_time_hits_organized = []
    bottom_y_time_hits_organized = []

    bottom_u_hits_organized = []
    bottom_v_hits_organized = []
    bottom_y_hits_organized = []

    # Append a list onto each of the entries of the lists with different 'while' loops over the lengths of the lists
    # Declare an iterator
    i = 0

    # Use the loop again (this time for the up_u_center_list)
    while i < len(up_u_center_list):

        # Append an empty list onto the original list
        up_u_hits_organized.append([])
        up_u_time_hits_organized.append([])

        # Increment the iterator
        i += 1


    # Reset the iterator to 0
    i = 0

    # Use the loop again (for the up_v_center_list)
    while i < len(up_v_center_list):

        # Append an empty list onto the original list
        up_v_hits_organized.append([])
        up_v_time_hits_organized.append([])
        
        # Increment the iterator
        i += 1

    # Reset the iterator to 0
    i = 0

    # Use the loop again (for the down_u_center_list)                                                                                                                        
    while i < len(down_u_center_list):

        # Append an empty list onto the original list
        down_u_hits_organized.append([])
        down_u_time_hits_organized.append([])

        # Increment the iterator
        i += 1

    
    # Reset the iterator to 0                                                                                                                                              
    i = 0

    # Use the loop again (for the down_v_center_list)                                                                                                                       
    while i < len(down_v_center_list):

        # Append an empty list onto the original list
        down_v_hits_organized.append([])
        down_v_time_hits_organized.append([])

        # Increment the iterator
        i += 1

    # Reset the iterator to 0                                                                                                                                              
    i = 0

    # Use the loop again (for the top_u_center_list)                                                                                                                        
    while i < len(top_u_center_list):

        # Append an empty list onto the original list
        top_u_hits_organized.append([])
        top_u_time_hits_organized.append([])

        # Increment the iterator
        i += 1


    # Reset the iterator to 0                                                                                                                                                
    i = 0

    # Use the loop again (for the top_v_center_list)                                                                                                                        
    while i < len(top_v_center_list):

        # Append an empty list onto the original list
        top_v_hits_organized.append([])
        top_v_time_hits_organized.append([])

        # Increment the iterator
        i += 1

    
    # Reset the iterator to 0                                                                                                                                                
    i = 0

    # Use the loop again (for the top_y_center_list)                                                                                                                           
    while i < len(top_y_center_list):

        # Append an empty list onto the original list
        top_y_hits_organized.append([])
        top_y_time_hits_organized.append([])

        # Increment the iterator 
        i += 1


    # Reset the iterator to 0                                                                                                                                              
    i = 0

    # Use the loop again (for the bottom_u_center_list)                                                                                                                     
    while i < len(bottom_u_center_list):

        # Append an empty list onto the original list
        bottom_u_hits_organized.append([])
        bottom_u_time_hits_organized.append([])

        # Increment the iterator
        i += 1

    
    # Reset the iterator to 0                                                                                                                                             
    i = 0

    # Use the loop again (for the bottom_v_center_list)                                                                                                                  
    while i < len(bottom_v_center_list):

        # Append an empty list onto the original list
        bottom_v_hits_organized.append([])
        bottom_v_time_hits_organized.append([])

        # Increment the iterator
        i += 1

    
    # Reset the iterator to 0                                                                                                                                           
    i = 0

    # Use the loop again (for the bottom_v_center_list)                                                                                                              
    while i < len(bottom_v_center_list):

        # Append an empty list onto the original list
        bottom_y_hits_organized.append([])
        bottom_y_time_hits_organized.append([])

        # Increment the iterator
        i += 1

    # Now, begin a loop over the upstream_hits to find out which u, v, and y center is closest to that particular pixel 
    for upstream_pixel_hit_group in upstream_pixel_hits:

        # Unpack the pixel components from upstream_pixel_hits:
        
        # I'm going to append the time to the list on the correct plane for whichever center is closest
        # Then I'll average the contents of each of list within each entry of the u, v, and y lists, and then I'll average those lists together
        time    = upstream_pixel_hits[upstream_pixel_hit_group][0]

        u_pixel = upstream_pixel_hits[upstream_pixel_hit_group][1]
        v_pixel = upstream_pixel_hits[upstream_pixel_hit_group][2]

        # (Re)define the closest center as the first center in each of the u, v, and y center lists
        u_center_closest = up_u_center_list[0]
        v_center_closest = up_v_center_list[0]

        # Now, loop over each center in u and v to find out which center is closest to this particular hit
        for u_center in up_u_center_list:

            if math.fabs(u_pixel - u_center) < math.fabs(u_pixel - u_center_closest):
        
                u_center_closest = u_center

        for v_center in up_v_center_list:

            if math.fabs(v_pixel - v_center) < math.fabs(v_pixel - v_center_closest):

                v_center_closest = v_center

        # Set the iterator to 0
        j = 0

        while j < len(up_u_center_list):

            if up_u_center_list[j] == u_center_closest:
                
                up_u_hits_organized[j].append(u_pixel)
                up_u_time_hits_organized[j].append(time)

            # Increment the iterator
            j += 1

        # Set the iterator to 0
        j = 0

        # Use the same loop on the v hits
        while j < len(up_v_center_list):

            if up_v_center_list[j] == v_center_closest:

                up_v_hits_organized[j].append(v_pixel)
                up_v_time_hits_organized[j].append(time)

            # Increment the iterator
            j += 1

    # Now, begin a loop over the downstream_hits to find out which u, v, and y center is closest to that particular pixel                                                           
    for downstream_pixel_hit_group in downstream_pixel_hits:

        # Unpack the pixel components from downstream_pixel_hits: 

        # I'm going to append the time to the list on the correct plane for whichever center is closest                                                                          
        # Then I'll average the contents of each of list within each entry of the u, v, and y lists, and then I'll average those lists together
        time    = downstream_pixel_hits[downstream_pixel_hit_group][0]

        u_pixel = downstream_pixel_hits[downstream_pixel_hit_group][1]
        v_pixel = downstream_pixel_hits[downstream_pixel_hit_group][2]

        # (Re)define the closest center as the first center in each of the u, v, and y center lists                                                                             
        # time_center_closest = down_time_center_list[0]
        u_center_closest = down_u_center_list[0]
        v_center_closest = down_v_center_list[0]

        # Now, loop over each center in u and v to find out which one is closest
        for u_center in down_u_center_list:

            if math.fabs(u_pixel - u_center) < math.fabs(u_pixel - u_center_closest):

                u_center_closest = u_center

        for v_center in down_v_center_list:

            if math.fabs(v_pixel - v_center) < math.fabs(v_pixel - v_center_closest):

                v_center_closest = v_center

        # Set the index to 0
        j = 0

        while j < len(down_u_center_list):

            if down_u_center_list[j] == u_center_closest:

                down_u_hits_organized[j].append(u_pixel)
                down_u_time_hits_organized[j].append(time)

            # Increment the iterator                                                                                                                                            
            j += 1

        # Set the index to 0                                                                                                                                                    
        j = 0

        # Use the same loop on the v hits                                                                                                                                       
        while j < len(down_v_center_list):

            if down_v_center_list[j] == v_center_closest:

                down_v_hits_organized[j].append(v_pixel)
                down_v_time_hits_organized[j].append(time)

            # Increment the iterator                                                                                                                                           
            j += 1

    # Now, begin a loop over the top_hits to find out which time, u, v, and y center is closest to that particular pixel
    for top_pixel_hit_group in top_pixel_hits:

        # Unpack the pixel components from upstream_pixel_hits:  

        # I'm going to append the time to the list on the correct plane for whichever center is closest                                                                          
        # Then I'll average the contents of each of list within each entry of the u, v, and y lists, and then I'll average those lists together
        time    = top_pixel_hits[top_pixel_hit_group][0]

        u_pixel = top_pixel_hits[top_pixel_hit_group][1]
        v_pixel = top_pixel_hits[top_pixel_hit_group][2]
        y_pixel = top_pixel_hits[top_pixel_hit_group][3]

        # (Re)define the closest center as the first center in each of the u, v, and y center lists                                                                              
        u_center_closest    = top_u_center_list[0]
        v_center_closest    = top_v_center_list[0]
        y_center_closest    = top_y_center_list[0]

        # Now, loop over each of the lists of centers to find out which center is the closest:                                                                                   
        for u_center in top_u_center_list:

            if math.fabs(u_pixel - u_center) < math.fabs(u_pixel - u_center_closest):

                u_center_closest = u_center

        for v_center in top_v_center_list:

            if math.fabs(v_pixel - v_center) < math.fabs(v_pixel - v_center_closest):

                v_center_closest = v_center

        for y_center in top_y_center_list:

            if math.fabs(y_pixel - y_center) < math.fabs(y_pixel - y_center_closest):

                y_center_closest = y_center

        # Set the index to 0
        j = 0

        while j < len(top_u_center_list):

            if top_u_center_list[j] == u_center_closest:

                top_u_hits_organized[j].append(u_pixel)
                top_u_time_hits_organized[j].append(time)

            # Increment the iterator                                                                                                                                             
            j += 1

        # Set the index to 0                                                                                                                                                     
        j = 0

        # Use the same loop on the v hits                                                                                                                                        
        while j < len(top_v_center_list):

            if top_v_center_list[j] == v_center_closest:

                top_v_hits_organized[j].append(v_pixel)
                top_v_time_hits_organized[j].append(time)

            # Increment the iterator                                                                                                                                           
            j += 1

        # Set the index to 0
        j = 0

        # Use the same loop on the v hits                                                                                                                                        
        while j < len(top_y_center_list):

            if top_y_center_list[j] == y_center_closest:

                top_y_hits_organized[j].append(y_pixel)
                top_y_time_hits_organized[j].append(time)

            # Increment the iterator
            j += 1

    # Now, begin a loop over the bottom_hits to find out which u, v, and y center is closest to that particular pixel                                                            
    for bottom_pixel_hit_group in bottom_pixel_hits:

        # Unpack the pixel components from upstream_pixel_hits:

        # I'm going to append the time to the list on the correct plane for whichever center is closest                                                                        
        # Then I'll average the contents of each of list within each entry of the u, v, and y lists, and then I'll average those lists together
        time    = bottom_pixel_hits[bottom_pixel_hit_group][0]

        u_pixel = bottom_pixel_hits[bottom_pixel_hit_group][1]
        v_pixel = bottom_pixel_hits[bottom_pixel_hit_group][2]
        y_pixel = bottom_pixel_hits[bottom_pixel_hit_group][3]

        # (Re)define the closest center as the first center in each of the u, v, and y center lists                                                                               
        # time_center_closest = bottom_time_center_list[0]
        u_center_closest    = bottom_u_center_list[0]
        v_center_closest    = bottom_v_center_list[0]
        y_center_closest    = bottom_y_center_list[0]

        # Now, loop over each of the lists of centers to find out which center is the closest:                                                                                   
        for u_center in bottom_u_center_list:

            if math.fabs(u_pixel - u_center) < math.fabs(u_pixel - u_center_closest):

                u_center_closest = u_center

        for v_center in bottom_v_center_list:

            if math.fabs(v_pixel - v_center) < math.fabs(v_pixel - v_center_closest):

                v_center_closest = v_center

        for y_center in bottom_y_center_list:

            if math.fabs(y_pixel - y_center) < math.fabs(y_pixel - y_center_closest):

                y_center_closest = y_center

        # Do another loop over the u, v, and y centers, using fact that the index of the list of lists for pixels is the same as the index of the center in the list of centers  
        # Set the index to 0
        j = 0

        while j < len(bottom_u_center_list):

            if bottom_u_center_list[j] == u_center_closest:

                bottom_u_hits_organized[j].append(u_pixel)
                bottom_u_time_hits_organized[j].append(time)

            # Increment the iterator                                                                                                                                             
            j += 1

        # Set the index to 0                                                                                                                                                      
        j = 0

        # Use the same loop on the v hits                                                                                                                                        
        while j < len(bottom_v_center_list):

            if bottom_v_center_list[j] == v_center_closest:

                bottom_v_hits_organized[j].append(v_pixel)
                bottom_v_time_hits_organized[j].append(time)
            
            # Increment the iterator                                                                                                                                              
            j += 1

        # Set the index to 0                                                                                                                                                      
        j = 0

        # Use the same loop on the v hits                                                                                                                                        
        while j < len(bottom_y_center_list):

            if bottom_y_center_list[j] == y_center_closest:

                bottom_y_hits_organized[j].append(y_pixel)
                bottom_y_time_hits_organized[j].append(time)

            # Increment the iterator                                                                                                                                            
            j += 1

    return [up_u_time_hits_organized, up_v_time_hits_organized, up_u_hits_organized, up_v_hits_organized, down_u_time_hits_organized, down_v_time_hits_organized, down_u_hits_organized, down_v_hits_organized, top_u_time_hits_organized, top_v_time_hits_organized, top_y_time_hits_organized, top_u_hits_organized, top_v_hits_organized, top_y_hits_organized, bottom_u_time_hits_organized, bottom_v_time_hits_organized, bottom_y_time_hits_organized, bottom_u_hits_organized, bottom_v_hits_organized, bottom_y_hits_organized]


# Define a function that will take the average of all of the pixels now that they're grouped by center, and declare that the new center.  The old list will be replaced with the average
# This function takes the same four arguments (upstream_pixel_hits, downstream_pixel_hits, top_pixel_hits, bottom_pixel_hits) (all in dictionary form)
def pixel_average_calculator(upstream_pixel_hits, downstream_pixel_hits, top_pixel_hits, bottom_pixel_hits):

    [up_u_time_hits_center_organized, up_v_time_hits_center_organized, up_u_hits_center_organized, up_v_hits_center_organized, down_u_time_hits_center_organized, down_v_time_hits_center_organized, down_u_hits_center_organized, down_v_hits_center_organized, top_u_time_hits_center_organized, top_v_time_hits_center_organized, top_y_time_hits_center_organized, top_u_hits_center_organized, top_v_hits_center_organized, top_y_hits_center_organized, bottom_u_time_hits_center_organized, bottom_v_time_hits_center_organized, bottom_y_time_hits_center_organized, bottom_u_hits_center_organized, bottom_v_hits_center_organized, bottom_y_hits_center_organized] = pixel_cluster_assignment_algo(upstream_pixel_hits, downstream_pixel_hits,top_pixel_hits, bottom_pixel_hits)

    # Do a loop to average each of the elements in the list of up_u_time_hits_center_organized


    ### Start of Section of Code for the Upstream_Time_Group_Hits ###

    # Define an iterator that will define the element of the list of up_u_time_hits_center_organized that we are on                                                             
    i = 0
    
    for upstream_u_time_group_hits in up_u_time_hits_center_organized:

        # Define the sum of the elements
        sum = 0
        
        # Define the average of the elements
        average = 0

        # Now, sum the elements and average them
        for element in upstream_u_time_group_hits: # because every element of upstream_u_time_group_hits is a list

            sum += element

        # Calculate the average
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5
        if ((float(sum)/float(len(upstream_u_time_group_hits)) - (sum/len(upstream_u_time_group_hits))) >= 0.5):
        
            average = sum/len(upstream_u_time_group_hits) + 1

        # Round down if the fractional part is less than 0.5
        else: 

            average = sum/len(upstream_u_time_group_hits)

        # Replace up_u_time_hits_center_organized with the integer form of the average of the "list within a list"'s average
        up_u_time_hits_center_organized[i] = average
        
        # Increment the iterator
        i += 1

        
    # Reset the iterator to 0
    i = 0
    
    for upstream_v_time_group_hits in up_v_time_hits_center_organized:

        # Define the sum of the elements                                                                                                                                         
        sum = 0

        # Define the average of the elements                                                                                                                                     
        average = 0

        # Now, sum the elements and average them                                                                                                                                  
        for element in upstream_v_time_group_hits: # because every element of upstream_u_time_group_hits is a list                                                               
            
            sum += element

        # Calculate the average                                                                                                                                                  
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5         
        if ((float(sum)/float(len(upstream_v_time_group_hits)) - (sum/len(upstream_v_time_group_hits))) >= 0.5):

            average = sum/len(upstream_v_time_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                      
        else:

            average = sum/len(upstream_v_time_group_hits)

        # Replace up_v_time_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                       
        up_v_time_hits_center_organized[i] = average

        # Increment the iterator                                                                                                                                                
        i += 1

    # Print out the vectors of the upstream time hits
    print "Up U Time Hits Organized: ", up_u_time_hits_center_organized
    print "Up V Time Hits Organized: ", up_v_time_hits_center_organized
    print "\n"

    # Now, average the elements of upstream_u_time_group_hits and upstream_v_time_group_hits into a new list: up_time_hits_center_organized
    up_time_hits_center_organized = []

    # Reset the iterator to 0
    i = 0

    while i < len(up_u_time_hits_center_organized):

        # Set the average of the entries from the vectors  equal to the average of the time pixels from the u and v planes
        average = (float(up_u_time_hits_center_organized[i]) + float(up_v_time_hits_center_organized[i]))/2.0

        # If the average is a decimal (with a '.5' at the end), then round up when the pixel number is converted back to an integer
        if math.fabs(average - int(average)) >= 0.5:

             average = int(average) + 1

        # Otherwise, you can just convert the average to type 'int' as usual
        else:

            average  = int(average)

         # Append the average onto the up_time_hits_center_organized vector
        up_time_hits_center_organized.append(average)

        # Increment the iterator (VERY IMPORTANT!!!)
        i += 1

    ### End of Section of Code for the Upstream Time Group Hits ###


    ### Start of Section of Code for the Upstream U and V Group Pixel Hits ###

    # Reset the iterator to 0                                                                                                                                                    
    i = 0

    # Repeat the same loop, this time for upstream_u_hits_center_grouped                                                                                                            
    for upstream_u_group_hits in up_u_hits_center_organized:

        # Define the sum of the elements of upstream_u_group_hits                                                                                                                   
        upstream_u_group_hits_sum = 0

        # Define the average of the hits in upstream_u_group_hits                                                                                                               
        upstream_u_group_hits_average = 0

        # Now, sum the elements and average them                                                                                                                                
        for element in upstream_u_group_hits: # because every element of upstream_u_group_hits is a list                                                                            

            upstream_u_group_hits_sum += element

        # Calculate the average                                                                                                                                                 
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5      
        if ((float(upstream_u_group_hits_sum)/float(len(upstream_u_group_hits)) - (upstream_u_group_hits_sum/len(upstream_u_group_hits))) >= 0.5):

            upstream_u_group_hits_average = upstream_u_group_hits_sum/len(upstream_u_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                   
        else:

            upstream_u_group_hits_average = upstream_u_group_hits_sum/len(upstream_u_group_hits)

        # Replace up_u_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                          
        up_u_hits_center_organized[i] = upstream_u_group_hits_average

        # Increment the iterator                                                                                                                                                
        i += 1

    # Reset the iterator to 0
    i = 0

    # Repeat the same loop, this time for upstream_v_hits_center_grouped                                                                                                            
    for upstream_v_group_hits in up_v_hits_center_organized:

        # Define the sum of the elements of upstream_v_group_hits                                                                                                                   
        upstream_v_group_hits_sum = 0

        # Define the average of the hits in upstream_v_group_hits                                                                                                                
        upstream_v_group_hits_average = 0

        # Now, sum the elements and average them                                                                                                                                
        for element in upstream_v_group_hits: # because every element of upstream_v_group_hits is a list                                                                            
            
            upstream_v_group_hits_sum += element

        # Calculate the average                                                                                                                                                   
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5        
        if ((float(upstream_v_group_hits_sum)/float(len(upstream_v_group_hits)) - (upstream_v_group_hits_sum/len(upstream_v_group_hits))) >= 0.5):

            upstream_v_group_hits_average = upstream_v_group_hits_sum/len(upstream_v_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                    
        else:

            upstream_v_group_hits_average = upstream_v_group_hits_sum/len(upstream_v_group_hits)

        # Replace up_v_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                            
        up_v_hits_center_organized[i] = upstream_v_group_hits_average

        # Increment the iterator                                                                                                                                                   
        i += 1

    ### End of the Section of Code for the Upstream U and V Pixel Hits ###


    ### Start of the Section of Code for the Downstream Time Pixel Hits ###

    # Define an iterator that will define the element of the list of down_u_time_hits_center_organized that we are on                                                               
    i = 0

    for downstream_u_time_group_hits in down_u_time_hits_center_organized:

        # Define the sum of the elements                                                                                                                                        
        sum = 0

        # Define the average of the elements                                                                                                                                 
        average = 0

        # Now, sum the elements and average them                                                                                                                               
        for element in downstream_u_time_group_hits: # because every element of downstream_u_time_group_hits is a list                                                          
            
            sum += element

        # Calculate the average                                                                                                                                                
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5       
        if ((float(sum)/float(len(downstream_u_time_group_hits)) - (sum/len(downstream_u_time_group_hits))) >= 0.5):

            average = sum/len(downstream_u_time_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                    
        else:

            average = sum/len(downstream_u_time_group_hits)

        # Replace down_u_time_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                   
        down_u_time_hits_center_organized[i] = average

        # Increment the iterator                                                                                                                                                 
        i += 1


    # Reset the iterator to 0                                                                                                                                                    
    i = 0

    for downstream_v_time_group_hits in down_v_time_hits_center_organized:

        # Define the sum of the elements                                                                                                                                   
        sum = 0

        # Define the average of the elements                                                                                                                            
        average = 0

        # Now, sum the elements and average them                                                                                                                            
        for element in downstream_v_time_group_hits: # because every element of downstream_u_time_group_hits is a list                                             
            
            sum += element

        # Calculate the average                                                                                                                                               
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5     
        if ((float(sum)/float(len(downstream_v_time_group_hits)) - (sum/len(downstream_v_time_group_hits))) >= 0.5):

            average = sum/len(downstream_v_time_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                
        else:

            average = sum/len(downstream_v_time_group_hits)

        # Replace down_v_time_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                   
        down_v_time_hits_center_organized[i] = average

        # Increment the iterator                                                                                                                                           
        i += 1

    # Now, average the elements of downstream_u_time_group_hits and downstream_v_time_group_hits into a new list: down_time_hits_center_organized
    down_time_hits_center_organized = []

    # Reset the iterator to 0                                                                                                                                               
    i = 0

    # Print out the downstream time hits
    print "Down U Time Hits Organized: ", down_u_time_hits_center_organized
    print "Down V Time Hits Organized: ", down_v_time_hits_center_organized
    print "\n"

    while i < len(down_u_time_hits_center_organized):

        # Set the average equal to the average of the time pixels from the u and v planes                                                                      
        average = (float(down_u_time_hits_center_organized[i]) + float(down_v_time_hits_center_organized[i]))/2.0

        # If the average is a decimal (with a '.5' at the end), then round up when the pixel number is converted back to an integer                                            
        if math.fabs(average - int(average)) >= 0.5:

            average = int(average) + 1

        # Otherwise, you can just convert the value of 'average' to type 'int' as usual                                                                        
        else:

            average = int(average)

        # Push back the average onto the new vector
        down_time_hits_center_organized.append(average)

        # Increment the iterator (VERY IMPORTANT!!!!)
        i += 1

    ### End of Section of Code for the Downstream Time Group Hits ###

 
    ### Start of the Section of Code for the Downstream U and V Pixel Hits ###

    # Reset the iterator to 0                                                                                                                                                     
    i = 0

    # Repeat the same loop, this time for downstream_u_hits_center_grouped                                                                                                     
    for downstream_u_group_hits in down_u_hits_center_organized:

        # Define the sum of the elements of downstream_u_group_hits                                                                                                            
        downstream_u_group_hits_sum = 0

        # Define the average of the hits in downstream_u_group_hits                                                                                                            
        downstream_u_group_hits_average = 0

        # Now, sum the elements and average them                                                                                                                                  
        for element in downstream_u_group_hits: # because every element of downstream_u_group_hits is a list                                                               
            
            downstream_u_group_hits_sum += element

        # Calculate the average                                                                                                                                                   
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5         
        if ((float(downstream_u_group_hits_sum)/float(len(downstream_u_group_hits)) - (downstream_u_group_hits_sum/len(downstream_u_group_hits))) >= 0.5):

            downstream_u_group_hits_average = downstream_u_group_hits_sum/len(downstream_u_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                      
        else:

            downstream_u_group_hits_average = downstream_u_group_hits_sum/len(downstream_u_group_hits)
                                                                                    
        # Replace down_u_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                       
        down_u_hits_center_organized[i] = downstream_u_group_hits_average

        # Increment the iterator                                                                                                                                                  
        i += 1

    # Reset the iterator to 0                                                                                                                                                       
    i = 0

    # Repeat the same loop, this time for downstream_v_hits_center_grouped                                                                                                       
    for downstream_v_group_hits in down_v_hits_center_organized:

        # Define the sum of the elements of downstream_v_group_hits                                                                                                             
        downstream_v_group_hits_sum = 0

        # Define the average of the hits in downstream_v_group_hits                                                                                                              
        downstream_v_group_hits_average = 0

        # Now, sum the elements and average them                                                                                                                                  
        for element in downstream_v_group_hits: # because every element of downstream_v_group_hits is a list                                                                    
            
            downstream_v_group_hits_sum += element

        # Calculate the average                                                                                                                                                  
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5        
        if ((float(downstream_v_group_hits_sum)/float(len(downstream_v_group_hits)) - (downstream_v_group_hits_sum/len(downstream_v_group_hits))) >= 0.5):

            downstream_v_group_hits_average = downstream_v_group_hits_sum/len(downstream_v_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                      
        else:

            downstream_v_group_hits_average = downstream_v_group_hits_sum/len(downstream_v_group_hits)

        # Replace down_v_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                         
        down_v_hits_center_organized[i] = downstream_v_group_hits_average

        # Increment the iterator                                                                                                                                                 
        i += 1

    ### End of the Section of Code for the Downstream Pixel U and V Hits ###


    ### Start of the Section of Code for the Top Time Pixel Hits ###

    # Define an iterator that will define the element of the list of top_u_time_hits_center_organized that we are on                                                               
    i = 0

    for top_u_time_group_hits in top_u_time_hits_center_organized:

        # Define the sum of the elements                                                                                                                                    
        sum = 0

        # Define the average of the elements                                                                                                                            
        average = 0

        # Now, sum the elements and average them                                                                                                                                
        for element in top_u_time_group_hits: # because every element of top_u_time_group_hits is a list                                                               

            sum += element

        # Calculate the average                                                                                                                                         
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5     
        if ((float(sum)/float(len(top_u_time_group_hits)) - (sum/len(top_u_time_group_hits))) >= 0.5):

            average = sum/len(top_u_time_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                         
        else:

            average = sum/len(top_u_time_group_hits)

        # Replace top_u_time_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                       
        top_u_time_hits_center_organized[i] = average

        # Increment the iterator                                                                                                                                             
        i += 1


    # Reset the iterator to 0                                                                                                                                                
    i = 0

    # Use the same loop but for the top hits on the v plane 
    for top_v_time_group_hits in top_v_time_hits_center_organized:

        # Define the sum of the elements                                                                                                                                    
        sum = 0

        # Define the average of the elements                                                                                                                          
        average = 0

        # Now, sum the elements and average them                                                                                                                                
        for element in top_v_time_group_hits: # because every element of top_u_time_group_hits is a list                                                               

            sum += element

        # Calculate the average                                                                                                                                                 
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5       
        if ((float(sum)/float(len(top_v_time_group_hits)) - (sum/len(top_v_time_group_hits))) >= 0.5):

            average = sum/len(top_v_time_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                 
        else:

            average = sum/len(top_v_time_group_hits)

        # Replace top_v_time_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                       
        top_v_time_hits_center_organized[i] = average

        # Increment the iterator                                                                                                                                           
        i += 1


    # Reset the iterator to 0
    i = 0

    # Use the same loop but for the top hits on the y plane
    for top_y_time_group_hits in top_y_time_hits_center_organized:

        # Define the sum of the elements                                                                                                                                   
        sum = 0

        # Define the average of the elements                                                                                                        
        average = 0

        # Now, sum the elements and average them                                                                                                                             
        for element in top_y_time_group_hits: # because every element of top_y_time_group_hits is a list

            sum += element 

        # Calculate the average                                                                                                                                               
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5      
        if ((float(sum)/float(len(top_y_time_group_hits))) - (sum/len(top_y_time_group_hits))) >= 0.5:
                
            average = sum/len(top_y_time_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                
        else: 

            average = sum/len(top_y_time_group_hits)

        # Replace top_y_time_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                       
        top_y_time_hits_center_organized[i] = average

        # Increment the iterator                                                                                                                                             
        i += 1

    # Print out the vectors of the top time hits                                                                                                                           
    print "Top U Time Hits Organized: ", top_u_time_hits_center_organized
    print "Top V Time Hits Organized: ", top_v_time_hits_center_organized
    print "Top Y Time Hits Organized: ", top_y_time_hits_center_organized
    print "\n"

    
    # Now, average the elements of top_u_time_group_hits, top_v_time_group_hits, and top_y_time_group_hits into a new list: top_time_hits_center_organized
    top_time_hits_center_organized = []

    # Reset the iterator to 0                                                                                                                                               
    i = 0

    while i < len(top_u_time_hits_center_organized):

        # Calculate the average of the time pixels from the u, v, and y planes
        average  = (float(top_u_time_hits_center_organized[i]) + float(top_v_time_hits_center_organized[i]) + float(top_y_time_hits_center_organized[i]))/3.0

        # If the average is a decimal (with a '.5' at the end), then round up when the pixel number is converted back to an integer                                              
        if math.fabs(average - int(average)) >= 0.5:

            average = int(average) + 1

        # Otherwise, you can just convert the average to type 'int' as usual                                                                             
        else:

            average = int(average)

        # Append the average onto the end of the top_time_hits_center_organized vector
        top_time_hits_center_organized.append(average)

        # Increment the iterator (VERY IMPORTANT!!!!)                                                                                                                       
        i += 1

    ### End of Section of Code for the Top Time Group Hits ###

    ### Start of the Section of Code for the Top U, V, and Y Pixels ###

    # Reset the iterator to 0                                                                                                                                                       
    i = 0

    # Repeat the same loop, this time for top_u_hits_center_grouped                                                                                                            
    for top_u_group_hits in top_u_hits_center_organized:

        # Define the sum of the elements of top_u_group_hits                                                                                                                      
        top_u_group_hits_sum = 0

        # Define the average of the hits in top_u_group_hits                                                                                                                  
        top_u_group_hits_average = 0

        # Now, sum the elements and average them                                                                                                                                  
        for element in top_u_group_hits: # because every element of top_u_group_hits is a list                                                                                 

            top_u_group_hits_sum += element

        # Calculate the average                                                                                                                                                  
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5        
        if ((float(top_u_group_hits_sum)/float(len(top_u_group_hits)) - (top_u_group_hits_sum/len(top_u_group_hits))) >= 0.5):

            top_u_group_hits_average = top_u_group_hits_sum/len(top_u_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                     
        else:

            top_u_group_hits_average = top_u_group_hits_sum/len(top_u_group_hits)

        # Replace top_u_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                        
        top_u_hits_center_organized[i] = top_u_group_hits_average

        # Increment the iterator                                                                                                                                                  
        i += 1

    # Reset the iterator to 0                                                                                                                                                       
    i = 0

    # Repeat the same loop, this time for top_v_hits_center_grouped                                                                                                               
    for top_v_group_hits in top_v_hits_center_organized:

        # Define the sum of the elements of top_v_group_hits                                                                                                                     
        top_v_group_hits_sum = 0

        # Define the average of the hits in top_v_group_hits                                                                                                                    
        top_v_group_hits_average = 0

        # Now, sum the elements and average them                                                                                                                                  
        for element in top_v_group_hits: # because every element of top_v_group_hits is a list                                                                                   
            
            top_v_group_hits_sum += element

        # Calculate the average                                                                                                                                                  
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5        
        if ((float(top_v_group_hits_sum)/float(len(top_v_group_hits)) - (top_v_group_hits_sum/len(top_v_group_hits))) >= 0.5):

            top_v_group_hits_average = top_v_group_hits_sum/len(top_v_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                     
        else: 

            top_v_group_hits_average = top_v_group_hits_sum/len(top_v_group_hits)

        # Replace top_v_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                         
        top_v_hits_center_organized[i] = top_v_group_hits_average

        # Increment the iterator                                                                                                                                                 
        i += 1

    # Reset the iterator to 0                                                                                                                                                       
    i = 0

    # Repeat the same loop, this time for top_y_hits_center_grouped                                                                                                               
    for top_y_group_hits in top_y_hits_center_organized:

        # Define the sum of the elements of top_y_group_hits                                                                                                                    
        top_y_group_hits_sum = 0

        # Define the average of the hits in top_y_group_hits                                                                                                                     
        top_y_group_hits_average = 0

        # Now, sum the elements and average them                                                                                                                                     
        for element in top_y_group_hits: # because every element of top_y_group_hits is a list                                                                                   
            
            top_y_group_hits_sum += element

        # Calculate the average                                                                                                                                                  
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5         
        if ((float(top_y_group_hits_sum)/float(len(top_y_group_hits)) - (top_y_group_hits_sum/len(top_y_group_hits))) >= 0.5):

            top_y_group_hits_average = top_y_group_hits_sum/len(top_y_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                       
        else:

            top_y_group_hits_average = top_y_group_hits_sum/len(top_y_group_hits)

        # Replace top_y_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                         
        top_y_hits_center_organized[i] = top_y_group_hits_average

        # Increment the iterator                                                                                                                                                  
        i += 1

    ### End of the Section of Code for the Top U, V, and Y Pixels ###

    
    ### Start of the Section of Code for the Bottom Time Pixels ###

    # Define an iterator that will define the element of the list of bottom_u_time_hits_center_organized that we are on                                                       
    i = 0

    for bottom_u_time_group_hits in bottom_u_time_hits_center_organized:

        # Define the sum of the elements                                                                                                                                     
        sum = 0

        # Define the average of the elements                                                                                                                           
        average = 0

        # Now, sum the elements and average them                                                                                                                            
        for element in bottom_u_time_group_hits: # because every element of bottom_u_time_group_hits is a list                                                       
            
            sum += element

        # Calculate the average                                                                                                                                             
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5       
        if ((float(sum)/float(len(bottom_u_time_group_hits)) - (sum/len(bottom_u_time_group_hits))) >= 0.5):

            average = sum/len(bottom_u_time_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                 
        else:

            average = sum/len(bottom_u_time_group_hits)

        # Replace top_u_time_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                       
        bottom_u_time_hits_center_organized[i] = average

        # Increment the iterator                                                                                                                                             
        i += 1

    # Reset the iterator to 0                                                                                                                                               
    i = 0

    # Use the same loop but for the bottom hits on the v plane                                                                                                                    
    for bottom_v_time_group_hits in bottom_v_time_hits_center_organized:

        # Define the sum of the elements                                                                                                                                     
        sum = 0

        # Define the average of the elements                                                                                                                            
        average = 0

        # Now, sum the elements and average them                                                                                                                                
        for element in bottom_v_time_group_hits: # because every element of bottom_u_time_group_hits is a list   

            sum += element

        # Calculate the average                                                                                                                                              
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5      
        if ((float(sum)/float(len(bottom_v_time_group_hits)) - (sum/len(bottom_v_time_group_hits))) >= 0.5):

            average = sum/len(bottom_v_time_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                 
        else:

            average = sum/len(bottom_v_time_group_hits)

        # Replace bottom_v_time_hits_center_organized with the integer form of the average of the "list within a list"'s average                                             
        bottom_v_time_hits_center_organized[i] = average

        # Increment the iterator                                                                                                                                         
        i += 1

    # Reset the iterator to 0                                                                                                                                               
    i = 0

    # Use the same loop but for the bottom hits on the y plane                                                                                                                   
    for bottom_y_time_group_hits in bottom_y_time_hits_center_organized:

        # Define the sum of the elements                                                                                                                               
        sum = 0

        # Define the average of the elements                                                                                                                       
        average = 0

        # Now, sum the elements and average them                                                                                                                              
        for element in bottom_y_time_group_hits: # because every element of bottom_y_time_group_hits is a list                                                      
            
            sum += element

        # Calculate the average                                                                                                                                                 
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5      
        if ((float(sum)/float(len(bottom_y_time_group_hits))) - (sum/len(bottom_y_time_group_hits))) >= 0.5:

            average = sum/len(bottom_y_time_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                
        else:

            average = sum/len(bottom_y_time_group_hits)

        # Replace bottom_y_time_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                
        bottom_y_time_hits_center_organized[i] = average

        # Increment the iterator                                                                                                                                           
        i += 1

    # Print out the vectors of the bottom time hits                                                                                                                                
    print "Bottom U Time Hits Organized: ", bottom_u_time_hits_center_organized
    print "Bottom V Time Hits Organized: ", bottom_v_time_hits_center_organized
    print "Bottom Y Time Hits Organized: ", bottom_y_time_hits_center_organized
    print "\n"

    # Now, average the elements of bottom_u_time_group_hits, bottom_v_time_group_hits, and bottom_y_time_group_hits into a new list: bottom_time_hits_center_organized    
    bottom_time_hits_center_organized = []

    # Reset the iterator to 0                                                                                                                                             
    i = 0

    while i < len(bottom_u_time_hits_center_organized):

        # Compute the average of the time pixels from the u, v, and y planes                                                                   
        average = (float(bottom_u_time_hits_center_organized[i]) + float(bottom_v_time_hits_center_organized[i]) + float(bottom_y_time_hits_center_organized[i]))/3.0

        # If the average is a decimal (with a '.5' at the end), then round up when the pixel number is converted back to an integer                                            
        if math.fabs(average  - int(average)) >= 0.5:

            average = int(average) + 1

        # Otherwise, you can just convert the entry of bottom_time_group_hits to type 'int' as usual                                                                         
        else:

            average = int(average)

        # Append the average onto the end of bottom_time_hits_center_organized vector above
        bottom_time_hits_center_organized.append(average)

        # Increment the iterator (VERY IMPORTANT!!!!)                                                                                                                      
        i += 1

    ### End of Section of Code for the Bottom Time Group Hits ### 


    ### Start of Section of Code for Bottom U, V, and Y Pixels ###

    # Reset the iterator to 0                                                                                                                                                       
    i = 0

    # Repeat the same loop, this time for bottom_u_hits_center_grouped                                                                                                            
    for bottom_u_group_hits in bottom_u_hits_center_organized:

        # Define the sum of the elements of bottom_u_group_hits                                                                                                                   
        bottom_u_group_hits_sum = 0

        # Define the average of the hits in bottom_u_group_hits
        bottom_u_group_hits_average = 0

        # Now, sum the elements and average them                                                                                                                                
        for element in bottom_u_group_hits: # because every element of bottom_u_group_hits is a list                                                                           

            bottom_u_group_hits_sum += element

        # Calculate the average                                                                                                                                                  
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5       
        if ((float(bottom_u_group_hits_sum)/float(len(bottom_u_group_hits)) - (bottom_u_group_hits_sum/len(bottom_u_group_hits))) >= 0.5):

            bottom_u_group_hits_average = bottom_u_group_hits_sum/len(bottom_u_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                      
        else:

            bottom_u_group_hits_average = bottom_u_group_hits_sum/len(bottom_u_group_hits)

        # Replace bottom_u_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                    
        bottom_u_hits_center_organized[i] = bottom_u_group_hits_average

        # Increment the iterator 
        i += 1

    # Reset the iterator to 0
    i = 0

    # Repeat the same loop, this time for bottom_v_hits_center_grouped                                                                                                          
    for bottom_v_group_hits in bottom_v_hits_center_organized:

        # Define the sum of the elements of bottom_v_group_hits                                                                                                                  
        bottom_v_group_hits_sum = 0

        # Define the average of the hits in bottom_v_group_hits                                                                                                                  
        bottom_v_group_hits_average = 0

        # Now, sum the elements and average them                                                                                                                                 
        for element in bottom_v_group_hits: # because every element of bottom_v_group_hits is a list                                                                               
            
            bottom_v_group_hits_sum += element

        # Calculate the average                                                                                                                                                   
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5       
        if ((float(bottom_v_group_hits_sum)/float(len(bottom_v_group_hits)) - (bottom_v_group_hits_sum/len(bottom_v_group_hits))) >= 0.5):

            bottom_v_group_hits_average = bottom_v_group_hits_sum/len(bottom_v_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                      
        else:

            bottom_v_group_hits_average = bottom_v_group_hits_sum/len(bottom_v_group_hits)
       
        # Replace bottom_v_hits_center_organized with the integer form of the average of the "list within a list"'s average                         
        bottom_v_hits_center_organized[i] = bottom_v_group_hits_average

        # Increment the iterator                                                                                                                                                
        i += 1

    # Set the iterator equal to 0
    i = 0

    # Repeat the same loop, this time for bottom_y_hits_center_grouped                                                                                                           
    for bottom_y_group_hits in bottom_y_hits_center_organized:

        # Define the sum of the elements of bottom_y_group_hits                                                                                                                  
        bottom_y_group_hits_sum = 0

        # Define the average of the hits in bottom_y_group_hits                                                                                                                 
        bottom_y_group_hits_average = 0

        # Now, sum the elements and average them                                                                                                                                 
        for element in bottom_y_group_hits: # because every element of bottom_y_group_hits is a list                                                                             
            
            bottom_y_group_hits_sum += element

        # Calculate the average                                                                                                                                                   
        # Account for the nature of the python 'int' conversion function by rounding up the result to the next greatest integer if the fractional part is greater than 0.5       
        if ((float(bottom_y_group_hits_sum)/float(len(bottom_y_group_hits)) - (bottom_y_group_hits_sum/len(bottom_y_group_hits))) >= 0.5):

            bottom_y_group_hits_average = bottom_y_group_hits_sum/len(bottom_y_group_hits) + 1

        # Round down if the fractional part is less than 0.5                                                                                                                     
        else:

            bottom_y_group_hits_average = bottom_y_group_hits_sum/len(bottom_y_group_hits)

        # Replace bottom_y_hits_center_organized with the integer form of the average of the "list within a list"'s average                                                      
        bottom_y_hits_center_organized[i] = bottom_y_group_hits_average

        # Increment the iterator                                                                                                                                                  
        i += 1

    ### End of the Section of Code for the Bottom U, V, and Y Pixels ###
        
    print "Upstream Time Hits Averaged: ", up_time_hits_center_organized
    print "Upstream U Hits Averaged: ", up_u_hits_center_organized
    print "Upstream V Hits Averaged: ", up_v_hits_center_organized
    print "\n"

    print "Downstream Time Hits Averaged: ", down_time_hits_center_organized
    print "Downstream U Hits Averaged: ", down_u_hits_center_organized
    print "Downstream V Hits Averaged: ", down_v_hits_center_organized
    print "\n"

    print "Top Time Hits Averaged: ", top_time_hits_center_organized
    print "Top U Hits Averaged: ", top_u_hits_center_organized
    print "Top V Hits Averaged: ", top_v_hits_center_organized
    print "Top Y Hits Averaged: ", top_y_hits_center_organized
    print "\n"

    print "Bottom Time Hits Averaged: ", bottom_time_hits_center_organized
    print "Bottom U Hits Averaged: ", bottom_u_hits_center_organized
    print "Bottom V Hits Averaged: ", bottom_v_hits_center_organized
    print "Bottom Y Hits Averaged: ", bottom_y_hits_center_organized
    print "\n"

    return [up_time_hits_center_organized, up_u_hits_center_organized, up_v_hits_center_organized, down_time_hits_center_organized, down_u_hits_center_organized, down_v_hits_center_organized, top_time_hits_center_organized, top_u_hits_center_organized, top_v_hits_center_organized, top_y_hits_center_organized, bottom_time_hits_center_organized, bottom_u_hits_center_organized, bottom_v_hits_center_organized, bottom_y_hits_center_organized]
    

    
        
  
    

    
        
        


  




                


    
    

    
    
    

    
    

    

    

    
