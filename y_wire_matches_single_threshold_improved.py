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

    # Declare a numpy array for the plane 1 and plane 2 upstream matches
    upstream_matches_dict = {}
    upstream_matches_iterator = 0

# Begin the loop for upstream wire matches 
    for i in range (0, 2400):

        for j in range (2400, 4800):
            
            if math.fabs(y_start_list[i] - y_end_list[j]) <= tolerance and z_start_list[i] < 0.036 and z_end_list[j] < 0.036:

                 upstream_matches_dict[upstream_matches_iterator] = [i, j-2400]
                 upstream_matches_iterator += 1
         
    # Declare a numpy array for the plane 1 and plnae 2 downstream matches
    downstream_matches_dict = {}
    downstream_matches_iterator = 0

# Begin the loop for downstream wire matches 
    for i in range(0, 2400):

        for j in range(2400, 4800):

            if math.fabs(y_end_list[i] - y_start_list[j]) <= tolerance and z_end_list[i] > 1036.9 and z_start_list[j] > 1036.9:

                downstream_matches_dict[downstream_matches_iterator] = [i, j-2400]
                downstream_matches_iterator += 1
      
    return upstream_matches_dict, downstream_matches_dict

# print wire_matching_algo(0.271)
