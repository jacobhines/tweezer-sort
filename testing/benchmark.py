# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 19:24:24 2020

@author: Jacob
"""

import numpy as np
from tweezerlyze.simulation.experiment import Experiment
from options import experiment_options
from tweezerlyze.detection import DetectionBot
from evaluation import getFidelity, getPSNR
from time import time
import matplotlib.pyplot as plt
import matplotlib

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 22}

matplotlib.rc('font', **font)

##### OPTIONS #####
# imaging times
n_imaging_times = 50
imaging_time_vec = 10**np.linspace(1, 3, n_imaging_times)

# runs per imaging time
n_runs = 20

# cropping
roi = {
    'xmin': 0,
    'xmax': 50,
    'ymin': 0,
    'ymax': 50,
    }

debug = False

##### REFERENCE IMAGE #####
experiment_options['atom_options']['p_filling'] = 1
experiment_options['tweezer_options']['n_sites'] = (1,1)

expt_reference = Experiment(**experiment_options)
expt_reference.load_atoms()
expt_reference.image_atoms(imaging_time=1e5)

reference_image = expt_reference.imaging.camera.crop_image(roi)
np.save('atoms_reference.npy', reference_image)


##### SPARSE IMAGES #####
# prepare experiment
experiment_options['atom_options']['p_filling'] = 0.5
experiment_options['tweezer_options']['n_sites'] = (10, 10)
expt_sparse = Experiment(**experiment_options)

# prepare bot
bot = DetectionBot()
spacing_um = np.array(expt_sparse.geometry.spacing)
camera_scale = expt_sparse.imaging.camera.scale #um/px
spacing_px = spacing_um / camera_scale
bot.set_spacing(spacing_px)
bot.set_reference(reference_image)

# data containers
template = np.zeros((len(imaging_time_vec), n_runs))
fidelity = np.copy(template)
psnr = np.copy(template)
dt = np.copy(template)
dark_mean = expt_sparse.imaging.camera.dark_mean

for i, imaging_time in enumerate(imaging_time_vec):
    print(f'{i}/{n_imaging_times}')
    for j in range(n_runs):
        # imaging
        expt_sparse.load_atoms()
        expt_sparse.image_atoms(imaging_time=imaging_time)
        image = expt_sparse.imaging.camera.crop_image(roi)
        
        # detection
        t_start = time()
        bot.set_blobs(image)
        bot.set_blob_mask(expt_sparse.geometry.n_sites)
        dt[i,j] = time()-t_start
        
        # evaluation
        psnr[i,j] = getPSNR(expt_sparse.imaging.camera.signal_cropped, expt_sparse.imaging.camera.image_cropped)
        fidelity[i,j] = getFidelity(bot.blob_mask, expt_sparse.geometry.gt_mask)
        
        
        if debug:
            bot.show_blobs(circles=False, text=True)
            print('PSNR:', psnr[i,j])
            print('Fidelity:', fidelity[i,j])
            print('Time:', dt[i,j]*1e3, ' ms')
          

fidelity_mean = np.mean(fidelity, axis=-1)
fidelity_std = np.std(fidelity, axis=-1)

psnr_mean = np.mean(psnr, axis=-1)
psnr_std = np.std(psnr, axis=-1)

dt_mean = np.mean(dt, axis=-1)
dt_std = np.std(dt, axis=-1)


fig, ax = plt.subplots(figsize=(10,6))
fig.patch.set_facecolor('white')
plt.errorbar(imaging_time_vec, fidelity_mean, yerr=fidelity_std, fmt='o')
plt.xscale('log')
plt.xlabel('scattering events')
plt.ylabel('fidelity')
plt.grid()

fig, ax = plt.subplots(figsize=(10,6))
fig.patch.set_facecolor('white')
plt.errorbar(psnr_mean, fidelity_mean, xerr=psnr_std, yerr=fidelity_std, fmt='o')
plt.xlabel('psnr')
plt.ylabel('fidelity')
plt.grid()

fig, ax = plt.subplots(figsize=(10,6))
fig.patch.set_facecolor('white')
plt.errorbar(imaging_time_vec, dt_mean*1e3, yerr=dt_std*1e3, fmt='o')
plt.xlabel('scattering events')
plt.ylabel('time (ms)')
plt.ylim([0,None])