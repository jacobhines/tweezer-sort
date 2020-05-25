# -*- coding: utf-8 -*-
"""
Created on Sun May 24 15:15:51 2020

@author: Jacob
"""
import numpy as np
from geometry import Tweezers
from atoms import Atoms
import matplotlib.pyplot as plt

class AndorIxon():
    def __init__(self, pixel_size, magnification, display_size, exposure_time, 
             dark_mean, dark_std, gain, offset, **kwargs):
        self.pixel_size = pixel_size
        self.display_size = display_size
        self.magnification = magnification
        self.exposure_time = exposure_time
        self.dark_mean = dark_mean
        self.dark_std = dark_std
        self.gain = gain
        self.photon_positions = None
        self.image = None
        self.offset = offset
        
        pixel_bins_x = (np.arange(display_size[0]+1) - self.offset[0])*pixel_size[0]/magnification
        pixel_bins_y = (np.arange(display_size[1]+1) - self.offset[1])*pixel_size[1]/magnification
        self.pixel_bins = [pixel_bins_x, pixel_bins_y]
        
    def generate_photons(self, atoms, n_photons):
        """
        Simulates photon collection from atoms.

        Parameters
        ----------
        atoms : class
            Atom class
            
        n_photons : int
            number of photons scattered by each atom
        """
        # initialize n_photons at each atom
        photon_positions = np.tile(atoms.positions, (n_photons, 1, 1))
        photon_positions = np.transpose(photon_positions, axes=[1,2,0])
        
        #each photon is gaussian distributed
        photon_positions = np.random.normal(loc=photon_positions, scale=atoms.sigma_thermal)
        xarr = photon_positions[0,:]
        yarr = photon_positions[1,:]
        self.photon_positions = np.stack([xarr.flatten(), yarr.flatten()])
        
        return self.photon_positions
        
    def plot_photons(self):
        """
        Visualize the photons.
        """
        if self.photon_positions is None:
            raise Exception('Must run generate_photons() before plotting them.')
        
        fig, ax = plt.subplots(figsize=(10,10))
        r = self.photon_positions
        x = r[0, :]
        y = r[1, :]
        plt.scatter(x, y)
        plt.xlabel('x (um)')
        plt.ylabel('y (um)')
        ax.set_aspect('equal')
        plt.title('Photon positions')
        fig.patch.set_facecolor('white')
    
    def expose(self, atoms):      
        # each atom scatters n_photons #TODO: consider adding in NA 
        n_photons = int(self.exposure_time * atoms.scattering_rate)
        
        # simulate photon capture
        photon_positions = self.generate_photons(atoms, n_photons)
        
        # base image has background and thermal noise
        self.noise = np.random.normal(self.dark_mean, self.dark_std, self.display_size)
        
        # bin the photons into pixels
        x = photon_positions[0,:]
        y = photon_positions[1,:]
        self.counts = np.histogram2d(x, y, bins=self.pixel_bins)[0]
        
        # combine noise with counts
        self.image = self.noise + self.gain*self.counts
        
    
    def grab_image(self):
        """
        Returns most recently exposed image.

        Returns
        -------
        self.image: ndarray
            Fluorescent counts in a 2D array.

        """
        return self.image
    
    def show_image(self, roi=None):
        """
        Displays the most recently acquired image.
        """
        
        if roi is not None:
            self.image_cropped = self.image[roi['xmin']:roi['xmax'], roi['ymin']:roi['ymax']]
        else:
            self.image_cropped = self.image
        
        fig, ax = plt.subplots(figsize=(15,10))
        plt.imshow(self.image_cropped.T, origin='lower')
        # plt.colorbar(label='counts')
        plt.xlabel('x (px)')
        plt.ylabel('y (px)')
        fig.patch.set_facecolor('white')
    
if __name__ == '__main__':
    tweezer_options = {
        'n_sites': (10,10),
        'spacing': (10,10),
        'angle': np.pi/6,
        }
    
    T = Tweezers(**tweezer_options)
    # T.plot_sites()
    
    atom_options = {
        'p_filling': 0.6,
        'scattering_rate': 1000,
        'sigma_thermal': 1
        }
    
    A = Atoms(**atom_options)
    A.generate_atoms(T.positions)
    # A.plot_atoms()
    
    camera_options = {
        'gain': 10,
        'pixel_size': (13.5, 13.5),
        'magnification': 2500/40,
        'display_size': (1024, 1024),
        'exposure_time': 1,
        'dark_mean': 500,
        'dark_std': 10,
        'offset': (25, 25)
        }
    
    C = AndorIxon(**camera_options)
    C.expose(A)
    # C.plot_photons()
    
    
    roi = {
        'xmin':0,
        'xmax': 700,
        'ymin': 0,
        'ymax': 425}
    
    C.show_image(roi)