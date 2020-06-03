# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:33:18 2020

@author: Jacob
"""

from steck import cesium
from atoms import Atoms
from geometry import Tweezers
from imaging import Imaging

import numpy as np


class Experiment:
    def __init__(self, atom_options, tweezer_options, imaging_options):
        self.atoms = Atoms(**atom_options)
        
        self.geometry = Tweezers(**tweezer_options)
        self.geometry.set_trap_depth(atoms=self.atoms, verbose=False)
        self.geometry.set_sigma_thermal(atoms=self.atoms, verbose=True)
        
        self.imaging = Imaging(**imaging_options)
        self.imaging.set_scattering_rate(scattering_rate = imaging_options['scattering_rate'])
        
        
        

        
    def load_atoms(self):
        self.atoms.load_atoms(self.geometry.positions)
        
    def image_atoms(self, imaging_time):
        # generate fluorescence photons
        photon_positions = self.atoms.generate_photons(self.imaging.scattering_rate,
                                                       self.geometry.sigma_thermal,
                                                       imaging_time)
        
        # propagate them through the imaging optics
        photon_positions = self.imaging.optics.apply_diffraction(photon_positions)
        
        # collect them on the camera
        self.imaging.camera.expose(photon_positions)
        
    def show_atoms(self, roi, scalebar=True, scalebar_length=None):
        if scalebar_length is None:
            scalebar_length = self.geometry.spacing[0]
        self.imaging.camera.show_image(roi, scalebar, scalebar_length)
        
        
if __name__ == '__main__':
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
        'scattering_rate': 100
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