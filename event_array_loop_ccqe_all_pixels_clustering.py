import sys
from larcv import larcv
import numpy as np

# Import the file that will contain the algorithm for matching the wire with other wires that //
# are at the same y and z coordinates
import y_wire_matches_single_threshold_improved
import z_wire_matches_single_threshold_improved
import barnes_pixel_clustering
import barnes_pixel_organization
import barnes_track_association

# Set np printing options
np.set_printoptions(threshold=np.nan)

try:
    # my preference is to use opencv to output the image                        
    # but we default to matplotlib if opencv 3 not available                    
    import cv2
    hascv = True
except:
    import matplotlib.pyplot as plt
    hascv = False

# Use this command to get the input root file from the user
inputfile = sys.argv[1]

# Producer name
IMAGE_PRODUCER="tpc"

# IOmanager
# Handles the ROOT file interface for us. Sets up branches
ioman = larcv.IOManager(larcv.IOManager.kREAD, "IO") # instantiate instance (in read mode)
ioman.add_in_file( inputfile ) # append file to manager
ioman.initialize() # setup the trees

# Event Loop
nentries = ioman.get_n_entries()

# This will be the loop to contain all of the information about the entries in each of the arrays

# Only loop through three of the entries for now
nentries = 1

# Declare a variable for the number of event that I'm on (to keep track)
# event_num = 0

