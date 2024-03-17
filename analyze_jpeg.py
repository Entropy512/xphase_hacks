#!/usr/bin/env python3

import cv2
from turbojpeg import TurboJPEG, TJPF_GRAY, TJSAMP_GRAY, TJFLAG_PROGRESSIVE
import colour
import sys
import numpy as np
import matplotlib.pyplot as plt

jpeg = TurboJPEG()


xpdmatrix = np.matrix([[1.69266987, -0.5626429913, -0.08418130087],
                    [-0.3848780093, 1.108350039, 0.3184210059],
                    [-0.0598646994, 0.1917970028, 1.04934001]])

xpdmatrix_inv = np.linalg.inv(xpdmatrix)
xpdprim = colour.primaries_whitepoint(xpdmatrix_inv)[0]
xpdwht = colour.primaries_whitepoint(xpdmatrix_inv)[1]
print(xpdprim)
xphasedng_cs = colour.models.RGB_Colourspace('XPhase DNG', xpdprim, xpdwht, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

#colour.plotting.plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(colourspaces=[xphasedng_cs])
d65_whitepoint = np.array([0.3127, 0.3290])
srgb_prim = np.array([0.64, 0.33,
                      0.30, 0.60,
                      0.15, 0.06])

srgb_cs = colour.models.RGB_Colourspace('sRGB', srgb_prim, d65_whitepoint, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

dng_cmat = np.array([[ 0.74154849,  0.20734154,  0.10171785],
                    [ 0.14347096,  0.62066485,  0.15853842],
                    [ 0.11812658,  0.19156313,  0.73891836]])
xpjmatrix_inv = np.matmul(xpdmatrix_inv, dng_cmat)
xpjprim = colour.primaries_whitepoint(xpjmatrix_inv)[0]
xpjwht = colour.primaries_whitepoint(xpjmatrix_inv)[1]
print(xpjprim)
xphasejpg_cs = colour.models.RGB_Colourspace('XPhase JPG', xpjprim, xpjwht, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

xpswht = xpdwht
xpsprim = (xpdprim-xpdwht)*0.5 + xpdwht
xphasescl_cs = colour.models.RGB_Colourspace('XPhase Scale', xpsprim, xpswht, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

#Where the heck did I get this from???
#Linearizing Zwikel's colorchecker shot and then dcamprofing it???
primaries_jpeg = np.array([[0.567968, 0.368446],
                           [0.30249, 0.64607],
                           [0.1293, 0.006655]])
whitepoint_jpeg = np.array([0.34567, 0.3585])
colorspace_jpeg = colour.models.RGB_Colourspace('JPEG color space', primaries_jpeg, whitepoint_jpeg, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

cplot = cplot = colour.plotting.plot_planckian_locus_in_chromaticity_diagram_CIE1931(['A','D50','D65'],standalone=False)
colour.plotting.plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(axes=cplot[1], colourspaces=[xphasejpg_cs, xphasedng_cs, xphasescl_cs, colorspace_jpeg])
plt.show()

lut = np.array([1.0000e+00, 1.0000e+00, 1.0000e+00, 1.0000e+00, 1.0000e+00,
       1.0000e+00, 1.0000e+00, 1.0000e+00, 1.0000e+00, 1.0000e+00,
       1.0000e+00, 1.0000e+00, 1.0000e+00, 1.0000e+00, 1.0000e+00,
       1.0000e+00, 1.0000e+00, 1.0000e+00, 1.0000e+00, 1.0000e+00,
       1.0000e+00, 1.0000e+00, 1.0000e+00, 1.0000e+00, 4.1000e+01,
       8.7000e+01, 1.3400e+02, 1.8100e+02, 2.5100e+02, 2.9800e+02,
       3.4500e+02, 3.9100e+02, 4.6100e+02, 5.0800e+02, 5.5500e+02,
       6.2500e+02, 6.7200e+02, 7.4200e+02, 7.8900e+02, 8.5900e+02,
       9.0600e+02, 9.7600e+02, 1.0460e+03, 1.1160e+03, 1.1630e+03,
       1.2330e+03, 1.3030e+03, 1.3740e+03, 1.4440e+03, 1.5140e+03,
       1.5840e+03, 1.6540e+03, 1.7240e+03, 1.8180e+03, 1.8880e+03,
       1.9580e+03, 2.0520e+03, 2.1220e+03, 2.2160e+03, 2.2860e+03,
       2.3790e+03, 2.4730e+03, 2.5430e+03, 2.6370e+03, 2.7300e+03,
       2.8240e+03, 2.9170e+03, 3.0110e+03, 3.1040e+03, 3.1980e+03,
       3.3150e+03, 3.4080e+03, 3.5020e+03, 3.6190e+03, 3.7120e+03,
       3.8290e+03, 3.9230e+03, 4.0400e+03, 4.1570e+03, 4.2740e+03,
       4.3910e+03, 4.5080e+03, 4.6240e+03, 4.7410e+03, 4.8580e+03,
       4.9990e+03, 5.1160e+03, 5.2560e+03, 5.3730e+03, 5.5130e+03,
       5.6540e+03, 5.7700e+03, 5.9110e+03, 6.0750e+03, 6.2150e+03,
       6.3550e+03, 6.4960e+03, 6.6360e+03, 6.8000e+03, 6.9630e+03,
       7.1040e+03, 7.2670e+03, 7.4310e+03, 7.5950e+03, 7.7580e+03,
       7.9460e+03, 8.1090e+03, 8.2730e+03, 8.4600e+03, 8.6470e+03,
       8.8110e+03, 8.9980e+03, 9.1850e+03, 9.3720e+03, 9.5590e+03,
       9.7700e+03, 9.9800e+03, 1.0167e+04, 1.0378e+04, 1.0588e+04,
       1.0799e+04, 1.1009e+04, 1.1243e+04, 1.1454e+04, 1.1664e+04,
       1.1898e+04, 1.2132e+04, 1.2366e+04, 1.2600e+04, 1.2857e+04,
       1.3091e+04, 1.3348e+04, 1.3582e+04, 1.3839e+04, 1.4097e+04,
       1.4377e+04, 1.4634e+04, 1.4915e+04, 1.5172e+04, 1.5453e+04,
       1.5734e+04, 1.6014e+04, 1.6318e+04, 1.6599e+04, 1.6903e+04,
       1.7207e+04, 1.7511e+04, 1.7839e+04, 1.8143e+04, 1.8470e+04,
       1.8797e+04, 1.9125e+04, 1.9452e+04, 1.9803e+04, 2.0154e+04,
       2.0481e+04, 2.0832e+04, 2.1206e+04, 2.1557e+04, 2.1931e+04,
       2.2306e+04, 2.2680e+04, 2.3077e+04, 2.3452e+04, 2.3849e+04,
       2.4247e+04, 2.4668e+04, 2.5065e+04, 2.5486e+04, 2.5907e+04,
       2.6352e+04, 2.6796e+04, 2.7217e+04, 2.7685e+04, 2.8129e+04,
       2.8573e+04, 2.9041e+04, 2.9532e+04, 3.0000e+04, 3.0515e+04,
       3.0982e+04, 3.1474e+04, 3.2011e+04, 3.2503e+04, 3.3017e+04,
       3.3555e+04, 3.4070e+04, 3.4631e+04, 3.5169e+04, 3.5754e+04,
       3.6291e+04, 3.6876e+04, 3.7461e+04, 3.8022e+04, 3.8630e+04,
       3.9238e+04, 3.9846e+04, 4.0478e+04, 4.1109e+04, 4.1717e+04,
       4.2396e+04, 4.3027e+04, 4.3682e+04, 4.4384e+04, 4.5038e+04,
       4.5740e+04, 4.6442e+04, 4.7143e+04, 4.7845e+04, 4.8593e+04,
       4.9342e+04, 5.0043e+04, 5.0839e+04, 5.1587e+04, 5.2359e+04,
       5.3154e+04, 5.3949e+04, 5.4744e+04, 5.5563e+04, 5.6405e+04,
       5.7223e+04, 5.8065e+04, 5.8931e+04, 5.9843e+04, 6.0685e+04,
       6.1597e+04, 6.2509e+04, 6.3421e+04, 6.4333e+04, 6.5281e+04,
       6.5281e+04, 6.5281e+04, 6.5281e+04, 6.5281e+04, 6.5281e+04,
       6.5281e+04, 6.5281e+04, 6.5281e+04, 6.5281e+04, 6.5281e+04,
       6.5281e+04, 6.5281e+04, 6.5281e+04, 6.5281e+04, 6.5281e+04,
       6.5281e+04, 6.5281e+04, 6.5281e+04, 6.5281e+04, 6.5281e+04,
       6.5281e+04, 6.5281e+04, 6.5281e+04, 6.5281e+04, 6.5281e+04,
       6.5281e+04])
#LUT output maxes out at 65281
lut /= 65281.0

#make LUT output sRGB instead of linear
#lut = np.where(lut <=0.0031308,12.92*lut,1.055*np.power(lut,1/2.4)-0.055)


with open(sys.argv[1], 'rb') as infile:
    planes = jpeg.decode_to_yuv_planes(infile.read())
    y = planes[0]/255.0
    y = y[0::2,0::2]
    u = (planes[1]-128.0)/255.0

    v = (planes[2]-128.0)/255.0

    if(1):
       h = v.shape[0]
       w = v.shape[1]
       imgdata_yuv = np.dstack((y,u,v))
       #print(imgdata_yuv[0])
       imgdata_rgb = np.matmul(imgdata_yuv,yuv_rgb_matrix.T)
       imgdata_rgb = imgdata_rgb * 255.0
       imgdata_rgb = np.minimum(np.maximum(imgdata_rgb,0),255).astype(np.uint8)
       imgdata_rgb = lut[imgdata_rgb]
       imgdata_rgb = np.clip(np.matmul(imgdata_rgb,cnvmatrix.T),0.0,1.0)
       imgdata_rgb = np.where(imgdata_rgb <=0.0031308,12.92*imgdata_rgb,1.055*np.power(imgdata_rgb,1/2.4)-0.055)
       imgdata_rgb = np.fliplr(np.flipud(imgdata_rgb))
       #    imgdata_rgb = imgdata_rgb.reshape(imgdata_yuv.shape)


       #    ydata = planes[0]
       #    yhist = np.histogram(ydata,256,range=(0,1))[0]
       #    print(np.count_nonzero(yhist))

       plt.imshow(imgdata_rgb)
       plt.show()

    else:
        plt.figure()
        plt.imshow(y)
        plt.title('Y')
        plt.figure()
        plt.imshow(u)
        plt.title('U')
        plt.figure()
        plt.imshow(v)
        plt.title('V')
        plt.show()
