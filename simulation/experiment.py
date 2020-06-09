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
        self.imaging.set_rates(scattering_rate = imaging_options['scattering_rate'])

        
    def load_atoms(self):
        self.atoms.load_atoms(self.geometry.positions)
        
    def image_atoms(self, imaging_time):
        # generate fluorescence photons
        photon_positions = self.atoms.generate_photons(self.imaging.collection_rate,
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