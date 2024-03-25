#!/usr/bin/env python3

import rawpy
import colour
import numpy as np
import matplotlib.pyplot as plt
import sys
from pprint import pprint

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
    #bayer_data = bayer_data[920:1652, 1424:1952,:]
    R = bayer_data[0:,0:,0]
    G = bayer_data[0:,0:,1]
    B = bayer_data[0:,0:,2]
    raw_data = bayer_data[:,:,0:3]

#raw_data = raw_data[0::2, 0::2, :]

#DNG color matrix
color_matrix_raw = np.matrix([[1.69266987, -0.5626429913, -0.08418130087],
                              [-0.3848780093, 1.108350039, 0.3184210059],
                              [-0.0598646994, 0.1917970028, 1.04934001]])
invmatrix_raw = np.linalg.inv(color_matrix_raw)
primaries_raw = colour.primaries_whitepoint(invmatrix_raw)[0]
whitepoint_raw = colour.primaries_whitepoint(invmatrix_raw)[1]
colorspace_raw = colour.models.RGB_Colourspace('RAW color space', primaries_raw, whitepoint_raw, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

#Derived from feeding create_jpeg mode 2 (black = 23, white=229) to rawhist mode 3
primaries_jpeg = np.array([[0.56798193, 0.36842969],
                            [0.30254015, 0.64607483],
                            [0.12929368, 0.00665573]])
whitepoint_jpeg = np.array([0.34566994, 0.35849447])
colorspace_jpeg = colour.models.RGB_Colourspace('JPEG color space', primaries_jpeg, whitepoint_jpeg, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

# Derived from feeding create_jpeg mode 2 (black = 0, white=48) to rawhist mode 3
# code value 48 is approximately where Xphase's transfer function transitions the human 5% luminance difference threshold for
# dim areas (see page 7 of https://downloads.bbc.co.uk/rd/pubs/whp/whp-pdf-files/WHP309.pdf )
primaries_5pjpeg = np.array([[0.74342915, 0.26049418],
                            [0.2797885, 0.86006897],
                            [-0.07825801, -0.47043385]])
whitepoint_5pjpeg = np.array([0.34483413, 0.36421049])
colorspace_5pjpeg = colour.models.RGB_Colourspace('Wide JPEG color space, 5%BT', primaries_5pjpeg, whitepoint_5pjpeg, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

# Derived from feeding create_jpeg mode 2 (black = 0, white = somewhere between 110 and 140, I can't remember) to rawhist mode 3
# corresponds to 2% luminance difference which is the human banding threshold for bright areas
primaries_2pjpeg = np.array([[ 0.63250848,  0.37111425],
       [ 0.29017827,  0.7297941 ],
       [ 0.04997669, -0.12299537]])
whitepoint_2pjpeg = np.array([ 0.34509653,  0.36231756])
colorspace_2pjpeg = colour.models.RGB_Colourspace('Wide JPEG color space, 2%BT', primaries_2pjpeg, whitepoint_2pjpeg, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

rhist = np.histogram(R, 65536, range=(0,65535))[0]
ghist = np.histogram(G, 65536, range=(0,65535))[0]
bhist = np.histogram(B, 65536, range=(0,65535))[0]

print(np.count_nonzero(rhist))
print(np.count_nonzero(ghist))
print(np.count_nonzero(bhist))


print(raw_data.shape)
print(raw_data[...,0].shape)

mode = 3
match mode:
    case 0:
        #bayer_data = bayer_data[0::2,0::2,0:]

        plt1 = plt.subplot(311)
        plt1.semilogy(rhist,'r', label='Red histogram')
        plt2 = plt.subplot(312, sharex=plt1)
        plt2.semilogy(ghist,'g', label='Green histogram')
        plt3 = plt.subplot(313, sharex=plt1)
        plt3.semilogy(bhist,'b', label='Blue histogram')

        plt.show()
    case 1:
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
    case 2:
        #raw_data = raw_data[0:,272::544,0:]
        raw_data = np.reshape(raw_data,(raw_data.shape[0]*raw_data.shape[1],raw_data.shape[2]))
        print(raw_data.shape)
        lum_data = np.power(np.amax(raw_data,axis=1),1/2.4)
        lumidx = np.argsort(lum_data)
        raw_data = raw_data[lumidx]
        lum_data = lum_data[lumidx]
        print(lum_data.shape)
        cplot = colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1931(raw_data,colourspace=colorspace_raw,scatter_kwargs={'s':1,'c':lum_data},show=False)
        cplot[0].colorbar(cplot[1].collections[2],ax=cplot[1])
        cplot = colour.plotting.plot_planckian_locus_in_chromaticity_diagram_CIE1931(['A','D50','D65'],axes=cplot[1],show=False)
        cplot = colour.plotting.plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931([colorspace_raw, colorspace_jpeg, colour.models.RGB_COLOURSPACE_sRGB],axes=cplot[1],show=False)
        plt.show()
    case 3:
        w = raw_data.shape[1]
        border = 4
        skip = int(w/4)
        data = []
        for k in range(4):
            region = raw_data[border:-border,k*skip+border:(k+1)*skip-border]
            data.append(np.mean(np.mean(region, axis=0), axis=0))
        data = np.array(data)
        pprint(data)
        pprint(colour.RGB_to_XYZ(RGB=data, colourspace=colorspace_raw))
        pprint(colour.XYZ_to_xy(colour.RGB_to_XYZ(RGB=data, colourspace=colorspace_raw))[0:3])
        pprint(colour.XYZ_to_xy(colour.RGB_to_XYZ(RGB=data, colourspace=colorspace_raw))[3])
        colour.plotting.plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931([colorspace_raw, colorspace_jpeg, colorspace_2pjpeg, colorspace_5pjpeg, colour.models.RGB_COLOURSPACE_sRGB])
