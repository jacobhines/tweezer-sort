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

# preamp setting / amplifier type / readout rate
# unit: electrons per A/D count
# Sensitivity is measured in electrons per A/D count from a plot of Variance [Noise squared] against Signal.
sensitivity_dict = {
    1: {
        'EM': {
            30e6: 18.6,
            20e6: 17.4,
            10e6: 16.3,
            1e6: 16.4,
            },
        'conventional': {
            1e6: 3.44,
            0.1e6: 3.47,
            }
        },
    2: {
        'EM': {
            30e6: 5.89,
            20e6: 4.76,
            10e6: 4.05,
            1e6: 3.97,
            },
        'conventional': {
            1e6: 0.820,
            0.1e6: 0.830,
            }
        }
    }

# preamp setting / amplifier type / readout rate
# unit: electrons
# RMS Readout Noise is measured for single pixel readout with the CCD in darkness
# at temperature indicated (-70C) and minimum exposure time. Noise values will change 
# with pre-amplifier gain selection [PAG].
single_pixel_noise_dict = {
    1: {
        'EM': {
            30e6: 250,
            20e6: 157,
            10e6: 86.2,
            1e6: 25.3,
            },
        'conventional': {
            1e6: 6.81,
            0.1e6: 9.61,
            }
        },
    2: {
        'EM': {
            30e6: 174,
            20e6: 73.1,
            10e6: 41.0,
            1e6: 12.4,
            },
        'conventional': {
            1e6: 4.97,
            0.1e6: 3.70,
            }
        }
    }

# image area saturation signal per pixel
# unit: electrons/pixel
well_depth = 88300 

# CIC is measured in darkness with EM gain set to the operating maximum (1000x) 
# at fastest Horizontal Shift Speed and second fastest Vertical Shift Speed. 
# A threshold in counts above the base mean level equivalent to the number of 
# electrons that would be output at the maximum EM gain is determined using the 
# camera's sensitivity at these settings. The number of pixels with count values 
# above that threshold is counted and this is converted to a number of events 
# per total pixels on the sensor.
# unit: events/pixel
clock_induced_charge_occurence = 0.00184 #events/pixel, see note 3

# Dark current falls of exponentially with temperature. However, for a given
# termperature the actual dark current can vary by more than an order of 
# magnitude from device to device. The devices are specified in terms of minimum 
# dark current achievable rather than minimum temperature.
# unit: electrons/pixel/second at -100C sensor temperature
minimum_dark_current = 9.1e-5

def getDarkCurrent(T, unit='K'):
    """
    calibrated from D(-80)=2.4e-4, D(-100)=1.1e-4 taken from andor ixon 
    generic spec sheet and D = D0 exp(-E/kT) = D0 exp(-epsilon/T)
    """
    
    if unit == 'K':
        pass
    elif unit == 'C':
        T += 273.15
    else:
        raise Exception('Unit must be K or C.')
    
    D0 = 0.3053152252888037
    epsilon = 1372.840497871531
    return D0 * np.exp(-epsilon/T)

# Quantum efficiency is probability of a photon being converted to a 
# photoelectron. Andor quotes > 95% quantum efficiency for iXon ultra 888,
# but this is at peak wavelength. At 852 our BV sensor is about 0.55
# unit: photoelectrons/photon
quantum_efficiency = 0.55


# We observe a constant offset of ~500 counts, reagardless of camera settings
signal_offset = 500

#standard values: preamp gain 1, 30 MHz hss, EM amplifier type, EM gain 100


class Optics():
    def __init__(self, magnification, NA):
        self.magnification = magnification
        self.NA = NA
        self.collection_efficiency = 0.5*(1 - np.sqrt(1 - NA**2))
        
    def set_diffraction(self, wavelength):
        self.sigma_diffraction = 0.42*wavelength/(2*self.NA)
        
    def apply_diffraction(self, photon_positions):
        #http://mtfmapper.blogspot.com/2012/11/importance-sampling-how-to-simulate.html
        # "It seems like quite a lot of effort to simulate images with PSFs that
        # correspond to diffraction effects, only to end up with images that look 
        # like those generated with Gaussian PSFs."
        return np.random.normal(loc=photon_positions, scale=self.sigma_diffraction)
        

