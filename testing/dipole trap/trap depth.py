# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 11:29:45 2020

@author: Jacob
"""

from tweezerlyze.calculation.dipoletrap import depth_grimm_classical, depth_steck_classical, depth_steck_quantum
import numpy as np

kwargs = {
    'power': 0.0225,
    'waist': 1e-6,
    'verbose': False,
    'unit': 'MHz',
    }

d_grimm_classical = depth_grimm_classical(**kwargs)
d_steck_classical = depth_steck_classical(polarization='pi', **kwargs)
d_steck_quantum = depth_steck_quantum(**kwargs)

print('d_grimm_classical =', np.round(d_grimm_classical, 3), kwargs['unit'])
print('d_steck_classical =', np.round(d_steck_classical, 3), kwargs['unit'])
print('d_steck_quantum =', np.round(d_steck_quantum, 3), kwargs['unit'])