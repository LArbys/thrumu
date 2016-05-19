import sys
from larcv import larcv
import numpy as np
try:
    # my preference is to use opencv to output the image
    # but we default to matplotlib if opencv 3 not available
    import cv2
    hascv = True
except:
    import matplotlib.pyplot as plt
    hascv = False

# input file
inputfile = sys.argv[1]

# Producer name
# Data in the ROOT files are stored in trees with the name pattern
#  (Data Type)_(Producer Name)_tree
# data type can be (but are not limited to):
#  image2d: the event images
#  partroi: meta data that tells us the type of image and for MC, the particles in the image and where they are located
IMAGE_PRODUCER="tpc"

# IOmanager
# Handles the ROOT file interface for us. Sets up branches
ioman = larcv.IOManager(larcv.IOManager.kREAD, "IO") # instantiate instance (in read mode)
ioman.add_in_file( inputfile ) # append file to manager
ioman.initialize() # setup the trees

# Event Loop
nentries = ioman.get_n_entries()
nentries = 5 # override, only dump 5
for entry in xrange(nentries):
    # Get an entry by index
    ioman.read_entry( entry )

    # Get a container with the event images
    # this command tells the iomanager to get a tree whose contents contain Image2D and whose
    #  "producer" label is IMAGE_PRODUCER
    # again, finds the tree with name: image2d_(IMAGE_PRODUCER)_tree
    event_images = ioman.get_data( larcv.kProductImage2D, IMAGE_PRODUCER )

    # get image vector (the image2d instances are stored in a std vector
    img_v = event_images.Image2DArray()

    # get the height (rows) and width (cols) of our image, using the first one in the vector
    # by convention our images are all the same size. mostly a restriction due to caffe.
    # notice how image meta data is stored in an ImageMeta class that we retrieve by the meta() method
    rows = img_v.front().meta().rows()
    cols = img_v.front().meta().cols()

    # We are going to output an BGR image, make the container for it
    outimg = np.zeros( (rows,cols,3) )
    
    # loop over the images in the array and put them into the numpy array
    for img in img_v:
        imgnd = larcv.as_ndarray(img) # we convert the Image2D data into a numpy array
        imgnd = np.transpose( imgnd, (1,0) ) # image2d and numpy conventions on row and cols are not the same...
        imgnd = imgnd[::-1,:] # my preference is to have time go from top to bottom, Image2D assumes otherwise, so I reverse the y-axis here (which are the rows)
        # we use the [0,255] BGR color scale. I'm not being careful about normalizing values. But I know that I want MIP tracks to be around 128.
        # the MIP peak was calibrated to be around 1.0 when we made this data.
        outimg[:,:,img.meta().plane()] = imgnd*128

    outname = 'entry_%d.png' % (entry)

    if not hascv:
        mat_display=plt.imshow( outimg )
        mat_display.write_png(outname)
    else:
        # note opencv uses BGR format
        # so B=U plane, G=V plane, R=Y plane
        cv2.imwrite( outname, outimg )


