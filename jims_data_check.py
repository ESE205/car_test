import sys
import argparse
import time 
import mod9_func as m9

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft

parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--delAD',  action='store', type=float, default=0.005,
                    help='time in between AD samples')
parser.add_argument('--delcal', action='store', type=float, default=0.01,
                    help='time in between speed calculations')
parser.add_argument('--debug',  action='store_true', 
                    help='specifies if debug statements are printed')
args = parser.parse_args()

if args.debug:
   print (f'arguments: {vars(args)}')

DEBUG   = args.debug
tdelta  = args.delAD
vdelta  = args.delcal
incVcal = max(10, int(vdelta/tdelta))

# open file, get data from user
fname   = input("Enter filename: ")
file    = open(fname, "r")
lines   = file.read().splitlines()
MAX_SIZE = len(lines)

# create a large array to hold data of MAX_SIZE, position is pointer to currval
datavals = [0] * MAX_SIZE
diffvals = [0] * MAX_SIZE
changes  = [0] * MAX_SIZE
times    = [0] * MAX_SIZE
speeds   = [0] * MAX_SIZE
that_spd = [0] * MAX_SIZE       # speed read from file for student
position = 0

i=0
for dat in lines:
   values      = dat.split()
   times[i]    = float(values[0])
   datavals[i] = float(values[1])
   that_spd[i] = float(values[2])
   i=i+1

# to start set threshold to 20% of difference bet DC offset and 1024 or 0
thresh = min(1024 - datavals[position], datavals[position])*0.2
updown = 0              # 0 - looking for up, 1 - looking for down
position = position + 1
tpos     = position

rotSpeed     = 0

for position in range(1, MAX_SIZE):
   tpos = position%MAX_SIZE
   diffvals[tpos] = datavals[tpos] - datavals[tpos -1]
   speeds[tpos]   = rotSpeed

   # detect change if one happened
   if (updown == 0 and m9.movingAvg(diffvals, tpos, 3) > thresh/5):
      changes[tpos] = 1
      updown    = 1
   elif (updown == 1 and m9.movingAvg(diffvals, tpos, 3) < -1*thresh/5):
      changes[tpos] = -1
      updown    = 0 
   else:
      changes[tpos] = 0
   if (DEBUG): 
      print (f'Pos: {position} Dat: {datavals[tpos]} ', end='')
      print (f'Dif: {diffvals[tpos]:4d} cng: {changes[tpos]} ', end='')
      print (f'ma: {m9.movingAvg(diffvals, tpos, 3)}')

   # Every displaydelta second display speed & calculate a new threshold
   if (position%incVcal == 0):
      # get new threshold in case it changed, use last 100 samples
      startIndex = tpos-100 if (tpos-100 >=0) else 0
      maxval  = max(datavals[startIndex:tpos])
      minval  = min(datavals[startIndex:tpos])
      thresh  = (maxval - minval)/2
      if (thresh < 15): thresh = 15
      
      # get the speed, count time between last 9 changes (8 time deltas)
      # if not 8, then take what you get and divide by the time between them
      # if no changes in a second, assume speed is zero
      cntChange   = 0
      i           = 0
      ttltime     = 0
      lastChange  = 0 
      firstChange = 0 
      changesNeed = 5
      if (DEBUG): print ("Threshold: ", thresh)
      while (cntChange < changesNeed and i < MAX_SIZE):
         if (changes[tpos - i] != 0):
            if (firstChange == 0): firstChange = i
            if (cntChange > 0):    # not first change
               ttltime = ttltime + i - lastChange
            lastChange = i
            cntChange = cntChange + 1
         #if (DEBUG): print ("i: ", i, " cntChange: " , cntChange)
         i = i+1
      # seconds per 1/4th of a rotation
      if (DEBUG): print ("ttltime: ", ttltime, " cntChange: " , cntChange)
      # full rotations / sec
      if (cntChange-1 > 0 and (lastChange - firstChange) < 3/tdelta):
         average_change_time = ttltime*tdelta/(cntChange - 1) 
         rotSpeed = 1 / (average_change_time * 4)
      else:
         rotSpeed = 0
      if (DEBUG): 
          print (cntChange, ttltime, i, " Rotational Speed: ", rotSpeed)

# write to file
fout = open("dataOut.txt", "w")
fout.write(f'{tdelta}\n')
for i in range(MAX_SIZE):
   fout.write(f'{times[i]:0.3f}\t{datavals[i]}\t{that_spd[i]:0.3f}\t{speeds[i]:0.3f}\t{diffvals[i]}\n')
fout.close()

fname   = "dataOut.txt"
file    = open(fname, "r")
lines   = file.read().splitlines()
MAXSIZE = len(lines)
debug   = True

times       = [0]*MAXSIZE
data        = [0]*MAXSIZE
their_speed = [0]*MAXSIZE
my_speed    = [0]*MAXSIZE
diff        = [0]*MAXSIZE

i=0
for dat in lines:
   if (i == 0):
      delay = float(dat)
   else: 
      values         = dat.split()
      times[i]       = float(values[0])
      data[i]        = float(values[1])
      their_speed[i] = float(values[2])
      my_speed[i]    = float(values[3])
      diff[i]        = float(values[4])
   i=i+1

N = 1024 if (1024<MAXSIZE) else 512
T = delay
plt.grid()
plt.plot(times[:N], their_speed[:N])
plt.plot(times[:N], my_speed[:N])
plt.xlabel('time - sec')
plt.ylabel('delta of Output')
plt.title('Your velocity in blue, expected in orange')
plt.savefig("speeds.png")
plt.clf()