class IxonUltra888():
    def __init__(self, pixel_size, sensor_size, gain, preamp_setting, 
                 amplifier_type, readout_rate, sensor_temperature, 
                 exposure_time, position=(0,0)):
        
        # store settings
        self.pixel_size = pixel_size
        self.sensor_size = sensor_size
        self.gain = gain
        self.preamp_setting = preamp_setting
        self.amplifier_type = amplifier_type
        self.readout_rate = readout_rate
        self.sensor_temperature = sensor_temperature
        self.exposure_time = exposure_time
        self.position = position
        
        # containers and state booleans
        self.photon_positions = None
        self.image = None
        self.scale_set = False
        
        # store performance sheet specs
        self.sensitivity = sensitivity_dict[preamp_setting][amplifier_type][readout_rate]
        self.single_pixel_noise = single_pixel_noise_dict[preamp_setting][amplifier_type][readout_rate]
        self.well_depth = well_depth
        self.clock_induced_charge_occurence = clock_induced_charge_occurence
        self.minimum_dark_current = minimum_dark_current
        self.quantum_efficiency = quantum_efficiency
        self.signal_offset = signal_offset
        self.dark_current = getDarkCurrent(sensor_temperature, unit='K')
        self.dark_charge = self.dark_current * self.exposure_time
        
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
        
        # bin the photons into pixels
        x = photon_positions[0,:]
        y = photon_positions[1,:]
        incident_photons = np.histogram2d(x, y, bins=self.pixel_bins)[0]
        
        # to account for shot noise we resample our binned photons from a poisson distribution
        incident_photons = np.random.poisson(incident_photons)
        
        # photoelectrons is incident photons multiplied by quantum efficiency
        photoelectrons = incident_photons * self.quantum_efficiency      
        
        # add pre-gain photoelectron noise sources
        dark_noise = np.random.poisson(self.dark_charge, photoelectrons.shape)
        charge_noise = np.random.poisson(self.clock_induced_charge_occurence, photoelectrons.shape)
        photoelectrons += dark_noise + charge_noise
        
        # signal electrons are photoelectrons multipled by EM gain
        signal_electrons = photoelectrons * self.gain
        
        # combine signal with electron readout noise to get image electrons
        noise = np.random.normal(0, self.single_pixel_noise, self.sensor_size)
        image_electrons = signal_electrons + noise
        
        # convert electrons to digital camera signal
        image = image_electrons / self.sensitivity
        signal = signal_electrons / self.sensitivity
        
        # add in offset
        image += self.signal_offset
        signal += self.signal_offset

        # convert to uint16
        self.signal = signal.astype('uint16')
        self.image = image.astype('uint16')
        
    
    def grab_image(self):
        """
        Returns most recently exposed image.

        Returns
        -------
        self.image: ndarray
            Fluorescent counts in a 2D array.

        """
        return self.image
    
    def crop_image(self, roi):
        """
        Crops the most recently acquired image.
        """
        self.image_cropped = self.image[roi['xmin']:roi['xmax'], roi['ymin']:roi['ymax']]
        self.signal_cropped = self.signal[roi['xmin']:roi['xmax'], roi['ymin']:roi['ymax']]

            
        return self.image_cropped
    
    def show_image(self, cropped=True, title=None, colorbar=False, scalebar=False, scalebar_length=None):
        """
        Displays the most recently acquired image.
        """
        if cropped:
            image = self.image_cropped
        else:
            image = self.image
        
        fig, ax = plt.subplots(figsize=(15,10))
        plt.imshow(image.T, origin='lower')
        
        if scalebar:
            scalebar = AnchoredSizeBar(ax.transData,
                               scalebar_length/self.scale[0],
                               f'{1e6*scalebar_length} um',
                               'upper right', 
                               pad=1,
                               color='white',
                               frameon=False,
                               size_vertical=0.5,
                               sep = 10,
                               fontproperties=fontprops)
    
            ax.add_artist(scalebar)

        if colorbar:
            plt.colorbar(label='counts', pad=0.01)
            
        if title:
            plt.title(title)
            
        plt.xlabel('x (px)')
        plt.ylabel('y (px)')
        fig.patch.set_facecolor('white')
        
        
class Imaging():
    def __init__(self, optics_options, camera_options, laser_options, scattering_rate=None, **kwargs):
        self.laser = Laser(**laser_options)
        
        self.optics = Optics(**optics_options)
        self.optics.set_diffraction(self.laser.wavelength)
        
        self.camera = IxonUltra888(**camera_options)
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