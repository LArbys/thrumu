import os,sys
import numpy as np
import ROOT as rt
import cv2

try:
   import cPickle as pickle
except:
   import pickle


def deteremine_dead_channels( orig_img ):
   print orig_img.shape
   rms = np.std( orig_img, axis=0 )
   chs = np.where( rms<0.1 )
   # sort by plane
   deadchs = {0:[],1:[],2:[]}
   for i in range(0,len(chs[0])):
      deadchs[ chs[1][i] ].append( chs[0][i] )

   return deadchs

def find_tracks( orig_img, clusters, iplane, debug=False ):
    """ connect cluster centers, follow line to see if track is there """
    # [pseudo code]
    # for each plane
    #   check combinations of tracks between cluster types

    deadchs = deteremine_dead_channels( orig_img )

    #iplane = 2
    width = 15
    ratio_thresh = 0.9
    step_thresh = 5
    cluster_types = [0,1,2,3]

    if debug:
       c = rt.TCanvas("c","c",800,600)
       #h = rt.TH2D("htrack","",1000,0,1000,100,0,1.0)
       h = rt.TH1D("htrack","",110,0,1.1)

    usedA = []
    usedB = []

    pairs = []

    test_track = []
    
    # instead of nested loop, probably make an index list in order to make it more readable?
    for itypeA in cluster_types[:-1]:
       try:
          clusterA_list = clusters[(itypeA,iplane)]
       except:
          continue

       for clustA in clusterA_list:
          print "-----------------"
          for itypeB in cluster_types[itypeA+1:]:
             try:
                clusterB_list = clusters[(itypeB,iplane)]
             except:
                continue
             for clustB in clusterB_list:
                #if tuple(clustB) in usedB:
                #   continue
                print "Testing clusterA(%d)="%(itypeA),clustA," to clusterB(%d)="%(itypeB),clustB,

                # calc, direction of track
                trackdir = (clustB-clustA).astype(np.float)
                slope = trackdir[1]/trackdir[0]
                nsteps = int( np.abs(trackdir[0]) )
                updown = 1
                if trackdir[0]<0:
                   updown = -1
                print " dir=",trackdir," slope=%0.2f"%(slope),"cols per row, nsteps=",nsteps,
                
                if nsteps<=0:
                   print
                   continue

                # is there a track in the neighborhood of the line?
                result = np.zeros( nsteps-1 )
                ndead = 0
                for istep in range(1,nsteps):
                   col = int( clustA[1] + updown*slope*istep )
                   row = int(clustA[0]) + updown*istep
                   if row>=orig_img.shape[0]:
                      break
                   if row<0:
                      break
                   neighborhood = orig_img[ row, np.maximum(col-width,0): np.minimum(col+width+1,orig_img.shape[1]), iplane]
                   nabove = np.where( neighborhood>10 )[0]

                   # for debug ----
                   if True and debug:
                      # Testing clusterA(0)= [322 261]  to clusterB(2)= [147 434]
                      if clustA[0]==322 and clustB[0]==147:
                         print istep,(row,col),[col-width,col+width+1], np.where( orig_img[row,:,iplane]>10 ),
                         if len(nabove)>0:
                            print " [hit]"
                         else:
                            print " [miss]"
                         test_track.append( (row,col) )
                   # --------------- end of debug

                   if len(nabove)>0:
                      result[istep-1] = 1.0
                   else:
                      if col in deadchs[iplane]:
                         ndead += 1

                raw_ratio = np.sum(result)/float(len(result))
                ratio = np.sum(result)/np.maximum(0, len(result)-ndead)
                print " above thresh=", np.sum(result)," frac above=%.2f"%(raw_ratio)," ndead=",ndead," corr. frac=%.2f"%(ratio)

                #h.Fill( nsteps, np.sum(result)/float(len(result)) )
                if debug:
                   h.Fill( ratio )

                if ratio>ratio_thresh and nsteps>step_thresh:

                   print "[[[ PAIRING ]]]]"

                   pairs.append( [ clustA, clustB ] )
                   usedB.append( tuple(clustB) )
                   #usedA.append( clustA )
                else:
                   print 
             
    print "Number of pairs!: ", len(pairs)

    img_out = np.copy(orig_img)
    for p in range(3):
       if p!=iplane:
          img_out[:,:,p] = 0.0
    img_out[ img_out<5 ] = 0.0
    img_out *= 2.0

    if iplane==0:
       # blue, could use help
       img_out[:,:,1] += img_out[:,:,0]

    out = img_out.astype(np.uint8)

    for ch in deadchs[iplane]:
       out[ :, ch, : ] = np.array( (25, 0, 25) )

    for pair in pairs:
       a = pair[0]
       b = pair[1]
       origin = (a[1],a[0])
       end    = (b[1],b[0])
       cv2.line( out, origin, end, (255,255,255), 1 )

    #cv2.line(out,(320,205),(367,103),(255,255,255),1)

    for mark in test_track:
       out[ mark[0], mark[1], : ] = np.array( (255,255,0) )


    cv2.imwrite("trackfindtest_plane%d.png"%(iplane),out)

    if debug:
       c.Draw()
       h.Draw("COLZ")
       c.Update()
       raw_input()
          

    return

if __name__ == "__main__":
    
    # load in test info
    fin = open("ex_clusters.pickle",'r')
    clusters = pickle.load( fin )
    fin.close()

    len(clusters)

    # load in images (and hit data)
    prev_stage = np.load( "out_tag_stage.npz", 'r' )
    hit_img = prev_stage["hitimage"]
    orig_img = prev_stage["img"]
    prev_stage.close()

    debug = False
    find_tracks( orig_img, clusters, 0, debug=debug )
    find_tracks( orig_img, clusters, 1, debug=debug )
    find_tracks( orig_img, clusters, 2, debug=debug )

