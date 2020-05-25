# -*- coding: utf-8 -*-
"""
Created on Sun May 24 15:52:48 2020

@author: Jacob
"""

import numpy as np
import matplotlib.pyplot as plt
from geometry import Tweezers


class Atoms:
    def __init__(self, p_filling, scattering_rate, sigma_thermal):
        self.p_filling = p_filling
        self.scattering_rate = scattering_rate
        self.sigma_thermal = sigma_thermal
        pass
        
    def generate_atoms(self, site_positions):
        n_sites = site_positions.shape[-1]
        
        # randomly fill sites
        self.occupation = np.random.binomial(1, self.p_filling, size=n_sites)
        self.positions = site_positions[:, self.occupation==1]
        
    def plot_atoms(self):
        """
        Visualize the atoms.
        """
        fig, ax = plt.subplots(figsize=(10,10))
        r = self.positions
        x = r[0, :]
        y = r[1, :]
        plt.scatter(x, y)
        plt.xlabel('x (um)')
        plt.ylabel('y (um)')
        ax.set_aspect('equal')
        plt.title('Atom positions')
        
if __name__ == '__main__':
    tweezer_options = {
        'n_sites': (15,10),
        'spacing': (5,5),
        'angle': np.pi/6,
        }
    
    T = Tweezers(**tweezer_options)
    T.plot_sites()
    
    atom_options = {
        'p_filling': 1,
        'scattering_rate': 1,
        'sigma': 0
        }
    
    A = Atoms(**atom_options)
    A.generate_atoms(T.positions)
    A.plot_atoms()