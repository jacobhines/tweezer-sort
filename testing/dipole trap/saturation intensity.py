# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 18:35:46 2020

@author: Jacob
"""


# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 11:29:45 2020

@author: Jacob
"""

from tweezerlyze.calculation.intensity import saturationIntensity
from tweezerlyze.calculation.steck_si import cesium

debug = False
Isat = {}

# 44-55 cycling
line = 'D2'
F = 4
Fprime = 5
polarization = 'sigma_plus'
configuration = 'pumped_plus'
far_detuned=False
Isat['44-55 cycling'] = saturationIntensity(cesium, line, F, Fprime, polarization, configuration, far_detuned, debug)

# 4-5 isotropic
line = 'D2'
F = 4
Fprime = 5
polarization = 'sigma_minus'
configuration = 'distributed'
far_detuned=False
Isat['4-5 isotropic'] = saturationIntensity(cesium, line, F, Fprime, polarization, configuration, far_detuned, debug)

# D2 detuned pi
line = 'D2'
F = None
Fprime = None
polarization = 'pi'
configuration = None
far_detuned=True
Isat['D2 detuned pi'] = saturationIntensity(cesium, line, F, Fprime, polarization, configuration, far_detuned, debug)

# D1 detuned pi
line = 'D1'
F = None
Fprime = None
polarization = 'pi'
configuration = None
far_detuned=True
Isat['D1 detuned pi'] = saturationIntensity(cesium, line, F, Fprime, polarization, configuration, far_detuned, debug)

# 4-5 sigma plus uniform distribution
line = 'D2'
F = 4
Fprime = 5
polarization = 'sigma_plus'
configuration = 'distributed'
far_detuned=False
Isat['4-5 sigma plus uniform distribution'] = saturationIntensity(cesium, line, F, Fprime, polarization, configuration, far_detuned, debug)

# 4-5 pi steady-state distribution
line = 'D2'
F = 4
Fprime = 5
polarization = 'pi'
configuration = {-2: 1/6, -1: 1/6, 0: 1/3, 1:1/6, 2:1/6} #shot in the dark, but clustered towards 0
far_detuned=False
Isat['4-5 pi steady-state distribution'] = saturationIntensity(cesium, line, F, Fprime, polarization, configuration, far_detuned, debug)

for key, val in Isat.items():
    print(key, val/10)