import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import TwoSlopeNorm
from matplotlib.colors import LinearSegmentedColormap


# Open the NetCDF4 file
file_path = "hgt.raw.2023.nc"   # Contains Geopotential Data For the entire globe
dataset = xr.open_dataset(file_path)



# Inspect the dataset
# print(dataset)


variable_name = 'hgt'

tm = '2023-03-01T12:00:00'

press_lvl_high = 500.0

press_lvl_low = 1000

data = (dataset[variable_name].sel(time=tm, level=press_lvl_high).squeeze().values - dataset[variable_name].sel(time=tm, level=press_lvl_low).squeeze().values)/10  # Choose the correct time and pressure level

# print(data)


# Extract latitude and longitude
lat = dataset['lat'].values  # Replace 'lat' with your dataset's latitude variable name
lon = dataset['lon'].values  # Replace 'lon' with your dataset's longitude variable name

# Convert longitudes from [0, 360] to [-180, 180]
lon = np.where(lon > 180, lon - 360, lon)


# [-130, -60, 20, 50]

# Apply constraints
lat_indices = np.where((lat >= 15) & (lat <= 55))[0]
lon_indices = np.where((lon >= -142) & (lon <= -50))[0]

lat_constrained = lat[lat_indices]
lon_constrained = lon[lon_indices]
data_constrained = data[np.ix_(lat_indices, lon_indices)]


# Create 2D latitude and longitude arrays
lon_2d, lat_2d = np.meshgrid(lon_constrained, lat_constrained)


projection = ccrs.LambertConformal(central_longitude=-96, central_latitude=37.5)  # Creates correct projection type


# Plot the data
fig, ax = plt.subplots(subplot_kw={'projection': projection}, figsize=(10, 6))
ax.set_extent([-125, -65, 25, 49], crs=ccrs.PlateCarree())  # Set map extent to US

# Add map features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.STATES, edgecolor='gray')


contour_levels = 30


# Create a diverging colormap centered at 0°C
norm = TwoSlopeNorm(vmin=data_constrained.min(), vcenter=540, vmax=data_constrained.max())  # Center white at 0°C
# cmap = plt.cm.winter # Diverging colormap (red for hot, blue for cold)

# Define the custom colormap
colors = [(17/255, 0/255, 255/255), (2/255,6/255,120/255), (0/255, 0/255, 0/255), (135/255,1/255,1/255) ,(227/255, 0/255, 0/255)]

# Create the colormap
cmap_name = "BlueBlackRed"
# n_colors = 500  # Number of colors in the colormap
custom_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=contour_levels)



# Optionally add contour lines
contour_lines = ax.contour(lon_2d, lat_2d, data_constrained, transform=ccrs.PlateCarree(), cmap=custom_cmap, norm=norm, linewidths=0.5, levels=contour_levels)



TTL = f"1000-500 hPa Thickness - {tm}"  # Formats correct title

# Add a colorbar (If Wanted)
# cbar = plt.colorbar(contour_lines, ax=ax, orientation='vertical', shrink=0.7, pad=0.05)
# cbar.set_label(f'{TTL}')


# Add labels to contour lines
ax.clabel(contour_lines, inline=True, inline_spacing=0.1, fontsize=9, fmt='%1.1f')

# Set title
ax.set_title(f"{TTL} over the US ({contour_levels} Contours)", fontsize=14)

# Show the plot
plt.show()

