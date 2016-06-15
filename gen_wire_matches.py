import os,sys
import numpy as np
import ROOT as rt
from math import fabs
try:
   import cPickle as pickle
except:
   import pickle

def binsearch( zpos, zlist, tolerance ):
    """
    Binary search to find matching value within tolerance. Finds first one.
    """
    imin = 0
    imax = len(zlist)
    #print zlist[200],zlist[10]
    i = imax/2
    while i!=imin and i!=imax:
        # match
        #print i,zpos,zlist[i],zlist[i]-zpos,imin,imax
        if fabs(zpos-zlist[i])<tolerance:
            return i
        # no match yet
        if zpos<zlist[i]:
            imax = int(i)
            i = (i+imin)/2
        else:
            imin = int(i)
            i = (imax+i)/2
    return None
            

def gen_wire_matches( nwire_pixels, dist_tolerance=0.3 ):
    """
    Generates a 3D numpy array with 0 or 1 if entry matches or not.
    Requires geoinfo.root file to get Wire information.
    """

    # Open File
    fgeo = rt.TFile("geoinfo.root")
    # root [4] wireInfo->Print()
    # ******************************************************************************
    # *Tree    :wireInfo  : Wire Geo Info                                          *
    # *Entries :     8256 : Total =          267376 bytes  File  Size =      72869 *
    # *        :          : Tree compression factor =   3.68                       *
    # ******************************************************************************
    # *Br    0 :plane     : plane/I                                                *
    # *Entries :     8256 : Total  Size=      33650 bytes  File Size  =        386 *
    # *Baskets :        2 : Basket Size=      32000 bytes  Compression=  85.95     *
    # *............................................................................*
    # *Br    1 :wireID    : wireID/I                                               *
    # *Entries :     8256 : Total  Size=      33656 bytes  File Size  =      11542 *
    # *Baskets :        2 : Basket Size=      32000 bytes  Compression=   2.87     *
    # *............................................................................*
    # *Br    2 :start     : start[3]/F                                             *
    # *Entries :     8256 : Total  Size=      99856 bytes  File Size  =      30375 *
    # *Baskets :        4 : Basket Size=      32000 bytes  Compression=   3.27     *
    # *............................................................................*
    # *Br    3 :end       : end[3]/F                                               *
    # *Entries :     8256 : Total  Size=      99840 bytes  File Size  =      29822 *
    # *Baskets :        4 : Basket Size=      32000 bytes  Compression=   3.33     *
    # *............................................................................*
    wireinfo = fgeo.Get("imagedivider/wireInfo")

    y_start = {0:{},1:{},2:{}}
    z_start = {0:{},1:{},2:{}}
    y_end   = {0:{},1:{},2:{}}
    z_end   = {0:{},1:{},2:{}}

    print "Extract Wire Data"
    for entry in range(0,wireinfo.GetEntries()):
        wireinfo.GetEntry(entry)
        y_start[ wireinfo.plane ][ wireinfo.wireID ] = wireinfo.start[1]
        z_start[ wireinfo.plane ][ wireinfo.wireID ] = wireinfo.start[2]
        y_end[ wireinfo.plane ][ wireinfo.wireID ]   = wireinfo.end[1]
        z_end[ wireinfo.plane ][ wireinfo.wireID ]   = wireinfo.end[2]
        

    _nwires = []
    
    for p in range(0,3):
        _nwires.append( len(y_start[p]) )
        print "Number of wires on plane ",p,": ",_nwires[p]
    nwires = np.array( _nwires )

    bot_matchlist = []

    zpos0 = z_start[0].values()
    zpos1 = z_start[1].values()
    zpos2 = z_start[2].values()
    zpos0.sort()
    zpos1.sort()
    zpos2.sort()

    # TPC bottom matchs
    for wireid, z in z_start[2].items():
        if y_start[2][wireid]>-115.0:
            continue
        print "Ywireid=",wireid, "zpos=",z_start[2][wireid],"ypos=",y_start[2][wireid]
        # look for matches on U,V  planes
        Umatches = []
        Vmatches = []
        for zlist,matches,plane in [(zpos0,Umatches,0),(zpos1,Vmatches,1)]:        
            match1 = binsearch( z, zlist, dist_tolerance )
            if match1 is not None:
               matches.append( match1 )
               # check in neighboorhood of match, for more matches
               for i in range(1,100):
                  if match1+i>=len(zlist):
                     break
                  if fabs(z-zlist[match1+i])<dist_tolerance and y_start[plane][match1+i]<-115.0:
                     # must be on bottom of TPC
                     matches.append( match1+i )
                  else:
                     break
               for i in range(1,100):
                  if match1-i<=0:
                     break
                  if fabs(z-zlist[match1-i])<dist_tolerance and y_start[plane][match1-1]<-115.0:
                     matches.append( match1-i )
                  else:
                     break
            print "matches: ",matches
            
        for U in Umatches:
            for V in Vmatches:
                bot_matchlist.append( (U,V,wireid) )
                print "Bottom Match: ",(U,V,wireid)
                print "  endpoints: ",z_start[0][U],z_start[1][V],z_start[2][wireid]
    #print "Number of Bottom Matches: ",np.sum( match )
    print "Saving match list:",len(bot_matchlist)
    fout = open("bottom_matches.pickle",'w')
    pickle.dump( bot_matchlist, fout )
    fout.close()

    # TPC Top matches
    top_matchlist = []

    zpos0 = z_end[0].values()
    zpos1 = z_end[1].values()
    zpos2 = z_end[2].values()
    zpos0.sort()
    zpos1.sort()
    zpos2.sort()
    
    for wireid, z in z_end[2].items():
       if y_end[2][wireid]<117.0:
           continue
       print "Ywireid=",wireid, "zpos=",z_end[2][wireid],"ypos=",y_end[2][wireid]
       # look for matches on U,V  planes
       Umatches = []
       Vmatches = []
       for zlist,matches,plane in [(zpos0,Umatches,0),(zpos1,Vmatches,1)]:        
          match1 = binsearch( z, zlist, dist_tolerance )
          matches.append( match1 )
          if match1 is not None:
             # check in neighboorhood of match, for more matches
             for i in range(1,100):
                if match1+i>=len(zlist):
                   break
                if fabs(z-zlist[match1+i])<dist_tolerance and y_end[plane][match1+i]>-117.0:
                   # must be on top of TPC
                   matches.append( match1+i )
                else:
                   break
             for i in range(1,100):
                if match1-i<=0:
                   break
                if fabs(z-zlist[match1-i])<dist_tolerance and y_end[plane][match1-1]>117.0:
                   matches.append( match1-i )
                else:
                   break
          print "matches: ",matches
       for U in Umatches:
          if U is None:
             continue
          for V in Vmatches:
             if V is None:
                continue
             top_matchlist.append( (U,V,wireid) )

    print "Saving top match list: ",len(top_matchlist)
    print "Saving bot match list: ",len(bot_matchlist)
    fout = open("top_matches.pickle",'w')
    pickle.dump( top_matchlist, fout )
    fout.close()
        
    return


if __name__ == "__main__":
    gen_wire_matches( 768, dist_tolerance=0.30 )

        


