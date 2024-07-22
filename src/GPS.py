import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import time

# Load initial geospatial data
tolls = pd.read_excel('Book1.xlsx')
toll_gdf = gpd.GeoDataFrame(
    tolls,
    geometry=gpd.points_from_xy(tolls.LONGITUDE, tolls.LATITUDE),
    crs="EPSG:4326"
)
buildings = gpd.read_file('chennai_shp.shp')
landuse = gpd.read_file('statehighway.shp')
# Assuming existing CRS and other layers are defined as in your example

# Create a Matplotlib figure and axes
fig, ax = plt.subplots(1, 1, figsize=(15, 15))

# Plot the layers
toll_gdf.plot(ax=ax, color='black', linewidth=1, label='Tolls')
buildings.plot(ax=ax, color='blue', alpha=0.5, label='Buildings')
landuse.plot(ax=ax, color='green', alpha=0.5, label='Land Use')

# Initialize the vehicle marker
vehicle_marker = Rectangle((0, 0), 0.001, 0.001, color='red', label='Vehicle')
ax.add_patch(vehicle_marker)

# Customize the plot
ax.set_title('Map with Roads, Buildings, and Land Use')
ax.legend()
ax.grid(True)

def update_plot():
    try:
        # Read the last line of the text file
        with open('coordinates.txt', 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                vehicle_lat, vehicle_lon = map(float, last_line.split(','))

                # Update the vehicle marker position
                vehicle_marker.set_xy((vehicle_lon, vehicle_lat))

                # Redraw the plot
                plt.pause(0.1)
    except Exception as e:
        print(f"Error updating plot: {e}")

# Set the plot to interactive mode
plt.ion()
plt.show()

# Infinite loop to update the plot with new coordinates
while True:
    update_plot()
    time.sleep(2)  # Update every second
