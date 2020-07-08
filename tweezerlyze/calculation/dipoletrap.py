# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 11:08:51 2020

@author: Jacob
"""

from .steck_si import cesium
import numpy as np
import scipy.constants as cnst


def J_to_unit(energy, unit):
    """
    Converts energy from J to specified unit.

    Parameters
    ----------
    energy : float
        Energy to convert in Joules.
    unit : string
        Unit to convert to.

    Returns
    -------
    energy : float
        Energy in specified unit.

    """
    
    if unit == 'J':
        energy *= 1
    elif unit == 'Hz':
        energy *= 1/cnst.h
    elif unit == 'MHz':
        energy *= 1e-6/cnst.h
    elif unit == 'K':
        energy *= 1/cnst.Boltzmann
    else:
        raise Exception('Unit must be J, Hz, or K')
        
    return energy


def getIntensity(power, waist):
    """
    Returns intensity for given power (W) and waist (m).

    Parameters
    ----------
    power : float
        Power in W. The default is None.
    waist : float
        Beam wasit in m. The default is None.

    Returns
    -------
    float
        Intensity in w/m2.

    """
    
    return 2*power/(np.pi*(waist**2))


def depth_oscillator(species=cesium, wavelength=1064e-9, power=None, waist=None,
          intensity=None, verbose=False, unit='Hz'):
    """
    Calculates trap depth following equation 10 in OPTICAL DIPOLE TRAPS FOR 
    NEUTRAL ATOMS by Grimm and Weidemuller. (Tori method). This method
    implicitly calculates saturation intensity.

    Parameters
    ----------
    species : TYPE, optional
        DESCRIPTION. The default is cesium.
    wavelength : TYPE, optional
        DESCRIPTION. The default is 1064e-9.
    power : TYPE, optional
        DESCRIPTION. The default is None.
    waist : TYPE, optional
        DESCRIPTION. The default is None.
    intensity : TYPE, optional
        DESCRIPTION. The default is None.
    verbose : TYPE, optional
        DESCRIPTION. The default is False.
    unit : TYPE, optional
        DESCRIPTION. The default is 'Hz'.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    # frequency of drive field in Hz
    drive_frequency = cnst.c/wavelength
    
    # and rad/s
    omega_drive = 2*np.pi*drive_frequency
    
    # intensity in W/m2
    if intensity is None:
        I = getIntensity(power, waist)
    else:
        I = intensity
    
    def u2level(omega_transition, linewidth):
        prefactor = (3*np.pi*cnst.c**2)/(2*omega_transition**3)
        freqFactor = -linewidth*(1/(omega_transition-omega_drive) + 1/(omega_transition+omega_drive))
        return prefactor*freqFactor*I
    
    depth = (2/3)*u2level(2*np.pi*species.D2.frequency, species.D2.linewidth) \
            + (1/3)*u2level(2*np.pi*species.D1.frequency, species.D1.linewidth)
        
    # change energy unit
    depth = J_to_unit(depth, unit)
            
    if verbose:
        print('depth:', depth)
        print('')
        
    return depth


