import math

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

# Initialize a vector to contain the instance of the two plane "2" (3)  hits and to find which
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

    
for i in range(0, 2400):
    
    for j in range(2400, 4800):

        if math.fabs(y_start_list[i] - y_start_list[j]) <= 0.295:
             
            if math.fabs(z_start_list[i] - z_start_list[j]) <= 0.295: 
                  
                     print "Front End Double Match!"
                     print "First Instance:", i, "Second Instance:", j
                     print "Wire Number:", wire_num_list[i], "Plane:", plane_num_list[i]
                     print "Wire Number:", wire_num_list[j], "Plane:", plane_num_list[j]
                     print "y Starting Position of First Instance:", y_start_list[i]
                     print "y Starting Position of Second Instance:", y_start_list[j]
                     print "z Starting Position of First Instance:", z_start_list[i]
                     print "z Starting Position of Second Instance:", z_start_list[j]
                     print "\n"

                     # Clear out the lists of the two hits on the third plane 

                     third_plane_hit_list = []

                     for k in range(4800, 8256):

                         if math.fabs(y_start_list[k] - y_start_list[i]) <= 0.295 and math.fabs(y_start_list[k] - y_start_list[j]) <= 0.295 and math.fabs(z_start_list[k] - z_start_list[i]) <= 0.295 and math.fabs(z_start_list[k] - z_start_list[j]) <= 0.295:
                                    
                             third_plane_hit_list.append(k)

                             # Include a condition for when there are two hits on the third plane recorded to compare the two

                             if len(third_plane_hit_list) > 2: print ("There are more than two corresponding hits on the third plane!")
                             if len(third_plane_hit_list) == 2:
                                 
                                 if math.fabs(y_start_list[third_plane_hit_list[0]] - y_start_list[i]) <= math.fabs(y_start_list[third_plane_hit_list[1]] - y_start_list[i]) and math.fabs(y_start_list[third_plane_hit_list[0]] - y_start_list[j]) <= math.fabs(y_start_list[third_plane_hit_list[1]] - y_start_list[j]) and math.fabs(z_start_list[third_plane_hit_list[0]] - z_start_list[i]) <= math.fabs(z_start_list[third_plane_hit_list[1]] - z_start_list[i]) and math.fabs(z_start_list[third_plane_hit_list[0]] - z_start_list[i]) <= math.fabs(z_start_list[third_plane_hit_list[1]] - z_start_list[i]):

                                     print "Hit 0 Wins!"       
                                     print "Third Instance:", third_plane_hit_list[0], "Plane:", plane_num_list[third_plane_hit_list[0]]
                                     print "Wire Number:", wire_num_list[third_plane_hit_list[0]]
                                     print "y Starting Position of Third Instance:", y_start_list[third_plane_hit_list[0]]
                                     print "z Starting Position of Third Instance:", z_start_list[third_plane_hit_list[0]]
                                     print "\n"


                                 else:
                                     
                                     print "Hit 1 Wins!"
                                     print "Third Instance:", third_plane_hit_list[1], "Plane:", plane_num_list[third_plane_hit_list[1]]
                                     print "Wire Number:", wire_num_list[third_plane_hit_list[1]]
                                     print "y Starting Position of Third Instance:", y_start_list[third_plane_hit_list[1]]
                                     print "z Starting Position of Third Instance:", z_start_list[third_plane_hit_list[1]]
                                     print "\n\n"


# Start the loop for the back end hits

# (I'm just going to repeat the loops from the front end case to separate the front end and back end in the output)
for i in range(0, 2400):

    for j in range(2400, 4800):

        if math.fabs(y_end_list[i] - y_end_list[j]) <= 0.295:

            if math.fabs(z_end_list[i] - z_end_list[j]) <= 0.295:

                print "Back End Double Match!"
                print "First Instance:", i, "Second Instance:", j
                print "Wire Number:", wire_num_list[i], "Plane:", plane_num_list[i]
                print "Wire Number:", wire_num_list[j], "Plane:", plane_num_list[j]
                print "y Ending Position of First Instance:", y_end_list[i]
                print "y Ending Position of Second Instance:", y_end_list[j]
                print "z Ending Position of First Instance:", z_end_list[i]
                print "z Ending Position of Second Instance:", z_end_list[j]
                print "\n"

                # Open up the third plane hit list again

                third_plane_hit_list = []

                for k in range(4800, 8256):

                    if math.fabs(y_end_list[k] - y_end_list[i]) <= 0.295 and math.fabs(y_end_list[k] - y_end_list[j]) <= 0.295 and math.fabs(z_end_list[k] - z_end_list[i]) <= 0.295 and math.fabs(z_end_list[k] - z_end_list[j]) <= 0.295:

                        third_plane_hit_list.append(k)

                        # Include a condition for when there are two hits on the third plane recorded to compare the two                                                        
                        if len(third_plane_hit_list) > 2: print ("There are more than two corresponding hits on the third plane!")
                        if len(third_plane_hit_list) == 2:

                                 if math.fabs(y_end_list[third_plane_hit_list[0]] - y_end_list[i]) <= math.fabs(y_end_list[third_plane_hit_list[1]] - y_end_list[i]) and math.fabs(y_end_list[third_plane_hit_list[0]] - y_end_list[j]) <= math.fabs(y_end_list[third_plane_hit_list[1]] - y_end_list[j]) and math.fabs(z_end_list[third_plane_hit_list[0]] - z_end_list[i]) <= math.fabs(z_end_list[third_plane_hit_list[1]] - z_end_list[i]) and math.fabs(z_end_list[third_plane_hit_list[0]] - z_end_list[i]) <= math.fabs(z_end_list[third_plane_hit_list[1]] - z_end_list[i]):

                                     print "Hit 0 Wins!"
                                     print "Third Instance:", third_plane_hit_list[0], "Plane:", plane_num_list[third_plane_hit_list[0]]
                                     print "Wire Number:", wire_num_list[third_plane_hit_list[0]]
                                     print "y Ending Position of Third Instance:", y_end_list[third_plane_hit_list[0]]
                                     print "z Ending Position of Third Instance:", z_end_list[third_plane_hit_list[0]]
                                     print "\n"

                                 else:

                                     print "Hit 1 Wins!"
                                     print "Third Instance:", third_plane_hit_list[1], "Plane:", plane_num_list[third_plane_hit_list[1]]
                                     print "Wire Number:", wire_num_list[third_plane_hit_list[1]]
                                     print "y Ending Position of Third Instance:", y_start_list[third_plane_hit_list[1]]
                                     print "z Ending Position of Third Instance:", z_start_list[third_plane_hit_list[1]]
                                     print "\n\n"


