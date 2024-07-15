import queue
import tkinter as tk
import simpy
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import geopandas as gpd
from Vehicle_movement import Vehicle, simulate_vehicle_movement
from Geospatial import route_gdfs, Toll_zones
from Toll_calculation import TollCalculator
from Report import display_vehicle_report
#from User_report import main

# Function to run simulation
result_queue = queue.Queue()
log_queue = queue.Queue()
def run_simulation(output_text):
    toll_calculator = TollCalculator()  # To calculate toll pricing

    # Initializing simulation environment
    env = simpy.Environment()

    # Read vehicle data and details from excel sheet
    vehicle_data = pd.read_excel('vehicle_data.xlsx')
    vehicles = []

    # Loop for adding all the vehicle details and data from the excel to a list
    for idx, row in vehicle_data.iterrows():
        vehicle_id = row['vehicle_id']
        vehicle_type = row['vehicle_type']
        start_index = (row['start_index'])
        stop_index = (row['stop_index'])
        route_index = row['route_index']
        vehicle_route = route_gdfs[route_index]
        # Use a different variable name for the route
        vehicle_toll_areas = Toll_zones  # Use a different variable name for the toll areas

        # Use the vehicle data and add it into the vehicle class
        vehicle = Vehicle(env, vehicle_id, vehicle_type, start_index, stop_index, vehicle_route, toll_calculator, vehicle_toll_areas)
        vehicles.append(vehicle)

    # Run the vehicle movement and simulation
    simulate_vehicle_movement(env, vehicles)
    env.run()  # Run the simulation

    # Output results
    results = []
    for vehicle in vehicles:
        vehicle_result = {
            "vehicle_id": vehicle.vehicle_id,
            "tolls_crossed": vehicle.tolls_crossed,
            "total_toll_amount": vehicle.total_toll_amount,
            "distance_travelled": vehicle.distance_travelled
        }
        results.append(vehicle_result)
        log_queue.put(vehicle.get_log())
    output_text.delete(1.0, tk.END)  # Clear the Text widget
    for result in results:
        output_text.insert(tk.END, f"Vehicle {result['vehicle_id']} details:\n")
        output_text.insert(tk.END, f"Tolls crossed: {result['tolls_crossed']}\n")
        output_text.insert(tk.END, f"Total toll amount: {result['total_toll_amount']}\n")
        output_text.insert(tk.END, f"Total distance traveled: {result['distance_travelled']} kilometers\n\n")

        print(f"Vehicle {vehicle.vehicle_id} details:")
        print(f"Tolls crossed: {vehicle.tolls_crossed}")
        total_toll_amount = vehicle.total_toll_amount
        print(f"Total toll amount: {total_toll_amount}")
        print(f"Total distance traveled: {vehicle.distance_travelled} kilometers")

    # Save results to an Excel file
    results_df = pd.DataFrame(results)
    results_df.to_excel('vehicle_simulation_results.xlsx', index=False)

    # Collect the vehicle positions for visualization
    vehicle_positions = []
    for vehicle in vehicles:
        for t, point in enumerate(vehicle.route[vehicle.start:vehicle.end + 1]):
            vehicle_positions.append({
                'vehicle_id': vehicle.vehicle_id,
                'lon': point[0],
                'lat': point[1],
                'time': t
            })

    vehicle_df = pd.DataFrame(vehicle_positions)

    # Plot the road network and vehicle trajectories
    fig = make_subplots(rows=1, cols=1, specs=[[{"type": "scattermapbox"}]])

    # Animation frames
    frames = []
    for t in sorted(vehicle_df['time'].unique()):
        frame_data = []
        for vehicle_id, traj in vehicle_df[vehicle_df['time'] == t].groupby('vehicle_id'):
            frame_data.append(go.Scattermapbox(
                lon=[traj.iloc[0]['lon']],
                lat=[traj.iloc[0]['lat']],
                mode='markers',
                marker=dict(size=12),
                name=vehicle_id
            ))
        frames.append(go.Frame(data=frame_data, name=str(t)))

    # Add initial vehicle positions as markers
    for vehicle_id, traj in vehicle_df[vehicle_df['time'] == 0].groupby('vehicle_id'):
        fig.add_trace(go.Scattermapbox(
            lon=[traj.iloc[0]['lon']],
            lat=[traj.iloc[0]['lat']],
            mode='markers',
            marker=dict(size=12),
            name=vehicle_id
        ))

    # Add frames to the figure
    fig.frames = frames

    # Animation settings
    fig.update_layout(
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": True},
                                    "fromcurrent": True, "mode": "immediate"}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                      "mode": "immediate"}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }]
    )

    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=15,
                      mapbox_center={"lat": np.mean(vehicle_df['lat']), "lon": np.mean(vehicle_df['lon'])},
                      title="Vehicle Simulation")

    fig.show()
    display_vehicle_report()
    #main()

if __name__ == "__main__":
    run_simulation()
