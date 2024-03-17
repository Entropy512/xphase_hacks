#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from xphase_data import XphaseTransfer

dta = [XphaseTransfer().lut]

codes = np.arange(256)
for c in [3231, 3600, 3800, 4000]:
    dta.append(XphaseTransfer(c).linearize_code(codes))

for p in dta:
    plt.plot(p)


plt.figure()
for p in dta:
    plt.plot(np.log2(p))

plt.figure()
for p in dta:
    plt.plot(1.0/np.diff(np.log2(p)))

plt.show()