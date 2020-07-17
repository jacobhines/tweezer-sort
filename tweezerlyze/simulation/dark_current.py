# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 18:14:50 2020

@author: Jacob
"""

import numpy as np

D1 = 2.5e-4
D2 = 1.1e-4

T1 = -80 + 273.15
T2 = -100 + 273.15

dT = 1/(1/T2 - 1/T1)

epsilon = -dT * np.log(D2/D1)
print('epsilon', epsilon)

D0 = D1*np.exp(epsilon/T1)

print('D0', D0)