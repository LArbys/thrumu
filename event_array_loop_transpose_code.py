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

# Only loop through ten of the entries for now
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

    # print uplane_imgnd[0]
    
    # if entry == 1:

    # print vplane_imgnd
    # print yplane_imgnd[0]

    # print "The dimension of the U plane matrix is ", uplane_imgnd.shape, "."
    # print "The dimension of the V plane matrix is ", vplane_imgnd.shape, "."
    # print "The dimension of the Y plane matrix is ", yplane_imgnd.shape, "."
    
    # Used in place of the 'for img in img_v' loop below
    # uplane_img   = img_v.at(0)
    # vplane_img   = img_v.at(4)
    # yplane_img   = img_v.at(8)

    # Converting each image into an ND array 
    # uplane_imgnd = larcv.as_ndarray(uplane_img)
    # vplane_imgnd = larcv.as_ndarray(vplane_img)
    # yplane_imgnd = larcv.as_ndarray(yplane_img)  

    # Loop through each of the arrays to find matches for the affected wires in each pixel 

    # Declare the ADC threshold for considering a signal in one of the pixels at a specific time
    threshold = 1

    # Define different thresholds for each of the three planes in the TPC (the values between each plane are quite different)
    # uplane_threshold = 56
    # vplane_threshold = 224
    # yplane_threshold = 560

    # Declare a variable for the smallest and largest wire indices that could have been excited
    wire_smallest = 0
    wire_largest  = 0

    # Declare variables for the pixels corresponding to the wires that were found by wire_matching_algo

    plane_one_pixel = 0
    plane_two_pixel = 0

    # The range of the new file is (756, 864)
    for i in range (0, 756): # This loops through each row, or time, for which data is being collected in a 'for' loop

        for j in range (0, 864): # This loops through each column, or pixel, for which that data is being collected in a 'for' loop

            if uplane_imgnd[i][j] >= threshold:

                # Reset the charge and total score variables to zero
                uplane_charge = 0
                vplane_charge = 0
                yplane_charge = 0
                total_score   = 0

                uplane_charge = uplane_imgnd[i][j]

                # Find the wires that correspond to the pixel in uplane that has been excited 
                
                # The Pixel does not correspond to any wire if it's greater than 479 so that should
                # automatically correspond to 0
                if j > 599: 

                    continue

                # Otherwise, find the smallest and greatest values that the wire could take to use them in the following loop

                wire_smallest = 5*j
                wire_greatest = 5*j + 4

                # There are no matches for wires less than 672, meaning that this cannot correspond to a hit on each of the three planes
                if wire_smallest < 672:

                    continue

                if wire_greatest > 2399:

                    continue

                # Check the matches for this wire and see if they carry charge
                # as well
                for k in range (wire_smallest, wire_greatest):

                    (plane_one_match, plane_two_match) = wire_matches_extra_tolerances.wire_assign_func(k)

                    plane_one_pixel = (plane_one_match - (plane_one_match % 5))/5

                    # Set plane_two_pixel = -1 at first, and change it to its real value if plane_two_match != -1
                    plane_two_pixel = plane_two_match

                    # Only convert the matching wire to a pixel if the plane two wire is not the default value
                    if plane_two_match != -1:

                        plane_two_pixel = (plane_two_match - (plane_two_match % 5))/5

                    # Check to make sure that the pixel on the first (second) plane is within range:
                    if plane_one_pixel > 599:

                        continue

                    # Check to make sure that the pixel on the second (third) plane is within range. The default value of -1 passes this test 
                    if plane_two_pixel > 863:

                        continue

                    if vplane_imgnd[i][plane_one_pixel] >= threshold:

                        vplane_charge = vplane_imgnd[i][plane_one_pixel]

                    if plane_two_pixel != -1:

                        if yplane_imgnd[i][plane_two_pixel] >= threshold:

                            yplane_charge = yplane_imgnd[i][plane_two_pixel]

                    # If the yplane pixel is just -1, then the variable yplane_charge is already set to 0 so you don't have to change it

                    # Fill in the total score variable now

                    total_score = uplane_charge + vplane_charge + yplane_charge

                    # If vplane_charge is greater than zero, then there must be hits at least on the first two planes
                    if vplane_charge > 0: 

                        if plane_two_pixel == -1:

                            for pixel in [j, plane_one_pixel]:
                        
                                uplane_imgnd[i][pixel] = uplane_imgnd[i][pixel] + total_score
                                vplane_imgnd[i][pixel] = vplane_imgnd[i][pixel] + total_score

                            # Use the break statement to limit the clustering of bright pixels from more than one set of matched wires close together
                            # break
                        
                        else: 

                            for pixel in [j, plane_one_pixel, plane_two_pixel]:

                                uplane_imgnd[i][pixel] = uplane_imgnd[i][pixel] + total_score
                                vplane_imgnd[i][pixel] = vplane_imgnd[i][pixel] + total_score
                                yplane_imgnd[i][pixel] = yplane_imgnd[i][pixel] + total_score

                            # Same as above
                            # break

                        # None of these print statements will print when the loop breaks
                        # Only print these if you find some total charge on at least two of the three planes (greater than the threshold)
                        print "Total Charge Score = ", total_score
                        print "U Plane Wire: ", k, "U Plane Charge: ", uplane_charge 
                        print "V Plane Wire: ", plane_one_match, "V Plane Charge: ", vplane_charge

                        # Only fill the yplane if the pixel does not correspond to the default value
                        if plane_two_pixel != -1:
                            print "Y Plane Wire: ", plane_two_match, "Y Plane Charge: ", yplane_charge
                        
                        print "\n"

    # Here the arrays for the individual planes are again set equal to the respective vectors in the outimg[,,] array
    outimg[:,:,0] = uplane_imgnd
    outimg[:,:,1] = vplane_imgnd
    outimg[:,:,2] = yplane_imgnd

    outname = 'threshold1ccqe_%d.png' % (entry)

    if not hascv:
        mat_display=plt.imshow( outimg )
        mat_display.write_png(outname)
    else:
        # note opencv uses BGR format                                                                                                                                               
        # so B=U plane, G=V plane, R=Y plane                                                                                                        
        cv2.imwrite( outname, outimg )

    








