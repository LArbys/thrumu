import sys
from larcv import larcv
import numpy as np

# Import the file that will contain the algorithm for matching the wire with other wires that //
# are at the same y and z coordinates
import wire_matches_extra_tolerances

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

# Limit the number of entries for the time being
nentries = 5

# Define variables for the threshold of each plane (I'll see if this location makes a difference)                                                          
uplane_threshold = 100
vplane_threshold = 100
yplane_threshold = 100

for entry in xrange(nentries):
    # Get an entry by index
    ioman.read_entry( entry )

    # Declare vectors that will contain the pixel numbers of the hits that are above threshold
    uplane_pixel_array = []
    vplane_pixel_array = []
    yplane_pixel_array = []

    # Declare a vector for the score of the three pixels corresponding to the same spot in the arrays as those pixels
    score_array        = []

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
        outimg[:,:,img.meta().plane()] = imgnd*128

    # This inverts what I'll do below in order to operate on each of the images.  I'll set each of the outimg third components equal to the imgnds at the end                        
    # when the image is to be displayed                                                                                                                                              
    uplane_imgnd  = outimg[:,:,0]
    vplane_imgnd  = outimg[:,:,1]
    yplane_imgnd  = outimg[:,:,2]
    
    # Define the uplane, vplane, and yplane images according to their locations in the img_v image folder
    # uplane_img = img_v.at(0)
    # vplane_img = img_v.at(4)
    # yplane_img = img_v.at(8)
    
    # Converting each image into an ND array 
    # uplane_imgnd = larcv.as_ndarray(uplane_img)
    # vplane_imgnd = larcv.as_ndarray(vplane_img)
    # yplane_imgnd = larcv.as_ndarray(yplane_img)  

    for i in range (0, 756):

        # You have to append the first index, the time, onto each of the pixel arrays and the score array
        score_array.append([])
        uplane_pixel_array.append([])
        vplane_pixel_array.append([])
        yplane_pixel_array.append([])

        for j in range (0, 864):

            if uplane_imgnd[i][j] >= uplane_threshold:

                # Reset the charge and total score variables to zero            
                uplane_charge = 0

                uplane_charge = uplane_imgnd[i][j]

                # The Pixel does not correspond to any wire if it's greater than 479 so that should                                                                                 
                # automatically correspond to 0                                                                                                                                  
                if j > 599:

                    continue

                # Otherwise, find the smallest and greatest values that the wire could take to use them in the following loop                                                       

                wire_smallest = 5*j
                wire_greatest = 5*j + 4

                # The only matches for the wire are found between wire_smallest and wire_greatest, so the interpreter will issue a key error if the wire
                # is outside of this range
                if wire_smallest < 672:

                    continue

                # Include this condition so that the KeyError: 2405 doesn't arise again
                if wire_greatest > 2399:

                    continue

                # Check the matches for this wire and see if they carry charge as well. This does not include the upper bound, the 'wire_greatest' value.
                for k in range (wire_smallest, wire_greatest):
                    
                    # You HAVE to reset the vplane_charge to zero each time you reenter this loop
                    vplane_charge = 0
                    yplane_charge = 0

                    # Reset the total score to 0 as well
                    total_score   = 0 

                    (plane_one_match, plane_two_match) = wire_matches_extra_tolerances.wire_assign_func(k)

                    plane_one_pixel = (plane_one_match - (plane_one_match % 5))/5

                    # Set plane_two_pixel = -1 at first, and change it to its real value if plane_two_match != -1          
                    plane_two_pixel = plane_two_match

                    # Only convert the matching wire to a pixel if the plane two wire is not the default value                                           
                    if plane_two_match != -1:
                        
                        plane_two_pixel = (plane_two_match - (plane_two_match % 5))/5

                    # Check to make sure that the pixel on the first (second) plane is within range (doesn't have a greater wire number than is possible):                      
                    if plane_one_pixel > 599:

                        continue

                    # Check to make sure that the pixel on the second (third) plane is within range. The default value of -1 passes this test            
                    if plane_two_pixel > 863:

                        continue

                    # Nesting these 'if' statements means that if you only get to the second (third) plane 'if' statement if you've gone through the first
                    if vplane_imgnd[i][plane_one_pixel] >= vplane_threshold:

                        vplane_charge = vplane_imgnd[i][plane_one_pixel]

                        if plane_two_pixel != -1 and yplane_imgnd[i][plane_two_pixel] >= yplane_threshold:

                            yplane_charge = yplane_imgnd[i][plane_two_pixel]

                    # This considers the case when the uplane pixel is above threshold, but none of the matching wires have a value above threshold 
                    else:

                        score_array[i].append(0)
                        uplane_pixel_array[i].append(0)
                        vplane_pixel_array[i].append(0)
                        yplane_pixel_array[i].append(0)

                    # If the yplane pixel is just -1, then the variable yplane_charge is already set to 0 so you don't have to change it           
                    # The vplane value is also set to 0 if its ADC reading was not above threshold

                    # Fill in the total score variable now                                                                                                                          
                    total_score = uplane_charge + vplane_charge + yplane_charge

                    # If vplane_charge is greater than zero, then there must be hits at least on the first two planes                                                               
                    # The time index is included in the first index ('i') of each of these variables
                    if vplane_charge > 0:
    
                            score_array[i].append(total_score)
                            uplane_pixel_array[i].append(j)
                            vplane_pixel_array[i].append(plane_one_pixel)
                            yplane_pixel_array[i].append(plane_two_pixel)
                            

                            # None of these print statements will print when the loop breaks                                                                                       
                            # Only print these if you find some total charge on the three planes together (greater than the threshold)                                              
                            print "Total Charge Score = ", total_score
                            print "U Plane Wire: ", k, "U Plane Charge: ", uplane_charge
                            print "V Plane Wire: ", plane_one_match, "V Plane Charge: ", vplane_charge

                            # Only fill the yplane if the pixel does not correspond to the default value                                                                           
                            if plane_two_pixel != -1:

                                print "Y Plane Wire: ", plane_two_match, "Y Plane Charge: ", yplane_charge

                            print "\n"

            # Include a condition for when the uplane_imgnd entry is not greater than uplane_threshold
            else:

                score_array[i].append(0)
                uplane_pixel_array[i].append(0)
                vplane_pixel_array[i].append(0)
                yplane_pixel_array[i].append(0)

    # Find which entries in the arrays are nonzero
    # Also declare a list to find out which time (i value) each of the nonzero score readings correspond to
    uplane_nonzero_elements = []
    vplane_nonzero_elements = []
    yplane_nonzero_elements = []
    score_nonzero_elements  = []
    time_index              = []

    # Loop over each of the entries in the pixel arrays to see which corresponds to a nonzero score
    # I can then dump all of the nonzero entries for each category into a one-dimensional array
    # This method will work because the arrays were all filled at the same time

    # print "The dimension of the score array is: ", len(score_array)

    for outer_index in range(len(score_array)):

        for inner_index in range(len(score_array[outer_index])):

            if score_array[outer_index][inner_index] > 0:

                uplane_nonzero_elements.append(uplane_pixel_array[outer_index][inner_index])
                vplane_nonzero_elements.append(vplane_pixel_array[outer_index][inner_index])
                yplane_nonzero_elements.append(yplane_pixel_array[outer_index][inner_index])
                score_nonzero_elements.append(score_array[outer_index][inner_index])
                time_index.append(outer_index)

    # Now, loop over the elements of these 1D arrays to find out which scores are the greatest for which wires

    # Declare variables for the greatest score for each of the planes
    uplane_greatest_score = 0
    vplane_greatest_score = 0
    yplane_greatest_score = 0

    # Declare variables for the greatest values of the score for each plane at each of the indices
    uplane_greatest_position_index = 0
    vplane_greatest_position_index = 0
    yplane_greatest_position_index = 0

    # Declare variables for the time index for each of the elements of the u,v,y planes corresponding to the greatest scores
    uplane_greatest_time_index = 0
    vplane_greatest_time_index = 0
    yplane_greatest_time_index = 0

    # print "Nonzero Score Length:", len(score_nonzero_elements)
    
    for index in range(len(score_nonzero_elements)):

        # print score_nonzero_elements[index]

        if score_nonzero_elements[index] > uplane_greatest_score:

            # print "New greatest score for the uplane!" 

            uplane_greatest_score           = score_nonzero_elements[index]
            uplane_greatest_position_index  = uplane_nonzero_elements[index]
            uplane_greatest_time_index      = time_index[index]

        if score_nonzero_elements[index] > vplane_greatest_score:

            # print "New greatest score for the vplane!"

            vplane_greatest_score          = score_nonzero_elements[index]
            vplane_greatest_position_index = vplane_nonzero_elements[index]
            vplane_greatest_time_index     = time_index[index]

        # Include an extra condition to ensure that the value of the array here is not equal to -1
        if score_nonzero_elements[index] > yplane_greatest_score and yplane_nonzero_elements[index] != -1:

            # print "New greatest score for the yplane!"

            yplane_greatest_score           = score_nonzero_elements[index]
            yplane_greatest_position_index  = yplane_nonzero_elements[index]
            yplane_greatest_time_index      = time_index[index]            
        
    # Now, fill up each of the pixels that correspond to the greatest score for each of the planes:

    # Print out the greatest time index and greatest position index for each event
    print "uplane greatest time index:", uplane_greatest_time_index
    print "uplane greatest position index:", uplane_greatest_position_index
    print "uplane greatest score:", uplane_greatest_score
    
    print "\n"

    print "vplane greatest time index:", vplane_greatest_time_index
    print "vplane greatest position index:", vplane_greatest_position_index
    print "vplane greatest score:", vplane_greatest_score

    print "\n"

    print "yplane greatest time index:", yplane_greatest_time_index
    print "yplane greatest position index:", yplane_greatest_position_index
    print "yplane greatest score:", yplane_greatest_score

    print "\n"
            
    uplane_imgnd[uplane_greatest_time_index][uplane_greatest_position_index] += 1000
    vplane_imgnd[uplane_greatest_time_index][uplane_greatest_position_index] += 1000
    yplane_imgnd[uplane_greatest_time_index][uplane_greatest_position_index] += 1000

    uplane_imgnd[vplane_greatest_time_index][vplane_greatest_position_index] += 1000
    vplane_imgnd[vplane_greatest_time_index][vplane_greatest_position_index] += 1000
    yplane_imgnd[vplane_greatest_time_index][vplane_greatest_position_index] += 1000
    
    uplane_imgnd[yplane_greatest_time_index][yplane_greatest_position_index] += 1000
    vplane_imgnd[yplane_greatest_time_index][yplane_greatest_position_index] += 1000
    yplane_imgnd[yplane_greatest_time_index][yplane_greatest_position_index] += 1000
            
    # Save the images from the planes to an outgoing image
    outimg[:,:,0] = uplane_imgnd
    outimg[:,:,1] = vplane_imgnd
    outimg[:,:,2] = yplane_imgnd

    outname = 'U100V100Y100_NewFile%d.png' % (entry)

    if not hascv:
        mat_display=plt.imshow( outimg )
        mat_display.write_png(outname)
    else:

        cv2.imwrite( outname, outimg )

    








