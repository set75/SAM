# Rayon_snd
# z[m] p[mb] tp[K] q[g/kg] u[m/s] v[m/s] for dp = 5 mb
# u,v = 0

import numpy as np
import pandas as pd

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.units import units
import metpy.constants as mpconst
from math import log
#%%
f = open('/Users/sarahtannenbaum/Documents/SAM/Rayon_soundings/time.txt', 'r')
time = f.read()
def convert(string):
    li = list(string.split(" "))
    return li
time = convert(time)
f.close()

# create file snd.txt
f = open('/Users/sarahtannenbaum/Documents/SAM/Rayon_soundings/snd0.txt', 'a+')
f.write('z[m] p[mb] tp[K] q[g/kg] u[m/s] v[m/s] \n')
#%%
# loop by regular pressure intervals 940:100 by 5 hPa
levels = np.arange(940, 95, -5)
#i = 0
for i in range(len(time)-1):
    print(i)
    date = float(time[i])

    # read data into data frame
    col_names = ['pressure', 'temperature', 'speed', 'direction', 'height', 'dewpoint']
    file = ('/Users/sarahtannenbaum/Documents/SAM/Rayon_soundings/soundings/rayon_' + str(i+1) + '.txt')
    df = pd.read_fwf(get_test_data(file, as_file_obj=False), skiprows=1, usecols=[1,2,4,5,8,12], names=col_names)
    df['pressure'] = pd.to_numeric(df['pressure'], errors='coerce')
    df['speed'] = pd.to_numeric(df['speed'], errors='coerce')
    df['direction'] = pd.to_numeric(df['direction'], errors='coerce')
    df['height'] = pd.to_numeric(df['height'], errors='coerce')
 
    df = df.dropna(how='any').reset_index(drop=True)
    p = df.pressure.values
    df['p'] = p
    
    row_index = []
    k=0
    for j in range(len(p)-1):
        if p[j] <= levels[k]:
            row_index.append(j)
            k+=1
            x=j
        if k == len(levels):
            break
 
    # get values
    z = df['height'].values * units.meters
    p = df['pressure'].values * units.hPa
    T = (df['temperature'].values + 273.15) * units.kelvin
    Td = df['dewpoint'].values * units.degC
    u = np.zeros(len(Td))
    v = np.zeros(len(Td))
    q = mpcalc.saturation_mixing_ratio(p,Td)       
    
    data1 = np.column_stack((z.magnitude, p.magnitude, T.magnitude, 
                q.magnitude*1000, u, v))

    data = data1[row_index,:]
    data[:,1] = levels
        
    np.savetxt('/Users/sarahtannenbaum/Documents/SAM/Rayon_soundings/data.txt',
               data, fmt='%1.3f', delimiter = ' ')
    [r,c] = data.shape
    str1 = str([date, r, p.magnitude[0]]).strip('[]')
    print(str1)
    f.write(str1)
    f.write('\n')
    f2 = open('/Users/sarahtannenbaum/Documents/SAM/Rayon_soundings/data.txt', 'r')
    f.write(f2.read())
    f2.close()
    
#%%
# close file
f.close()
