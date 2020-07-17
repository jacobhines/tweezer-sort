# -*- coding: utf-8 -*-
"""
Created on Mon May 25 15:03:01 2020

@author: Jacob
"""

import numpy as np
import matplotlib.pyplot as plt
from ..calculation.unit_conversions import K_to_unit


class Atoms():
    def __init__(self, species, p_filling, temperature, imaging_transition='D2'):
        self.species = species        
        self.p_filling = p_filling

        self.temperature = temperature
        # self.thermal_energy = 0.5* K_to_unit(self.temperature*self.Hz_per_K
        
        line = getattr(self.species, imaging_transition)
        self.wavelength = line.wavelength
        
        self.atoms_generated = False
        self.photons_generated = False
        self.n_photons = None
        
    def load_atoms(self, site_positions):
        n_sites = site_positions.shape[-1]
        
        # randomly fill sites
        self.occupation = np.random.binomial(1, self.p_filling, size=n_sites)
        self.positions = site_positions[:, self.occupation==1]
        
        self.atoms_generated = True
        
    def generate_photons(self, scattering_rate, sigma_thermal, exposure_time, collection_efficiency=1):
        """
        Generate fluorescence photons
        """
        
        # scattering rate and exposure give number of photons, but we'll only generate as many as the imaging system would capture
        self.n_photons = int(exposure_time * scattering_rate * collection_efficiency)
        
        # initialize n_photons at each atom
        photon_positions = np.tile(self.positions, (self.n_photons, 1, 1))
        photon_positions = np.transpose(photon_positions, axes=[1,2,0])
        
        #each photon is gaussian distributed according to thermal motion               
        photon_positions = np.random.normal(loc=photon_positions, scale=sigma_thermal)
        xarr = photon_positions[0,:]
        yarr = photon_positions[1,:]
        self.photon_positions = np.stack([xarr.flatten(), yarr.flatten()])
        
        self.photon_generated = True
        
        return self.photon_positions
    
    def plot_atoms(self):
        """
        Visualize the atoms.
        """
        if not self.atoms_generated:
            raise Exception('Must generate atoms before plotting them')
        
        fig, ax = plt.subplots(figsize=(10,10))
        r = self.positions*1e6
        x = r[0, :]
        y = r[1, :]
        plt.scatter(x, y)
        plt.xlabel('x (um)')
        plt.ylabel('y (um)')
        ax.set_aspect('equal')
        plt.title('Atom positions')
        
    def plot_photons(self):
        """
        Visualize the photons.
        """
        if not self.photons_generated:
            raise Exception('Must generate photons before plotting them')
        
        fig, ax = plt.subplots(figsize=(10,10))
        r = self.photon_positions*1e6
        x = r[0, :]
        y = r[1, :]
        plt.scatter(x, y)
        plt.xlabel('x (um)')
        plt.ylabel('y (um)')
        ax.set_aspect('equal')
        plt.title('Photon positions')
        fig.patch.set_facecolor('white')