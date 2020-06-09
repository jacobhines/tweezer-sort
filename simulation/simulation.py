# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:42:29 2020

@author: Jacob
"""

from steck import cesium
import numpy as np
from experiment import Experiment

atom_options = {
    'species': cesium,
    'p_filling': 0.6,
    'temperature': 20, #uK
    }

tweezer_options = {
    'n_sites': (10,10), #int
    'spacing': (5,5), #um
    'angle': np.pi/6, #rad
    'wavelength': 1064, #nm
    'power': 100, #mW
    'waist': 1, #um
    }

optics_options = {
    'magnification': 500/40,
    'NA': 0.6,
    }

camera_options = {
    'pixel_size': (13.5, 13.5), #um
    'sensor_size': (1024, 1024), #px
    'gain': 10,
    'position': (5, 5), #px
    'dark_mean': 500, 
    'dark_std': 10,
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
    'scattering_rate': 1000
    }

expt = Experiment(atom_options, tweezer_options, imaging_options)
expt.load_atoms()
expt.image_atoms(imaging_time=0.5)

roi = {
    'xmin':0,
    'xmax': 80,
    'ymin': 0,
    'ymax': 50,
    }
    
expt.show_atoms(roi)