def depth_steck_classical(species=cesium, wavelength=1064e-9, power=None,
                          waist=None, intensity=None, verbose=False, unit='Hz'):
    """
    Calculates trap depth following equation 1.76 in Quantum and Atom Optics
    by Steck. This method looks up the saturation intensity for D1 and D2.
    (Jacob method).

    Parameters
    ----------
    species : TYPE, optional
        DESCRIPTION. The default is cesium.
    wavelength : TYPE, optional
        DESCRIPTION. The default is 1064e-9.
    power : TYPE, optional
        DESCRIPTION. The default is None.
    waist : TYPE, optional
        DESCRIPTION. The default is None.
    intensity : TYPE, optional
        DESCRIPTION. The default is None.
    verbose : TYPE, optional
        DESCRIPTION. The default is False.
    unit : TYPE, optional
        DESCRIPTION. The default is 'Hz'.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    # frequency of laser field in Hz
    drive_frequency = cnst.c/wavelength
    
    # and rad/s
    omega_drive = 2*np.pi*drive_frequency
    
    # intensity in W/m2
    if intensity is None:
        I = getIntensity(power, waist)
    else:
        I = intensity
        
    weights = {'D2': 2/3,
               'D1': 1/3}
    
    def stark(omega_transition, linewidth, I_sat):
        prefactor = cnst.hbar * linewidth**2 / 8
        freqfactor = 1/(omega_drive - omega_transition) - 1/(omega_drive + omega_transition)
        s0 = I/I_sat
        return prefactor*freqfactor*s0
    
    depth = 0
    
    for transition in weights:           
        t = getattr(species, transition)
        I_sat = species.saturation_intensity('detuned', transition, 'linear')
        depth += weights[transition]*stark(2*np.pi*t.frequency, t.linewidth, I_sat)
        
    # change energy unit
    depth = J_to_unit(depth, unit)
            
    if verbose:
        print('depth:', depth)
        print('')
        
    return depth
        
        
def depth_oscillator_rwa(species=cesium, wavelength=1064e-9, power=None,
                            waist=None, intensity=None, verbose=False, unit='Hz'):
    """
    Calculates trap depth following equation 2 in Loading an optical dipole trap
    by Kuppens et al. (Jacob method).

    Parameters
    ----------
    species : Atom class, optional
        Class containing atomic properties, as defined in steck.py. The default
        is cesium.
    wavelength : float, optional
        Trapping beam wavelength in m. The default is 1064e-9.
    power : float, optional
        Trapping beam power in W. The default is None.
    waist : float, optional
        Trapping beam waist in m. The default is None.
    intensity : float, optional
        Trapping beam intensity in W/m2. The default is None.
    verbose : bool, optional
        Set to True to display debugging values. The default is False.
    unit : str, optional
        Unit for the returned trap depth, can be J, K, or Hz. The default is 'Hz'.

    Returns
    -------
    depth : float
        Trap depth in specified units.
        
    """
    
    # intensity in W/m2
    if intensity is None:
        I = getIntensity(power, waist)
    else:
        I = intensity
        
    # saturation parameter
    I_sat = species.saturation_intensity('detuned', 'D2', 'linear')
    s0 = I/I_sat
    
    # inverse detuning in linewidths
    drive_frequency = cnst.c/wavelength #Hz 
    delta1 = 2*np.pi*(drive_frequency - species.D1.frequency)/(species.D1.linewidth)
    delta2 = 2*np.pi*(drive_frequency - species.D2.frequency)/(species.D2.linewidth)
    inv_delta = (1/3)*(1/delta1 + 2/delta2)
    
    depth = cnst.hbar * (species.D2.linewidth / 8) * s0 * inv_delta
    
    # change energy unit
    depth = J_to_unit(depth, unit)

    if verbose:
        print('I:', I)
        print('I_sat:', I_sat)
        print('s0:', s0)
        print('inv_delta', inv_delta)
        print('depth:', depth, unit)
        print('')
            
    return depth
        

def depth_steck_quantum(species=cesium, wavelength=1064e-9, power=None, waist=None, 
                        intensity=None, verbose=False, unit='Hz', method='simplified'):
    """
    Calculates trap depth following equations 7.304 and 7.457 in Quantum and
    Atom Optics by Steck. (Ogi method).

    Parameters
    ----------
    species : Atom class, optional
        Class containing atomic properties, as defined in steck.py. The default
        is cesium.
    wavelength : float, optional
        Trapping beam wavelength in m. The default is 1064e-9.
    power : float, optional
        Trapping beam power in W. The default is None.
    waist : float, optional
        Trapping beam waist in m. The default is None.
    intensity : float, optional
        Trapping beam intensity in W/m2. The default is None.
    verbose : bool, optional
        Set to True to display debugging values. The default is False.
    unit : str, optional
        Unit for the returned trap depth, can be J, K, or Hz. The default is 'Hz'.

    Returns
    -------
    depth : float
        Trap depth in specified units.
        
    """

    # Steck quantum optics 7.296 connects reduced matrix element with linewidth
    def rMatrixElement(omega_transition, linewidth, Jg, Je):
        prefactor = 3*np.pi*cnst.epsilon_0*cnst.hbar*cnst.c**3
        degeneracyfactor = (2*Je+1)/(2*Jg+1)
        return np.sqrt(degeneracyfactor*prefactor*linewidth/omega_transition**3)
    
    # Steck quantum optics 7.485 (update: 7.457?) gives formula for lare detuning optical stark shift
    def OpticalStarkShiftFull(omega_transition, omega_drive, linewidth, Jg, Je, I):
        #In steck this is the positive frequency E field component E_0+ for which |E_0|^2 = 4 |E_0+|^2:
        Esquared = I*2*cnst.mu_0*cnst.c 
        freqfactor = omega_transition/(omega_transition**2-omega_drive**2)
        return -2*freqfactor*Esquared*rMatrixElement(omega_transition, linewidth, Jg, Je)**2/(3*cnst.hbar)
    
    # simplified formula
    def OpticalStarkShiftSimplified(omega_transition, omega_drive, linewidth, Jg, Je, I):
        degeneracyfactor = (2*Je+1)/(2*Jg+1)
        freqfactor = omega_transition**2*(omega_transition**2-omega_drive**2)
        return -1*degeneracyfactor*4*np.pi*cnst.c**2*linewidth*I/freqfactor
    
    # choose method
    if method =='simplified':
        f = OpticalStarkShiftSimplified
    elif method == 'full':
        f =  OpticalStarkShiftFull
    else:
        raise Exception('Method must be simplified or full.')
        
    # intensity in W/m2
    if intensity is None:
        I = getIntensity(power, waist)
    else:
        I = intensity
        
    # frequency of laser field in Hz
    drive_frequency = cnst.c/wavelength
    
    # and rad/s
    omega_drive = 2*np.pi*drive_frequency
        
    shift = {}
    
    transitions = ['D2', 'D1']
    for transition in transitions:
        t = getattr(species, transition)
        
        omega_transition = 2*np.pi*t.frequency
        
        linewidth = t.linewidth
        Jg = t.Jg
        Je = t.Je
        
        if verbose:
            print('omega_transition:', omega_transition)
            print('omega_drive:', omega_drive)
            print('linewidth', linewidth)
            print('Jg', Jg)
            print('Je', Je)
            print('I:', I)
            print('')
        
        shift[transition] = f(omega_transition, omega_drive, linewidth, Jg, Je, I)
        
    depth = np.sum(list(shift.values())) #J

    # change energy unit
    depth = J_to_unit(depth, unit)
        
    if verbose:
        print('depth:', depth)
        
    return depth