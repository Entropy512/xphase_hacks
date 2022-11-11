#!/usr/bin/env python3

import rawpy
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

rawfile = rawpy.imread('IMG_00_0.dng')

jpgfile = cv2.cvtColor(cv2.imread('IMG_00_0.jpg'),cv2.COLOR_BGR2RGB)

#print(rawfile.camera_whitebalance)
#print(rawfile.color_matrix)
#print(rawfile.rgb_xyz_matrix)
#print(rawfile.white_level)
#print(rawfile.raw_pattern)
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

B_jpg = jpgfile[0:,0:,2]
G_jpg = jpgfile[0:,0:,1]
R_jpg = jpgfile[0:,0:,0]

#we should check for nonequal shapes, but this is a very
#specific data analysis script
#h = jpgfile.shape[0]
#w = jpgfile.shape[1]
#lut = np.zeros(256)

#for y in range(h):
#    lut[R_jpg[y][0]] = R_raw[y][0]
matrix_jpg2camrgb = np.array([[ 0.74222153,  0.14044039,  0.11733808],
                              [ 0.20818888,  0.60000388,  0.19180724],
                              [ 0.102492  ,  0.15562963,  0.74187837]])

matrix_camrgb2srgb = np.linalg.inv(matrix_srgb2camrgb)

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

#print(repr(lut))
ilut = np.arange(0.0,65281.0,1.0)
ilut_flor = np.digitize(ilut,lut,right=True)

print(raw_data.shape)
print(jpgfile.shape)
lkup_data = ilut_flor[raw_data.astype(np.int16)]
print(lkup_data.shape)
print(np.amax(raw_data))
print(np.amin(raw_data))
print(np.amax(lkup_data))
print(np.amin(lkup_data))
#plt.plot(1.0/np.diff(np.log2(lut/65535.0)))
#plt.plot(codevals_xphase[:-1], 1.0/np.diff(np.log2(outputs_srgb/65535.0)))
#plt.plot(codevals_xphase[:-1], 1.0/np.diff(np.log2(outputs_gamma/65535.0)))
#plt.show()
jpg_expand = lut[jpgfile]
print(jpg_expand.shape)
print(np.amax(jpg_expand))
inp_ref = jpg_expand[100:,408::816,:]
out_ref = raw_data[100:,408::816,:]
ref_len = inp_ref.shape[0]*inp_ref.shape[1]
inp_ref = np.reshape(inp_ref,(ref_len,3))
out_ref = np.reshape(out_ref,(ref_len,3))
#print(inp_ref.shape)
#print(inp_ref)
#print(out_ref)
ccm = np.linalg.pinv(inp_ref/255.0).dot(out_ref/255.0)
print(np.mean(np.sum(ccm,axis=0)))
#ccm /= np.mean(np.sum(ccm,axis=0))
print(repr(ccm))
#print(np.mean(np.sum(ccm,axis=0)))

yuvdata = cv2.cvtColor(jpgfile,cv2.COLOR_RGB2YUV)/255.0

srgbraw_data = np.matmul(raw_data/65535.0,matrix_camrgb2srgb)
#srgbraw_data = raw_data/65535.0
if(0):
    plt.figure(1)
    plt.imshow(np.power(np.matmul(jpg_expand,ccm)/65535.0,1/2.4))
    plt.title('Corrected Input')
    plt.figure(2)
    plt.imshow(np.power(raw_data/65535.0,1/2.4))
    plt.title('DNG with nonlinear transform')
    plt.show()
else:
    plt.figure(1)
    plt1 = plt.subplot(311)
    plt1.plot(yuvdata[0:256*8:8,408*3,0],'k')
    plt1.plot(srgbraw_data[0:256*8:8,408*3,0],'r')
    plt1.plot(srgbraw_data[0:256*8:8,408*3,1],'g')
    plt1.plot(srgbraw_data[0:256*8:8,408*3,2],'b')
    plt2 = plt.subplot(312,sharex=plt1)
    plt2.plot(yuvdata[0:256*8:8,408*5,0],'k')
    plt2.plot(srgbraw_data[0:256*8:8,408*5,0],'r')
    plt2.plot(srgbraw_data[0:256*8:8,408*5,1],'g')
    plt2.plot(srgbraw_data[0:256*8:8,408*5,2],'b')
    plt3 = plt.subplot(313,sharex=plt1)
    plt3.plot(yuvdata[0:256*8:8,408*7,0],'k')
    plt3.plot(srgbraw_data[0:256*8:8,408*7,0],'r')
    plt3.plot(srgbraw_data[0:256*8:8,408*7,1],'g')
    plt3.plot(srgbraw_data[0:256*8:8,408*7,2],'b')
    #plt.figure(2)
    #plt.plot(jpgfile[0:,408*3,0],jpgfile[0:,408*3,0]/lkup_data[0:,408*3,0])
    #plt.figure(3)
    #plt.plot(R_raw/R_jpg)
    plt.show()
