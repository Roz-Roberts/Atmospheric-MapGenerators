import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import TwoSlopeNorm


# Open the NetCDF4 file
file_path = "air.2m.gauss.2023.nc"   # Contains Temperature Data For the entire globe


dataset = xr.open_dataset(file_path)


# Inspect the dataset
# print(dataset)
# exit()

variable_name = 'air'  # Temperature Variable


tm = '2023-03-01T12:00:00'



v = dataset[variable_name].sel(time=tm).squeeze().values - 273

# print(v.shape)
# exit()

# Extract latitude and longitude
lat = dataset['lat']  # Replace 'lat' with your dataset's latitude variable name
lon = dataset['lon']  # Replace 'lon' with your dataset's longitude variable name

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


# Create a diverging colormap centered at 0°C
norm = TwoSlopeNorm(vmin=v.min(), vcenter=0, vmax=v.max())  # Center white at 0°C
cmap = plt.cm.bwr # Diverging colormap (red for hot, blue for cold)


# Plot voriticty contours

contour_levels = 40

# Plot using contourf (filled contours)
contour = ax.contourf(lon_2d, lat_2d, v, transform=ccrs.PlateCarree(), cmap=cmap, norm=norm, levels=contour_levels)

TTL = f"2m Temperature (Centigrade) - {tm}"

# Add a colorbar
cbar = plt.colorbar(contour, ax=ax, orientation='vertical', shrink=0.8, pad=0.05)
cbar.set_label(f'Temperature (Centigrade)')


# Set title
ax.set_title(f"{TTL}", fontsize=14)

# Show the plot
plt.show()
