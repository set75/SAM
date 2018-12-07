# Read SAM output

from netCDF4 import Dataset
data = Dataset('/Users/sarahtannenbaum/Documents/SAM/Rayon_soundings/72241375_5day/RAYON_Rayon_2_4_0000000194.2Dcom_1.nc')
print(data.file_format)
print(data.dimensions.keys())
# x,y,time -> 192 x 288 x 1
#print(data.dimensions['y'])
x = data.variables['x'][:]
y = data.variables['y'][:]
time = data.variables['time'][:]

