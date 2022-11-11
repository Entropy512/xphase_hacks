#!/usr/bin/env python3

import cv2
from turbojpeg import TurboJPEG, TJSAMP_420
import sys
import numpy as np
import matplotlib.pyplot as plt

jpeg = TurboJPEG()

w = 3264
h = 2448

hald_level = 11

imgdata = np.ones((h,w,3),dtype=np.int8)*50
if(1):
    for y in range(h):
        val = 0 + int(np.floor(((255.0-0.0)*y)/h))
        #val = 150
        if(1):
            for x in range(w):
                if(x < w/3):
                    imgdata[y][x] = [255,val,val]
                elif(x < 2*w/3):
                    imgdata[y][x] = [val, 255, val]
                else:
                    imgdata[y][x] = [val, val, 255]
        else:
            for x in range(w):
                imgdata[y][x] = [val, val, val]
else:
    haldsq = hald_level**2
    print(haldsq)
    hald_mod = int(np.floor(3264/(2*haldsq)))
    print(hald_mod)
    print((hald_mod)*haldsq*2)
    maxy = 0
    maxx = 0
    for r in range(haldsq):
        for g in range(haldsq):
            for b in range(haldsq):
                quadrant_x = (b % hald_mod)*haldsq
                quadrant_y = (np.floor(b/hald_mod).astype(np.uint8))*haldsq
                #print(str(quadrant_x) + " " + str(quadrant_y))

                x = quadrant_x + r
                y = quadrant_y + g
                maxy = np.maximum(y,maxy)
                maxx = np.maximum(x,maxx)
                rval = int(255.0*r/haldsq)
                gval = int(255.0*g/haldsq)
                bval = int(255.0*b/haldsq)
                imgdata[y*2:y*2+2,x*2:x*2+2] = [bval, gval, rval]
    print(maxy*2)
    print(maxx*2)
with open('multisat.jpg', 'wb') as outfile:
    outfile.write(jpeg.encode(imgdata,quality=99, jpeg_subsample=TJSAMP_420))
