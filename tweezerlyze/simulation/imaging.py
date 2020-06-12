# -*- coding: utf-8 -*-
"""
Created on Sun May 24 15:15:51 2020

@author: Jacob
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
fontprops = fm.FontProperties(size=18)
from .lasers import Laser


class Optics():
    def __init__(self, magnification, NA):
        self.magnification = magnification
        self.NA = NA
        self.collection_efficiency = 0.5*(1 - np.sqrt(1 - NA**2))
        
    def set_diffraction(self, wavelength):
        self.sigma_diffraction = wavelength/(2*self.NA)
        
    def apply_diffraction(self, photon_positions):
        return np.random.normal(loc=photon_positions, scale=self.sigma_diffraction) #TODO: factor of 2?
        

class Camera():
    def __init__(self, pixel_size, sensor_size, gain, dark_mean, dark_std, position=(0,0)):
        
        self.pixel_size = pixel_size
        self.sensor_size = sensor_size
        self.dark_mean = dark_mean
        self.dark_std = dark_std
        self.gain = gain
        self.position = position
        
        self.photon_positions = None
        self.image = None
        self.scale_set = False
        
    def set_scale(self, magnification):
        # scale of image in um/px
        self.scale = np.array(self.pixel_size)/magnification
        
        # set pixel bins according to scale
        pixel_bins_x = (np.arange(self.sensor_size[0]+1) - self.position[0])*self.scale[0]
        pixel_bins_y = (np.arange(self.sensor_size[1]+1) - self.position[1])*self.scale[1]
        self.pixel_bins = [pixel_bins_x, pixel_bins_y]
        
        self.scale_set = True
    
    def expose(self, photon_positions):
        if not self.scale_set:
            raise Exception('Must set scale before exposing camera.')
        
        # base image has background and thermal noise
        self.noise = np.random.normal(self.dark_mean, self.dark_std, self.sensor_size)
        
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
    
    def show_image(self, roi=None, scalebar=False, scalebar_length=None):
        """
        Displays the most recently acquired image.
        """
        
        if roi is not None:
            self.image_cropped = self.image[roi['xmin']:roi['xmax'], roi['ymin']:roi['ymax']]
        else:
            self.image_cropped = self.image
        
        fig, ax = plt.subplots(figsize=(15,10))
        plt.imshow(self.image_cropped.T, origin='lower')
        
        scalebar = AnchoredSizeBar(ax.transData,
                           scalebar_length/self.scale[0],
                           f'{scalebar_length} um',
                           'upper right', 
                           pad=1,
                           color='white',
                           frameon=False,
                           size_vertical=0.5,
                           sep = 10,
                           fontproperties=fontprops)

        ax.add_artist(scalebar)
        ax.add_artist(scalebar)
        # plt.colorbar(label='counts')
        plt.xlabel('x (px)')
        plt.ylabel('y (px)')
        fig.patch.set_facecolor('white')
        
        
class Imaging():
    def __init__(self, optics_options, camera_options, laser_options, scattering_rate=None, **kwargs):
        self.laser = Laser(**laser_options)
        
        self.optics = Optics(**optics_options)
        self.optics.set_diffraction(self.laser.wavelength*1e-3)
        
        self.camera = Camera(**camera_options)
        self.camera.set_scale(self.optics.magnification)
        
        self.set_rates(scattering_rate)
        
    def set_rates(self, scattering_rate=None):
        self.scattering_rate = scattering_rate
        
        if scattering_rate is None:
            self.collection_rate = None
        else:
            self.collection_rate = self.optics.collection_efficiency * self.scattering_rate
        
    def collect_photons(self, photon_positions):
        photon_positions = self.optics.apply_diffraction(photon_positions)
        self.camera.expose(photon_positions)