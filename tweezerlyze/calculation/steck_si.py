# -*- coding: utf-8 -*-
"""
Created on Sun May 24 15:52:48 2020

@author: Jacob

Cesium properties pulled from D Steck, Cesium D Line Data
"""

import numpy as np

class quantity(float):
    def __new__(self, value, unit):
        return float.__new__(self, value)
    def __init__(self, value, unit):
        float.__init__(value)
        self.unit = unit

class Transition():
    def __init__(self, properties):
        for k, qtuple in properties.items():
            value, unit = qtuple
            setattr(self, k, quantity(value, unit))


class Atom():
    def __init__(self, properties, transition_properties):
        
        for key, qtuple in properties.items():
            value, unit = qtuple
            setattr(self, key, quantity(value, unit))
        
        for line, tp in transition_properties.items():
            setattr(self, line, Transition(tp))
            
def saturation_intensity(frequency, line, polarization):
    if (frequency == 'resonant') and (line == '45') and (polarization == 'isotropic'):
        return quantity(2.7059*10, 'W/m2')
    elif (frequency == 'detuned') and (line == 'D2') and (polarization == 'linear'):
        return quantity(1.6536*10, 'W/m2')
    elif (frequency == 'resonant') and (line == 'cycling') and (polarization == 'circular'):
        return quantity(1.1023*10, 'W/m2')
    elif (frequency == 'detuned') and (line == 'D1') and (polarization == 'linear'):
        return quantity(2.4981*10, 'W/m2')
    else:
        raise Exception('Saturation intensity not precalcualted for this combination of frequency, line, and polarization.')

physical_properties = {
    'atomic_number': (55, ''),
    'total_nucleons': (133, ''),
    'relative_natural_abundance': (1, ''),
    'nuclear lifetime': (np.inf, 's'),
    'atomic_mass': (2.20694695e-25, 'kg'),
    'density_stp': (1.93 * 1e6 * 1e-3, 'kg/m3'),
    'melting_point': (28.44 + 273.15, 'K'),
    'boiling_point': (671 + 273.15, 'K'),
    'specific_heat_capacity': (0.242 * 1e3, 'J/kg*K'),
    'molar_heat_capacity': (32.210, 'J/mol*K'),
    'vapor_pressure_stp': (1.3e-6, 'torr'),
    'nuclear_spin': (7/2, ''),
    'ionization_limit': (3.89390532 * 1.602e-19, 'J'),
    }

d2_properties = {
    'frequency': (351.72571850 * 1e12, 'Hz'),
    'transition_energy': (1.454620542 * 1.602e-19, 'J'),
    'wavelength': (852.34727582 * 1e-9, 'm'),
    'lifetime': (30.473 * 1e-9, 's,'),
    'linewidth': (2 * np.pi * 5.2227 * 1e6, 'Hz'),
    'oscillator_strength': (0.7148, ''),
    'recoil_velocity': (3.5225 * 1e-3, 'm/s'),
    'recoil_energy': (2*np.pi * 2.0663 * 1e3, 'Hz'),
    'recoil_temperature': (198.34 * 1e-9, 'K'),
    'doppler_shift': (2*np.pi * 4.1327 * 1e3, 'Hz'),
    'doppler_temperature': (125 * 1e-6, 'K'),
    'Jg': (0.5, ''),
    'Je': (1.5, ''),
    }

d1_properties = {
    'frequency': (335.116048807 * 1e12, 'Hz'),
    'transition_energy': (1.385928475 * 1.602e-19, 'J'),
    'wavelength': (894.59295986 * 1e-9, 'm'),
    'lifetime': (34.894 * 1e-9, 's'),
    'linewidth': (2*np.pi * 4.5612 * 1e6, 'Hz'),
    'oscillator_strength': (0.3438, ''),
    'recoil_velocity': (3.3561 * 1e-3, 'm/s'),
    'recoil_energy': (2*np.pi * 1.8758 * 1e3 , 'Hz'),
    'recoil_temperature': (180.05 * 1e-9, 'K'),
    'doppler_shift': (2*np.pi * 3.7516 * 1e3, 'Hz'),
    'Jg': (0.5, ''),
    'Je': (0.5, ''),
    }

hyperfine_constants = {
    'magnetic_dipole_6p12': ()}

transition_properties = {
    'D1': d1_properties,
    'D2': d2_properties,
    }

cesium = Atom(physical_properties, transition_properties)
cesium.saturation_intensity = saturation_intensity