# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 10:25:49 2020

@author: Jacob
"""

from skimage import data, feature, exposure
import numpy as np
import matplotlib.pyplot as plt

from math import sqrt
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
from skimage.util import img_as_uint, img_as_ubyte


class DetectionBot():
    def __init__(self):
        self.calibrated = {'center': False,
                           'spacing': False}
        
        #images
        self.reference = None
        self.background = None
        self.image = None
        
        #positions
        self.reference_tweezer = None
        self.blob_sizes = None
        self.blob_pixels = None
        self.blob_indices = None
        self.spacing = None
        
    def set_background(self, background):
        """
        Set image to use for background subtraction
        """
        self.background = background
        
        
    def set_spacing(self, spacing):
        if type(spacing) in [list, tuple]:
            spacing = np.array(spacing)
            
        self.spacing = spacing
    
    def normalize(self, image, dtype='uint8'):
        if image.dtype == np.dtype('float64'):
            image *= 1/np.max(image)
        
        if dtype=='uint8':
            return img_as_ubyte(image)
        elif dtype=='uint16':
            return img_as_uint(image)
        
    def get_blob_pixels(self, image, method='dog', min_sigma=1, max_sigma=1,
                  threshold=0.01, **blob_kwargs):
        if method == 'dog':
            blob_funct = blob_dog
        elif method == 'log':
            blob_funct = blob_log
            
        blobs = blob_funct(image,
                           min_sigma=min_sigma,
                           max_sigma=max_sigma,
                           threshold=threshold,
                           **blob_kwargs)
        
        # separate positions and sizes
        positions = blobs[:, 0:2]
        sizes = blobs[:, 2] * sqrt(2)

        return positions, sizes
        
    def set_reference(self, reference):
        """
        Set the reference point of the tweezer array by passing an image of atoms
        loaded only into the reference site
        """
        reference = self.normalize(reference)
        
        self.reference = reference
        blobs, _ = self.get_blob_pixels(reference)
        if len(blobs) > 1:
            raise Exception('Reference image should only contain one blob.')  

        self.reference_tweezer = blobs[0]
        
    def get_blob_indices(self, blobs):
        if self.reference_tweezer is None:
            raise Exception('Must call set_reference before acquiring atom indices.')
        
        # pixel positions relative to reference tweezer, dropping blob size
        blobs_relative = blobs - self.reference_tweezer
        
        if self.spacing is None:
            raise Exception('Must set spacng before acquiring atom indices.')
        
        blob_indices = np.round(blobs_relative/self.spacing).astype('int')
        return blob_indices
    
    def set_blobs(self, image, **blob_kwargs):
        self.image = self.normalize(image)
        self.blob_pixels, self.blob_sizes = self.get_blob_pixels(image, **blob_kwargs)
        self.blob_indices = self.get_blob_indices(self.blob_pixels)
    
    def show_blobs(self, circles=False, text=True):
        if self.blob_pixels is None:
            raise Exception('Must call set_blobs before show_blobs')
            
        fig, ax = plt.subplots(figsize=(6, 6))
    
        ax.imshow(self.image.T, origin='lower')
        
        for idx, blob in enumerate(self.blob_pixels):
            x, y = blob
            
            if circles:
                r = self.blob_sizes[idx]
                c = plt.Circle((x, y), r, color='yellow', linewidth=2, fill=False)
                ax.add_patch(c)
            
            if text:
                i, j = self.blob_indices[idx]
                t = plt.text(x, y, f'({i},{j})', color='white')

        ax.set_axis_off()
        
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    bot = DetectionBot()
    spacing_um = np.array([5,5])
    camera_scale = np.array([1.08, 1.08]) #um/px
    spacing_px = spacing_um / camera_scale
    bot.set_spacing(spacing_px)
    
    reference = np.load('atoms_reference.npy')
    bot.set_reference(reference)
    
    image = np.load('atoms_sparse.npy')
    bot.set_blobs(image)

    bot.show_blobs()