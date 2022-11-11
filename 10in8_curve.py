#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

tonecurve = np.array([])

nblocks = 4
blocksize = 256/nblocks
for j in range(4):
    print(j)
    tonecurve = np.append(tonecurve, (np.power(2,j)-1)*(blocksize+1) + np.arange(blocksize) * np.power(2,j))

print(tonecurve[-1])
print(tonecurve[0])
plt.plot(tonecurve)
plt.figure()
plt.semilogy(tonecurve)
plt.figure()
plt.plot(1.0/np.diff(np.log2(tonecurve)))
plt.show()
