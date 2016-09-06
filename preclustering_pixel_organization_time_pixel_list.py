# Define a function that will organize the plane hits from their dictionary form (i.e. [time, u_hit, v_hit] for upstream and downstream and [time, u_hit, v_hit, y_hit] for top and bottom) and place them into a list of lists of length two (structure [time, plane_hit])
# This is the same as the previous function except it takes a list of len() = 2, because it includes both the pixel number and the associated time with that pixel hit

# The first argument will be the dictionary of hits with time as the first entry and the plane hits as the following entries
# The second argument is the number of entries in the hit dictionary list, which will be either 3 (for upstream and downstream hits) or 4 (for top and bottom hits)

# This function gives the output for every combination of time pixel and plane pixel, which must be unpacked upon use
def plane_hit_organization_algo(hit_dictionary, num_entry):

    # Use four loops for the case of an empty dictionary of upstream and downstream hits, an empty dictionary of top and bottom hits, a dictionary of lists of only three entries (the upstream and downstream hit lists), and a dictionary of lists of four entries (the top and bottom lists)

    ## These are meant to keep the function from crashing if the hit dictionary has no entry at index 0 (meaning that it is empty)

    # The first 'if' statement will handle the case of an empty dictionary of upstream and downstream hits
    if hit_dictionary == {} and num_entry == 3:

        # I'll just return two empty lists representing the u and v hits
        return [[], []]

    
    # The second 'if' statement will handle the case of an empty dictionary of top and bottom hits
    if hit_dictionary == {} and num_entry == 4:

        # I'll just return three empty lists representing the u, v, and y hits
        return [[], [], []]


    ## These next two loops handle dictionaries that have components, meaning lists of upstream and downstream hits (three entries) and lists of top and bottom hits (four entries)

    # This first statement is to remove any chance that the program will crash
    if len(hit_dictionary) != 0:

        # 'if' statement for the upstream and downstream hits
        if len(hit_dictionary[0]) == 3:

            # Initialize lists for the u hits and the v hits
            time_u_hits = []
            time_v_hits = []

            # Loop through the dictionary to fill these lists
            for entry in hit_dictionary:

                # Fill the u and v hits with the time and the appropriate plane hit in the dictionary
                time_u_hits.append([hit_dictionary[entry][0], hit_dictionary[entry][1]])
                time_v_hits.append([hit_dictionary[entry][0], hit_dictionary[entry][2]])

            # Once these lists have been filled, you can return them
            return [time_u_hits, time_v_hits]

        
        # 'if' statement for the top and bottom hits                                                                                                                   
        if len(hit_dictionary[0]) == 4:

            # Initialize lists for the u hits, the v hits, and the y hits                                                                          
            time_u_hits = []
            time_v_hits = []
            time_y_hits = [] 

            # Loop through the dictionary to fill these lists                                                                        
            for entry in hit_dictionary:

                # Fill the u and v hits with the time and the appropriate plane hit in the dictionary                                                                
                time_u_hits.append([hit_dictionary[entry][0], hit_dictionary[entry][1]])
                time_v_hits.append([hit_dictionary[entry][0], hit_dictionary[entry][2]])
                time_y_hits.append([hit_dictionary[entry][0], hit_dictionary[entry][3]])

            # Once these lists have been filled, you can return them                                                                                                            
            return [time_u_hits, time_v_hits, time_y_hits]

        

    
        
        

    
