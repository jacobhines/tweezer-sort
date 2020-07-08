# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 19:24:24 2020

@author: Jacob
"""

import numpy as np
from tweezerlyze.simulation.experiment import Experiment
from options import experiment_options
from tweezerlyze.detection import DetectionBot
from evaluation import getFidelity, getPSNR, getSNR
from time import time
import matplotlib.pyplot as plt
import matplotlib

font = {
        # 'family' : 'normal',
        # 'weight' : 'normal',
        'size'   : 15,
        }

matplotlib.rc('font', **font)

##### OPTIONS #####
# imaging times
# imaging_time_vec = 2**np.arange(0, 11, 0.25)
imaging_time_vec = np.linspace(1, 300, 25)
n_imaging_times = len(imaging_time_vec)
# imaging_time_vec = [200]

# runs per imaging time
n_runs = 100

# cropping
roi = {
    'xmin': 0,
    'xmax': 50,
    'ymin': 0,
    'ymax': 50,
    }

debug = False
plots = True

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
expt = Experiment(**experiment_options)

# prepare bot
bot = DetectionBot()
spacing_um = np.array(expt.geometry.spacing)
camera_scale = expt.imaging.camera.scale #um/px
spacing_px = spacing_um / camera_scale
bot.set_spacing(spacing_px)
bot.set_reference(reference_image)

# data containers
template = np.zeros((len(imaging_time_vec), n_runs))
n_photons = np.copy(template)
fidelity = np.copy(template)
snr = np.copy(template)
psnr = np.copy(template)
dt = np.copy(template)
expt.load_atoms()

# photon distribution radius
sigma = np.sqrt(expt.geometry.sigma_thermal**2 + expt.imaging.optics.sigma_diffraction**2)
sigma = sigma / expt.imaging.camera.scale[0] #px


for i, imaging_time in enumerate(imaging_time_vec):
    print(f'{i}/{n_imaging_times}')
    for j in range(n_runs):
        # imaging
        
        expt.image_atoms(imaging_time=imaging_time)
        image = expt.imaging.camera.crop_image(roi)
        
        # detection
        t_start = time()
        bot.set_blobs(image, threshold=0.008, min_sigma=sigma, max_sigma=sigma)
        bot.set_blob_mask(expt.geometry.n_sites)
        dt[i,j] = time()-t_start
        
        # evaluation
        snr[i,j] = getSNR(expt.atoms.n_photons, expt.imaging.camera.noise_std, np.pi*(sigma**2))
        psnr[i,j] = getPSNR(expt.imaging.camera.signal_cropped, expt.imaging.camera.image_cropped)
        fidelity[i,j] = getFidelity(bot.blob_mask, expt.geometry.gt_mask)
        
        
        if debug:
            bot.show_blobs(circles=True,
                           text=False,
                           true_mask=expt.geometry.gt_mask,
                           title=f'SE = {imaging_time}',
                           cmap='viridis')
            print('SNR:', snr[i,j])
            print('PSNR:', psnr[i,j])
            print('Fidelity:', fidelity[i,j])
            print('Time:', dt[i,j]*1e3, ' ms')
          

fidelity_mean = np.mean(fidelity, axis=-1)
fidelity_std = np.std(fidelity, axis=-1)

snr_mean = np.mean(snr, axis=-1)
snr_std = np.std(snr, axis=-1)

psnr_mean = np.mean(psnr, axis=-1)
psnr_std = np.std(psnr, axis=-1)

dt_mean = np.mean(dt, axis=-1)
dt_std = np.std(dt, axis=-1)

if plots:
    fig, ax = plt.subplots(figsize=(10,6))
    fig.patch.set_facecolor('white')
    plt.errorbar(imaging_time_vec, fidelity_mean, yerr=fidelity_std, fmt='o')
    # plt.xscale('log')
    plt.xlabel('scattering events')
    plt.ylabel('fidelity')
    # plt.ylim([0, 1.05])
    plt.grid()
    
    fig, ax = plt.subplots(figsize=(10,6))
    fig.patch.set_facecolor('white')
    plt.errorbar(snr_mean, fidelity_mean, xerr=snr_std, yerr=fidelity_std, fmt='o')
    plt.xlabel('SNR')
    plt.ylabel('fidelity')
    # plt.ylim([0, 1.05])
    plt.grid()
    
    fig, ax = plt.subplots(figsize=(10,6))
    fig.patch.set_facecolor('white')
    plt.errorbar(psnr_mean, fidelity_mean, xerr=psnr_std, yerr=fidelity_std, fmt='o')
    plt.xlabel('psnr')
    plt.ylabel('fidelity')
    # plt.ylim([0, 1.05])
    plt.grid()
    
    fig, ax = plt.subplots(figsize=(10,6))
    fig.patch.set_facecolor('white')
    plt.errorbar(imaging_time_vec, dt_mean*1e3, yerr=dt_std*1e3, fmt='o')
    plt.xlabel('scattering events')
    plt.ylabel('time (ms)')
    # plt.xscale('log')
    plt.ylim([0,None])