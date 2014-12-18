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
summoner = ''  # sets the summoner name of the person

# iterates over each file in the log directory and parses the champ stats
for f in os.listdir(filepath):
     temp = open(filepath + f)
     str = temp.read()
     # checks whether the log corresponds to an actual game that ended
     # and not to a disconnect (checks for EXITCODE_WIN or _LOSE)
     fullgame = re.search(r'EXITCODE_(LOSE)|(WIN)', str)
     # if it matches, get the champion name and update the dict
     if fullgame:
          # working on identifying the person who created the logs
          # if the netUID is a single digit, then that person was in the game
          # if the netUID is ffffffff or whatever, then it's a spectate
          played = re.search(r'netUID: (\d)', str)
          if played:
               UID = played.group(1)
               name = re.search(r'Spawning champion \((.*?)\) .+ clientID {} and summonername \((.+?)\)'.format(UID), str)
               gamecount += 1
               champstats[name.group(1)] += 1
               summoner = name.group(2)
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
