import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as scp
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature



# Open the NetCDF4 file
file_path = "hgt.raw.2023.nc"   # Contains Geopotential Data Fro the entire globe
dataset = xr.open_dataset(file_path)



# Inspect the dataset
print(dataset)

# Convert a variable to a Pandas DataFrame
# Replace 'your_variable_name' with the variable you want to extract
variable_name = 'hgt'

tm = '2023-03-01T18:00:00'

press_lvl = 500.0

data = dataset[variable_name].sel(time=tm, level=press_lvl).squeeze()  # Choose time index if applicable

print(data)


# Extract latitude and longitude
lat = dataset['lat']  # Replace 'lat' with your dataset's latitude variable name
lon = dataset['lon']  # Replace 'lon' with your dataset's longitude variable name

# Create 2D latitude and longitude arrays
lon_2d, lat_2d = np.meshgrid(lon, lat)


projection = ccrs.LambertConformal(central_longitude=-96, central_latitude=37.5)


# Plot the data
fig, ax = plt.subplots(subplot_kw={'projection': projection}, figsize=(10, 6))
ax.set_extent([-130, -60, 20, 50], crs=ccrs.PlateCarree())  # Set map extent to US

# Add map features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.STATES, edgecolor='gray')


contour_levels = 50

# Plot using contourf (filled contours)
contour = ax.contourf(lon_2d, lat_2d, data, transform=ccrs.PlateCarree(), cmap='bwr', levels=contour_levels)

# Optionally add contour lines
contour_lines = ax.contour(lon_2d, lat_2d, data, transform=ccrs.PlateCarree(), colors='black', linewidths=0.5, levels=contour_levels)



TTL = f"500 hPa Geopotential - {tm}"
# # Add a colorbar
# cbar = plt.colorbar(contour, ax=ax, orientation='vertical', shrink=0.7, pad=0.05)
# cbar.set_label(f'{TTL}')

# Add labels to contour lines
ax.clabel(contour_lines, inline=True, fontsize=8, fmt='%1.1f')

# Set title
ax.set_title(f"{TTL} over the US (50 Contours)", fontsize=14)

# Show the plot
plt.show()

