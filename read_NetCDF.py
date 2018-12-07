# Read SAM output

from netCDF4 import Dataset 
# First specify the file path
data = Dataset('/Users/sarahtannenbaum/Documents/SAM/Rayon_soundings/72241375_5day/RAYON_Rayon_2_4_0000000194.2Dcom_1.nc')
print(data.file_format) # this tells you the type of NetCDF file
print(data.dimensions.keys()) # This tells you the variables
# This is how you would extract the data into vectors
x = data.variables['x'][:]
y = data.variables['y'][:]
time = data.variables['time'][:]

