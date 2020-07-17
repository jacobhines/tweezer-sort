# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 18:23:43 2020

@author: Jacob
"""

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