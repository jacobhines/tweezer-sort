# -*- coding: utf-8 -*-
"""
Created on Mon May 25 15:03:01 2020

@author: Jacob
"""

import numpy as np
import matplotlib.pyplot as plt
from ..calculation.unit_conversions import K_to_unit


class Atoms():
    def __init__(self, species, temperature, imaging_transition='D2'):
        
        self.species = species
        self.temperature = temperature
        # self.thermal_energy = 0.5* K_to_unit(self.temperature*self.Hz_per_K
        
        line = getattr(self.species, imaging_transition)
        self.wavelength = line.wavelength
        
        self.atoms_generated = False
        self.photons_generated = False
        self.n_photons = None
        
    def load_atoms(self, sites, filling_distribution, filling_distribution_kwargs={}):
        n_sites = len(sites)
        avg_filling = np.array([s.avg_filling for s in sites])
        
        # fill sites based on filling distribution
        if filling_distribution == 'binomial':
            self.occupancies = np.random.binomial(1, avg_filling, size=n_sites, **filling_distribution_kwargs)
            
        elif filling_distribution == 'poisson':
            self.occupancies = np.random.poisson(avg_filling, size=n_sites, **filling_distribution_kwargs)
        
        elif filling_distribution == 'normal':
            self.occupancies = np.random.normal(avg_filling, size=n_sites, **filling_distribution_kwargs)
            self.occupancies = np.clip(self.occupancies, 0, np.inf)
            self.occupancies = self.occupancies.astype('int')
        else:
            raise Exception(f'Invalid filling distribution {filling_distribution}')
            
            
        site_positions = np.array([site.position for site in sites]).T
            
        self.occupied_positions = site_positions[:, self.occupancies > 0]
        self.nonzero_occupancies = [o for o in self.occupancies if o != 0]
        
        # record position of each atom
        atom_positions = np.zeros((2,0))

        for position, occupancy in zip(self.occupied_positions.T, self.nonzero_occupancies):
            tmp = np.ones((2, occupancy))*position[:, np.newaxis]
            atom_positions = np.concatenate((atom_positions, tmp), axis=1)
            
        self.atom_positions = atom_positions
        
        self.atoms_generated = True
        
    def generate_photons(self, scattering_rate, sigma_thermal, exposure_time, collection_efficiency=1):
        """
        Generate fluorescence photons
        """
        
        # scattering rate and exposure give number of photons per atom, but we'll only generate as many as the imaging system would capture
        self.n_photons = int(exposure_time * scattering_rate * collection_efficiency)
        
        # initialize photons
        photon_positions = np.tile(self.atom_positions, (self.n_photons, 1, 1))
        photon_positions = np.transpose(photon_positions, axes=[1,2,0])
        
        #each photon is gaussian distributed according to thermal motion   
        if type(sigma_thermal) == tuple:
            (sigma_thermal_x, sigma_thermal_y) = sigma_thermal
        else:
            sigma_thermal_x = sigma_thermal
            sigma_thermal_y = sigma_thermal
        scale_template = np.ones(photon_positions.shape[1:])          
        scale = np.array([sigma_thermal_x*scale_template, 
                          sigma_thermal_y*scale_template])        
        
        photon_positions = np.random.normal(loc=photon_positions, scale=scale)
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