import barnes_pixel_clustering

# Define a function that will organize the upstream, downstream, top, and bottom hits into a list of lists, with each inner-list consisting of the time, u hit, the v hit, and the y hit for the top and bottom hits
def barnes_pixel_organization_func(upstream_pixel_dict, downstream_pixel_dict, top_pixel_dict, bottom_pixel_dict):

    # Inherit all of the types of hits from the pixel_average_calculator function in barnes_pixel_clustering.  Use these to make the list of list
    [upstream_time_hits_avgd, upstream_u_hits_avgd, upstream_v_hits_avgd, downstream_time_hits_avgd, downstream_u_hits_avgd, downstream_v_hits_avgd, top_time_hits_avgd, top_u_hits_avgd, top_v_hits_avgd, top_y_hits_avgd, bottom_time_hits_avgd, bottom_u_hits_avgd, bottom_v_hits_avgd, bottom_y_hits_avgd] = barnes_pixel_clustering.pixel_average_calculator(upstream_pixel_dict, downstream_pixel_dict, top_pixel_dict, bottom_pixel_dict)
    
    # Declare Lists for each type of hits in order to fill them                                                                                                                
    upstream_list_hits      = []
    downstream_list_hits    = []
    top_list_hits           = []
    bottom_list_hits        = []

    # Declare an iterator                                                                                                                                                       
    j = 0

    # Use a loop over the indices of the upstream_hits_avgd to group the pixels together into a new list of hits                                                                    
    while j < len(upstream_time_hits_avgd):

        upstream_list_hits.append([])
        upstream_list_hits[j] = [upstream_time_hits_avgd[j], upstream_u_hits_avgd[j], upstream_v_hits_avgd[j]]

        # Increment the iterator                                                                                                                                          
        j += 1

    # Reset the iterator to 0                                                                                                                                                
    j = 0

    # Use a loop over the indices of the downstream_hits_avgd to group the pixels together into a new list of hits
    while j < len(downstream_time_hits_avgd):

        downstream_list_hits.append([])
        downstream_list_hits[j] = [downstream_time_hits_avgd[j], downstream_u_hits_avgd[j], downstream_v_hits_avgd[j]]

        # Increment the iterator                                                                                                                                         
        j += 1

    # Reset the iterator to 0                                                                                                                                              
    j = 0

    # Use a loop over the indices of the top_hits_avgd to group the pixels together into a new list of hits
    while j < len(top_time_hits_avgd):

        top_list_hits.append([])
        top_list_hits[j] = [top_time_hits_avgd[j], top_u_hits_avgd[j], top_v_hits_avgd[j], top_y_hits_avgd[j]]

        # Increment the iterator                                                                                                                                           
        j += 1

    # Reset the iterator to 0                                                                                                                                               
    j = 0

    # Use a loop over the indices of the bottom_hits_avgd to group the pixels together into a new list of hits
    while j < len(bottom_time_hits_avgd):

        bottom_list_hits.append([])
        bottom_list_hits[j] = [bottom_time_hits_avgd[j], bottom_u_hits_avgd[j], bottom_v_hits_avgd[j], bottom_y_hits_avgd[j]]

        # Increment the iterator                                                                                                                                           
        j += 1

    
    # Return the organized list of hits
    return [upstream_list_hits, downstream_list_hits, top_list_hits, bottom_list_hits]
    
