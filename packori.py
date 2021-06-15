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

#horribly hackish Xphase ORI packer
#much code kanged from stackoverflow samples -
# https://stackoverflow.com/questions/49182097/searching-for-all-occurance-of-byte-strings-in-binary-file
# https://stackoverflow.com/questions/2363483/python-slicing-a-very-large-binary-file

import os
import sys
import struct
import numpy as np

def bulkread(srcfh,destfh,dststart,filelen,bufsize=1024*1024):
    srcfh.seek(0)
    destfh.seek(dststart)
    while filelen:
        chunk = min(bufsize,filelen)
        data = srcfh.read(chunk)
        destfh.write(data)
        filelen -= chunk

def get_filelen(fname):
    with open(fname, 'rb') as checkfile:
        checkfile.seek(0, os.SEEK_END)
        file_len = checkfile.tell()
        return file_len

if(len(sys.argv) < 2):
    print("Too few arguments")
    exit(-1)

bin_file = sys.argv[1]

#with open(bin_file,'rb') as myfile:
#    for j in range(25):
#        myfile.seek(0x434+3080*j)
#        idx = myfile.read(2)
#        print(hex(struct.unpack('<H',idx)[0]))

with open(bin_file,'wb') as myfile:
    blocknum = 0
    myfile.write(struct.pack('<H', 0x73C1))

    with open('headerdata.bin', 'rb') as hdrfile:
        hdrfile.seek(0,os.SEEK_END)
        hdrlen = hdrfile.tell()
        if(hdrlen != 256):
            raise("Header length not 256 - not supported!")
        myfile.write(struct.pack('<hL',-48, hdrlen))
        bulkread(hdrfile, myfile, myfile.tell(), hdrlen)

    with open('smallblock.bin', 'rb') as sbfile:
        sbfile.seek(0,os.SEEK_END)
        sblen = sbfile.tell()
        if(sblen != 800):
            raise("Smallblock length not 800 - not supported!")
        myfile.write(struct.pack('<hL',-40, sblen))
        bulkread(sbfile, myfile, myfile.tell(), sblen)

    with open('largeblock.bin', 'rb') as lbfile:
        lbfile.seek(0,os.SEEK_END)
        lblen = lbfile.tell()
        if(lblen != 77000):
            raise("Largeblock length not 77000 - not supported!")
        myfile.write(struct.pack('<hL',-41, lblen))
        bulkread(lbfile, myfile, myfile.tell(), lblen)


    #Write out ORI table.  We always go in a deterministic order
    #but we do need to cache file lengths in the table unless we want to re-get the
    #lengths
    imgdata_start = myfile.tell() + 3012
    tbllen = 3000 # 3-shot
    myfile.write(struct.pack('<hL', -39, tbllen))
    filelens = np.zeros((25,3,2),dtype=np.int32)
    filetotal = 0
    for typ in range(2):
        for lens in range(25):
            for exp in range(3):
                if(typ == 0):
                    fname = str(lens) + "_" + str(exp) + "_preview.jpg"
                else:
                    fname = str(lens) + "_" + str(exp) + ".jpg"
                filelen = get_filelen(fname)
                filelens[lens][exp][typ] = filelen
                fileptr = filetotal
                myfile.write(struct.pack('<HHHxxxxxxLL', typ+1, lens, exp, fileptr, filelen))
                filetotal += filelen

    #actual image data
    #fileptr is, at this point, the total length because we incremented it after
    #writing the last table entry
    myfile.write(struct.pack('<hL', -45, filetotal))
    for typ in range(2):
        for lens in range(25):
            for exp in range(3):
                if(typ == 0):
                    fname = str(lens) + "_" + str(exp) + "_preview.jpg"
                else:
                    fname = str(lens) + "_" + str(exp) + ".jpg"
                with open(fname, 'rb') as jpgfile:
                    bulkread(jpgfile, myfile, myfile.tell(), filelens[lens][exp][typ])

    with open('sparedup.jpg', 'rb') as prvfile:
        prvfile.seek(0,os.SEEK_END)
        prvlen = prvfile.tell()
        myfile.write(struct.pack('<hL',-46, prvlen))
        bulkread(prvfile, myfile, myfile.tell(), prvlen)
