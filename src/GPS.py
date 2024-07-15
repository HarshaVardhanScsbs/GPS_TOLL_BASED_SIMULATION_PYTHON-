import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from shapely.geometry import Point
from geopy.distance import geodesic
from matplotlib.animation import FuncAnimation

accounts = pd.read_excel('/vehicle_data.xlsx')

def debit_toll_and_print_balance(vehicle_number, toll_amount):
    account = accounts.loc[accounts['vehicle_id'] == vehicle_number]
    account['InitialBalance'] -= toll_amount
    updated_balance = account['InitialBalance']
    print(f'Vehicle {vehicle_number}: New balance = {updated_balance.values[0]:.2f}')

NATIONAL_HIGHWAYS_PATH = '/Data/Map network/chennai_shp.shp'
STATE_HIGHWAYS_PATH = '/Data/Map network/statehighway.shp'

national_highway = gpd.read_file(NATIONAL_HIGHWAYS_PATH)
state_highway = gpd.read_file(STATE_HIGHWAYS_PATH)

crs = national_highway.crs

tolls = pd.read_excel('/Data/toll_coordinates.xlsx')
toll_gdf = gpd.GeoDataFrame(
    tolls,
    geometry=gpd.points_from_xy(tolls.LONGITUDE, tolls.LATITUDE),
    crs="EPSG:4326"
)
toll_gdf = toll_gdf.to_crs(crs)

Toll_zones = gpd.read_file('/Data/Map network/toll_zone_coordinates.shp')

def is_point_in_toll_zones(point, toll_zones):
    for i, toll_zone in enumerate(toll_zones.geometry):
        if toll_zone.contains(point):
            print(f"Point {point} is inside toll zone {i + 1}")
            return i + 1  # Return the toll zone index (1-based)
    print(f"Point {point} is not inside any toll zone")
    return None

class TollCalculator:
    def __init__(self):
        self.rates = {1: {"car": 2.0, "jeep": 2.5, "van": 3.0, "minibus": 3.5, "bus": 4.0, "truck": 5.0, "4axle": 6.0, "7axle": 7.0},
                      2: {"car": 1.5, "jeep": 3.0, "van": 3.1, "minibus": 3.2, "bus": 3.7, "truck": 5.5, "4axle": 6.4, "7axle": 7.2},
                      3: {"car": 2.5, "jeep": 2.1, "van": 2.9, "minibus": 4.0, "bus": 4.2, "truck": 5.7, "4axle": 6.6, "7axle": 7.5},
                      4: {"car": 1.0, "jeep": 2.7, "van": 3.2, "minibus": 3.1, "bus": 4.5, "truck": 4.9, "4axle": 6.7, "7axle": 8.0},
                      5: {"car": 2.3, "jeep": 2.6, "van": 3.5, "minibus": 3.8, "bus": 5.0, "truck": 5.2, "4axle": 7.0, "7axle": 7.5},
                      6: {"car": 1.8, "jeep": 2.8, "van": 2.6, "minibus": 4.1, "bus": 4.8, "truck": 5.8, "4axle": 6.2, "7axle": 6.9},
                      }

    def calculate_toll(self, distance, vehicle_type, toll_zone_index):
        vehicle_type = vehicle_type.lower()
        if toll_zone_index + 1 in self.rates and vehicle_type in self.rates[toll_zone_index + 1]:
            rate_per_km = self.rates[toll_zone_index + 1][vehicle_type]
            return distance * rate_per_km
        else:
            print(f"Error: Toll rate for vehicle type '{vehicle_type}' in zone '{toll_zone_index + 1}' not found.")
            return 0

vehicle_data = pd.read_excel('/vehicle_data.xlsx')

vehicle_id = 'TN01 AA2369'  
vehicle_info = vehicle_data[vehicle_data['vehicle_id'] == vehicle_id].iloc[0]
vehicle_type = vehicle_info['vehicle_type']

toll_calculator = TollCalculator()
inside_toll_zone = False
toll_start_point = None
current_toll_zone = None
distance_travelled = 0
total_toll_amount = 0
tolls_crossed = set()

tolls = pd.read_excel('/Data/toll_coordinates.xlsx')
toll_gdf = gpd.GeoDataFrame(
    tolls,
    geometry=gpd.points_from_xy(tolls.LONGITUDE, tolls.LATITUDE),
    crs="EPSG:4326"
)
buildings = gpd.read_file('/Data/Map network/chennai_shp.shp')
landuse = gpd.read_file('/Data/Map network/statehighway.shp')

fig, ax = plt.subplots(1, 1, figsize=(15, 15))

toll_gdf.plot(ax=ax, color='black', linewidth=1, label='Tolls')
buildings.plot(ax=ax, color='blue', alpha=0.5, label='Buildings')
landuse.plot(ax=ax, color='green', alpha=0.5, label='Land Use')

vehicle_marker = Rectangle((0, 0), 0.001, 0.001, color='red', label='Vehicle')
ax.add_patch(vehicle_marker)

ax.set_title('Map with Roads, Buildings, and Land Use')
ax.legend()
ax.grid(True)

def calculate_distance(point1, point2):
    return geodesic((point1[1], point1[0]), (point2[1], point2[0])).kilometers

def update_plot(frame):
    global inside_toll_zone, toll_start_point, current_toll_zone, distance_travelled, total_toll_amount, tolls_crossed
    try:
        with open('/coordinates.txt', 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                vehicle_lat, vehicle_lon = map(float, last_line.split(','))

                vehicle_marker.set_xy((vehicle_lon, vehicle_lat))

                current_point = Point(vehicle_lon, vehicle_lat)

                if not inside_toll_zone:
                    for i, zone in enumerate(Toll_zones.geometry):
                        if current_point.within(zone):
                            inside_toll_zone = True
                            toll_start_point = current_point
                            current_toll_zone = i
                            print(f"Vehicle {vehicle_id} has entered toll zone: {i + 1}")
                            break
                else:
                    if not current_point.within(Toll_zones.geometry[current_toll_zone]):
                        inside_toll_zone = False
                        distance_in_toll_zone = calculate_distance((toll_start_point.y, toll_start_point.x),
                                                                   (vehicle_lat, vehicle_lon))
                        toll_amount = toll_calculator.calculate_toll(distance_in_toll_zone, vehicle_type,
                                                                     current_toll_zone)
                        total_toll_amount += toll_amount
                        tolls_crossed.add(current_toll_zone + 1)
                        print(f"Vehicle {vehicle_id} has exited toll zone: {current_toll_zone + 1}")
                        print(f"Distance in toll zone: {distance_in_toll_zone:.2f} km")
                        print(f"Toll amount: {toll_amount:.2f}")

                        debit_toll_and_print_balance(vehicle_id, toll_amount)

                fig.canvas.draw_idle()
    except Exception as e:
        print(f"Error: {e}")

ani = FuncAnimation(fig, update_plot, interval=1000)

plt.show()
