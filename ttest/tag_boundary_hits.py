import sys
from larcv import larcv
import numpy as np
try:
    # my preference is to use opencv to output the image
    # but we default to matplotlib if opencv 3 not available
    import cv2
    hascv = True
    print "HAS CV"
except:
    import matplotlib.pyplot as plt
    hascv = False
    print "NO CV"

from load_match_list import load_match_list


# input file
inputfile = sys.argv[1]

# Producer name
# Data in the ROOT files are stored in trees with the name pattern
#  (Data Type)_(Producer Name)_tree
# data type can be (but are not limited to):
#  image2d: the event images
#  partroi: meta data that tells us the type of image and for MC, the particles in the image and where they are located
#IMAGE_PRODUCER="tpc_12ch_mean"
IMAGE_PRODUCER="tpc"

# match tensor
match_types = load_match_list( 864 )
match_colors = { "top_matches":(255,255,102),  # cyan
                 "bottom_matches":(255,102,255), # magent
                 "upstream_matches":(102,255,255), # yellow
                 "downstream_matches":(255,255,255) } # white
matchtypelist = match_colors.keys()
matchtypelist.sort()

plane_scalefactor = [ 175.0, 110.0, 185.0 ] # DATA
# NEED MC VALUES

# Neighborhood size: 
N = 5

# Set MIP Scale for RGB Value
IMGSCALE = 75.0

# Threshold values
uthresh = 0.4*IMGSCALE
vthresh = 0.4*IMGSCALE
ythresh = 0.4*IMGSCALE

# IOmanager
# Handles the ROOT file interface for us. Sets up branches
ioman = larcv.IOManager(larcv.IOManager.kREAD, "IO") # instantiate instance (in read mode)
ioman.add_in_file( inputfile ) # append file to manager
ioman.initialize() # setup the trees

# Event Loop
nentries = ioman.get_n_entries()
nentries = 1 # override, only dump 5
start_entry = 29

# START
for entry in xrange(start_entry,start_entry+nentries):
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
    print "ROWS,COLS: ",(rows,cols)

    # We are going to output an BGR image, make the container for it
    origimg = np.zeros( (rows,cols,3) )  # original image
    hitimg  = np.zeros( (4,rows,cols,3) )  # places marked by hits, 4 boundary types
    hitimg2 = np.zeros( (4,rows,cols,3) )  # places marked by hits, 4 boundary types, for display
    
    # loop over the images in the array and put them into the numpy array
    #for ch in [0,4,8]:
    for ch in [0,1,2]:
        img = img_v.at(ch)
        imgnd = larcv.as_ndarray(img) # we convert the Image2D data into a numpy array
        imgnd = np.transpose( imgnd, (1,0) ) # image2d and numpy conventions on row and cols are not the same...
        imgnd = imgnd[::-1,:] # my preference is to have time go from top to bottom, Image2D assumes otherwise, so I reverse the y-axis here (which are the rows)
        # we use the [0,255] BGR color scale. I'm not being careful about normalizing values. But I know that I want MIP tracks to be around 128.
        # the MIP peak was calibrated to be around 1.0 when we made this data.
        origimg[:,:,img.meta().plane()] = imgnd/plane_scalefactor[img.meta().plane()]*IMGSCALE
        print imgnd.shape


    for imatch,matchtype in enumerate(matchtypelist):
        print "Finding ",matchtype
        #if matchtype not in ["bottom_matches"]:
        #    continue

        for row in range(0, rows ): # Loop over rows (or time)
            print "  row ",row," of ",rows,"(",matchtype,")"
            for match in match_types[matchtype]:
                # we are provided with a triple (u,v,y)
                # we look at the combinations of pixels in the neighboorhood of this point
                # we mark a hit for any pixel combination where all pixels have charge above some certain threshold
                # optimization: we could look at each combination of [u-N,u+N], [v-N,v+N], [y-N,y+N],
                #               however, finding all combinations of (u,v,y), which is (2N)^3, should be the same as 
                #               labeling all pixels in the neighbor hood with charge above threshold (3N)
                #print match

                # define neighborhood
                umin = np.minimum( np.maximum(match[0]-N,0), cols-(2*N+1) )
                umax = np.maximum( np.minimum(match[0]+N+1,cols), (2*N+1) )
                vmin = np.minimum( np.maximum(match[1]-N,0), cols-(2*N+1) )
                vmax = np.maximum( np.minimum(match[1]+N+1,cols), (2*N+1) )
                ymin = np.minimum( np.maximum(match[2]-N,0), cols-(2*N+1) )
                ymax = np.maximum( np.minimum(match[2]+N+1,cols), (2*N+1) )

                #print "u-range: ",umin,umax
                #print "v-range: ",vmin,vmax
                #print "y-range: ",ymin,ymax

                # make copy of slice
                uslice = np.copy( origimg[row,umin:umax,0] )
                vslice = np.copy( origimg[row,vmin:vmax,1] )
                yslice = np.copy( origimg[row,ymin:ymax,2] )
                #print uslice.shape,vslice.shape,yslice.shape

                # mark slice up based on threshold
                uslice[ uslice<uthresh ] = 0.0
                vslice[ vslice<vthresh ] = 0.0
                yslice[ yslice<ythresh ] = 0.0
                uslice[ uslice>uthresh ] = 1.0
                vslice[ vslice>vthresh ] = 1.0
                yslice[ yslice>ythresh ] = 1.0

                # we want the neighborhoods on all planes to have at least one hit
                if np.sum( uslice )==0.0 or np.sum(vslice)==0.0 or np.sum(yslice)==0.0:
                    continue

                # mark hit image (where charge was also seen)
                for ich in range(0,3):
                    hitimg2[imatch,row,umin:umax,ich] = uslice*match_colors[matchtype][ich]
                    hitimg2[imatch,row,vmin:vmax,ich] = vslice*match_colors[matchtype][ich]
                    hitimg2[imatch,row,ymin:ymax,ich] = yslice*match_colors[matchtype][ich]

                hitimg[imatch,row,umin:umax,0] = uslice*match_colors[matchtype][0]
                hitimg[imatch,row,vmin:vmax,1] = vslice*match_colors[matchtype][1]
                hitimg[imatch,row,ymin:ymax,2] = yslice*match_colors[matchtype][2]

                

    hitout = np.sum( hitimg2, axis=0 )
    imgout = np.copy(origimg)
    imgout[ hitout>0 ] = hitout[ hitout>0 ]
    print "Hit out: ",hitout.shape

    outname = 'entry%03d_width%d_u%0.2f_v%0.2f_y%0.2f.png' % (entry, N, uthresh/IMGSCALE, vthresh/IMGSCALE, ythresh/IMGSCALE)
    #hitout = np.transpose( hitout, (2,1,0) )

    if not hascv:
        mat_display=plt.imshow( out )
        mat_display.write_png(outname)
    else:
        print "Use OpenCV"
        # note opencv uses BGR format
        # so B=U plane, G=V plane, R=Y plane
        cv2.imwrite( outname, imgout )

    out_tag = open( "out_tag_stage.npz", 'w' )
    np.savez( out_tag, hitimage=hitimg, img=origimg )
    out_tag.close()


