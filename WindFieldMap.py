import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import LinearSegmentedColormap


# Open the NetCDF4 file
file_pathu = "uwnd.2023.nc"   # Contains U-Wind Data For the entire globe
file_pathv = "vwnd.2023.nc"   # Contains V-Wind Data For the entire globe

datasetu = xr.open_dataset(file_pathu)
datasetv = xr.open_dataset(file_pathv)



# Inspect the dataset
# print(datasetv)



u_wind = 'uwnd'  # Gets U-Vector Wind

v_wind = 'vwnd'  # Gets V-Vector Wind

tm = '2023-03-01T12:00:00'

press_lvl = 850.0

u = datasetu[u_wind].sel(time=tm, level=press_lvl).squeeze().values
v = datasetv[v_wind].sel(time=tm, level=press_lvl).squeeze().values

wspd = np.sqrt(u**2 + v**2)


# print(u)

# print(v)


# Extract latitude and longitude
lat = datasetu['lat']  # Replace 'lat' with your dataset's latitude variable name
lon = datasetu['lon']  # Replace 'lon' with your dataset's longitude variable name

# Create 2D latitude and longitude arrays
lon_2d, lat_2d = np.meshgrid(lon, lat)


projection = ccrs.LambertConformal(central_longitude=-96, central_latitude=37.5) # Sets the type of projection


# Plot the data
fig, ax = plt.subplots(subplot_kw={'projection': projection}, figsize=(10, 6))
ax.set_extent([-130, -60, 20, 50], crs=ccrs.PlateCarree())  # Set map extent to US

# Add map features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.STATES, edgecolor='gray')


# Plot Wind Barb Vecotrs/Streamlines:

skip = 1

# barbs = ax.barbs(lon_2d[::skip, ::skip], lat_2d[::skip, ::skip], u[::skip, ::skip], v[::skip, ::skip], length = 6, transform=ccrs.PlateCarree())

stream = ax.streamplot(lon_2d, lat_2d, u, v, transform=ccrs.PlateCarree(), color='black', linewidth=1, density=0.6, broken_streamlines=False)


# Plot wind speed contours

contour_levels = 40

# Plot using contourf (filled contours)
contour = ax.contourf(lon_2d, lat_2d, wspd, transform=ccrs.PlateCarree(), cmap='coolwarm', levels=contour_levels)


TTL = f"{press_lvl} hPa Wind-field (streamlines with overlayed wind speed) - {tm}"

# Add a colorbar
cbar = plt.colorbar(contour, ax=ax, orientation='vertical', shrink=0.7, pad=0.05)
cbar.set_label(f'Wind Speed [m/s]')


# Set title
ax.set_title(f"{TTL}", fontsize=14)

# Show the plot
plt.show()
