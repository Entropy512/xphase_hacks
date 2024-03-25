#!/usr/bin/env python3

from turbojpeg import TurboJPEG, TJSAMP_420
import argparse
import numpy as np
import matplotlib.pyplot as plt

jpeg = TurboJPEG()

ap = argparse.ArgumentParser()
ap.add_argument('-m', '--mode', required=True, type=int, default=0,
    help='creation mode, read source code for details')

ap.add_argument('--minval', type=int, default=23,
    help='minimum value for various modes, read source for details')

ap.add_argument('--maxval', type=int, default=229,
    help='maximum value for various modes, read source for details')

ap.add_argument('-o', '--outfile', help='Output filename override')

args = vars(ap.parse_args())

w = 3264
h = 2448

hald_level = 11

imgdata = np.ones((h,w,3),dtype=np.uint8)*20
mode = args['mode']
minval = args['minval']
maxval = args['maxval']
match mode:
    case 0:
        for y in range(h):
            val = minval + int(np.floor(((maxval+1-minval)*y)/h))
            for x in range(w):
                if(x < w/3):
                    imgdata[y][x] = [maxval, val, val]
                elif(x < 2*w/3):
                    imgdata[y][x] = [val, maxval, val]
                else:
                    imgdata[y][x] = [val, val, maxval]

    case 1:
        for y in range(h):
            val = minval + int(np.floor(((maxval+1-minval)*y)/h))
            for x in range(w):
                if(x < w/3):
                    imgdata[y][x] = [val, minval, minval]
                elif(x < 2*w/3):
                    imgdata[y][x] = [minval, val, minval]
                else:
                    imgdata[y][x] = [minval, minval, val]

    case 2:
        imgdata[:,0:int(w/4)] = [minval, minval, maxval]
        imgdata[:,int(w/4):int(2*w/4)] = [minval, maxval, minval]
        imgdata[:,int(2*w/4):int(3*w/4)] = [maxval, minval, minval]
        imgdata[:,int(3*w/4):] = [maxval, maxval, maxval]

    case 3:
        for y in range(h):
            val = minval + int(np.floor(((maxval-minval)*y)/h))
            imgdata[y][:] = [val,val,val]

    case 4:
        haldsq = hald_level**2
        print(haldsq)
        hald_mod = int(np.floor(3264/(2*haldsq)))
        print(hald_mod)
        print((hald_mod)*haldsq*2)
        maxy = 0
        maxx = 0
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
    

if(args['outfile'] is not None):
    fname = args['outfile']
else:
    fname = 'mode{:02}.jpg'.format(mode)

with open(fname, 'wb') as outfile:
    outfile.write(jpeg.encode(imgdata,quality=99, jpeg_subsample=TJSAMP_420))
