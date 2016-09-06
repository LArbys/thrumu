import math
import numpy as np

def wire_matching_algo(tolerance):

    fin = open("output_with_y.txt")
    lines = fin.readlines()

    str_data_list  = []
    instance_list  = []
    plane_num_list = []
    wire_num_list  = []
    y_start_list   = []
    y_end_list     = []
    z_start_list   = []
    z_end_list     = []

    # Initialize a vector to contain the instance of the two plane "2" (3) hits and to find which
    # one is closer to the hits on the first two planes
    third_plane_hit_list = []

    for l in lines:

        str_data  = l.split(' ') # splits by space
        instance  = int(str_data[0])
        plane_num = int(str_data[1])
        wire_num  = int(str_data[2])
        y_start   = float(str_data[3])
        y_end     = float(str_data[4])
        z_start   = float(str_data[5])
        z_end     = float(str_data[6])

        instance_list.append(instance)
        plane_num_list.append(plane_num)
        wire_num_list.append(wire_num)
        y_start_list.append(y_start)
        y_end_list.append(y_end)
        z_start_list.append(z_start)
        z_end_list.append(z_end)

    # Declare an array for the plane 1 and plane 2 matches at the bottom of the TPC
    bottom_matches_planes1and2  = []
    bottom_matches = np.zeros([2400,2400,2], int)

# Begin the loop for wire matches on the first two planes on the bottom of the TPC 
    for i in range (0, 2400):
        
        for j in range (2400, 4800):
            
            if math.fabs(z_start_list[i] - z_start_list[j]) <= tolerance and y_start_list[i] < -115 and y_start_list[j] < -115:

                 bottom_matches_planes1and2.append((i, j-2400))
                 
# Now, loop through each tuple and find the third plane wires that correspond to each of the matches on the first two planes
    for first_iterator in bottom_matches_planes1and2:

        # Loop through each of the wires on the third plane to see if they're a match
        
        bottom_match_iterator = 0

        for plane_three_iterator in range(4800, 8256):

            if math.fabs(z_start_list[plane_three_iterator] - z_start_list[first_iterator[0]]) <= tolerance and math.fabs(z_start_list[plane_three_iterator] - z_start_list[first_iterator[1] + 2400]) <= tolerance and y_start_list[plane_three_iterator] < -115: # The last 'if' statement is just to ensure that the wire is on the bottom of the TPC

                bottom_matches[first_iterator[0]][first_iterator[1]][bottom_match_iterator] = plane_three_iterator - 4800
                
                # Increment the bottom_match_iterator (^^I can use a numpy array above because I am only expecting two matching wires on the third plane)
                bottom_match_iterator += 1

         
# Begin the loop for wire matches on the first_two_planes on the top of the TPC
    
    top_matches_planes1and2 = []
    top_matches = np.zeros([2400,2400,2], int)

    for i in range(0, 2400):

        for j in range(2400, 4800):

            if math.fabs(z_end_list[i] - z_end_list[j]) <= tolerance and y_end_list[i] > 117 and y_end_list[j] > 117:

                top_matches_planes1and2.append((i, j-2400))

    # Now, loop through each tuple and find the third plane wires that correspond to each of the matches on the first two planes

    for first_iterator in top_matches_planes1and2:

        # Loop through each of the wires on the third plane to see if they're a match

        top_match_iterator = 0

        for plane_three_iterator in range(4800,8256):

                if math.fabs(z_end_list[plane_three_iterator] - z_end_list[first_iterator[0]]) <= tolerance and math.fabs(z_end_list[plane_three_iterator] - z_end_list[first_iterator[1] + 2400]) <= tolerance and y_end_list[plane_three_iterator] > 117:

                    top_matches[first_iterator[0]][first_iterator[1]][top_match_iterator] = plane_three_iterator - 4800

                    top_match_iterator += 1
            
  
    # Now, arrange both the top_matches and the bottom_matches into a dictionary

    top_matches_dict = {}
    bottom_matches_dict = {}
  
    # Define iterators for the index of the dictionary that we've created
    # Using tolerance 0.3, all of the plane one and plane two wires have two matches on plane three

    top_match_dict_iter = 0
    bottom_match_dict_iter = 0
  
    for i in range(0,2400):

        for j in range(0,2400):

            # This is if there's a single entry corresponding to the third_plane_wire                                                                                            
            if top_matches[i][j][0] > 0 and top_matches[i][j][1] > 0:
                
                top_matches_dict[top_match_dict_iter] = [i, j, top_matches[i][j][0], top_matches[i][j][1]] 

                top_match_dict_iter += 1
        
            if bottom_matches[i][j][0] > 0 and bottom_matches[i][j][1] > 0:

                bottom_matches_dict[bottom_match_dict_iter] = [i, j, bottom_matches[i][j][0], bottom_matches[i][j][1]]
                
                bottom_match_dict_iter += 1
    
    # print "The list of top matches is: ", top_matches_dict, "\n"
    # print "The list of bottom matches is: ", bottom_matches_dict, "\n"

    return top_matches_dict, bottom_matches_dict
