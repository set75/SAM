# Check soundings for bad data points

import numpy as np
import pandas as pd

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.units import units
import metpy.constants as mpconst
from math import log
#%%
col_names = ['pressure', 'temperature', 'speed', 'direction', 'height', 'dewpoint']
number = ['float64', 'float64','float64','int32', 'float64','float64'] 

df = pd.read_fwf(get_test_data('/Users/sarahtannenbaum/Documents/SAM/Rayon_soundings/soundings/rayon_1.txt', 
                               as_file_obj=False), skiprows=1, usecols=[1,2,4,5,8,12], names=col_names, dtype=number)
df = df.replace(['---', '----', '-----', '------'], 'na')
df = df.dropna(subset=('temperature', 'dewpoint', 'direction', 'speed',), 
                   how='all').reset_index(drop=True)
#%%
direction = df['direction'].values
direction = np.ndarray.tolist(direction)
#%%
for i in range(len(direction)):
    direction[i] = int(direction[i])
    n = i


#%%

df['u_wind'], df['v_wind'] = mpcalc.get_wind_components(df['speed'],
                                                        np.deg2rad(df['direction']))
