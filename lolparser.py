import re
import os
import sqlite3
from collections import Counter

# initializes the dictionary for key = champ name and value = number of times played
champstats = Counter()
filepath = "/Volumes/Macintosh HD/Applications/League of Legends.app/C\
ontents/LoL/Logs/Game - R3d Logs/"
gamecount = 0
speccount = 0

# iterates over each file in the log directory and parses the champ stats
for f in os.listdir(filepath):
     temp = open(filepath + f)
     str = temp.read()
     # checks whether the log corresponds to an actual game that ended
     # and not to a disconnect (checks for EXITCODE_WIN or _LOSE)
     fullgame = re.search(r'EXITCODE', str)
     # if it matches, get the champion name and update the dict
     if fullgame:
          # working on identifying the person who created the logs
          # UID = re.search(r'netUID: (\d)'
          match = re.search(r'Hero (.*?)\(\d\) created for morbidflight', str)
          if match:
               gamecount += 1
               champstats[match.group(1)] += 1
          else:
               speccount += 1
     temp.close()

print "You played {} games.".format(gamecount)
print "You spectated {} games.".format(speccount)
print champstats.most_common()
