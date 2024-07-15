#Geospatial.py

import geopandas as gpd
import pandas as pd
import os

# Load routes from text files
def load_route(file_path):
    with open(file_path, 'r') as f:
        return eval(f.read())

# Shapefile of all road networks
NATIONAL_HIGHWAYS_PATH = '../Data/Map network/chennai_shp.shp'
STATE_HIGHWAYS_PATH = '../Data/Map network/statehighway.shp'

# Textfile of specific routes
def load_routes_from_folder(folder_path):
    routes = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            route_path = os.path.join(folder_path, filename)
            routes.append(load_route(route_path))
    return routes

# Define the folder path where your routes are stored
folder_path = '../Data/Paths'

# Load routes from the folder
ROUTES = load_routes_from_folder(folder_path)
# Excel sheet of toll points (Only for map plotting purposes)

# Load shapefiles into GeoDataframes
national_highway = gpd.read_file(NATIONAL_HIGHWAYS_PATH)
state_highway = gpd.read_file(STATE_HIGHWAYS_PATH)

# Ensure all layers use the same coordinate reference system (CRS)
crs = national_highway.crs

# Convert the routes to the same CRS
route_gdfs = []
for route in ROUTES:
    route_gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy([p[1] for p in route], [p[0] for p in route]))
    route_gdf = route_gdf.set_crs(epsg=4326).to_crs(crs)
    route_gdfs.append(list(zip(route_gdf.geometry.x, route_gdf.geometry.y)))

# Load toll points from Excel file
tolls = pd.read_excel('toll_coordinates.xlsx')
toll_gdf = gpd.GeoDataFrame(
    tolls,
    geometry=gpd.points_from_xy(tolls.LONGITUDE, tolls.LATITUDE),
    crs="EPSG:4326"
)
toll_gdf = toll_gdf.to_crs(crs)

# Load the shapefile for specific toll zones for vehicle to travel
Toll_zones = gpd.read_file('/Data/Map network/toll_zone_coordinates.shp')


# Function to determine if a vehicle is in toll zones
def is_point_in_toll_zones(point, toll_zones):
    for i, toll_zone in enumerate(toll_zones):
        if toll_zone.contains(point):
            print(f"Point {point} is inside toll zone {i + 1}")
            return i + 1  # Return the toll zone index (1-based)
    print(f"Point {point} is not inside any toll zone")
    return None