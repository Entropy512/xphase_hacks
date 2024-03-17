#!/usr/bin/env python3

import rawpy
from turbojpeg import TurboJPEG
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import argparse
import os
import colour
from pprint import pprint
from xphase_data import XphaseTransfer

jpeg = TurboJPEG()

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=True,
    help='path to input file')

args = vars(ap.parse_args())
ap_name = ap.prog #TODO: Determine if we care about this, rawpy did it but we don't really need it.

filebase = os.path.splitext(args['input'])[0]
dngname = filebase + '.dng'

rawfile = rawpy.imread(dngname)

with open(args['input'], 'rb') as jpgfile:
    planes = jpeg.decode_to_yuv_planes(jpgfile.read())
    yplane = planes[0]
    uplane = planes[1]
    vplane = planes[2]

with open(args['input'], 'rb') as jpgfile:
    bgrdata = jpeg.decode(jpgfile.read())
    rgbdata = bgrdata.copy()
    rgbdata[:,:,0] = bgrdata[:,:,2]
    rgbdata[:,:,2] = bgrdata[:,:,0]


bayer_pattern = rawfile.raw_pattern
print(bayer_pattern)
raw_data = rawfile.raw_image_visible.astype('float64')
#handling bayer currently useless for our primary purpose,
#but might be useful for comparing ORI to input DNG later
#instead of fuzzing PanoManager by feeding it synthetic JPGs

if(bayer_pattern is not None):
    iRrow,  iRclmn  = np.argwhere(bayer_pattern == 0)[0]
    iG0row, iG0clmn = np.argwhere(bayer_pattern == 1)[0]
    iBrow,  iBclmn  = np.argwhere(bayer_pattern == 2)[0]
    iG1row, iG1clmn = np.argwhere(bayer_pattern == 3)[0]

    R_raw  = raw_data[ iRrow::2,  iRclmn::2]
    G_raw = raw_data[iG0row::2, iG0clmn::2]
    #G1 = bayer_data[iG1row::2, iG1clmn::2]
    B_raw  = raw_data[ iBrow::2,  iBclmn::2]
else:
    raw_data = raw_data[0:,0:,0:-1]
    R_raw = raw_data[0:,0:,0]
    G_raw = raw_data[0:,0:,1]
    B_raw = raw_data[0:,0:,2]

# It seems like every lens except 00, 01, 23, 24 are flipped upside down by PanoManager
(garbage, lensnum, shotnum) = filebase.split("_",3)
if int(lensnum) not in [0, 1, 23, 24]:
    raw_data = np.fliplr(np.flipud(raw_data))

xt = XphaseTransfer()
lut = xt.lut

print(np.amin(yplane))
print(np.amax(yplane))

print(raw_data.shape)
print(rgbdata.shape)

lindata = lut[rgbdata]
print(np.amax(lindata))
print(np.amax(raw_data))
#raw_data = ilut_flor[raw_data.astype(np.uint16)]

#DNG color matrix
color_matrix_raw = np.matrix([[1.69266987, -0.5626429913, -0.08418130087],
                              [-0.3848780093, 1.108350039, 0.3184210059],
                              [-0.0598646994, 0.1917970028, 1.04934001]])