for entry in xrange(nentries):

    # print "Event #", event_num
    # print "\n"

    # Increment the event number 
    # event_num += 1

    # Get an entry by index
    ioman.read_entry( entry )

    # Get a container with the event images
    # this command tells the iomanager to get a tree whose contents contain Image2D and whose
    #  "producer" label is IMAGE_PRODUCER
    # again, finds the tree with name: image2d_(IMAGE_PRODUCER)_tree
    event_images = ioman.get_data( larcv.kProductImage2D, IMAGE_PRODUCER)

    # get image vector (the image2d instances are stored in a std vector)
    img_v = event_images.Image2DArray()

    # get the height (rows) and width (cols) of our image, using the first one in the vector
    # by convention our images are all the same size. mostly a restriction due to caffe.
    # notice how image meta data is stored in an ImageMeta class that we retrieve by the meta() method
    rows = img_v.front().meta().rows()
    cols = img_v.front().meta().cols()

    # We are going to output an BGR image, make the container for it           
    outimg = np.zeros( (rows,cols,3) )

    # Now I need to transpose the matrix before tagging the end of the particle tracks

    # loop over the images in the array and put them into the numpy array       
    for img in img_v:                
        
        # we convert the Image2D data into a numpy array
        imgnd = larcv.as_ndarray(img)

        # image2d and numpy conventions on row and cols are not the same...
        imgnd = np.transpose( imgnd, (1,0) )
        
        # my preference is to have time go from top to bottom, Image2D assumes otherwise, so I reverse the y-axis here (which are the rows)
        imgnd = imgnd[::-1,:]
        
        # we use the [0,255] BGR color scale. I'm not being careful about normalizing values. But I know that I want MIP tracks to be around 128.              
        # the MIP peak was calibrated to be around 1.0 when we made this data.  
        outimg[:,:,img.meta().plane()] = imgnd

    # This inverts what I'll do below in order to operate on each of the images.  I'll set each of the outimg third components equal to the imgnds at the end
    # when the image is to be displayed
    uplane_imgnd  = outimg[:,:,0]
    vplane_imgnd  = outimg[:,:,1]
    yplane_imgnd  = outimg[:,:,2]

    # Loop through each of the arrays to find matches for the affected wires in each pixel 

    # Declare the ADC threshold for considering a signal in one of the pixels at a specific time (keep the standard threshold at an ADC value of 0.10)
    threshold = 0.10

    # Declare a variable for the number of pixels on either side of the match that you would like to check to account for the space charge effect (keep the pixel_check_range to a value of 3 pixels or less to avoid errant matches of charge across the three planes)
    pixel_check_range = 3

    # Declare a variable for the smallest and largest wire indices that could have been excited
    wire_smallest = 0
    wire_largest  = 0

    # Declare variables for the pixels corresponding to the wires that were found by wire_matching_algo

    plane_one_pixel = 0
    plane_two_pixel = 0
    plane_three_pixel = 0

    # Set two lists equal to the top wire matches and the bottom wire matches
    upstream_wire_matches   = y_wire_matches_single_threshold_improved.wire_matching_algo(0.271)[0]
    downstream_wire_matches = y_wire_matches_single_threshold_improved.wire_matching_algo(0.271)[1]
    top_wire_matches        = z_wire_matches_single_threshold_improved.wire_matching_algo(0.300)[0]
    bottom_wire_matches     = z_wire_matches_single_threshold_improved.wire_matching_algo(0.300)[1]

    # Define dictionaries for the pixels that are colored for each type of hit
    upstream_pixel_dict   = {}
    downstream_pixel_dict = {}
    top_pixel_dict        = {}
    bottom_pixel_dict     = {}

    # Define an iterator for each of the dictionaries here
    upstream_pixel_dict_iter   = 0
    downstream_pixel_dict_iter = 0
    top_pixel_dict_iter        = 0
    bottom_pixel_dict_iter     = 0

    # The range of the new file is (756, 864)
    for i in range (0, 756): # This loops through each row, or time, for which data is being collected in a 'for' loop

        for wire in range(len(upstream_wire_matches)):
            
            # Define each of the wires 
            first_plane_wire  = upstream_wire_matches[wire][0]
            second_plane_wire = upstream_wire_matches[wire][1]
            
            # Convert each of these wires to pixels
            first_plane_pixel  = (first_plane_wire - (first_plane_wire % 4))/4
            second_plane_pixel = (second_plane_wire - (second_plane_wire % 4))/4

            # Go to the next wire if this value of uplane_imgnd[i][first_plane_pixel] is less than the threshold
            # I have to include the possibility that the uplane_imgnd is greater than 100 (if it's already been filled)
            if uplane_imgnd[i][first_plane_pixel] < threshold:

                continue

            # Define a variable for the number of pixels on the second plane that are above threshold
            plane_two_neighbors_above_threshold = 0

            # Check to see if the pixel reading value is less than zero.  If it is, then continue.  The neighboring pixel will be picked up in another loop                      
            #/using pixel_check_range                                                                                                                                           
            if vplane_imgnd[i][second_plane_pixel] < 0:

                continue

            for plane_two_pixel in range(second_plane_pixel - pixel_check_range, second_plane_pixel + pixel_check_range + 1):

                # Get out of index_range errors by including 'if' statements for the possibility that the loop goes over values
                # that are out of range

                if plane_two_pixel < 0:

                    continue

                if plane_two_pixel > 863:

                    continue

                if vplane_imgnd[i][plane_two_pixel] < 0 or vplane_imgnd[i][plane_two_pixel] > 100: # If it's greater than 100 than it's already been illuminated

                    continue

                # If this cycle of the 'for' loop has made it this far, then check to see if the vplane_imgnd value is above threshold
                if vplane_imgnd[i][plane_two_pixel] > threshold:

                    plane_two_neighbors_above_threshold += 1

            # Now, continue onto the next wire if plane_two_neighbors_above_threshold is equal to 0

            if plane_two_neighbors_above_threshold == 0:

                continue
         
            # Include a statement to ensure that all of the pixels being filled are less than 100 (meaning that they haven't been filled before)
            # This is redundant for the code written above, but it's better to be redundant than to fill the same pixel more than once in different iterations
            if uplane_imgnd[i][first_plane_pixel] < 100 and vplane_imgnd[i][first_plane_pixel] < 100 and uplane_imgnd[i][second_plane_pixel] < 100 and vplane_imgnd[i][second_plane_pixel] < 100:

                # Fill this entry in the dict with a list of the time, first plane pixel, and second plane pixel
                upstream_pixel_dict[upstream_pixel_dict_iter] = [i, first_plane_pixel, second_plane_pixel]
                upstream_pixel_dict_iter += 1

                # Print out the wire and pixel information if you make it this far
                print "Upstream Pixel Match!"
                print "First Plane Wire: ", first_plane_wire, "First Plane Pixel: ", first_plane_pixel
                print "Second Plane Wire: ", second_plane_wire, "Second Plane Pixel: ", second_plane_pixel
                print '\n'

        # Repeat the same loop for the bottom wire matches
        for wire in range(len(downstream_wire_matches)):

            # Define each of the wires                                                                                                                                            
            first_plane_wire  = downstream_wire_matches[wire][0]
            second_plane_wire = downstream_wire_matches[wire][1]

            # Convert each of these wires to pixels                                                                                                                             
            first_plane_pixel  = (first_plane_wire - (first_plane_wire % 4))/4
            second_plane_pixel = (second_plane_wire - (second_plane_wire % 4))/4

            # Go to the next wire if this value of uplane_imgnd[i][first_plane_pixel] is less than the threshold                                                                
            if uplane_imgnd[i][first_plane_pixel] < threshold:

                continue

            # Define a variable for the number of pixels on the second plane that are above threshold                                                                         
            plane_two_neighbors_above_threshold = 0

            # Check to see if the pixel reading value is less than zero.  If it is, then continue.  The neighboring pixel will be picked up in another loop                      
            #/using pixel_check_range                                                                                                                                            
            if vplane_imgnd[i][second_plane_pixel] < 0:

                continue

            for plane_two_pixel in range(second_plane_pixel - pixel_check_range, second_plane_pixel + pixel_check_range + 1):

                # Get out of index_range errors by including 'if' statements for the possibility that the loop goes over values                                                  
                # that are out of range                                                                                                                                         
                if plane_two_pixel < 0:

                    continue

                if plane_two_pixel > 863:

                    continue

                if vplane_imgnd[i][plane_two_pixel] < 0 or vplane_imgnd[i][plane_two_pixel] > 100: # If it's greater than 100 than it's already been illuminated                
                    
                    continue

                # If this cycle of the 'for' loop has made it this far, then check to see if the vplane_imgnd value is above threshold                                          
                if vplane_imgnd[i][plane_two_pixel] > threshold:

                    plane_two_neighbors_above_threshold += 1

                # Now, continue onto the next wire if plane_two_neighbors_above_threshold is equal to 0                                                                         
            if plane_two_neighbors_above_threshold == 0:

                continue

            # Include a statement to ensure that all the pixels being filled are less than 100 (meaning they haven't been filled before)
            # This is redundant for the code written above, but it's better to be redundant than to fill the same pixel more than once in different iterations
            if vplane_imgnd[i][first_plane_pixel] < 100 and yplane_imgnd[i][first_plane_pixel] < 100 and vplane_imgnd[i][second_plane_pixel] < 100 and yplane_imgnd[i][second_plane_pixel] < 100:

                # Fill this entry in the dict with a list of the time, first plane pixel, and second plane pixel
                downstream_pixel_dict[downstream_pixel_dict_iter] = [i, first_plane_pixel, second_plane_pixel]
                downstream_pixel_dict_iter += 1
                
                # Print out the wire and pixel information if you make it this far                                                                                           
                print "Downstream Pixel Match!"
                print "First Plane Wire: ", first_plane_wire, "First Plane Pixel: ", first_plane_pixel
                print "Second Plane Wire: ", second_plane_wire, "Second Plane Pixel: ", second_plane_pixel
                print '\n'

        for wire in range(len(top_wire_matches)):

            # Define each of the wires                                                                                                                                          
            first_plane_wire  = top_wire_matches[wire][0]
            second_plane_wire = top_wire_matches[wire][1]

            # There are two wires on the third plane, but I'll just define the first one because I'll loop over the pixels within a range                                      
            # of pixel_check_range on either side of the central pixel                                                                                                           
            third_plane_wire  = top_wire_matches[wire][2]

            # Convert each of these wires to pixels                                                                                                                             
            first_plane_pixel  = (first_plane_wire - (first_plane_wire % 4))/4
            second_plane_pixel = (second_plane_wire - (second_plane_wire % 4))/4
            third_plane_pixel  = (third_plane_wire - (third_plane_wire % 4))/4

            # Go to the next wire if this value of uplane_imgnd[i][first_plane_pixel] is less than the threshold                                                               
            # I have to include the possibility that the uplane_imgnd is greater than 100 (if it's already been filled)                                                          
            if uplane_imgnd[i][first_plane_pixel] < threshold:

                continue

            # Define a variable for the number of pixels on the second plane that are above threshold                                                                          
            plane_two_neighbors_above_threshold = 0

            # Check to see if the pixel reading value is less than zero.  If it is, then continue.  The neighboring pixel will be picked up in another loop                      
            # using pixel_check_range                                                                                                                                            
            if vplane_imgnd[i][second_plane_pixel] < 0:

                continue

            for plane_two_pixel in range(second_plane_pixel - pixel_check_range, second_plane_pixel + pixel_check_range + 1):

                # Get out of index_range errors by including 'if' statements for the possibility that the loop goes over values                                                
                # that are out of range                                                                                                                                        
                if plane_two_pixel < 0:

                    continue

                if plane_two_pixel > 863:

                    continue

                if vplane_imgnd[i][plane_two_pixel] < 0 or vplane_imgnd[i][plane_two_pixel] > 100: # If it's greater than 100 than it's already been illuminated                
                    
                    continue

             # If this cycle of the 'for' loop has made it this far, then check to see if the vplane_imgnd value is above threshold                                               
                if vplane_imgnd[i][plane_two_pixel] > threshold:

                    plane_two_neighbors_above_threshold += 1

            # Now, continue onto the next wire if plane_two_neighbors_above_threshold is equal to 0                                                                             
            if plane_two_neighbors_above_threshold == 0:

                continue

            # Define a variable for the number of pixels on the third plane that are above threshold                                                                             
            plane_three_neighbors_above_threshold = 0

            # Check to see if the pixel reading value is less than zero.  If it is, then continue.  The neighboring pixel will be picked up in another loop                      
            # using pixel_check_range                                                                                                                                            
            if yplane_imgnd[i][third_plane_pixel] < 0:

                continue

            for plane_three_pixel in range(third_plane_pixel - pixel_check_range, third_plane_pixel + pixel_check_range + 1):

                # Get out of index_range errors by including 'if' statements for the possibility that the loop goes over values                                                 
                # that are out of range                                                                                                                                        
                if plane_three_pixel < 0:

                    continue

                if plane_three_pixel > 863:

                    continue

                if yplane_imgnd[i][plane_three_pixel] < 0 and yplane_imgnd[i][plane_three_pixel] > 100:

                    continue

                if yplane_imgnd[i][plane_three_pixel] > threshold:

                    plane_three_neighbors_above_threshold += 1

            # Check to see if plane_three_neighbors_above_threshold is equal to 0.  Continue if it is.                                                                           
            if plane_three_neighbors_above_threshold == 0:

                continue

            # Include a statement to ensure that all of the pixels being filled are less than 100 (meaning that they haven't been filled before)                                 
            # This is redundant for the code written above, but it's better to be redundant than to fill the same pixel more than once in different iterations                  
            if uplane_imgnd[i][first_plane_pixel] < 100 and vplane_imgnd[i][first_plane_pixel] < 100 and yplane_imgnd[i][second_plane_pixel] < 100 and uplane_imgnd[i][second_plane_pixel] < 100 and vplane_imgnd[i][second_plane_pixel] < 100 and yplane_imgnd[i][second_plane_pixel] < 100 and uplane_imgnd[i][third_plane_pixel] < 100 and vplane_imgnd[i][third_plane_pixel] < 100 and yplane_imgnd[i][third_plane_pixel] < 100:

                # Fill this entry in the dict with a list of the time, first plane pixel, second plane pixel, and the third plane pixel
                top_pixel_dict[top_pixel_dict_iter] = [i, first_plane_pixel, second_plane_pixel, third_plane_pixel]
                top_pixel_dict_iter += 1                

                # Print out the wire and pixel information if you make it this far                                                                                                
                print "Top Pixel Match!"
                print "First Plane Wire: ", first_plane_wire, "First Plane Pixel: ", first_plane_pixel
                print "Second Plane Wire: ", second_plane_wire, "Second Plane Pixel: ", second_plane_pixel
                print "Third Plane Wire: ", third_plane_wire, "Third Plane Pixel: ", third_plane_pixel
                print '\n'

        # Repeat the same loop for the bottom wire matches                                                                                                                     
        for wire in range(len(bottom_wire_matches)):

            # Define each of the wires                                                                                                                                         
            first_plane_wire  = bottom_wire_matches[wire][0]
            second_plane_wire = bottom_wire_matches[wire][1]

            # There are two wires on the third plane, but I'll just define the first one because I'll loop over the pixels within a range                                      
            # of pixel_check_range on either side of the central pixel                                                                                                         
            third_plane_wire  = bottom_wire_matches[wire][2]

            # Convert each of these wires to pixels                                                                                                                           
            first_plane_pixel  = (first_plane_wire - (first_plane_wire % 4))/4
            second_plane_pixel = (second_plane_wire - (second_plane_wire % 4))/4
            third_plane_pixel  = (third_plane_wire - (third_plane_wire % 4))/4

            # Go to the next wire if this value of uplane_imgnd[i][first_plane_pixel] is less than the threshold                                                               
            if uplane_imgnd[i][first_plane_pixel] < threshold:

                continue

            # Define a variable for the number of pixels on the second plane that are above threshold                                                                          
            plane_two_neighbors_above_threshold = 0

            # Check to see if the pixel reading value is less than zero.  If it is, then continue.  The neighboring pixel will be picked up in another loop                     
            # using pixel_check_range                                                                                                                                           
            if vplane_imgnd[i][second_plane_pixel] < 0:

                continue

            for plane_two_pixel in range(second_plane_pixel - pixel_check_range, second_plane_pixel + pixel_check_range + 1):

                # Get out of index_range errors by including 'if' statements for the possibility that the loop goes over values                                                
                # that are out of range                                                                                                                                         
                if plane_two_pixel < 0:

                    continue

                if plane_two_pixel > 863:

                    continue

                if vplane_imgnd[i][plane_two_pixel] < 0 or vplane_imgnd[i][plane_two_pixel] > 100: # If it's greater than 100 than it's already been illuminated                
                    
                    continue

                # If this cycle of the 'for' loop has made it this far, then check to see if the vplane_imgnd value is above threshold                                         
                if vplane_imgnd[i][plane_two_pixel] > threshold:

                    plane_two_neighbors_above_threshold += 1

                # Now, continue onto the next wire if plane_two_neighbors_above_threshold is equal to 0                                                                        
            if plane_two_neighbors_above_threshold == 0:

                continue

            # Define a variable for the number of pixels on the third plane that are above threshold                                                                           
            plane_three_neighbors_above_threshold = 0

            # Check to see if the pixel reading value is less than zero.  If it is, then continue.  The neighboring pixel will be picked up in another loop                    
            #using pixel_check_range                                                                                                                                         
            if yplane_imgnd[i][third_plane_pixel] < 0:

                continue

            for plane_three_pixel in range(third_plane_pixel - pixel_check_range, third_plane_pixel + pixel_check_range + 1):

                # Get out of index_range errors by including 'if' statements for the possibility that the loop goes over values                                                 
                # that are out of range                                                                                                                                          
                if plane_three_pixel < 0:

                    continue

                if plane_three_pixel > 863:

                    continue

                if yplane_imgnd[i][plane_three_pixel] < 0 and yplane_imgnd[i][plane_three_pixel] > 100:

                    continue

                if yplane_imgnd[i][plane_three_pixel] > threshold:

                    plane_three_neighbors_above_threshold += 1

            # Check to see if plane_three_neighbors_above_threshold is equal to 0.  Continue if it is.                                                                           
            if plane_three_neighbors_above_threshold == 0:

                continue

            # Include a statement to ensure that all the pixels being filled are less than 100 (meaning they haven't been filled before)                           
            # This is redundant for the code written above, but it's better to be redundant than to fill the same pixel more than once in different iterations                   
 
            if uplane_imgnd[i][first_plane_pixel] < 100 and vplane_imgnd[i][first_plane_pixel] < 100 and yplane_imgnd[i][second_plane_pixel] < 100 and uplane_imgnd[i][second_plane_pixel] < 100 and vplane_imgnd[i][second_plane_pixel] < 100 and yplane_imgnd[i][second_plane_pixel] < 100 and uplane_imgnd[i][third_plane_pixel] < 100 and vplane_imgnd[i][third_plane_pixel] < 100 and yplane_imgnd[i][third_plane_pixel] < 100:

                # Fill this entry in the dict with a list of the time, first plane pixel, second plane pixel, and the third plane pixel                                         
                bottom_pixel_dict[bottom_pixel_dict_iter] = [i, first_plane_pixel, second_plane_pixel, third_plane_pixel]
                bottom_pixel_dict_iter += 1

                # Print out the wire and pixel information if you make it this far                                                                                              
                print "Bottom Pixel Match!"
                print "First Plane Wire: ", first_plane_wire, "First Plane Pixel: ", first_plane_pixel
                print "Second Plane Wire: ", second_plane_wire, "Second Plane Pixel: ", second_plane_pixel
                print "Third Plane Wire: ", third_plane_wire, "Third Plane Pixel: ", third_plane_pixel
                print '\n'

    
    # Call the barnes_track_association function to see if it works

    # Now, I will color the up hits yellow
    # for upstream_entry in up_list_hits:

        # Fill the two vectors at the two pixels in the correct ratios to turn the up hits yellow
        # for pixel in [upstream_entry[1], upstream_entry[2]]:

            # vplane_imgnd[upstream_entry[0]][pixel] += 150
            # yplane_imgnd[upstream_entry[0]][pixel] += 150

    # Now, I will color the down hits orange
    # for downstream_entry in down_list_hits:

        # Fill the two vectors at the two pixels in the correct ratios to turn the down hits orange
        # for pixel in [downstream_entry[1], downstream_entry[2]]:

            # vplane_imgnd[downstream_entry[0]][pixel] += 100
            # yplane_imgnd[downstream_entry[0]][pixel] += 200

    # Now, I will color the top hits cyan
    # for top_entry in top_list_hits:
  
        # Fill the two vectors at the two pixels in the correct ratios to turn the top hits cyan
        # for pixel in [top_entry[1], top_entry[2], top_entry[3]]:

            # uplane_imgnd[top_entry[0], pixel] += 100
            # vplane_imgnd[top_entry[0], pixel] += 200

    # Now, I will color the bottom hits magenta
    # for bottom_entry in bottom_list_hits:

        # Fill the two vectors at the two pixels in the correct ratios to turn the bottom hits magenta
        # for pixel in [bottom_entry[1], bottom_entry[2], bottom_entry[3]]:

            # uplane_imgnd[bottom_entry[0]][pixel] += 100
            # yplane_imgnd[bottom_entry[0]][pixel] += 200

    # Check to see if the barnes_track_association_function works
    barnes_track_association.barnes_track_association_func(upstream_pixel_dict, downstream_pixel_dict, top_pixel_dict, bottom_pixel_dict, uplane_imgnd, vplane_imgnd, yplane_imgnd)

    # Here the arrays for the individual planes are again set equal to the respective vectors in the outimg[,,] array                                                               
    # outimg[:,:,0] = 128*uplane_imgnd
    # outimg[:,:,1] = 128*vplane_imgnd
    # outimg[:,:,2] = 128*yplane_imgnd


    # outname = 'threshold0.30checkrange3fullbarnesclustering_%d.png' % (entry)

    # if not hascv:
        # mat_display=plt.imshow( outimg )
        # mat_display.write_png(outname)
    # else:
        # note opencv uses BGR format                                                                                                                                               
        # so B=U plane, G=V plane, R=Y plane                                                                                                                 
        # cv2.imwrite( outname, outimg )





    








