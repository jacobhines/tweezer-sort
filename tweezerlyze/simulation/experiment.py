# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:33:18 2020

@author: Jacob
"""

from . atoms import Atoms
from . geometry import Tweezers
from . imaging import Imaging


class Experiment:
    def __init__(self, atom_options, tweezer_options, imaging_options):
        self.atoms = Atoms(**atom_options)
        
        self.geometry = Tweezers(**tweezer_options)
        self.geometry.set_trap_depth(atoms=self.atoms, verbose=False)
        self.geometry.set_sigma_thermal(atoms=self.atoms, verbose=False)
        
        self.imaging = Imaging(**imaging_options)
        self.imaging.set_rates(scattering_rate = imaging_options['scattering_rate'])

        
    def load_atoms(self):
        self.atoms.load_atoms(self.geometry.positions)
        self.geometry.occupation = self.atoms.occupation
        self.geometry.set_gt_mask()
        
    def image_atoms(self, imaging_time):
        # generate fluorescence photons
        photon_positions = self.atoms.generate_photons(self.imaging.collection_rate,
                                                       self.geometry.sigma_thermal,
                                                       imaging_time,
                                                       self.imaging.optics.collection_efficiency)
        
        # propagate them through the imaging optics
        photon_positions = self.imaging.optics.apply_diffraction(photon_positions)
        
        # collect them on the camera
        self.imaging.camera.expose(photon_positions)
        
    def show_atoms(self, image=None, roi=None, title=None, colorbar=False, scalebar=True, scalebar_length=None):
        if scalebar_length is None:
            scalebar_length = self.geometry.spacing[0]
            
        if roi is not None:
            self.imaging.camera.crop_image(roi)
            
        self.imaging.camera.show_image(image=image,
                                       cropped=bool(roi),
                                       colorbar=colorbar,
                                       title=title,
                                       scalebar=scalebar,
                                       scalebar_length=scalebar_length)