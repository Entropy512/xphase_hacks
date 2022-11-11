#!/usr/bin/env python3

import rawpy
import colour
import numpy as np
import matplotlib.pyplot as plt
import sys

rawfile = rawpy.imread(sys.argv[1])

#print(rawfile.camera_whitebalance)
#print(rawfile.white_level)
#print(rawfile.raw_pattern)
bayer_pattern = rawfile.raw_pattern
print(bayer_pattern)
bayer_data = rawfile.raw_image_visible.astype('float64')
#zwickel's colorchecker shot has corners of:
#(1431,920), (1950,920), (1425,1646), (1956,1650)
#so let's take 1424-1950 and 920-1650

#pseudohald is 3416x2420
#bayer_data = bayer_data[0:2421,0:3147,:]

if(bayer_pattern is not None):
    iRrow,  iRclmn  = np.argwhere(bayer_pattern == 0)[0]
    iG0row, iG0clmn = np.argwhere(bayer_pattern == 1)[0]
    iBrow,  iBclmn  = np.argwhere(bayer_pattern == 2)[0]
    iG1row, iG1clmn = np.argwhere(bayer_pattern == 3)[0]
    bayer_data = bayer_data[920:1652, 1424:1952]
    print(bayer_data.shape)
    R  = bayer_data[ iRrow::2,  iRclmn::2]
    G = bayer_data[iG0row::2, iG0clmn::2]
    G1 = bayer_data[iG1row::2, iG1clmn::2]
    B  = bayer_data[ iBrow::2,  iBclmn::2]
    raw_data = np.zeros((R.shape[0],R.shape[1],3))
    raw_data[0:,0:,0] = R
    raw_data[0:,0:,1] = (G + G1)/2
    raw_data[0:,0:,2] = B
else:
    bayer_data = bayer_data[920:1652, 1424:1952,:]
    R = bayer_data[0:,0:,0]
    G = bayer_data[0:,0:,1]
    B = bayer_data[0:,0:,2]
    raw_data = bayer_data[0::2,0::2,0:3]

#raw_data = raw_data[0::2, 0::2, :]

color_matrix_raw = np.matrix([[1.69266987, -0.5626429913, -0.08418130087],
                              [-0.3848780093, 1.108350039, 0.3184210059],
                              [-0.0598646994, 0.1917970028, 1.04934001]])
invmatrix_raw = np.linalg.inv(color_matrix_raw)
primaries_raw = colour.primaries_whitepoint(invmatrix_raw)[0]
whitepoint_raw = colour.primaries_whitepoint(invmatrix_raw)[1]
colorspace_raw = colour.models.RGB_Colourspace('RAW color space', primaries_raw, whitepoint_raw, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

primaries_jpeg = np.array([[0.567968, 0.368446],
                           [0.30249, 0.64607],
                           [0.1293, 0.006655]])
whitepoint_jpeg = np.array([0.34567, 0.3585])
colorspace_jpeg = colour.models.RGB_Colourspace('JPEG color space', primaries_jpeg, whitepoint_jpeg, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

raw_to_jpeg_matrix = colour.matrix_RGB_to_RGB(colorspace_raw, colorspace_jpeg)

rhist = np.histogram(R, 65536, range=(0,65535))[0]
ghist = np.histogram(G, 65536, range=(0,65535))[0]
bhist = np.histogram(B, 65536, range=(0,65535))[0]

print(np.count_nonzero(rhist))
print(np.count_nonzero(ghist))
print(np.count_nonzero(bhist))

raw_data = raw_data/65535.0
print(raw_data.shape)
print(raw_data[...,0].shape)
if(0):
    #bayer_data = bayer_data[0::2,0::2,0:]

    plt1 = plt.subplot(311)
    plt1.semilogy(rhist,'r', label='Red histogram')
    plt2 = plt.subplot(312, sharex=plt1)
    plt2.semilogy(ghist,'g', label='Green histogram')
    plt3 = plt.subplot(313, sharex=plt1)
    plt3.semilogy(bhist,'b', label='Blue histogram')

    plt.show()
elif(0):
    jpeg_data = np.matmul(raw_data,raw_to_jpeg_matrix.T)
    print(jpeg_data.shape)
    plt.figure(1)
    plt1 = plt.subplot(311)
    plt1.plot(jpeg_data[0:, 272,0],'r')
    plt1.plot(jpeg_data[0:, 272,1],'g')
    plt1.plot(jpeg_data[0:, 272,2],'b')
    plt2 = plt.subplot(312,sharex=plt1)
    plt2.plot(jpeg_data[0:,272*3,0],'r')
    plt2.plot(jpeg_data[0:,272*3,1],'g')
    plt2.plot(jpeg_data[0:,272*3,2],'b')
    plt3 = plt.subplot(313,sharex=plt1)
    plt3.plot(jpeg_data[0:,272*5,0],'r')
    plt3.plot(jpeg_data[0:,272*5,1],'g')
    plt3.plot(jpeg_data[0:,272*5,2],'b')
    plt.show()
else:
    #raw_data = raw_data[0:,272::544,0:]
    raw_data = np.reshape(raw_data,(raw_data.shape[0]*raw_data.shape[1],raw_data.shape[2]))
    print(raw_data.shape)
    lum_data = np.power(np.amax(raw_data,axis=1),1/2.4)
    lumidx = np.argsort(lum_data)
    raw_data = raw_data[lumidx]
    lum_data = lum_data[lumidx]
    print(lum_data.shape)
    cplot = colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1931(raw_data,colourspace=colorspace_raw,scatter_kwargs={'s':1,'c':lum_data},standalone=False)
    cplot = colour.plotting.plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931([colorspace_raw, colorspace_jpeg, colour.models.RGB_COLOURSPACE_sRGB],axes=cplot[1],standalone=False)
    cplot[0].colorbar(cplot[1].collections[2],ax=cplot[1])
    cplot = colour.plotting.plot_planckian_locus_in_chromaticity_diagram_CIE1931(['A','D50','D65'],axes=cplot[1],standalone=False)
    plt.show()
