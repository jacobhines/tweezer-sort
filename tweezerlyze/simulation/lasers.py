# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:34:34 2020

@author: Jacob
"""

import numpy as np
from . import constants as cs

class Laser():
    def __init__(self, wavelength, power, waist):
        """
        Parameters
        ----------
        wavelength : float
            wavelength in nm.
        power : float
            power in mW.
        waist : TYPE
            beam waist in um.
        """
        self.wavelength = wavelength
        self.power = power
        self.waist = waist
        self.intensity = 2*power/(np.pi*((waist*1e-4)**2)) #mW/cm2
        self.frequency = 1e-12 * cs.c / (self.wavelength*1e-9) #THz