# -*- coding: utf-8 -*-
"""
Created on Sun May 24 15:52:48 2020

@author: Jacob
"""

import numpy as np
import matplotlib.pyplot as plt
from geometry import Tweezers


class Atoms():
    def __init__(self, p_filling):
        self.p_filling = p_filling
        pass
        
    def generate_atoms(self, site_positions, sigma):
        n_sites = site_positions.shape[-1]
        self.occupation = np.random.binomial(1, self.p_filling, size=n_sites)
        self.occupied_positions = site_positions[:, self.occupation==1]
        self.atom_positions = np.random.normal(self.occupied_positions, sigma)
        
    def plot_atoms(self):
        """
        Visualize the atoms.
        """
        fig, ax = plt.subplots(figsize=(10,10))
        r = self.atom_positions
        x = r[0, :]
        y = r[1, :]
        plt.scatter(x, y)
        plt.xlabel('x (um)')
        plt.ylabel('y (um)')
        ax.set_aspect('equal')
        plt.title('Atom positions')
        
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