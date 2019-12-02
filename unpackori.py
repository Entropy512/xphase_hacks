#!/usr/bin/python3

#Copyright 2019 Andrew T. Dodd

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

#horribly hackish Xphase ORI unpacker
#much code kanged from stackoverflow samples -
# https://stackoverflow.com/questions/49182097/searching-for-all-occurance-of-byte-strings-in-binary-file
# https://stackoverflow.com/questions/2363483/python-slicing-a-very-large-binary-file

import os
import sys
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

bin_file = sys.argv[1]

#with open(bin_file,'rb') as myfile:
#    for j in range(25):
#        myfile.seek(0x434+3080*j)
#        idx = myfile.read(2)
#        print(hex(struct.unpack('<H',idx)[0]))

with open(bin_file,'rb') as myfile:
    cur_offset = 2

    blocknum = 0
    myfile.seek(0, os.SEEK_END)
    filelen = myfile.tell()

    while(cur_offset < filelen):
        myfile.seek(cur_offset)
        (blocktype, nbytes) = struct.unpack('<hL', myfile.read(6))
        print("Block number " + str(blocknum) + " has type " + str(blocktype) +
              " with length " + str(nbytes) + " at offset " + hex(cur_offset + 6))

        if(blocktype == -48):
            print("\tUnknown file header data")

        elif(blocktype == -40):
            print("\tSmall lens data blocks (32 bytes per lens)")

        elif(blocktype == -41):
            print("\tLarge lens data blocks (3080 bytes per lens)")
            with open('largeblock.bin', 'wb') as largeblockfile:
                myfile.seek(cur_offset + 6)
                largeblockfile.write(myfile.read(nbytes))

        elif(blocktype == -39):
            tablestart = cur_offset + 6
            tablelen = nbytes
            myfile.seek(tablestart)
            oritable = myfile.read(tablelen)
            print("\tORI image table found")

        elif(blocktype == -45):
            imgstart = cur_offset + 6
            print("\tImage data block found")

        elif(blocktype == -46):
            previewstart = cur_offset + 6
            print("\tSpare duplicate image block found")
            with open('sparedup.jpg', 'wb') as sparedupfile:
                myfile.seek(previewstart)
                sparedupfile.write(myfile.read(nbytes))

        elif(blocktype == -43):
            previewstart = cur_offset + 6
            print("\tUser Nadir image block found")
            with open('usernadir.jpg', 'wb') as previewfile:
                myfile.seek(previewstart)
                previewfile.write(myfile.read(nbytes))

        else:
            print("\tUnknown block type")
        cur_offset += 6 + nbytes

for entrynum in range(int(tablelen/20)):
    tbloffset = entrynum * 20
    (imgtype, lens, shot, fileoffset, filelen) = struct.unpack_from('<HHHxxxxxxLL', oritable, offset=tbloffset)
    filestart = imgstart + fileoffset
    if(imgtype == 1):
        dest_fname = str(lens) + "_" + str(shot) + "_preview.jpg"
    elif(imgtype == 2):
        dest_fname = str(lens) + "_" + str(shot) + ".jpg"
    else:
        print("Unknown image type " + str(imgtype) + " found in ORI table in entry " + str(entrynum) + ", aborting")
        exit(-1)
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
