# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 18:50:05 2020

@author: Jacob
"""
import numpy as np
from tweezerlyze.calculation.steck import cesium

#All units are SI

atom_options = {
    'species': cesium,
    'p_filling':0.5,
    'temperature': 20*1e-6, #K
    }

tweezer_options = {
    'n_sites': (10,10), #int
    'spacing': (5e-6, 5e-6), #m
    'angle': 0*np.pi/6, #rad
    'wavelength': 1064e-9, #m
    'power': 10e-3, #W
    'waist': 1e-6, #m
    'offset': (0,0) #m
    }

optics_options = {
    'magnification': 500/40,
    'NA': 0.6,
    }

camera_options = {
    'pixel_size': (13.5e-6, 13.5e-6), #m
    'sensor_size': (1024, 1024), #px
    'gain': 100,
    'preamp_setting': 1, 
    'amplifier_type': 'EM',
    'readout_rate': 30e6, #Hz
    'sensor_temperature': -70+273.15, #K
    'exposure_time': 5e-3, #s
    'position': (4, 4), #px
    }

imaging_laser_options = {
    'wavelength': cesium.D2.wavelength,
    'power': 1e-3, #W
    'waist': 1e-3, #m
    }

imaging_options = {
    'camera_options': camera_options,
    'optics_options': optics_options,
    'laser_options': imaging_laser_options,
    'scattering_rate': 1
    }

experiment_options = {'atom_options': atom_options,
                      'tweezer_options': tweezer_options,
                      'imaging_options': imaging_options,
                      }