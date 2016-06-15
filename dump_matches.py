import os,sys
try:
   import cPickle as pickle
except:
   import pickle

fin_bot = open("bottom_matches.pickle",'r')
fin_top = open("top_matches.pickle",'r')
bot_matches = pickle.load( fin_bot )
top_matches = pickle.load( fin_top )

fin_bot.close()
fin_top.close()

print "All Top matches: "
print len(top_matches)

print "All Bottom matches: "
print len(bot_matches)

nskipped = 0
for t in top_matches:
   if t[0]<672:
      print "skipped?: ",t
      nskipped += 1
   if t[0]>2399:
      nskipped += 1

print "top skipped: ",nskipped,"of",len(top_matches)

nskipped = 0
for t in bot_matches:
   if t[0]<672:
      print "skipped?: ",t
      nskipped += 1
   if t[0]>2399:
      nskipped += 1

print "bot skipped: ",nskipped,"of",len(bot_matches)

#print bot_matches
