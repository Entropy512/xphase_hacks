#!/usr/bin/env python3

import cv2
from turbojpeg import TurboJPEG, TJSAMP_420
import sys
import numpy as np
import matplotlib.pyplot as plt

jpeg = TurboJPEG()

w = 3264
h = 2448

imgdata = np.zeros((h,w,3),dtype=np.int8)
for y in range(h):
    val = 23 + int(np.floor(((230.0-23.0)*y)/h))
    if(1):
        for x in range(w):
            if(x < w/4):
                imgdata[y][x] = [val,val,val]
            elif(x < w/2):
                imgdata[y][x] = [val, 0, 0]
            elif(x < 3*w/4):
                imgdata[y][x] = [0, val, 0]
            else:
                imgdata[y][x] = [0, 0, val]
    else:
        for x in range(w):
            imgdata[y][x] = [val, val, val]

with open('multigrad.jpg', 'wb') as outfile:
    outfile.write(jpeg.encode(imgdata,quality=99, jpeg_subsample=TJSAMP_420))
