# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 18:16:12 2020

@author: Jacob
"""

import numpy as np

def get_shifts_1d(occupancies, alignment='left'):
    
    if occupancies.dtype == int:
        occupancies = occupancies.astype('bool')
    
    if type(alignment) == int:
        reference = alignment
    elif alignment == 'left':
        reference = 0
    elif alignment == 'right':
        reference = len(occupancies)-1
    elif alignment == 'center':
        reference = len(occupancies)//2
    else:
        raise Exception('Alignment must be left, right, or center.')
        
    # indices of occupied sites
    indices = np.arange(len(occupancies))[occupancies]
    shifts = []
    
    for idx, occupied in enumerate(occupancies):
        # skip if not occupied
        if not occupied:
            shifts.append(float('nan'))
            continue
        
        # shift by the number of zeros between occupied site and reference site  
        start = min([idx, reference])
        stop = max([idx, reference])  
        occupancies_slice = occupancies[start:stop]
        shift = np.count_nonzero(occupancies_slice==0)
        
        # set direction
        if idx > reference:
            shift *= -1
            
        shifts.append(shift)
            
    return shifts

if __name__ == '__main__':
    
    occupancies = np.round(np.random.rand(10)).astype('int')
    alignment = 'left'
    shifts = get_shifts_1d(occupancies, alignment=alignment)
    print(occupancies)
    print(shifts)