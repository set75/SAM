# Rayon_sfc.py reads flux tower data into text file for SAM

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime as dt
import numpy as np

colnames = ['time', 'LE', 'H', 'Temp']
df = pd.read_excel('/Users/sarahtannenbaum/Documents/SAM/Rayon_soundings/rayon_flux_data.xlsx',
                   sheetname='Rayon', skiprows=2, usecols=[0,7,11,20], names=colnames)
df = df.drop(df[(df.Temp == -9999)].index)
df = df.reset_index()
#%%
# format date & time
time = df.time
date = []
day = []
hour = []
for i in range(len(time)):
    t = float(time[i].dayofyear) + time[i].hour/24 + time[i].minute/(60*24)
    date.append(t)
    day.append(time[i].dayofyear)
    hour.append(time[i].hour + time[i].minute/60)
#%%
date = np.asarray(date)
Temp = np.asarray(df.Temp + 273.15)
H = np.asarray(df.H)
LE = np.asarray(df.LE)
tau = np.asarray([0] * len(date))
#%%
# check data for outliers & mitigate them
import matplotlib.pyplot as plt 
import statistics as st

sdT = np.std(Temp)
#Temp = Temp[5108:5118]
dTemp = np.diff(Temp)
#plt.hist(dTemp, bins = 20, range=(-2,2))
n = len(dTemp)-1
for k in range(2,n):
    if ((dTemp[k] > 1.6) | (dTemp[k] < -1)):
        Temp[k+1] = Temp[k-1]
        dTemp = np.diff(Temp)

sdH = np.std(H)
dH = np.diff(H)
#plt.hist(dH, bins = 20, range=(-200,200))
n = len(dH)-1
for k in range(2,n):
    if ((dH[k] > 150) | (dH[k] < -150)):
        H[k+1] = H[k-1]
        dH = np.diff(H)

sdLE = np.std(LE)
dLE = np.diff(LE)
#plt.hist(dLE, bins = 20, range=(-200,200))
n = len(dLE)-1
for k in range(2,n):
    if ((dLE[k] > 150) | (dLE[k] < -150)):
        LE[k+1] = LE[k-1]
        dLE = np.diff(LE)

#%%
dTemp = np.diff(Temp)
dH = np.diff(H)
dLE = np.diff(LE)
#plt.plot(dTemp)
#plt.plot(dH)
#plt.plot(dLE)
#%%        
# create data matrix
data = np.column_stack((date, Temp, H, LE, tau))
#data = pd.DataFrame({'date': date, 'Temp': Temp, 'H': H, 'LE': LE, 'tau': tau})
#data = data.drop(data[(data.Temp == -9999)].index)

# subset dates to match snd
data_index = []
for j in range(len(date)-1):
    if data[j,0] >= 226.3:
        data_index.append(j)
    if data[j,0] >= 231.35:
        break

data = data[data_index,:]

#%%
np.savetxt('/Users/sarahtannenbaum/Documents/SAM/Rayon_soundings/data.txt', data,
           fmt='%1.3f', delimiter = ' ')

#%%
# create .txt file
f = open('/Users/sarahtannenbaum/Documents/SAM/Rayon_soundings/sfc.txt', 'w+')
f.write('day sst(K) H(W/m2) LE(W/m2) TAU(m2/s2) \n')
f2 = open('/Users/sarahtannenbaum/Documents/SAM/Rayon_soundings/data.txt', 'r')
f.write(f2.read())
f.close()

