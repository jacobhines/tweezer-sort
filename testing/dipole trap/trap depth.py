# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 11:29:45 2020

@author: Jacob
"""

from tweezerlyze.calculation.dipoletrap import depthGrimmClassical, depthSteckClassical, depthSteckQuantum
import numpy as np

kwargs = {
    'power': 10e-3, #W
    'waist': 1e-6, #M
    'verbose': False,
    'unit': 'uK',
    }

dp = 5

d_grimm_classical = depthGrimmClassical(**kwargs)
d_steck_classical = depthSteckClassical(polarization='pi', **kwargs)
d_steck_quantum = depthSteckQuantum(**kwargs)

print('d_grimm_classical =', np.round(d_grimm_classical, dp), kwargs['unit'])
print('d_steck_classical =', np.round(d_steck_classical, dp), kwargs['unit'])
print('d_steck_quantum =', np.round(d_steck_quantum, dp), kwargs['unit'])