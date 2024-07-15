#Toll_calculation.py

class TollCalculator:
    def __init__(self):

        # Initialize toll rates for different vehicle types in each toll zone
        # The rates change for vehicle type and different toll zones
        self.rates = {1: {"car": 2.0, "jeep": 2.5, "van": 3.0, "minibus": 3.5, "bus": 4.0, "truck": 5.0, "4axle": 6.0, "7axle": 7.0},
                      2: {"car": 1.5, "jeep": 3.0, "van": 3.1, "minibus": 3.2, "bus": 3.7, "truck": 5.5, "4axle": 6.4, "7axle": 7.2},
                      3: {"car": 2.5, "jeep": 2.1, "van": 2.9, "minibus": 4.0, "bus": 4.2, "truck": 5.7, "4axle": 6.6, "7axle": 7.5},
                      4: {"car": 1.0, "jeep": 2.7, "van": 3.2, "minibus": 3.1, "bus": 4.5, "truck": 4.9, "4axle": 6.7, "7axle": 8.0},
                      5: {"car": 2.3, "jeep": 2.6, "van": 3.5, "minibus": 3.8, "bus": 5.0, "truck": 5.2, "4axle": 7.0, "7axle": 7.5},
                      6: {"car": 1.8, "jeep": 2.8, "van": 2.6, "minibus": 4.1, "bus": 4.8, "truck": 5.8, "4axle": 6.2, "7axle": 6.9},
                      }

        self.vehicle_count = {i: 0 for i in range(1, 8)}
    # Function to calculate toll according to vehicle type, toll zone and the distance travelled within the toll zone
    def calculate_toll(self, distance, vehicle_type, toll_zone_index):

        # Ensure vehicle type is in lowercase
        vehicle_type = vehicle_type.lower()

        if toll_zone_index + 1 in self.rates and vehicle_type in self.rates[toll_zone_index + 1]:
            rate_per_km = self.rates[toll_zone_index + 1][vehicle_type]
            return distance * rate_per_km

        else: # Else case when the vehicle type or toll zones are wrong
            print(f"Error: Toll rate for vehicle type '{vehicle_type}' in zone '{toll_zone_index + 1}' not found.")
            return 0
    def increment_vehicle_count(self, toll_zone_index):
        temp_count = self.vehicle_count.get(toll_zone_index + 1, 0)
        temp_count += 1
        self.vehicle_count[toll_zone_index + 1] = temp_count

    def decrement_vehicle_count(self, toll_zone_index):
        self.vehicle_count[toll_zone_index + 1] -= 1