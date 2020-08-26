# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 08:29:26 2020

@author: Jacob
"""

from tweezerlyze.simulation.experiment import Experiment
from options import experiment_options
import numpy as np
import matplotlib.pyplot as plt

# change readout rate
rr = 1e6
experiment_options['imaging_options']['camera_options']['readout_rate'] = rr
experiment_options['atom_options']['p_filling'] = 0.5
experiment_options['tweezer_options']['n_sites'] = (10,1)
experiment_options['tweezer_options']['waist'] = (12e-6, 4e-6)
experiment_options['tweezer_options']['spacing'] = (24e-6, 24e-6)
experiment_options['imaging_options']['camera_options']['position'] = (25,25)

scattering_events = 5000

roi = {
    'xmin': 0,
    'xmax': 250,
    'ymin': 0,
    'ymax': 50,
    }

n_shots = 50
expt_sparse = Experiment(**experiment_options)

# generate shots
shots = []


for idx in range(n_shots):
    expt_sparse.load_atoms()
    expt_sparse.image_atoms(imaging_time=scattering_events)
    expt_sparse.show_atoms(roi=roi, colorbar=True)
    image = expt_sparse.imaging.camera.image_cropped
    
    shots.append(image)



shots = np.array(shots)
mean = np.mean(shots, axis=0)

expt_sparse.show_atoms(image=mean, roi=roi, colorbar=True, title='mean')

np.save('shots_for_histogram.npy', shots)