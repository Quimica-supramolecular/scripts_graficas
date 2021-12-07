# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 10:56:29 2021

@author: jan_c
"""

import pandas as pd
from scipy.stats.mstats import winsorize 
import numpy as np

a = [185.2, 180, 159.5, 157.2, 179.7, 200.4,\
     196.5, 165.6, 173.7, 179.3, 154.0]
    
b = winsorize(a, limits=[0.05, 0.05])

print(np.mean(a))
print(np.mean(b))

print(a)
print(b)

#%% datos de wiki

c = np.array([92, 19, 101 , 58, 1053 , 91, 26, 78, 10, 13, -40, 101 , 86, 85, 15, 89, 89, 28, -5 , 41])
d = winsorize(c, limits=[0.05, 0.05])
print(np.mean(c))
print(np.mean(d))

