# -*- coding: utf-8 -*-
"""
Created on Sun May 24 15:52:48 2020

@author: Jacob

Cesium properties pulled from D Steck, Cesium D Line Data
"""

import numpy as np
from . import constants as cs


class Transition():
    def __init__(self, properties):
        for k, qtuple in properties.items():
            value, unit = qtuple
            setattr(self, k, cs.quantity(value, unit))


class Atom():
    def __init__(self, properties, transition_properties):
        
        for key, qtuple in properties.items():
            value, unit = qtuple
            setattr(self, key, cs.quantity(value, unit))
        
        for line, tp in transition_properties.items():
            setattr(self, line, Transition(tp))
            
def saturation_intensity(frequency, line, polarization):
    if (frequency == 'resonant') and (line == '45') and (polarization == 'isotropic'):
        return cs.quantity(2.7059, 'mW/cm2')
    elif (frequency == 'detuned') and (line == 'D2') and (polarization == 'linear'):
        return cs.quantity(1.6536, 'mW/cm2')
    elif (frequency == 'resonant') and (line == 'cycling') and (polarization == 'circular'):
        return cs.quantity(1.1023, 'mW/cm2')
    elif (frequency == 'detuned') and (line == 'D1') and (polarization == 'linear'):
        return cs.quantity(2.4981, 'mW/cm2')
    else:
        raise Exception('Saturation intensity not precalcualted for this combination of frequency, line, and polarization.')

physical_properties = {
    'atomic_number': (55, ''),
    'total_nucleons': (133, ''),
    'relative_natural_abundance': (1, ''),
    'nuclear lifetime': (np.inf, 's'),
    'atomic_mass': (2.20694695e-25, 'kg'),
    'density_stp': (1.93, 'g/cm3'),
    'melting_point': (28.44, 'degC'),
    'boiling_point': (671, 'degC'),
    'specific_heat_capacity': (0.242, 'J/g*K'),
    'molar_heat_capacity': (32.210, 'J/mol*K'),
    'vapor_pressure_stp': (1.3e-6, 'torr'),
    'nuclear_spin': (7/2, ''),
    'ionization_limit': (3.89390532, 'eV'),
    }

d2_properties = {
    'frequency': (351.72571850, 'THz'),
    'transition_energy': (1.454620542, 'eV'),
    'wavelength': (852.34727582, 'nm'),
    'lifetime': (30.473, 'ns,'),
    'linewidth': (2*np.pi * 5.2227, 'MHz'),
    'oscillator_strength': (0.7148, ''),
    'recoil_velocity': (3.5225, 'mm/s'),
    'recoil_energy': (2*np.pi * 2.0663, 'kHz'),
    'recoil_temperature': (198.34, 'nk'),
    'doppler_shift': (2*np.pi * 4.1327, 'kHz'),
    'doppler_temperature': (125, 'uk'),
    }

d1_properties = {
    'frequency': (335.116048807, 'THz'),
    'transition_energy': (1.385928475, 'eV'),
    'wavelength': (894.59295986, 'nm'),
    'lifetime': (34.894, 'ns,'),
    'linewidth': (2*np.pi * 4.5612, 'MHz'),
    'oscillator_strength': (0.3438,''),
    'recoil_velocity': (3.3561, 'mm/s'),
    'recoil_energy': (2*np.pi * 1.8758 , 'kHz'),
    'recoil_temperature': (180.05, 'nk'),
    'doppler_shift': (2*np.pi * 3.7516, 'kHz'),
    }

hyperfine_constants = {
    'magnetic_dipole_6p12': ()}

transition_properties = {
    'D1': d1_properties,
    'D2': d2_properties,
    }

cesium = Atom(physical_properties, transition_properties)
cesium.saturation_intensity = saturation_intensity