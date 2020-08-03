# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 10:25:49 2020

@author: Jacob
"""

import numpy as np
import matplotlib.pyplot as plt

from math import sqrt
from skimage.feature import blob_dog, blob_log
from skimage.util import img_as_uint, img_as_ubyte, img_as_float


class DetectionBot():
    def __init__(self):       
        #images
        self.reference_image = None
        self.background_image = None
        self.image = None
        
        #positions
        self.reference_pixels = None
        self.blob_sizes = None
        self.blob_pixels = None
        self.blob_indices = None
        self.spacing = None
        
        #boolean mask
        self.blob_mask = None
        
    def set_background(self, background):
        """
        Set image to use for background subtraction
        """
        self.background = background
        
        
    def set_spacing(self, spacing):
        if type(spacing) in [list, tuple]:
            spacing = np.array(spacing)
            
        self.spacing = spacing
    
    def normalize(self, image, dtype='float'):
        image = image/np.max(image)
        
        if dtype=='float':
            return img_as_float(image)
        elif dtype=='uint8':
            return img_as_ubyte(image)
        elif dtype=='uint16':
            return img_as_uint(image)
        
    def get_blob_pixels(self, image, method='dog', min_sigma=1, max_sigma=1,
                  threshold=0.01, exclude_border=False, **blob_kwargs):
        if method == 'dog':
            blob_funct = blob_dog
        elif method == 'log':
            blob_funct = blob_log
            
        blobs = blob_funct(image,
                           min_sigma=min_sigma,
                           max_sigma=max_sigma,
                           threshold=threshold,
                           exclude_border=exclude_border,
                           **blob_kwargs)
        
        # separate positions and sizes
        positions = blobs[:, 0:2]
        sizes = blobs[:, 2] * sqrt(2)

        return positions, sizes
        
    def set_reference(self, reference_image, reference_tuple=(0,0)):
        """
        Set the reference point of the tweezer array by passing an image of atoms
        loaded only into the reference site
        """
        reference_image = self.normalize(reference_image)
        self.reference_image = reference_image
        self.reference_tuple = reference_tuple
        
        blobs, sizes = self.get_blob_pixels(self.reference_image)
        
        if len(blobs) == 0:
            self.show_blobs(self.reference_image, blobs, sizes, circles=True, text=False)
            raise Exception('No reference blob found)')
        if len(blobs) > 1:
            print('blobs', blobs)
            self.show_blobs(self.reference_image, blobs, sizes, circles=True, text=False)
            raise Exception('Reference image should only contain one blob.')


        self.reference_pixels = blobs[0]
        
    def get_blob_indices(self, blobs):
        if self.reference_pixels is None:
            raise Exception('Must call set_reference before acquiring atom indices.')
        
        # pixel positions relative to reference tweezer, dropping blob size
        blobs_relative = blobs - self.reference_pixels
        
        if self.spacing is None:
            raise Exception('Must set spacng before acquiring atom indices.')
        
        blob_indices = np.round(blobs_relative/self.spacing).astype('int')
        
        # shift relative to reference_tuple
        blob_indices += np.array(self.reference_tuple)
        
        return blob_indices
    
    def set_blobs(self, image, **blob_kwargs):
        image = self.normalize(image)
        self.image = image
        self.blob_pixels, self.blob_sizes = self.get_blob_pixels(image, **blob_kwargs)
        
        if self.reference_pixels is not None:
            self.blob_indices = self.get_blob_indices(self.blob_pixels)
            
        return self.blob_pixels
        
    def set_blob_mask(self, n_sites):
        if self.blob_indices is None:
            raise Exception('Must call set_blobs before setting blob mask.')
            
        mask = np.zeros(n_sites)
        for i, j in self.blob_indices:
            try:
                mask[i,j] = 1
            except:
                pass
            
        self.blob_mask = mask.astype('bool')
    
    def show_blobs(self, image=None, blobs=None, sizes=None, circles=False, text=True,
                   true_mask=None, title=None, cmap='gray'):
        if image is None:
            image = self.image
            
        if blobs is None:
            if self.blob_pixels is None:
                raise Exception('Must provide blobs or call set_blobs before show_blobs')
            else:
                blobs = self.blob_pixels
                sizes = self.blob_sizes
            
        fig, ax = plt.subplots(figsize=(6, 6))
    
        ax.imshow(image.T, origin='lower', cmap=cmap)
        
        for idx, blob in enumerate(blobs):
            x, y = blob
            
            if circles:
                r = sizes[idx]
                c = plt.Circle((x, y), r, color='yellow', linewidth=2, fill=False)
                ax.add_patch(c)
            
            if (text) and (self.blob_indices is not None):
                i, j = self.blob_indices[idx]
                
                
                if true_mask is not None:
                    try:
                        if (i < 0) or (j < 0):
                            color = 'red'
                        elif true_mask[i,j] == self.blob_mask[i,j]:
                            color = 'white'
                        else:
                            color = 'red'
                    except:
                        color = 'red'
                else:
                    color = 'white'
                    
                plt.text(x, y, f'({i},{j})', color=color, fontdict={'size':15})

        ax.set_axis_off()
        if title:
            plt.title(title)
        plt.tight_layout()
        plt.show()