import re
import os
import sqlite3
from collections import Counter

# initializes the dictionary for key = champ name and value = number of times played
champstats = Counter()
filepath = "/Volumes/Macintosh HD/Applications/League of Legends.app/C\
ontents/LoL/Logs/Game - R3d Logs/"
gamecount = 0  # counts the number of games played by the person
speccount = 0  # counts the number of games spectated by the person
borkcount = 0  # counts the number of times the game was abandoned
summoner  = None  # holds the summoner name of the person
exitcode  = re.compile(r'EXITCODE_(LOSE)|(WIN)')
netUID    = re.compile(r'netUID: (\d)')
champfind = None

# iterates over each file in the log directory and parses the champ stats
for f in os.listdir(filepath):
     temp = open(filepath + f)
     str = temp.read()
     # checks whether the log corresponds to an actual game that ended
     # and not to a disconnect (checks for EXITCODE_WIN or _LOSE)
     fullgame = exitcode.search(str)
     # if it matches, get the champion name and update the dict
     if fullgame:
          # working on identifying the person who created the logs
          # if the netUID is a single digit, then that person was in the game
          # if the netUID is ffffffff or whatever, then it's a spectate
          played = netUID.search(str)
          if played:
               # extracts the name of the person whose logs it is
               # takes the first summoner name and then uses it to create a regex 
               if not summoner:
                    UID = played.group(1)
                    name = re.search(r'Spawning champion \((.*?)\) .+ clientID {} and summonername \((.+?)\)'.format(UID), str)
                    summoner = name.group(2)
                    champfind = re.compile(r'Spawning champion \((.*?)\) .+ summonername \(({})\)'.format(summoner))
               # this might be cheaper processing-wise to use a compiled regex
               else:
                    name = champfind.search(str)
               if name:  # need to be sure that it's the person you want!
                         # if it's another account, don't count it!
                    gamecount += 1
                    champstats[name.group(1)] += 1
          else:
               speccount += 1
     else:
          abandonship = re.search(r'EXITCODE_ABANDON', str)
          if abandonship:
               borkcount += 1
     temp.close()

print 'Analyzing logs for {}.'.format(summoner)
print 'You played {} games.'.format(gamecount)
print 'You spectated {} games.'.format(speccount)
print 'You broke {} games. Rito pls!'.format(borkcount)
print champstats.most_common(3)
