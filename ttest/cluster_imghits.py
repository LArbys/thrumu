import os,sys
import numpy as np
import ROOT as rt
import cv2
import time

try:
   import cPickle as pickle
except:
   import pickle

# cheat as much as possible
from sklearn.cluster import MeanShift, estimate_bandwidth, DBSCAN

def cluster_imghits( orig_img, hit_img, quantile=0.1 ):
    """ take match hits and cluster them. goal is to find ends of tracks."""

    # [pseudocode]
    # for each cluster type
    #    we make a (x,y) list of hits above a certain threshold
    #    pass that to MeanShift algorithm
    #    if works, do something else with time saved from writing algo

    ntypes, nticks, nwires, nplanes = hit_img.shape

    features = {}
    clusters = {}
    for iplane in range(nplanes):
        for itype in range(ntypes):
            # slice the array
            planedata = hit_img[itype,:,:,iplane]
            hits = np.where( planedata>0.5 )
            nhits = hits[0].shape[0]

            if nhits<1:
                continue

            feature_v = np.zeros( ( nhits, 2 ) )
            feature_v[:,0] = hits[0][:]
            feature_v[:,1] = hits[1][:]
            features[ (itype,iplane) ] = feature_v

            start = time.time()
            # MeanShift
            #bandwidth = estimate_bandwidth( feature_v, quantile=quantile, n_samples=nhits )
            #ms = MeanShift( bandwidth=bandwidth, bin_seeding=True )
            #ms.fit(feature_v)

            # DBScan
            ms = DBSCAN( eps=5, min_samples=1 )
            ms.fit(feature_v)

            cluster_time = time.time()-start
            labels = ms.labels_
            
            labels_unique = np.unique(labels)
            n_clusters_ = len(labels_unique)
            print (itype,iplane),": number of clusters=",n_clusters_," %0.3f secs"%(cluster_time)

            print "nhits: ",nhits
            print len(labels)

            # generate random colors
            ncolors = np.random.rand( n_clusters_, 3 )*255
            #for icolor in range(0,n_clusters_):
            #    ncolors[icolor,0] = np.random.*256
            #    ncolors[icolor,1] = np.random()*256
            #    ncolors[icolor,2] = np.random()*256
                

            # make copy of img
            out_img = np.copy( orig_img )
            out_img *= 2.0
            # blank out non-plane
            for p in range(3):
                if p!=iplane:
                    out_img[:,:,p] = 0

            # add in hits
            #out_img[planedata>0] = 255
                    
            # make markers/clusters
            clusters[(itype,iplane)] = []
            for icluster in range( n_clusters_ ):
                # we want to mark track ends. 
                # we find the min and max time (row) and then ave charge 5 pixels beyond.  we take the side with less charge as the "end"
                cluster = feature_v[ labels==icluster ]
                print "-- [%d,%d] --"%(itype,iplane)
                print cluster
                center = np.mean(cluster, axis=0).astype(np.int)
                print icluster,center
                print "-------------"
                clusters[(itype,iplane)].append( center )

            # add clusters
            for ihit in range(nhits):
                out_img[ hits[0][ihit], hits[1][ihit], : ] = ncolors[ labels[ihit], : ]

            out_img[ out_img<10.0 ] = 0.0
            mat = out_img.astype( np.uint8 )
            for cluster in clusters[(itype,iplane)]:
                center = ( cluster[1], cluster[0] )
                print center
                cv2.circle( mat, center, 2, (255,255,255), -1 )

            cv2.imwrite( "cluster_test_plane%d_endtype%d.png"%(iplane,itype), mat )


    return clusters


if __name__=="__main__":
    
    prev_stage = np.load( "out_tag_stage.npz", 'r' )
    hit_img = prev_stage["hitimage"]
    orig_img = prev_stage["img"]
    print "hit image=",hit_img.shape,"orig_img=",orig_img.shape

    clusters = cluster_imghits( orig_img, hit_img )

    fout = open( "ex_clusters.pickle", 'w' )
    pickle.dump( clusters, fout )
    fout.close()
