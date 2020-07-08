# -*- coding: utf-8 -*-
"""
Created on Mon May 25 20:56:40 2020

@author: Jacob
"""

class quantity(float):
    def __new__(self, value, unit):
        return float.__new__(self, value)
    def __init__(self, value, unit):
        float.__init__(value)
        self.unit = unit
        
c = quantity(2.99792458e8, 'm/s')
h = quantity(4.13566727e-15, 'eV*s')
hbar = quantity(6.58211889e-16, 'eV*s')
uK_per_MHz = 7.63823511
K_per_Hz = 7.63823511-12