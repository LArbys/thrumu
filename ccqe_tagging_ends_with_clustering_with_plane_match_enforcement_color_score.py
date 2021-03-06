import sys
from larcv import larcv
import numpy as np

# Import the file that will contain the algorithm for matching the wire with other wires that //
# are at the same y and z coordinates
import y_wire_matches_single_threshold_improved
import z_wire_matches_single_threshold_improved
import preclustering_pixel_organization_time_pixel_list
import barnes_pixel_clustering_2D_clustering
import multiple_plane_hits_enforcement_grouping
import adjacent_pixels_color_scoring
import pixel_color_adding_algo
# import dead_pixel_region_classifier
# import dead_pixel_region_classifier_encapsulated

# Set np printing options
# np.set_printoptions(threshold=np.nan) # Not really necessary at this point

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
nentries = 5

for entry in xrange(nentries):

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

    # We are going to output an BGR image ** for the clustering algorithm **, make the container for it          
    outimg = np.zeros( (rows,cols,3) )

    # Now I need to transpose the matrix before tagging the end of the particle tracks
    # Loop over the images in the array and put them into the numpy array       
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

    # This inverts what I'll do below in order to operate on each of the images.  I'll set each of the 'outimg' third components equal to the imgnds at the end
    # when the image is to be displayed

    # I'll separate out the three components of the 'outimg' array for when I examine their components
    uplane_imgnd = outimg[:, :, 0]
    vplane_imgnd = outimg[:, :, 1]
    yplane_imgnd = outimg[:, :, 2]

    # Loop through each of the arrays to find matches for the affected wires in each pixel 

    # Define a minimum ADC value that must be in each matching pixel to even consider the neighboring pixels for a greater amount of charge
    # minimum_matching_pixel_ADC_value = 0.02

    # Declare the ADC threshold for considering a signal in one of the pixels at a specific time (keep the standard threshold at an ADC value of 0.10)
    upstream_threshold   = 0.05
    downstream_threshold = 0.03
    top_threshold        = 0.15
    bottom_threshold     = 0.15

    # Declare a variable for the number of pixels on either side of the match that you would like to check to account for the space charge effect (keep the pixel_check_range to a value of 3 pixels or less to avoid errant matches of charge across the three planes)
    pixel_check_range = 8

    # Declare a variable for the smallest and largest wire indices that could have been excited
    wire_smallest = 0
    wire_largest  = 0

    # Declare variables for the pixels corresponding to the wires that were found by wire_matching_algo
    plane_one_pixel   = 0
    plane_two_pixel   = 0
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

            # Add a loop to ensure that that the three matching pixels have a minimum ADC value before considering the neighbors' values 
            # // for each type of hit.  This can go at the beginning to save time in the loop (we already know this information)
            # if uplane_imgnd[i][first_plane_pixel] < 0 or vplane_imgnd[i][second_plane_pixel] < 0:

                # continue

            # Define a variable for any neighboring pixels on the uplane that are above threshold
            plane_one_neighbors_above_threshold = 0

            for plane_one_pixel in range (first_plane_pixel - pixel_check_range, first_plane_pixel + pixel_check_range + 1):

                if plane_one_pixel < 0:

                    continue

                if plane_one_pixel > 599:

                    continue

                if uplane_imgnd[i][plane_one_pixel] < 0:

                    continue

                # If this cycle of the 'for' loop has made it this far, then check to see if the vplane_imgnd value is above threshold                                         
                if uplane_imgnd[i][plane_one_pixel] > upstream_threshold:

                    plane_one_neighbors_above_threshold += 1

            # Check to see if 'plane_one_neighbors_above_threshold' is greater than 0
            if plane_one_neighbors_above_threshold == 0:

                continue

            # Define a variable for the number of pixels on the second plane that are above threshold
            plane_two_neighbors_above_threshold = 0

            # Loop through the neighboring pixels to see if any on plane two are above threshold
            for plane_two_pixel in range(second_plane_pixel - pixel_check_range, second_plane_pixel + pixel_check_range + 1):

                # Get out of index_range errors by including 'if' statements for the possibility that the loop goes over values
                # that are out of range
                if plane_two_pixel < 0:

                    continue

                if plane_two_pixel > 599:

                    continue

                # The '> 100' part was removed, because the coloring takes place at the bottom of the script
                if vplane_imgnd[i][plane_two_pixel] < 0: 

                    continue

                # If this cycle of the 'for' loop has made it this far, then check to see if the vplane_imgnd value is above threshold
                if vplane_imgnd[i][plane_two_pixel] > upstream_threshold:

                    plane_two_neighbors_above_threshold += 1

            # Now, continue onto the next wire if plane_two_neighbors_above_threshold is equal to 0
            if plane_two_neighbors_above_threshold == 0:

                continue

            # Check to see if at this time, the '0' pixel is below threshold.  If it is, then continue.
            if yplane_imgnd[i][0] < upstream_threshold:

                continue

            # The loop has made it through every single test by this point in the algorithm
            # You don't have to fill in the '0' pixel as the y-plane one, because it's done in the pixel coloring file

            # Check to ensure that the previous entry in 'upstream_pixel_dict' is not the same as the pixel that you have now (I've seen a lot of multiple matches)
            # First, avoid an error by ensuring that the iterator is greater than zero
            if upstream_pixel_dict_iter > 0 and upstream_pixel_dict[upstream_pixel_dict_iter - 1] == [i, first_plane_pixel, second_plane_pixel]:
                    
                    # You should continue with the loop because you are recording a combination that has already been placed in the dictionary
                    continue


            upstream_pixel_dict[upstream_pixel_dict_iter] = [i, first_plane_pixel, second_plane_pixel]
            upstream_pixel_dict_iter += 1

                # Print out the wire and pixel information if you make it this far
                # print "Upstream Pixel Match!"
                # print "First Plane Wire: ", first_plane_wire, "First Plane Pixel: ", first_plane_pixel
                # print "Second Plane Wire: ", second_plane_wire, "Second Plane Pixel: ", second_plane_pixel
                # print '\n'

        # Repeat the same loop for the bottom wire matches
        for wire in range(len(downstream_wire_matches)):

            # Define each of the wires                                                                                                                                      
            first_plane_wire  = downstream_wire_matches[wire][0]
            second_plane_wire = downstream_wire_matches[wire][1]

            # Convert each of these wires to pixels                                                                                                                       
            first_plane_pixel  = (first_plane_wire - (first_plane_wire % 4))/4
            second_plane_pixel = (second_plane_wire - (second_plane_wire % 4))/4

            # Add a loop to ensure that that the three matching pixels have a minimum ADC value before considering the neighbors' values                                       
            # // for each type of hit.  This can go at the beginning to save time in the loop (we already know this information)                                               
            # if uplane_imgnd[i][first_plane_pixel] < 0 or vplane_imgnd[i][second_plane_pixel] < 0:

                # continue

            # Define a variable for any neighboring pixels on the uplane that are above threshold                                                                         
            plane_one_neighbors_above_threshold = 0

            for plane_one_pixel in range (first_plane_pixel - pixel_check_range, first_plane_pixel + pixel_check_range + 1):

                if plane_one_pixel < 0:

                    continue

                if plane_one_pixel > 599:

                    continue

                if uplane_imgnd[i][plane_one_pixel] < 0:

                    continue

                # If this cycle of the 'for' loop has made it this far, then check to see if the vplane_imgnd value is above threshold                                    
                if uplane_imgnd[i][plane_one_pixel] > downstream_threshold:

                    plane_one_neighbors_above_threshold += 1

            # Check to see if 'plane_one_neighbors_above_threshold' is greater than 0                                                                                          
            if plane_one_neighbors_above_threshold == 0:

                continue

            # Define a variable for the number of pixels on the second plane that are above threshold                                                                         
            plane_two_neighbors_above_threshold = 0

            for plane_two_pixel in range(second_plane_pixel - pixel_check_range, second_plane_pixel + pixel_check_range + 1):

                # Get out of index_range errors by including 'if' statements for the possibility that the loop goes over values                                           
                # that are out of range                                                                                                                                  
                if plane_two_pixel < 0:

                    continue

                if plane_two_pixel > 599:

                    continue

                # The '> 100' part was removed, because the coloring takes place at the bottom of the script
                if vplane_imgnd[i][plane_two_pixel] < 0:
                    
                    continue

                # If this cycle of the 'for' loop has made it this far, then check to see if the vplane_imgnd value is above threshold                                    
                if vplane_imgnd[i][plane_two_pixel] > downstream_threshold: # I'm using a higher threshold here to clean up the cluster at the end of the vplane track

                    plane_two_neighbors_above_threshold += 1

            # Now, continue onto the next wire if plane_two_neighbors_above_threshold is equal to 0                                                                   
            if plane_two_neighbors_above_threshold == 0:

                continue

            # Check to see if at this time, the '863' pixel is below threshold.  If it is, then continue.                                                                    
            if yplane_imgnd[i][863] < downstream_threshold:

                continue

            # Check to ensure that the previous entry in 'downstream_pixel_dict' is not the same as the pixel that you have now (I've seen a lot of multiple matches)       
            # First, avoid an error by ensuring that the iterator is greater than zero                                                                               
            if downstream_pixel_dict_iter > 0 and downstream_pixel_dict[downstream_pixel_dict_iter - 1] == [i, first_plane_pixel, second_plane_pixel]:

                # You should continue with the loop because you are recording a combination that has already been placed in the dictionary                     
                continue

            # The loop has made it through every single test by this point in the algorithm
            # You don't have to fill in the '0' pixel as the y-plane one, because it's done in the pixel coloring file
            downstream_pixel_dict[downstream_pixel_dict_iter] = [i, first_plane_pixel, second_plane_pixel]
            downstream_pixel_dict_iter += 1
                
                # Print out the wire and pixel information if you make it this far                                                                                           
                # print "Downstream Pixel Match!"
                # print "First Plane Wire: ", first_plane_wire, "First Plane Pixel: ", first_plane_pixel
                # print "Second Plane Wire: ", second_plane_wire, "Second Plane Pixel: ", second_plane_pixel
                # print '\n'

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

             # Add a loop to ensure that that the three matching pixels have a minimum ADC value before considering the neighbors' values                                      
             # // for each type of hit.  This can go at the beginning to save time in the loop (we already know this information)                                                
            # if uplane_imgnd[i][first_plane_pixel] < 0 or vplane_imgnd[i][second_plane_pixel] < 0 or yplane_imgnd[i][third_plane_pixel] < 0:

                # continue

            # Define a variable for any neighboring pixels on the uplane that are above threshold                                                                         
            plane_one_neighbors_above_threshold = 0

            for plane_one_pixel in range (first_plane_pixel - pixel_check_range, first_plane_pixel + pixel_check_range + 1):

                if plane_one_pixel < 0:

                    continue

                if plane_one_pixel > 599:

                    continue

                if uplane_imgnd[i][plane_one_pixel] < 0:

                    continue

                # If this cycle of the 'for' loop has made it this far, then check to see if the vplane_imgnd value is above threshold                                         
                if uplane_imgnd[i][plane_one_pixel] > top_threshold:

                    plane_one_neighbors_above_threshold += 1

            # Check to see if 'plane_one_neighbors_above_threshold' is greater than 0                                                                                         
            if plane_one_neighbors_above_threshold == 0:

                continue

            # Define a variable for the number of pixels on the second plane that are above threshold                                                                          
            plane_two_neighbors_above_threshold = 0

            # Check to see if any of the pixels within range are above threshold
            for plane_two_pixel in range(second_plane_pixel - pixel_check_range, second_plane_pixel + pixel_check_range + 1):

                # Get out of index_range errors by including 'if' statements for the possibility that the loop goes over values                                                
                # that are out of range                                                                                                                                        
                if plane_two_pixel < 0:

                    continue

                if plane_two_pixel > 599:

                    continue

                # Some of the ADC values may become negative in the deconvolution.  The '> 100' part was removed, because the coloring takes place at the bottom of the 
                # script
                if vplane_imgnd[i][plane_two_pixel] < 0:
                    
                    continue

                # If this cycle of the 'for' loop has made it this far, then check to see if the vplane_imgnd value is above threshold                                    
                if vplane_imgnd[i][plane_two_pixel] > top_threshold:

                    plane_two_neighbors_above_threshold += 1

            # Now, continue onto the next wire if plane_two_neighbors_above_threshold is equal to 0                                                                     
            if plane_two_neighbors_above_threshold == 0:

                continue

            # Define a variable for the number of pixels on the third plane that are above threshold                                                                     
            plane_three_neighbors_above_threshold = 0

            for plane_three_pixel in range(third_plane_pixel - pixel_check_range, third_plane_pixel + pixel_check_range + 1):

                # Get out of index_range errors by including 'if' statements for the possibility that the loop goes over values                                           
                # that are out of range                                                                                                                                        
                if plane_three_pixel < 0:

                    continue

                if plane_three_pixel > 863:

                    continue

                # Some of the ADC values may become negative in the deconvolution. The '> 100' part was removed, because the coloring takes place at the bottom of the      
                # script
                if yplane_imgnd[i][plane_three_pixel] < 0:

                    continue

                if yplane_imgnd[i][plane_three_pixel] > top_threshold:

                    plane_three_neighbors_above_threshold += 1

            # Check to see if plane_three_neighbors_above_threshold is equal to 0.  Continue if it is.                                                                    
            if plane_three_neighbors_above_threshold == 0:

                continue

            # Check to ensure that the previous entry in 'top_pixel_dict' is not the same as the pixel that you have now (I've seen a lot of multiple matches)     
            # First, avoid an error by ensuring that the iterator is greater than zero                                                                                     
            if top_pixel_dict_iter > 0 and top_pixel_dict[top_pixel_dict_iter - 1] == [i, first_plane_pixel, second_plane_pixel, third_plane_pixel]:

                # You should continue with the loop because you are recording a combination that has already been placed in the dictionary                           
                continue

            # The loop has made it through every single test by this point in the algorithm
            # Fill 'top_pixel_dict' with the time (y-axis) and the three plane pixels
            top_pixel_dict[top_pixel_dict_iter] = [i, first_plane_pixel, second_plane_pixel, third_plane_pixel]
            top_pixel_dict_iter += 1                

                # Print out the wire and pixel information if you make it this far                                                                                         
                # print "Top Pixel Match!"
                # print "First Plane Wire: ", first_plane_wire, "First Plane Pixel: ", first_plane_pixel
                # print "Second Plane Wire: ", second_plane_wire, "Second Plane Pixel: ", second_plane_pixel
                # print "Third Plane Wire: ", third_plane_wire, "Third Plane Pixel: ", third_plane_pixel
                # print '\n'

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

            # Add a loop to ensure that that the three matching pixels have a minimum ADC value before considering the neighbors' values                                            
            # // for each type of hit.  This can go at the beginning to save time in the loop (we already know this information)                                             
            # if uplane_imgnd[i][first_plane_pixel] < 0 or vplane_imgnd[i][second_plane_pixel] < 0 or yplane_imgnd[i][third_plane_pixel] < 0:

                # continue

            # Define a variable for any neighboring pixels on the uplane that are above threshold                                                                              
            plane_one_neighbors_above_threshold = 0

            for plane_one_pixel in range (first_plane_pixel - pixel_check_range, first_plane_pixel + pixel_check_range + 1):

                if plane_one_pixel < 0:

                    continue

                if plane_one_pixel > 599:

                    continue

                if uplane_imgnd[i][plane_one_pixel] < 0:

                    continue

                # If this cycle of the 'for' loop has made it this far, then check to see if the vplane_imgnd value is above threshold                                       
                if uplane_imgnd[i][plane_one_pixel] > bottom_threshold:

                    plane_one_neighbors_above_threshold += 1

            # Check to see if 'plane_one_neighbors_above_threshold' is greater than 0                                                                                          
            if plane_one_neighbors_above_threshold == 0:

                continue

            # Define a variable for the number of pixels on the second plane that are above threshold                                                                          
            plane_two_neighbors_above_threshold = 0
            
            # Loop over the pixels in the vicinity of the central pixel
            for plane_two_pixel in range(second_plane_pixel - pixel_check_range, second_plane_pixel + pixel_check_range + 1):

                # Get out of index_range errors by including 'if' statements for the possibility that the loop goes over values                                                
                # that are out of range                                                                                                                                   
                if plane_two_pixel < 0:

                    continue

                if plane_two_pixel > 599:

                    continue

                # The '> 100' part was removed, because the coloring takes place at the bottom of the script
                if vplane_imgnd[i][plane_two_pixel] < 0: 
                    
                    continue

                # If this cycle of the 'for' loop has made it this far, then check to see if the vplane_imgnd value is above threshold                                         
                if vplane_imgnd[i][plane_two_pixel] > bottom_threshold:

                    plane_two_neighbors_above_threshold += 1

                # Now, continue onto the next wire if plane_two_neighbors_above_threshold is equal to 0                                                                        
            if plane_two_neighbors_above_threshold == 0:

                continue

            # Define a variable for the number of pixels on the third plane that are above threshold                                                                           
            plane_three_neighbors_above_threshold = 0

            # Loop over the pixels in the vicinity of the central pixel
            for plane_three_pixel in range(third_plane_pixel - pixel_check_range, third_plane_pixel + pixel_check_range + 1):

                # Get out of index_range errors by including 'if' statements for the possibility that the loop goes over values                                           
                # that are out of range                                                                                                                                    
                if plane_three_pixel < 0:

                    continue

                if plane_three_pixel > 863:

                    continue

                # The '> 100' part was removed, because the coloring takes place at the bottom of the script
                if yplane_imgnd[i][plane_three_pixel] < 0: 

                    continue

                if yplane_imgnd[i][plane_three_pixel] > bottom_threshold:

                    plane_three_neighbors_above_threshold += 1

            # Check to see if plane_three_neighbors_above_threshold is equal to 0.  Continue if it is.                                                                    
            if plane_three_neighbors_above_threshold == 0:

                continue

            # Check to ensure that the previous entry in 'bottom_pixel_dict' is not the same as the pixel that you have now (I've seen a lot of multiple matches)            
            # First, avoid an error by ensuring that the iterator is greater than zero                                                                                   
            if bottom_pixel_dict_iter > 0 and bottom_pixel_dict[bottom_pixel_dict_iter - 1] == [i, first_plane_pixel, second_plane_pixel, third_plane_pixel]:

                # You should continue with the loop because you are recording a combination that has already been placed in the dictionary                           
                continue

            # This iteration of the loop has passed every conditional if it makes it this far, so this is a set of bottom matched pixels
            # Fill this entry in the dict with a list of the time, first plane pixel, second plane pixel, and the third plane pixel                                         
            bottom_pixel_dict[bottom_pixel_dict_iter] = [i, first_plane_pixel, second_plane_pixel, third_plane_pixel]
            bottom_pixel_dict_iter += 1

                # Print out the wire and pixel information if you make it this far                                                                                        
                # print "Bottom Pixel Match!"
                # print "First Plane Wire: ", first_plane_wire, "First Plane Pixel: ", first_plane_pixel
                # print "Second Plane Wire: ", second_plane_wire, "Second Plane Pixel: ", second_plane_pixel
                # print "Third Plane Wire: ", third_plane_wire, "Third Plane Pixel: ", third_plane_pixel
                # print '\n'


    ### Fill out the variables for the Top Pixels ###
    
    # Print out the top_pixel_dict:                                                                                                                                      
    print "Top Pixel Hit Dictionary: ", top_pixel_dict
    print "\n"

    ### Fill out the variables for the Bottom Pixels ###
    
    # Print out the bottom_pixel_dict:
    print "Bottom Pixel Hit Dictionary: ", bottom_pixel_dict
    print "\n"

    ### Fill out the variables for the Upstream Pixels ###

    # Print out the upstream_pixel_dict:
    print "Upstream Pixel Hit Dictionary: ", upstream_pixel_dict
    print "\n"

    ### Fill out the variables for the Downstream Pixels ###

    # Print out the downstream_pixel_dict:
    print "Downstream Pixel Hit Dictionary: ", downstream_pixel_dict
    print "\n"


    # Write code to organize the pixels using the existing clustering algorithm
    # First, organize all of the plane pixel hits into separate lists for each type of hit (i.e. top u hits, top v hits, top y hits; bottom u hits, ....) all paired with their corresponding time pixel
    
    # Top Tagged Pixels
    [top_u_TIME_AND_pixel_list_preclustering, top_v_TIME_AND_pixel_list_preclustering, top_y_TIME_AND_pixel_list_preclustering] = preclustering_pixel_organization_time_pixel_list.plane_hit_organization_algo(top_pixel_dict, 4)

    # Bottom Tagged Pixels
    [bottom_u_TIME_AND_pixel_list_preclustering, bottom_v_TIME_AND_pixel_list_preclustering, bottom_y_TIME_AND_pixel_list_preclustering] = preclustering_pixel_organization_time_pixel_list.plane_hit_organization_algo(bottom_pixel_dict, 4)

    # Upstream Tagged Pixels
    [upstream_u_TIME_AND_pixel_list_preclustering, upstream_v_TIME_AND_pixel_list_preclustering] = preclustering_pixel_organization_time_pixel_list.plane_hit_organization_algo(upstream_pixel_dict, 3)

    # Downstream Tagged Pixels
    [downstream_u_TIME_AND_pixel_list_preclustering, downstream_v_TIME_AND_pixel_list_preclustering] = preclustering_pixel_organization_time_pixel_list.plane_hit_organization_algo(downstream_pixel_dict, 3)



    # Find the quadrature sums with the first function in 'barnes_pixel_clustering_2D_clustering.py'

    # Top Quadrature Sums
    [top_u_pixel_time_quad_sums, top_v_pixel_time_quad_sums, top_y_pixel_time_quad_sums] = barnes_pixel_clustering_2D_clustering.pixel_quadrature_sum(top_pixel_dict, 4)

    # Bottom Quadrature Sums
    [bottom_u_pixel_time_quad_sums, bottom_v_pixel_time_quad_sums, bottom_y_pixel_time_quad_sums] = barnes_pixel_clustering_2D_clustering.pixel_quadrature_sum(bottom_pixel_dict, 4)

    # Upstream Quadrature Sums
    [upstream_u_pixel_time_quad_sums, upstream_v_pixel_time_quad_sums] = barnes_pixel_clustering_2D_clustering.pixel_quadrature_sum(upstream_pixel_dict, 3)
    
    # Downstream Quadrature Sums                                                                                                                                        
    [downstream_u_pixel_time_quad_sums, downstream_v_pixel_time_quad_sums] = barnes_pixel_clustering_2D_clustering.pixel_quadrature_sum(downstream_pixel_dict, 3)


    
    # Use the 'center_list_finder' to find the centers of all of the lists of 'quad_sums', defining 5 to be a center far enough away
    # Top Quad Sums
    top_u_quad_sums_centers = barnes_pixel_clustering_2D_clustering.center_list_finder(top_u_pixel_time_quad_sums, 5)
    top_v_quad_sums_centers = barnes_pixel_clustering_2D_clustering.center_list_finder(top_v_pixel_time_quad_sums, 5)
    top_y_quad_sums_centers = barnes_pixel_clustering_2D_clustering.center_list_finder(top_y_pixel_time_quad_sums, 5)

    # Bottom Quad Sums
    bottom_u_quad_sums_centers = barnes_pixel_clustering_2D_clustering.center_list_finder(bottom_u_pixel_time_quad_sums, 5)
    bottom_v_quad_sums_centers = barnes_pixel_clustering_2D_clustering.center_list_finder(bottom_v_pixel_time_quad_sums, 5)
    bottom_y_quad_sums_centers = barnes_pixel_clustering_2D_clustering.center_list_finder(bottom_y_pixel_time_quad_sums, 5)

    # Upstream Quad Sums
    upstream_u_quad_sums_centers = barnes_pixel_clustering_2D_clustering.center_list_finder(upstream_u_pixel_time_quad_sums, 5)
    upstream_v_quad_sums_centers = barnes_pixel_clustering_2D_clustering.center_list_finder(upstream_v_pixel_time_quad_sums, 5)

    # Downstream Quad Sums
    downstream_u_quad_sums_centers = barnes_pixel_clustering_2D_clustering.center_list_finder(downstream_u_pixel_time_quad_sums, 5)
    downstream_v_quad_sums_centers = barnes_pixel_clustering_2D_clustering.center_list_finder(downstream_v_pixel_time_quad_sums, 5)

    

    # Assign each set of [time, pixel] coordinates according to which center their quadrature sum of time and pixel is closest to

    # Top U, V, Y Pixel Group Assignment
    top_u_TIME_AND_pixels_organized_by_center = barnes_pixel_clustering_2D_clustering.center_assignment_quadrature_func(top_u_TIME_AND_pixel_list_preclustering, top_u_pixel_time_quad_sums, top_u_quad_sums_centers)
    top_v_TIME_AND_pixels_organized_by_center = barnes_pixel_clustering_2D_clustering.center_assignment_quadrature_func(top_v_TIME_AND_pixel_list_preclustering, top_v_pixel_time_quad_sums, top_v_quad_sums_centers)
    top_y_TIME_AND_pixels_organized_by_center = barnes_pixel_clustering_2D_clustering.center_assignment_quadrature_func(top_y_TIME_AND_pixel_list_preclustering, top_y_pixel_time_quad_sums, top_y_quad_sums_centers)

   # Bottom U, V, Y Pixel Group Assignment
    bottom_u_TIME_AND_pixels_organized_by_center = barnes_pixel_clustering_2D_clustering.center_assignment_quadrature_func(bottom_u_TIME_AND_pixel_list_preclustering, bottom_u_pixel_time_quad_sums, bottom_u_quad_sums_centers)
    bottom_v_TIME_AND_pixels_organized_by_center = barnes_pixel_clustering_2D_clustering.center_assignment_quadrature_func(bottom_v_TIME_AND_pixel_list_preclustering, bottom_v_pixel_time_quad_sums, bottom_v_quad_sums_centers)
    bottom_y_TIME_AND_pixels_organized_by_center = barnes_pixel_clustering_2D_clustering.center_assignment_quadrature_func(bottom_y_TIME_AND_pixel_list_preclustering, bottom_y_pixel_time_quad_sums, bottom_y_quad_sums_centers)

    # Upstream U and V Pixel Group Assignment
    upstream_u_TIME_AND_pixels_organized_by_center = barnes_pixel_clustering_2D_clustering.center_assignment_quadrature_func(upstream_u_TIME_AND_pixel_list_preclustering, upstream_u_pixel_time_quad_sums, upstream_u_quad_sums_centers)
    upstream_v_TIME_AND_pixels_organized_by_center = barnes_pixel_clustering_2D_clustering.center_assignment_quadrature_func(upstream_v_TIME_AND_pixel_list_preclustering, upstream_v_pixel_time_quad_sums, upstream_v_quad_sums_centers)

    # Downstream U and V Pixel Group Assignment
    downstream_u_TIME_AND_pixels_organized_by_center = barnes_pixel_clustering_2D_clustering.center_assignment_quadrature_func(downstream_u_TIME_AND_pixel_list_preclustering, downstream_u_pixel_time_quad_sums, downstream_u_quad_sums_centers)
    downstream_v_TIME_AND_pixels_organized_by_center = barnes_pixel_clustering_2D_clustering.center_assignment_quadrature_func(downstream_v_TIME_AND_pixel_list_preclustering, downstream_v_pixel_time_quad_sums, downstream_v_quad_sums_centers)



    # Duplicate these lists so that I won't run into the issue of the two lists being at the same address in Python

    # Top Pixels Organized by Center Duplicated
    top_u_TIME_AND_pixels_organized_by_center_DUPLICATE        = top_u_TIME_AND_pixels_organized_by_center[:][:]
    top_v_TIME_AND_pixels_organized_by_center_DUPLICATE        = top_v_TIME_AND_pixels_organized_by_center[:][:]
    top_y_TIME_AND_pixels_organized_by_center_DUPLICATE        = top_y_TIME_AND_pixels_organized_by_center[:][:]

    # Bottom Pixels Organized by Center Duplicate
    bottom_u_TIME_AND_pixels_organized_by_center_DUPLICATE     = bottom_u_TIME_AND_pixels_organized_by_center[:][:]
    bottom_v_TIME_AND_pixels_organized_by_center_DUPLICATE     = bottom_v_TIME_AND_pixels_organized_by_center[:][:]
    bottom_y_TIME_AND_pixels_organized_by_center_DUPLICATE     = bottom_y_TIME_AND_pixels_organized_by_center[:][:]

    # Upstream Pixels Organized by Center Duplicate
    upstream_u_TIME_AND_pixels_organized_by_center_DUPLICATE   = upstream_u_TIME_AND_pixels_organized_by_center[:][:]
    upstream_v_TIME_AND_pixels_organized_by_center_DUPLICATE   = upstream_v_TIME_AND_pixels_organized_by_center[:][:]
    
    # Downstream Pixels Organized by Center Duplicate
    downstream_u_TIME_AND_pixels_organized_by_center_DUPLICATE = downstream_u_TIME_AND_pixels_organized_by_center[:][:]
    downstream_v_TIME_AND_pixels_organized_by_center_DUPLICATE = downstream_v_TIME_AND_pixels_organized_by_center[:][:]


    # Look at the input lists that the function is taking in
    # Top
    print "The top u time and pixels organized by center are: ", top_u_TIME_AND_pixels_organized_by_center_DUPLICATE, "."
    print "\n"
    print "The top v time and pixels organized by center are: ", top_v_TIME_AND_pixels_organized_by_center_DUPLICATE, "."
    print "\n"
    print "The top y time and pixels organized by center are: ", top_y_TIME_AND_pixels_organized_by_center_DUPLICATE, "."
    print "\n"

    # Bottom
    # This is the printout statement of the entire list..
    print "The bottom u time and pixels organized by center are: ", bottom_u_TIME_AND_pixels_organized_by_center_DUPLICATE, "."
    print "\n"
    print "The bottom v time and pixels organized by center are: ", bottom_v_TIME_AND_pixels_organized_by_center_DUPLICATE, "."
    print "\n"
    print "The bottom y time and pixels organized by center are: ", bottom_y_TIME_AND_pixels_organized_by_center_DUPLICATE, "."
    print "\n"

    # print "The Rows of the Organized Bottom Y Pixels (before their center is calculated) is: " 
    # print "\n"

    # output_matrix_iterator = 0

    # Print out each row of the bottom u pixels to have something that's readable
    # for row in bottom_y_TIME_AND_pixels_organized_by_center_DUPLICATE:

        # print "Row #", output_matrix_iterator, ": ", row
        # output_matrix_iterator += 1
        # print "\n"

    # Declare a boolean to see if you should print out the rest of this section
    print_out = True

    if print_out == True:
    
        # Upstream 
        print "The upstream u time and pixels organized by center are: ", upstream_u_TIME_AND_pixels_organized_by_center_DUPLICATE, "."
        print "\n"
        print "The upstream v time and pixels organized by center are: ", upstream_v_TIME_AND_pixels_organized_by_center_DUPLICATE, "."
        print "\n"

        # Downstream
        print "The downstream u time and pixels organized by center are: ", downstream_u_TIME_AND_pixels_organized_by_center_DUPLICATE, "."
        print "\n"
        print "The downstream v time and pixels organized by center are: ", downstream_v_TIME_AND_pixels_organized_by_center_DUPLICATE, "."
        print "\n"

    
        # Use the 'center_average_calculator' function from 'barnes_pixel_clustering_2D_clustering' to calculate the average of the time and plane pixels in each list in the '..TIME_AND_pixels_organized_by_center' 
    
        # Top Pixel Combos
        top_u_clustered_time_pixel_combos        = barnes_pixel_clustering_2D_clustering.center_average_calculator(top_u_TIME_AND_pixels_organized_by_center_DUPLICATE, uplane_imgnd)
        top_v_clustered_time_pixel_combos        = barnes_pixel_clustering_2D_clustering.center_average_calculator(top_v_TIME_AND_pixels_organized_by_center_DUPLICATE, vplane_imgnd)
        top_y_clustered_time_pixel_combos        = barnes_pixel_clustering_2D_clustering.center_average_calculator(top_y_TIME_AND_pixels_organized_by_center_DUPLICATE, yplane_imgnd)

        # Bottom Pixel Combos
        bottom_u_clustered_time_pixel_combos     = barnes_pixel_clustering_2D_clustering.center_average_calculator(bottom_u_TIME_AND_pixels_organized_by_center_DUPLICATE, uplane_imgnd)
        bottom_v_clustered_time_pixel_combos     = barnes_pixel_clustering_2D_clustering.center_average_calculator(bottom_v_TIME_AND_pixels_organized_by_center_DUPLICATE, vplane_imgnd)
        bottom_y_clustered_time_pixel_combos     = barnes_pixel_clustering_2D_clustering.center_average_calculator(bottom_y_TIME_AND_pixels_organized_by_center_DUPLICATE, yplane_imgnd)

        # Upstream Pixel Combos
        upstream_u_clustered_time_pixel_combos   = barnes_pixel_clustering_2D_clustering.center_average_calculator(upstream_u_TIME_AND_pixels_organized_by_center_DUPLICATE, uplane_imgnd)
        upstream_v_clustered_time_pixel_combos   = barnes_pixel_clustering_2D_clustering.center_average_calculator(upstream_v_TIME_AND_pixels_organized_by_center_DUPLICATE, vplane_imgnd)

        # Downstream Pixel Combos
        downstream_u_clustered_time_pixel_combos = barnes_pixel_clustering_2D_clustering.center_average_calculator(downstream_u_TIME_AND_pixels_organized_by_center_DUPLICATE, uplane_imgnd)
        downstream_v_clustered_time_pixel_combos = barnes_pixel_clustering_2D_clustering.center_average_calculator(downstream_v_TIME_AND_pixels_organized_by_center_DUPLICATE, vplane_imgnd)




        # Print out this information along with the list of pixels and the list of centers (as a test of some of the other information)
        # Bottom Y  Pixels (Previously Top U Pixels)
        # print "The list of unclustered bottom Y pixels with their time pixel is: ", bottom_y_TIME_AND_pixel_list_preclustering, "."
        # print "\n"
        
        # print "The list of bottom Y quadrature sums is: ", bottom_y_pixel_time_quad_sums, "."
        # print "\n"

        # print "The list of centers of the bottom Y quadrature sums is: ", bottom_y_quad_sums_centers, "."
        # print "\n"

        # print "The list of bottom Y pixels with their time pixel organized by quadrature sum is: ", bottom_y_TIME_AND_pixels_organized_by_center, "."
        # print "\n

        # print "The list of Bottom Y pixels with their time pixel AVERAGED in both pixel dimensions after organization is: ", bottom_y_clustered_time_pixel_combos, "."
        # print "\n"


        # Upstream U Pixels (Previously Upstream V Pixels)                                                                                                                          
        # print "The list of these unclustered upstream U pixels with their time pixel is: ", upstream_u_TIME_AND_pixel_list_preclustering, "."
        # print "\n"

        # print "The list of upstream U quadrature sums is: ", upstream_u_pixel_time_quad_sums, "."
        # print "\n"

        # print "The list of centers of the upstream U quadrature sums is: ", upstream_u_quad_sums_centers, "."
        # print "\n"
        
        # print "The list of upstream U pixels with their time pixel organized by quadrature sum is: ", upstream_u_TIME_AND_pixels_organized_by_center, "."
        # print "\n"

        # print "The list of upstream U  pixels with their time pixel AVERAGED in both pixel dimensions after organization is: ", upstream_u_clustered_time_pixel_combos, "."
        # print "\n"


        
        # I'm printing out the different types of organized pixels here

        # Top Organized Pixels
        print "The list of Top U pixels with their time pixel AVERAGED in both pixel dimensions after organization is: ", top_u_clustered_time_pixel_combos, "."
        print "\n"

        print "The list of Top V pixels with their time pixel AVERAGED in both pixel dimensions after organization is: ", top_v_clustered_time_pixel_combos, "."
        print "\n"
        
        print "The list of Top Y pixels with their time pixel AVERAGED in both pixel dimensions after organization is: ", top_y_clustered_time_pixel_combos, "."
        print "\n"


        # Bottom Organized Pixels

        print "The list of Bottom U pixels with their time pixel AVERAGED in both pixel dimensions after organization is: ", bottom_u_clustered_time_pixel_combos, "."
        print "\n"

        print "The list of Bottom V pixels with their time pixel AVERAGED in both pixel dimensions after organization is: ", bottom_v_clustered_time_pixel_combos, "."
        print "\n"
    
        print "The list of Bottom Y pixels with their time pixel AVERAGED in both pixel dimensions after organization is: ", bottom_y_clustered_time_pixel_combos, "."
        print "\n"


        # Upstream Organized Pixels

        print "The list of Upstream U pixels with their time pixel AVERAGED in both pixel dimensions after organization is: ", upstream_u_clustered_time_pixel_combos, "."
        print "\n"

        print "The list of Upstream V pixels with their time pixel AVERAGED in both pixel dimensions after organization is: ", upstream_v_clustered_time_pixel_combos, "."
        print "\n"

    
        # Downstream Organized Pixels

        print "The list of Downstream U pixels with their time pixel AVERAGED in both pixel dimensions after organization is: ", downstream_u_clustered_time_pixel_combos, "."
        print "\n"

        print "The list of Downstream V pixels with their time pixel AVERAGED in both pixel dimensions after organization is: ", downstream_v_clustered_time_pixel_combos, "."
        print "\n"


        # Organize the hits into lists of three matched pixels at a time (for top and bottom hits) and lists of two matched pixels at a time (for upstream and downstream hits)
        top_pixel_matched_plane_hits      = multiple_plane_hits_enforcement_grouping.new_pixel_organization(5, 3, 10, top_u_clustered_time_pixel_combos, top_v_clustered_time_pixel_combos, top_y_clustered_time_pixel_combos)
        bottom_pixel_matched_plane_hits   = multiple_plane_hits_enforcement_grouping.new_pixel_organization(5, 3, 10, bottom_u_clustered_time_pixel_combos, bottom_v_clustered_time_pixel_combos, bottom_y_clustered_time_pixel_combos) 
        upstream_pixel_matched_plane_hits = multiple_plane_hits_enforcement_grouping.new_pixel_organization(5, 3, 10, upstream_u_clustered_time_pixel_combos, upstream_v_clustered_time_pixel_combos, None)
        downstream_pixel_matched_plane_hits = multiple_plane_hits_enforcement_grouping.new_pixel_organization(5, 3, 10, downstream_u_clustered_time_pixel_combos, downstream_v_clustered_time_pixel_combos, None)    

        # Print out the organized pixel hits for the event after the above functions
        print "The top pixels matched across the three planes are: ", top_pixel_matched_plane_hits
        print "\n"

        print "The bottom pixels matched across the three planes are: ", bottom_pixel_matched_plane_hits
        print "\n"

        print "The upstream pixels matched across the first two planes planes are: ", upstream_pixel_matched_plane_hits
        print "\n"

        print "The downstream pixels matched across the three planes are: ", downstream_pixel_matched_plane_hits
        print "\n"

        # Use the new function to calculate the pixel combinations with the highest score
        top_pixel_matches_highest_scores        = adjacent_pixels_color_scoring.adjacent_pixels_color_scoring_algo(top_pixel_matched_plane_hits, uplane_imgnd, vplane_imgnd, yplane_imgnd, 0)
        bottom_pixel_matches_highest_scores     = adjacent_pixels_color_scoring.adjacent_pixels_color_scoring_algo(bottom_pixel_matched_plane_hits, uplane_imgnd, vplane_imgnd, yplane_imgnd, 1) 
        upstream_pixel_matches_highest_scores   = adjacent_pixels_color_scoring.adjacent_pixels_color_scoring_algo(upstream_pixel_matched_plane_hits, uplane_imgnd, vplane_imgnd, yplane_imgnd, 2) 
        downstream_pixel_matches_highest_scores = adjacent_pixels_color_scoring.adjacent_pixels_color_scoring_algo(downstream_pixel_matched_plane_hits, uplane_imgnd, vplane_imgnd, yplane_imgnd, 3)
    
        # Print out the list of the pixels with the highest scores
        print "Top Pixels with the highest ADC scores: ", top_pixel_matches_highest_scores, "."
        print "\n"

        print "Bottom Pixels with the highest ADC scores: ", bottom_pixel_matches_highest_scores, "."
        print "\n"

        print "Upstream Pixels with the highest ADC scores: ", upstream_pixel_matches_highest_scores, "."
        print "\n"

        print "Downstream Pixels with the highest ADC scores: ", downstream_pixel_matches_highest_scores, "."
        print "\n"

        # First, set them equal to lists of the same values to avoid identical address issues
        starting_uplane_array = uplane_imgnd[:][:]
        starting_vplane_array = vplane_imgnd[:][:]
        starting_yplane_array = yplane_imgnd[:][:]

        # Now, use the 'pixel_color_adding_algo' to add color to the form of the old color plane arrays (NOT the old color plane arrays themselves exactly)
        [uplane_array_filled, vplane_array_filled, yplane_array_filled] = pixel_color_adding_algo.pixel_color_adding_algo(top_pixel_matches_highest_scores, bottom_pixel_matches_highest_scores, upstream_pixel_matches_highest_scores, downstream_pixel_matches_highest_scores, starting_uplane_array, starting_vplane_array, starting_yplane_array)

        # Load the final (!!) uplane arrays into the 'new_plane_array's, as I'll call them
        new_uplane_array = uplane_array_filled[:][:]
        new_vplane_array = vplane_array_filled[:][:]
        new_yplane_array = yplane_array_filled[:][:]

        # Go forth with filling the output image
        # Here the arrays for the individual planes are again set equal to the respective vectors in the outimg[,,] array                
        outimg[:,:,0] = 128*new_uplane_array[:, :]
        outimg[:,:,1] = 128*new_vplane_array[:, :]
        outimg[:,:,2] = 128*new_yplane_array[:, :]

        # Provide names for the basic coloring and for the clustering algorithms
        outname = 'normalthresholds_clustered_pixel_scoring_lonesome_dot_removal_with_better_center_assignment_tidier_less_stringent_081826_%d.png' % entry

        # Display the images
        if not hascv:
            mat_display=plt.show( outimg )
            mat_display.write(outname)
        else:
            # note opencv uses BGR format                                                                                        
            # so B=U plane, G=V plane, R=Y plane                                                                                                                                    
            cv2.imwrite( outname, outimg )





    








