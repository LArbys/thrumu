import math
import numpy as np

def wire_matching_algo(plane1toplane2_tolerance, plane1toplane3_tolerance, plane2toplane3_tolerance):

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

# Match the wires on the first plane with the wires from the second and third planes using a dictionary, which is declared here

    wire_match_dict = {}

# Declare variables for the second plane wire and the first plane wire
    second_plane_wire = 0
    third_plane_wire = 0

# Begin the activity for frontend hits

    for i in range (0, 2400):

        for j in range (2400, 4800):

            # Set the second plane wire equal to -1 the third plane wire equal to -1 and see if the values are reset at the end of the loop
            # -1 will be a default value if there is no match on the second plane, the third plane, or both
            second_plane_wire = -1
            third_plane_wire = -1

            if math.fabs(y_start_list[i] - y_start_list[j]) <= plane1toplane2_tolerance and math.fabs(z_start_list[i] - z_start_list[j]) <= plane1toplane2_tolerance: 

                second_plane_wire = j - 2400
 
                # Clear out the lists of the two hits on the third plane 

                third_plane_hit_list = []

                for k in range(4800, 8256):

                    if math.fabs(y_start_list[k] - y_start_list[i]) <= plane1toplane3_tolerance and math.fabs(y_start_list[k] - y_start_list[j]) <= plane2toplane3_tolerance and math.fabs(z_start_list[k] - z_start_list[i]) <= plane1toplane3_tolerance and math.fabs(z_start_list[k] - z_start_list[j]) <= plane2toplane3_tolerance:

                        third_plane_hit_list.append(k)

                        if len(third_plane_hit_list) == 2:
                                 
                            if math.fabs(y_start_list[third_plane_hit_list[0]] - y_start_list[i]) <= math.fabs(y_start_list[third_plane_hit_list[1]] - y_start_list[i]) and math.fabs(y_start_list[third_plane_hit_list[0]] - y_start_list[j]) <= math.fabs(y_start_list[third_plane_hit_list[1]] - y_start_list[j]) and math.fabs(z_start_list[third_plane_hit_list[0]] - z_start_list[i]) <= math.fabs(z_start_list[third_plane_hit_list[1]] - z_start_list[i]) and math.fabs(z_start_list[third_plane_hit_list[0]] - z_start_list[j]) <= math.fabs(z_start_list[third_plane_hit_list[1]] - z_start_list[j]):

                                third_plane_wire = third_plane_hit_list[0] - 4800
                                
                            else:

                                third_plane_wire = third_plane_hit_list[1] - 4800

            # Go on to the next 'j' if there is no match on either of the two planes
            if second_plane_wire == -1 and third_plane_wire == -1:

                continue
            
            else: 
                
                wire_match_dict[i] = (second_plane_wire, third_plane_wire)
                
# Begin the loop for backend hits

    for i in range(0, 2400):

        for j in range(2400, 4800):

          # Set the second plane wire equal to -1 the third plane wire equal to -1 and see if the values are reset at the end of the loop                                          
          # -1 will be a default value if there is no match on the second plane, the third plane, or both  
          second_plane_wire = -1
          third_plane_wire  = -1
    
          if math.fabs(y_end_list[i] - y_end_list[j]) <= plane1toplane2_tolerance and math.fabs(z_end_list[i] - z_end_list[j]) <= plane1toplane2_tolerance:

              second_plane_wire = j - 2400

              # Initialize a list to hold all of the hits on the third wire plane of the detector
              third_plane_hit_list = []

              for k in range(4800, 8256):

                  if math.fabs(y_end_list[k] - y_end_list[i]) <= plane1toplane3_tolerance and math.fabs(y_end_list[k] - y_end_list[j]) <= plane2toplane3_tolerance and math.fabs(z_end_list[k] - z_end_list[i]) <= plane1toplane3_tolerance and math.fabs(z_end_list[k] - z_end_list[j]) <= plane2toplane3_tolerance:

                      third_plane_hit_list.append(k)

                      # Include a condition for when there are two hits on the third plane recorded to compare the two and identify one as the third hit of the three

                      if len(third_plane_hit_list) == 2:

                          if math.fabs(y_end_list[third_plane_hit_list[0]] - y_end_list[i]) <= math.fabs(y_end_list[third_plane_hit_list[1]] - y_end_list[i]) and math.fabs(y_end_list[third_plane_hit_list[0]] - y_end_list[j]) <= math.fabs(y_end_list[third_plane_hit_list[1]] - y_end_list[j]) and math.fabs(z_end_list[third_plane_hit_list[0]] - z_end_list[i]) <= math.fabs(z_end_list[third_plane_hit_list[1]] - z_end_list[i]) and math.fabs(z_end_list[third_plane_hit_list[0]] - z_end_list[j]) <= math.fabs(z_end_list[third_plane_hit_list[1]] - z_end_list[j]):

                              third_plane_wire = third_plane_hit_list[0] - 4800

                          else:

                              third_plane_wire = third_plane_hit_list[1] - 4800

        # Go on to the next 'j' if there is no match on either of the two planes                                                                                                
        if second_plane_wire == -1 and third_plane_wire == -1:

            continue

        # Fill wire_match_dict[i] with (second_plane_wire, third_plane_wire) if there was a match on at least the second plane                                                  
        # third_plane_wire = -1 will be a default value meaning that there was no match on the third plane                                                                   
        else:

            wire_match_dict[i] = (second_plane_wire, third_plane_wire)


    # Return the dictionary for the matching wires
    return wire_match_dict



# Define a list that can contain the results of the previous function
wire_match_list = wire_matching_algo(0.30, 0.30, 0.30)


# Define another function to find the matching wires upon being given first_wire, the wire in zero_plane
def wire_assign_func(zero_wire):
    
    # Initialize variables for the matching wires on the first (second) and second (third) planes
    first_wire = 0
    second_wire = 0

    # Assign variables to the three lists that are given by wire_matching_algo
    (first_wire, second_wire) = wire_match_list[zero_wire]

    return (first_wire, second_wire)

# print wire_match_list
