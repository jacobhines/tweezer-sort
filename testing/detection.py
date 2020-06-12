# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 19:25:39 2020

@author: Jacob
"""

from tweezerlyze.detection import DetectionBot
import numpy as np

bot = DetectionBot()
spacing_um = np.array([5,5])
camera_scale = np.array([1.08, 1.08]) #um/px
spacing_px = spacing_um / camera_scale
bot.set_spacing(spacing_px)

reference = np.load('atoms_reference.npy')
reference = reference/np.max(reference)
bot.set_reference(reference)

image = np.load('atoms_sparse.npy')
image = image / np.max(image)
bot.set_blobs(image)
bot.set_blob_mask((10,10))

bot.show_blobs(circles=True, text=False)
