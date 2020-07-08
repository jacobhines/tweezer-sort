# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 20:48:10 2020

@author: Jacob
"""

import numpy as np
from skimage.metrics import peak_signal_noise_ratio

def getFidelity(mask1, mask2):
    return np.mean(mask1 == mask2)

def getSNR(signal_mean, noise_std, area, quadrature=False):
    qty = (signal_mean/area)/noise_std
    if quadrature:
        return qty**2
    else: 
        return qty

def getPSNR(image_true, image_test, offset=0):
    image_true -= offset
    image_test -= offset
    return peak_signal_noise_ratio(image_true,
                                   image_test,
                                   data_range=np.max(image_true).astype(int))