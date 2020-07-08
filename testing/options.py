# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 18:50:05 2020

@author: Jacob
"""
import numpy as np



from tweezerlyze.calculation.steck import cesium

atom_options = {
    'species': cesium,
    'p_filling':0.5,
    'temperature': 20, #uK
    }

tweezer_options = {
    'n_sites': (10,10), #int
    'spacing': (5,5), #um
    'angle': 0*np.pi/6, #rad
    'wavelength': 1064, #nm
    'power': 100, #mW
    'waist': 1, #um
    'offset': (0,0) #um
    }

optics_options = {
    'magnification': 500/40,
    'NA': 0.6,
    }

camera_options = {
    'pixel_size': (13.5, 13.5), #um
    'sensor_size': (1024, 1024), #px
    'gain': 10,
    'position': (4, 4), #px
    'noise_mean': 500, 
    'noise_std': 10,
    }

imaging_laser_options = {
    'wavelength': cesium.D2.wavelength,
    'power': 1, #mW
    'waist': 1e3, #um
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