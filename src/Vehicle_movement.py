# vehicle_movement.py

from Distance_calculation import *
from shapely.geometry import Point

class Vehicle:
    def __init__(self, env, vehicle_id, vehicle_type, start_index, end_index, route, toll_calculator, zones):
        self.env = env
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.start = start_index
        self.end = end_index
        self.route = route
        self.distance_travelled = 0
        self.tolls_crossed = set()
        self.toll_zones = zones
        self.toll_calculator = toll_calculator
        self.total_toll_amount = 0
        self.inside_toll_zone = False
        self.toll_start_point = None
        self.current_toll_zone = None
        self.log = []
    def log_output(self, message):
        self.log.append(message)

    def move(self, env, route):
        self.log_output(f"Vehicle {self.vehicle_id} starts from {self.start}")
        self.log_output(f"Vehicle {self.vehicle_id} ends at {self.end}")
        print(f"Vehicle {self.vehicle_id} starts from {self.start}")
        print(f"Vehicle {self.vehicle_id} ends at {self.end}")
        last_point = self.route[self.start]
        self.route_points = []

        for point in self.route[self.start:self.end + 1]:
            yield env.timeout(0.1)
            self.distance_travelled += calculate_distance(last_point, point)
            last_point = point
            current_point = Point(point)
            self.route_points.append((current_point.x, current_point.y))

            if not self.inside_toll_zone:
                for i, zone in enumerate(self.toll_zones.geometry):
                    if current_point.within(zone):
                        self.inside_toll_zone = True
                        self.toll_start_point = current_point
                        self.current_toll_zone = i
                        self.toll_calculator.increment_vehicle_count(i + 1)
                        print(f"Vehicle {self.vehicle_id} has entered toll zone: {i + 1}")
                        self.log_output(f"Vehicle {self.vehicle_id} has entered toll zone: {i + 1}")
                        break
            else:
                if not current_point.within(self.toll_zones.geometry[self.current_toll_zone]):
                    self.inside_toll_zone = False
                    distance_in_toll_zone = calculate_distance(
                        (self.toll_start_point.x, self.toll_start_point.y),
                        (current_point.x, current_point.y)
                    )
                    toll_amount = self.toll_calculator.calculate_toll(distance_in_toll_zone, self.vehicle_type, self.current_toll_zone)
                    self.total_toll_amount += toll_amount
                    self.tolls_crossed.add(self.current_toll_zone + 1)
                    self.toll_calculator.decrement_vehicle_count(self.current_toll_zone + 1)
                    print(f"Vehicle {self.vehicle_id} has exited toll zone: {self.current_toll_zone + 1}")
                    print(f"Distance in toll zone: {distance_in_toll_zone}, Toll amount: {toll_amount}")
                    self.log_output(f"Vehicle {self.vehicle_id} has exited toll zone: {self.current_toll_zone + 1}")
                    self.log_output(f"Distance in toll zone: {distance_in_toll_zone}, Toll amount: {toll_amount}")

    # Function to get the log output
    def get_log(self):
        return self.log



# Function to simulate vehicle movement
def simulate_vehicle_movement(env, vehicles):
    for vehicle in vehicles:
        env.process(vehicle.move(env, vehicle.route))