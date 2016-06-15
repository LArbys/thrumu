import os,sys
import numpy as np
import ROOT as rt
from math import fabs
try:
   import cPickle as pickle
except:
   import pickle

def load_match_list( wire_pixels ):
    fin_bot = open("bottom_matches.pickle",'r')
    fin_top = open("top_matches.pickle",'r')
    bot_matches = pickle.load( fin_bot )
    top_matches = pickle.load( fin_top )

    fin_bot.close()
    fin_top.close()

    print "Top matches: ",len(top_matches)
    print "Bottom matches: ",len(bot_matches)

    
    # fill the tensors
    downsize_factor = 3456/wire_pixels
    if 3456%wire_pixels!=0:
       downsize_factor+=0
    print "downsize factor: ",downsize_factor

    top_list = []
    bot_list = []
    
    for match in top_matches:
       u = match[0]/downsize_factor
       v = match[1]/downsize_factor
       y = match[2]/downsize_factor
       match = (u,v,y)
       if match not in top_list:
          top_list.append( match )

    for match in bot_matches:
       u = match[0]/downsize_factor
       v = match[1]/downsize_factor
       y = match[2]/downsize_factor
       match = (u,v,y)
       if match not in bot_list:
          bot_list.append( match )

    return top_list,bot_list

def load_match_tensor( wire_pixels ):
    fin_bot = open("bottom_matches.pickle",'r')
    fin_top = open("top_matches.pickle",'r')
    bot_matches = pickle.load( fin_bot )
    top_matches = pickle.load( fin_top )

    fin_bot.close()
    fin_top.close()

    print "Top matches: ",len(top_matches)
    print "Bottom matches: ",len(bot_matches)

    top_match_tensor = np.zeros( (wire_pixels,wire_pixels,wire_pixels), dtype=np.uint )
    bot_match_tensor = np.zeros( (wire_pixels,wire_pixels,wire_pixels), dtype=np.uint )
    
    # fill the tensors
    downsize_factor = 3456/768 + 1
    print "downsize factor: ",downsize_factor
    
    for match in top_matches:
       u = match[0]/downsize_factor
       v = match[1]/downsize_factor
       y = match[2]/downsize_factor
       top_match_tensor[u,v,y] = 1

    for match in bot_matches:
       u = match[0]/downsize_factor
       v = match[1]/downsize_factor
       y = match[2]/downsize_factor
       bot_match_tensor[u,v,y] = 1

    return top_match_tensor,bot_match_tensor

if __name__=="__main__":
   top, bot = load_match_tensor( 768 )
   print "top match tensor: ",top.shape
   print "number of matches: ",np.sum(top)


