# -*- coding: utf-8 -*-
"""
Created on Sun May 24 16:01:29 2020

@author: Jacob
"""

import numpy as np
import matplotlib.pyplot as plt
from .lasers import Laser
from . import constants as cs

class Tweezers:
    def __init__(self, n_sites, spacing, angle, offset, wavelength, power, waist, **kwargs):
        self.n_sites = n_sites
        self.spacing = spacing
        self.angle = angle
        self.offset=offset
        
        # laser for each tweezer
        self.laser = Laser(wavelength, power, waist)
        self.trap_depth = None
        self.sigma_thermal = None
        
        self.generate_sites()
        
    def set_trap_depth(self, trap_depth=None, atoms=None, verbose=False):
        if trap_depth is not None:
            self.trap_depth = trap_depth
            
        elif atoms is not None:
            # saturation parameter
            I = self.laser.intensity
            I_sat = atoms.species.saturation_intensity('detuned', 'D2', 'linear')
            # I_sat = 2*(np.pi**2)*(cs.hbar*cs.c)*(self.species.D2.linewidth)/(3*(self.wavelength**3))
            s0 = I/I_sat
            
            # inverse detuning in linewidths
            nu = self.laser.frequency
            delta1 = (nu - atoms.species.D1.frequency)/(atoms.species.D1.linewidth*1e-6)
            delta2 = (nu - atoms.species.D2.frequency)/(atoms.species.D2.linewidth*1e-6)
            inv_delta = (1/3)*(1/delta1 + 2/delta2)
            
            # trap depth in uK
            self.trap_depth = - cs.uK_per_MHz * (atoms.species.D2.linewidth / 8) * s0 * inv_delta
            
            if verbose:
                print('I:', I)
                print('I_sat:', I_sat)
                print('s0:', s0)
                print('trap depth:', self.trap_depth, 'uK')
                
        else:
            raise Exception('Must provde atom properties or fix trap_depth')
            
    def set_sigma_thermal(self, sigma_thermal=None, atoms=None, verbose=False):
        if sigma_thermal is not None:
            self.sigma_thermal = sigma_thermal

        elif atoms is not None:
            waist = self.laser.waist
            temperature = atoms.temperature
            trap_depth = self.trap_depth
            self.sigma_thermal = waist*np.sqrt(-0.5*np.log(1 - temperature/(2*trap_depth)))
            
            if verbose:
                print('sigma_thermal:', self.sigma_thermal, 'um')
            
        else:
            raise Exception('Must provide atom properties or fix sigma_thermal')
    
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
        
    def plot_sites(self):
        """
        Visualize the tweezers.
        """
        fig, ax = plt.subplots(figsize=(10,10))
        r = self.positions
        x = r[0, :]
        y = r[1, :]
        plt.scatter(x, y)
        plt.xlabel('x (um)')
        plt.ylabel('y (um)')
        ax.set_aspect('equal')
        plt.title('Tweezer positions')