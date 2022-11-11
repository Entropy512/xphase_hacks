#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

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

#ilut = np.arange(0.0,65536.0,1.0)
#ilut_flor = np.digitize(ilut,lut)

#plt.plot(ilut_flor)
#plt.show()

codevals_xphase = np.arange(23.0,229.0,1.)
outputs_hlg = []
hlg_a = 0.17883277
hlg_b = 0.28466892
hlg_c = 0.55991073

for j in codevals_xphase:
    dataval = (j-23.0)/(229.0-23.0)
    if(dataval < 0.5):
        outputs_hlg.append(4*dataval**2)
    else:
        outputs_hlg.append(np.exp((dataval-hlg_c)/hlg_a)+hlg_b)

outputs_hlg = np.array(outputs_hlg)
datavals_xphase = codevals_xphase-23
ncv = 229-23
lut = lut/np.amax(lut)

codevals_xphase = codevals_xphase.astype(np.uint8)

codevals_lin8 = np.arange(0.0, 256.0, 1.0)
codevals_lin10 = np.arange(0.0, 1024.0, 1.0)
cvthresh = 69.0
evdelt = np.log2(cvthresh/1023.0)
cvdens = (cvthresh-255.0)/evdelt

altvals = np.where(codevals_lin10 <= cvthresh, codevals_lin10, cvthresh+cvdens*np.log2(codevals_lin10/cvthresh))

altlog = np.where(codevals_lin8 <= cvthresh, codevals_lin8, cvthresh*np.power(2.0, (codevals_lin8-cvthresh)/cvdens))


plt.plot(np.log2(lut[codevals_xphase])[:-1],1.0/np.diff(np.log2(lut[codevals_xphase])), label='Xphase JPEG')
plt.plot(np.log2(codevals_lin10/1023.0)[:-1],1.0/np.diff(np.log2(codevals_lin10/1023.0)), label='Xphase RAW')
plt.plot(np.log2(altlog/1023.0)[:-1],1.0/np.diff(np.log2(altlog/1023.0)), label='Alternate log formula')
plt.axhline(y=1.0/np.log2(1.05), alpha=0.5, color='k', dashes=(5,1,2,1), label='Human dim threshold (5%)')
plt.axhline(y=1.0/np.log2(1.02), alpha=0.5, color='k', dashes=(2,2), label='Human bright threshold (2%)')
#plt.axhline(y=1.0/np.log2(1.01), alpha=0.5, color='k', dashes=(2,1), label='Human bright threshold (1%)')

#plt.semilogy(codevals_xphase,65535*np.power((codevals_xphase-23)/(229-23),2.4))
#plt.semilogy(codevals_xphase,65535*np.power((codevals_xphase-23)/(229-23),2.6))
#plt.semilogy(codevals_xphase,outputs_hlg*65535.0/12.0)
#plt.semilogy(codevals_xphase,65536*np.power(2,(datavals_xphase-ncv)/40))
plt.xlabel('EV from Sensor Clip')
plt.ylabel('Code values per EV')
plt.legend()
plt.show()
