#!/usr/bin/env python3

import cv2
from turbojpeg import TurboJPEG, TJPF_GRAY, TJSAMP_GRAY, TJFLAG_PROGRESSIVE
import sys
import numpy as np
import matplotlib.pyplot as plt

jpeg = TurboJPEG()

with open(sys.argv[1], 'rb') as infile:
    yuvdata = jpeg.decode_to_yuv(infile.read())
    yuv = yuvdata[0]
    ydim = yuvdata[1][0]

    ylen = ydim[0]*ydim[1]
    ydata = yuv[0:ylen]
    
    #    ydata = planes[0]
    yhist = np.histogram(ydata,256)[0]
    print(np.count_nonzero(yhist))
    plt.plot(yhist)
    plt.show()
