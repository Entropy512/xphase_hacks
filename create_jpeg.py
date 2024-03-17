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

imgdata = np.ones((h,w,3),dtype=np.uint8)*20
mode = 2
match mode:
    case 0:
        for y in range(h):
            val = 0 + int(np.floor(((256.0-0.0)*y)/h))
            for x in range(w):
                if(x < w/3):
                    imgdata[y][x] = [255,val,val]
                elif(x < 2*w/3):
                    imgdata[y][x] = [val, 255, val]
                else:
                    imgdata[y][x] = [val, val, 255]

    case 1:
        for y in range(h):
            val = 0 + int(np.floor(((256.0-0.0)*y)/h))
            for x in range(w):
                if(x < w/3):
                    imgdata[y][x] = [val,0,0]
                elif(x < 2*w/3):
                    imgdata[y][x] = [0, val, 0]
                else:
                    imgdata[y][x] = [0, 0, val]

    case 2:
        for y in range(h):
            val = 0 + int(np.floor(((256.0-0.0)*y)/h))
            imgdata[y][:] = [val,val,val]

    case 3:
        haldsq = hald_level**2
        print(haldsq)
        hald_mod = int(np.floor(3264/(2*haldsq)))
        print(hald_mod)
        print((hald_mod)*haldsq*2)
        maxy = 0
        maxx = 0
        minval = 23
        maxval = 229
        dval = (maxval-minval)*1.0
        print(dval)
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
                    rval = int(dval*r/(haldsq-1))+minval
                    gval = int(dval*g/(haldsq-1))+minval
                    bval = int(dval*b/(haldsq-1))+minval
                    imgdata[y*2:y*2+2,x*2:x*2+2] = [bval, gval, rval]
        print(maxy*2)
        print(maxx*2)
        print(np.amax(imgdata))
with open('multisat.jpg', 'wb') as outfile:
    outfile.write(jpeg.encode(imgdata,quality=99, jpeg_subsample=TJSAMP_420))
