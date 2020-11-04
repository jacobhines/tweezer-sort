# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:42:29 2020

@author: Jacob
"""

from tweezerlyze.simulation.experiment import Experiment
from options import experiment_options
import numpy as np

# change readout rate
rr = 30e6
experiment_options['imaging_options']['camera_options']['readout_rate'] = rr


# generate reference image
experiment_options['atom_options']['p_filling'] = 1
experiment_options['tweezer_options']['n_sites'] = (1,1)

expt_reference = Experiment(**experiment_options)
expt_reference.load_atoms()
expt_reference.image_atoms(imaging_time=10000)

roi = {
    'xmin': 0,
    'xmax': 50,
    'ymin': 0,
    'ymax': 50,
    }
    
expt_reference.show_atoms(roi=roi)
reference_image = expt_reference.imaging.camera.image_cropped

np.save('atoms_reference.npy', reference_image)

# generate sparsely filled image
experiment_options['atom_options']['p_filling'] = 1
experiment_options['tweezer_options']['n_sites'] = (10,1)

expt_sparse = Experiment(**experiment_options)
expt_sparse.load_atoms()

# times = 2**np.arange(0, 11)
times = [10000]

for t in times:
    expt_sparse.image_atoms(imaging_time=t)
    expt_sparse.show_atoms(roi=roi, colorbar=True, title=f'Readoute rate = {rr/1e6} MHz')

image = expt_sparse.imaging.camera.image_cropped

np.save('atoms_sparse.npy', image)