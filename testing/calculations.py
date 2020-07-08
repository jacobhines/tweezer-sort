# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 11:29:45 2020

@author: Jacob
"""

from tweezerlyze.calculation.dipoletrap import depth_oscillator, depth_steck_classical, depth_oscillator_rwa, depth_steck_quantum

verbose=False
unit = 'MHz'

d_osc = depth_oscillator(power=5, waist=50e-6, verbose=verbose, unit=unit)
d_steck_classical = depth_steck_classical(power=5, waist=50e-6, verbose=verbose, unit=unit)
d_apx = depth_oscillator_rwa(power=5, waist=50e-6, verbose=verbose, unit=unit)
d_steck_quantum = depth_steck_quantum(power=5, waist=50e-6, verbose=verbose, unit=unit, method='simplified')

print('d_osc =', d_osc, unit)
print('d_steck_classical =', d_steck_classical, unit)
print('d_apx =', d_apx, unit)
print('d_steck_quantum =', d_steck_quantum, unit)