#!/usr/bin/python3

#horribly hackish Xphase ORI unpacker
#much code kanged from stackoverflow samples -
# https://stackoverflow.com/questions/49182097/searching-for-all-occurance-of-byte-strings-in-binary-file
# https://stackoverflow.com/questions/2363483/python-slicing-a-very-large-binary-file

from bitstring import ConstBitStream
import os
import sys
import mmap

def copypart(src,dest,start,length,bufsize=1024*1024):
    with open(src,'rb') as f1:
        f1.seek(start)
        with open(dest,'wb') as f2:
            while length:
                chunk = min(bufsize,length)
                data = f1.read(chunk)
                f2.write(data)
                length -= chunk

if(len(sys.argv) < 2):
    print("Too few arguments")
    exit(-1)

byte_data = rb'JFIF'

bin_file = sys.argv[1]

s = ConstBitStream(filename=bin_file)
occurances = s.findall(byte_data, bytealigned=True)
occurances = list(occurances)
totalOccurances = len(occurances)
#print(totalOccurances)
for j in range(len(occurances)):
    occurances[j] = int(occurances[j]/8)

#Lens identifier/index
lensidx = 0

#Bracket identifier/index
bktidx = 0
maxbkt = 3 #TODO, change this if len(occurances) is 301

for j in range(len(occurances)-1):
    if(j % 2 == 0):  #Even numbered images are thumbnails, skip them
        continue;
    dest_fname = str(lensidx) + "_" + str(bktidx) + ".jpg"
    bktidx += 1
    if(bktidx >= maxbkt):
        lensidx += 1
        bktidx = 0
    datalen = occurances[j+1] - occurances[j]
    print(str(j) + " " + str(datalen))
    #JFIF text is 6 bytes past beginning of file.  FIXME:  Handle this more cleanly
    copypart(bin_file,dest_fname, occurances[j]-6, datalen+6)
