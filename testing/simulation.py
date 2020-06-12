# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:42:29 2020

@author: Jacob
"""

import tweezerlyze as tz
from tweezerlyze.simulation.steck import cesium
from tweezerlyze.simulation.experiment import Experiment
import numpy as np

atom_options = {
    'species': cesium,
    'p_filling':0.6,
    'temperature': 20, #uK
    }

tweezer_options = {
    'n_sites': (1,1), #int
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
    'xmin': 0,
    'xmax': 50,
    'ymin': 0,
    'ymax': 50,
    }
    
expt.show_atoms(roi)

np.save('atoms_reference.npy', expt.imaging.camera.image_cropped)