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
import argparse
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

ap = argparse.ArgumentParser()
ap.add_argument('-o', '--output', required=True,
    help='path to output file')

# FIXME:  Find a way to get this from the original file bins that is better
# than analyzing the original oritable
ap.add_argument('-b', '--bracketcount', help='Shot bracket count (3 or 6)',
                default=3, type=int, choices=[3,6])

# FIXME:  Find a way to get this from the original file bins too
ap.add_argument('-n', '--usernadir', help='Look for and add a user nadir block', action='store_true')

# FIXME:  Scan ORIs SOOC have a bunch of empty entries.  Needs testing to see if these matter to PanoManager
ap.add_argument('-s', '--scan', help='Pack an Xphase Scan ORI file', action='store_true')

args = vars(ap.parse_args())
bin_file = args['output']
bracket_count = args['bracketcount']
# Scan ORIs seem to have placeholders for higher shot count, may be a problem depending on settings?
entry_count = 36 if args['scan'] else 25
shot_count = 30 if args['scan'] else 25
lens_count = 3 if args['scan'] else 25

# ORIs must be of a specific format, and the date in the header must match the date encoded in the filename
# Extract the year,month,day,hours,minutes,seconds from the file name
(filebase,fileext) = bin_file.rsplit('.',1)
if(fileext != 'ori'):
    exit('File must end in .ori')
datetime = filebase.split('_')
if(len(datetime) != 2):
    exit('File must be of the form YYYY-MM-DD_HH.MM.SS.ori')
ymd = datetime[0].split('-')
if(len(ymd) != 3):
    exit('File must be of the form YYYY-MM-DD_HH.MM.SS.ori')
hms = datetime[1].split('.')
if(len(hms) != 3):
    exit('File must be of the form YYYY-MM-DD_HH.MM.SS.ori')

datelist = [int(i) for i in (ymd+hms)]


with open(bin_file,'wb') as myfile:
    blocknum = 0
    myfile.write(struct.pack('<H', 0x73C1))

    with open('headerdata.bin', 'rb') as hdrfile:
        hdrfile.seek(0,os.SEEK_END)
        hdrlen = hdrfile.tell()
        if(hdrlen != 256):
            raise("Header length not 256 - not supported!")
        myfile.write(struct.pack('<hL',-48, hdrlen))
        hdrstart = myfile.tell()
        bulkread(hdrfile, myfile, hdrstart, hdrlen)
        #Write the date which matches the filename to the appropriate location in the header
        myfile.seek(hdrstart+8)
        myfile.write(struct.pack('<LLLLLL',*datelist))
        myfile.seek(0,os.SEEK_END)

    with open('smallblock.bin', 'rb') as sbfile:
        sbfile.seek(0,os.SEEK_END)
        sblen = sbfile.tell()
        if(sblen != 32*lens_count):
            raise("Smallblock length not " + str(32*lens_count) + " - not supported!")
        myfile.write(struct.pack('<hL',-40, sblen))
        bulkread(sbfile, myfile, myfile.tell(), sblen)

    with open('largeblock.bin', 'rb') as lbfile:
        lbfile.seek(0,os.SEEK_END)
        lblen = lbfile.tell()
        if(lblen != 3080*lens_count):
            raise("Largeblock length not " + str(3080*lens_count) + " - not supported!")
        myfile.write(struct.pack('<hL',-41, lblen))
        bulkread(lbfile, myfile, myfile.tell(), lblen)


    #Write out ORI table.  We always go in a deterministic order
    #but we do need to cache file lengths in the table unless we want to re-get the
    #lengths
    tbllen = 40*entry_count*bracket_count        
    imgdata_start = myfile.tell() + 12+tbllen

    myfile.write(struct.pack('<hL', -39, tbllen))
    filelens = np.zeros((shot_count,bracket_count,2),dtype=np.int32)
    filetotal = 0
    for typ in range(2):
        for lens in range(entry_count):
            for exp in range(bracket_count):
                if(lens < shot_count):
                    if(typ == 0):
                        fname = "IMG_{:02}_".format(lens) + str(exp) + "_preview.jpg"
                    else:
                        fname = "IMG_{:02}_".format(lens) + str(exp) + ".jpg"
                    filelen = get_filelen(fname)
                    filelens[lens][exp][typ] = filelen
                    fileptr = filetotal
                else:
                    # Scan ORIs have a bunch of empty table entries with offset 0 and length 0
                    filelen = 0
                    fileptr = 0

                myfile.write(struct.pack('<HHHxxxxxxLL', typ+1, lens, exp, fileptr, filelen))
                filetotal += filelen

    #actual image data
    #fileptr is, at this point, the total length because we incremented it after
    #writing the last table entry
    myfile.write(struct.pack('<hL', -45, filetotal))
    for typ in range(2):
        for lens in range(shot_count):
            for exp in range(bracket_count):
                if(typ == 0):
                    fname = "IMG_{:02}_".format(lens) + str(exp) + "_preview.jpg"
                else:
                    fname = "IMG_{:02}_".format(lens) + str(exp) + ".jpg"
                with open(fname, 'rb') as jpgfile:
                    bulkread(jpgfile, myfile, myfile.tell(), filelens[lens][exp][typ])

    with open('sparedup.jpg', 'rb') as prvfile:
        prvfile.seek(0,os.SEEK_END)
        prvlen = prvfile.tell()
        myfile.write(struct.pack('<hL',-46, prvlen))
        bulkread(prvfile, myfile, myfile.tell(), prvlen)

    if(args['usernadir']):
        with open('usernadir.jpg', 'rb') as prvfile:
            prvfile.seek(0,os.SEEK_END)
            prvlen = prvfile.tell()
            myfile.write(struct.pack('<hL',-43, prvlen))
            bulkread(prvfile, myfile, myfile.tell(), prvlen)