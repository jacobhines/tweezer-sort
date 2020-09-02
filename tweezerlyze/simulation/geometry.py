# -*- coding: utf-8 -*-
"""
Created on Sun May 24 16:01:29 2020

@author: Jacob
"""

import numpy as np
import matplotlib.pyplot as plt
from .lasers import Laser
from ..calculation.dipoletrap import trapDepth

class Tweezers:
    def __init__(self, n_sites, spacing, angle, offset, wavelength, power, waist, **kwargs):
        self.n_sites = n_sites
        self.spacing = spacing
        self.angle = angle
        self.offset=offset
        
        self.occupation = None
        self.indices = None
        self.positions = None
        
        # laser for each tweezer
        self.laser = Laser(wavelength, power, waist)
        self.trap_depth = None
        self.sigma_thermal = None
        
        self.generate_sites()
        
    def set_trap_depth(self, trap_depth=None, atoms=None, verbose=False):
        
        if trap_depth is not None:
            self.trap_depth = trap_depth
        elif atoms is not None:
            self.trap_depth = trapDepth(species=atoms.species,
                                        intensity = None,
                                        power = self.laser.power,
                                        waist = self.laser.waist,
                                        wavelength = self.laser.wavelength,
                                        unit='K')
        else:
            raise Exception('Must provde atom properties or fix trap_depth')
            
        if verbose:
            print('trap depth:', self.trap_depth, 'K')
            
    def set_sigma_thermal(self, sigma_thermal=None, atoms=None, verbose=False):
        if sigma_thermal is not None:
            self.sigma_thermal = sigma_thermal

        elif atoms is not None:
            waist = self.laser.waist
            temperature = atoms.temperature
            trap_depth = self.trap_depth
            sigma_thermal = [w*np.sqrt(-0.5*np.log(1 - temperature/(2*trap_depth))) for w in waist]
            
            self.sigma_thermal = tuple(sigma_thermal)
            
        else:
            raise Exception('Must provide atom properties or fix sigma_thermal')
            
        if verbose:
            print('sigma_thermal:', self.sigma_thermal*1e6, 'um')
    
    def get_position(self, i, j):
        """
        Calculates position of site (i,j).
        """
        if np.shape(i) != np.shape(j):
            raise Exception('i and j must be the same shape')
        
        x = i*self.spacing[0] + j*self.spacing[1]*np.sin(self.angle)
        y = j*self.spacing[1]*np.cos(self.angle)
        
        return x, y
    
    def generate_sites(self): 
        """
        Generate and store lists of indices and physical positions of each tweezer.
        """
        ni, nj = self.n_sites
        ivec = np.arange(ni)
        jvec = np.arange(nj)
        iarr, jarr = np.meshgrid(ivec, jvec)
        xarr, yarr = self.get_position(iarr,jarr)
        
        xarr += self.offset[0]
        yarr += self.offset[1]
        
        self.indices = np.stack([iarr.flatten(), jarr.flatten()])
        self.positions = np.stack([xarr.flatten(), yarr.flatten()])
        
    def set_gt_mask(self):
        if self.occupation is None:
            raise Exception('Must set occupation before generating ground truth mask')
            
        mask = np.zeros(self.n_sites, dtype=bool)
            
        for idx, idx_tuple in enumerate(self.indices.T):
            i, j = idx_tuple
            mask[i,j] = bool(self.occupation[idx])
            
        self.gt_mask = mask
        
    def plot_sites(self):
        """
        Visualize the tweezers.
        """
        fig, ax = plt.subplots(figsize=(10,10))
        r = self.positions*1e6
        x = r[0, :]
        y = r[1, :]
        plt.scatter(x, y)
        plt.xlabel('x (um)')
        plt.ylabel('y (um)')
        ax.set_aspect('equal')
        plt.title('Tweezer positions')