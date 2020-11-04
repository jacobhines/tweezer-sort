# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:34:34 2020

@author: Jacob
"""

import numpy as np
import scipy.constants as cnst

class Laser():
    def __init__(self, wavelength, power, waist):
        """
        Parameters
        ----------
        wavelength : float
            wavelength in m.
        power : float
            power in W.
        waist : float or iterable of len 2
            beam waist in m.
        """
        
        self.wavelength = wavelength
        self.power = power
        
        # waist should be a length 2 iterable
        try:
            iter(waist)
            assert(len(waist)==2)
        except TypeError:
            waist = (waist, waist)
        else:
            raise Exception('Waist must be a scalar or a length-2 iterable')
        
        self.waist = waist
        (waist_x, waist_y) = waist
        
        self.intensity = 2*power/(np.pi*waist_x*waist_y) #W/m2
        self.frequency = cnst.c / (self.wavelength*1e-9) #Hz