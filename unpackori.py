#!/usr/bin/python3

#horribly hackish Xphase ORI unpacker
#much code kanged from stackoverflow samples -
# https://stackoverflow.com/questions/49182097/searching-for-all-occurance-of-byte-strings-in-binary-file
# https://stackoverflow.com/questions/2363483/python-slicing-a-very-large-binary-file

from bitstring import ConstBitStream
import os
import sys
import mmap
import struct

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
maxlens = 25

#Bracket identifier/index
bktidx = 0
maxbkt = 3 #TODO, change this if len(occurances) is 301

if(len(occurances) == 151):
    mode = 0
elif(len(occurances) == 301):
    mode = 1
else:
    print("Unknown number of images in file, falling back to analysis mode")
    mode = 2

with open(bin_file,'rb') as myfile:
    for j in range(25):
        myfile.seek(0x434+3080*j)
        idx = myfile.read(2)
        print(hex(struct.unpack('<H',idx)[0]))

with open(bin_file,'rb') as myfile:
    myfile.seek(0x130fc+2)
    tablelen = struct.unpack('<H', myfile.read(2))[0]
    myfile.seek(0x130fc)
    oritable = myfile.read(tablelen+12)
    imgstart = 0x130fc+12+tablelen #Instead of calculating this, I think we can just pull it from the table
    print(hex(imgstart))

nshots = int(tablelen/1000)

for lens in range(25):
    for shot in range(nshots):
        print(str((lens*nshots)+shot))
        tbloffset = 0x12 + ((lens*nshots) + shot) * 20
        tbloffset += 25*nshots*20
        (fileoffset, filelen) = struct.unpack_from('<LL', oritable, offset=tbloffset)
        filestart = imgstart + fileoffset
        dest_fname = str(lens) + "_" + str(shot) + ".jpg"
        copypart(bin_file, dest_fname, filestart, filelen)

#FIXME:  We are currently ignoring the last image in the ORI.  It's probably SOME sort of preview.
#We should append the file size as the last entry in the list of occurances so the code below can handle it
if(0):
    for j in range(len(occurances)-1):
        tbloffset = (occurances[j]-6)-imgstart
        tblloc = oritable.find(struct.pack('<L', tbloffset))
        datalen = occurances[j+1] - occurances[j]
        print(str(j) + "," + str(tbloffset) + "," + str(tblloc) + "," + str(datalen))
        if(mode == 0): #3-shot ORIs store images for a single lens together in bracket sequence
            if(j % 2 == 0):  #Even numbered images are thumbnails, skip them
                continue
            dest_fname = str(lensidx) + "_" + str(bktidx) + ".jpg"
            bktidx += 1
            if(bktidx >= maxbkt):
                lensidx += 1
                bktidx = 0
        elif(mode == 1):
            #As opposed to 3-shot, 6-shot ORIs store all images for a given EV together,
            #sequencing across lenses and then repeating
            if(j % 2 == 0):  #Even numbered images are still thumbnails, skip them
                continue
            dest_fname = str(lensidx) + "_" + str(bktidx) + ".jpg"
            #honestly we can keep the above common to both mode0 and mode1 and have the if here,
            #FIXME later
            lensidx += 1
            if(lensidx >= maxlens):
                bktidx += 1
                lensidx = 0
        else:
            dest_fname = str(int(j)) + ".jpg"
        #JFIF text is 6 bytes past beginning of file.  FIXME:  Handle this more cleanly
        copypart(bin_file,dest_fname, occurances[j]-6, datalen)
