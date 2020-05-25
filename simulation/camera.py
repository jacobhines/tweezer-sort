# -*- coding: utf-8 -*-
"""
Created on Sun May 24 15:15:51 2020

@author: Jacob
"""
import numpy as np
from geometry import Tweezers
from atoms import Atoms

class AndorIxon():
    def init(self, pixel_size, magnification, display_size, exposure, 
             dark_mean, dark_std, **kwargs):
        self.pixel_size = pixel_size
        self.magnification = magnification
        self.display_size = display_size
        self.exposure = exposure
        self.dark_mean = dark_mean
        self.dark_std = dark_std
        self.image = None
        
    def expose(self, atoms):
        """
        Simulates exposure of camera with given noise properties on atoms.

        Parameters
        ----------
        atoms : list
            Atom instances that fluoresce during exposure.

        Returns
        -------
        None.

        """
        self.image = np.random.normal(self.dark_mean, self.dark_std, self.display_size)
        #TODO: add atoms
        
    
    def grab_image(self):
        """
        Returns most recently exposed image.

        Returns
        -------
        self.image: ndarray
            Fluorescent counts in a 2D array.

        """
        return self.image
    
    
if __name__ == '__main__':
    n_sites = (15,10)
    spacing = (5,5)
    angle = np.pi/6
    
    T = Tweezers(n_sites, spacing, angle)
    T.plot_sites()
    
    p_filling = 1
    A = Atoms(p_filling)
    
    sigma = 0.5
    A.generate_atoms(T.site_positions, sigma)
    A.plot_atoms()