invmatrix_raw = np.linalg.inv(color_matrix_raw)
primaries_raw = colour.primaries_whitepoint(invmatrix_raw)[0]
whitepoint_raw = colour.primaries_whitepoint(invmatrix_raw)[1]
colorspace_raw = colour.models.RGB_Colourspace('RAW color space', primaries_raw, whitepoint_raw, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

#Where the heck did I get this from???
#Linearizing Zwikel's colorchecker shot and then dcamprofing it???
#Or tracing the borders of a HALD-derived DNG that has no values below 23?
primaries_jpeg = np.array([[0.567968, 0.368446],
                           [0.30249, 0.64607],
                           [0.1293, 0.006655]])
whitepoint_jpeg = np.array([0.34567, 0.3585])
colorspace_jpeg = colour.models.RGB_Colourspace('JPEG color space', primaries_jpeg, whitepoint_jpeg, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

raw_to_jpeg_matrix = colour.matrix_RGB_to_RGB(colorspace_raw, colorspace_jpeg)

# Estimated color matrix from an earlier mode 0 run
cmat_est1 = np.array([[0.74066847, 0.20708179, 0.10163293],
                    [0.14307383, 0.62007526, 0.15846967],
                    [0.11811859, 0.19158811, 0.73919268]])

# Sanity check our matrices
pprint(raw_to_jpeg_matrix)
pprint(np.linalg.inv(raw_to_jpeg_matrix))
pprint(cmat_est1)

jpeg_to_raw_matrix = np.linalg.inv(raw_to_jpeg_matrix)

mode = 2
match mode:
    case 0:
        # Attempt to reverse engineer the color matrix that transforms from JPEG to RAW by fitting a matrix to
        # the difference between linearized JPEG and RAW, works best with a HALD-ish image that only has values from
        # 23 to 229.  (create.jpeg.py mode 2 with minval=23 and maxval=229)
        # Trying to fit outside of the luma-only LUT region creates too many reverse engineering variables
        ldata = np.reshape(lindata, (lindata.shape[0]*lindata.shape[1], lindata.shape[2]))
        print(ldata.shape)
        rdata = np.reshape(raw_data, (raw_data.shape[0]*raw_data.shape[1], raw_data.shape[2]))
        cmat = np.matmul(np.matmul(np.linalg.inv(np.matmul(ldata.T,ldata)), ldata.T), rdata)

        np.printoptions(legacy=False)
        pprint(cmat_est1)
        pprint(cmat)
        print(np.amax(np.matmul(lindata,cmat)))
        plt.figure()
        plt.imshow(raw_data/65535.0)
        plt.figure()
        plt.imshow(lindata/65535.0)
        plt.figure()
        plt.imshow(np.matmul(lindata,cmat.T)/65535.0)
        plt.figure()
        print(np.amax(np.matmul(lindata,cmat)/raw_data))
        print(np.amin(np.matmul(lindata,cmat)/raw_data))
        print(np.mean(np.matmul(lindata,cmat)/raw_data))
        plt.imshow(0.5*np.matmul(lindata,cmat)/raw_data)
        plt.show()
    case 1:
        #really hackish things intended for images generated using create_jpeg_from_yuv.py
        plt.figure()
        plt1 = plt.subplot(211)
        plt1.plot(uplane[204*3,0::4], raw_data[408*3,0::8,0],'r')
        plt1.plot(uplane[204*3,0::4], raw_data[408*3,0::8,1],'g')
        plt1.plot(uplane[204*3,0::4], raw_data[408*3,0::8,2],'b')
        plt1.axhline(y=0, color='k', alpha=0.5)

        plt2 = plt.subplot(212, sharex=plt1)
        plt2.plot(uplane[204*3,0::4], rgbdata[408*3,0::8,0],'r')
        plt2.plot(uplane[204*3,0::4], rgbdata[408*3,0::8,1],'g')
        plt2.plot(uplane[204*3,0::4], rgbdata[408*3,0::8,2],'b')
        plt2.axhline(y=0, color='k', alpha=0.5)
        plt2.axhline(y=23, color='k', alpha=0.3)


        plt.figure()
        plt1 = plt.subplot(211)
        plt1.plot(vplane[204*3,0::4], raw_data[408*3,0::8,0],'r')
        plt1.plot(vplane[204*3,0::4], raw_data[408*3,0::8,1],'g')
        plt1.plot(vplane[204*3,0::4], raw_data[408*3,0::8,2],'b')
        plt1.axhline(y=0, color='k', alpha=0.5)
        plt2 = plt.subplot(212, sharex=plt1)

        plt2.plot(vplane[204*3,0::4], rgbdata[408*3,0::8,0],'r')
        plt2.plot(vplane[204*3,0::4], rgbdata[408*3,0::8,1],'g')
        plt2.plot(vplane[204*3,0::4], rgbdata[408*3,0::8,2],'b')
        plt2.axhline(y=0, color='k', alpha=0.5)
        plt2.axhline(y=23, color='k', alpha=0.3)

        vslice = int(3264*(40/255))
        plt.figure()
        plt1 = plt.subplot(211)
        plt1.plot(yplane[0::8,vslice], raw_data[0::8,vslice,0],'r')
        plt1.plot(yplane[0::8,vslice], raw_data[0::8,vslice,1],'g')
        plt1.plot(yplane[0::8,vslice], raw_data[0::8,vslice,2],'b')
        plt2 = plt.subplot(212, sharex=plt1)
        plt2.plot(yplane[0::8,vslice], rgbdata[0::8,vslice,0],'r')
        plt2.plot(yplane[0::8,vslice], rgbdata[0::8,vslice,1],'g')
        plt2.plot(yplane[0::8,vslice], rgbdata[0::8,vslice,2],'b')

        plt.show()

    case 2:
        #Intended for images generated using create_jpeg.py modes 0 and 1
        h = rgbdata.shape[0]
        w = rgbdata.shape[1]
        mod_data = np.matmul(raw_data, raw_to_jpeg_matrix.T)
        for i in range(3):
            plt.figure()
            rdslice = mod_data[0::8,int((w/3)*i + w/6), :]
            plt1 = plt.subplot(211)
            plt1.plot(rdslice[:,0], 'r')
            plt1.plot(rdslice[:,1], 'g')
            plt1.plot(rdslice[:,2], 'b')
            plt2 = plt.subplot(212, sharex=plt1)
            plt2.plot(rgbdata[0::8,int((w/3)*i + w/6), 0], 'r')
            plt2.plot(rgbdata[0::8,int((w/3)*i + w/6), 1], 'g')
            plt2.plot(rgbdata[0::8,int((w/3)*i + w/6), 2], 'b')

            plt.figure()
            plt.plot(rgbdata[0::8,int((w/3)*i + w/6), 0], rdslice[:,0],'r')
            plt.plot(rgbdata[0::8,int((w/3)*i + w/6), 1], rdslice[:,1],'g')
            plt.plot(rgbdata[0::8,int((w/3)*i + w/6), 2], rdslice[:,2],'b')
            x = np.linspace(0,255,2000)
            plt.plot(x, xt.linearize_code(x), 'k')
            

        w6 = int(w/6)
        raw_data=raw_data[0::8,w6::2*w6,:]
        raw_data = np.reshape(raw_data,(raw_data.shape[0]*raw_data.shape[1],raw_data.shape[2]))
        lum_data = np.log2(np.amax(raw_data/65281.0,axis=1))
        lumidx = np.argsort(lum_data)
        raw_data = raw_data[lumidx]
        lum_data = lum_data[lumidx]
        print(lum_data.shape)
        cplot = colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1931(raw_data,colourspace=colorspace_raw,scatter_kwargs={'s':1,'c':lum_data},show=False)
        cplot[0].colorbar(cplot[1].collections[2],ax=cplot[1])
        cplot = colour.plotting.plot_planckian_locus_in_chromaticity_diagram_CIE1931(['A','D50','D65'],axes=cplot[1],show=False)
        cplot = colour.plotting.plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931([colorspace_raw, colorspace_jpeg, colour.models.RGB_COLOURSPACE_sRGB],axes=cplot[1],show=False)
        plt.show()