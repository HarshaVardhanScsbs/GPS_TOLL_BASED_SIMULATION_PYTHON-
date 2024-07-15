import folium
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests
import os
import json

# Function to generate Folium map for traveled paths and save as HTML
def generate_folium_map(traveled_paths, colors, vehicle_name):
    try:
        # Initialize the map centered on the starting point of the first route
        start_point = traveled_paths[0][0]
        print(traveled_paths[0] , start_point[1] , start_point[0])
        folium_map = folium.Map(location=[start_point[0], start_point[1]], zoom_start=15)

        # Add the traveled paths to the map
        for path, color in zip(traveled_paths, colors):
            # Correct the order of coordinates while creating the PolyLine
            folium.PolyLine([(point[0], point[1]) for point in path], color=color, weight=5).add_to(folium_map)

        # Add markers for the start and end points of each route
        for path, color in zip(traveled_paths, colors):
            start_point = path[0]
            folium.Marker(location=[start_point[0], start_point[1]], popup='Start', icon=folium.Icon(color=color)).add_to(folium_map)
            end_point = path[-1]
            folium.Marker(location=[end_point[0], end_point[1]], popup='End', icon=folium.Icon(color=color)).add_to(folium_map)

        # Save the map as HTML
        html_file_path = f"{vehicle_name}.html"
        folium_map.save(html_file_path)
        print(f"Folium map saved as {html_file_path}")
        return html_file_path
    except Exception as e:
        print(f"Error generating Folium map: {e}")
        return None

# Function to upload a file to Google Drive
def upload_file_to_drive(file_name, credentials):
    try:
        # Build the Drive API client
        service = build('drive', 'v3', credentials=credentials)

        # Define the file metadata
        file_metadata = {
            'name': file_name,
            'mimeType': 'text/html'
        }

        # Upload the file
        file_path = file_name
        media = MediaFileUpload(file_path, mimetype='text/html')

        # Create the file on Google Drive
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        # Get the file ID
        file_id = file.get('id')

        # Make the file publicly accessible
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        service.permissions().create(fileId=file_id, body=permission).execute()

        # Get the web view link
        file = service.files().get(fileId=file_id, fields='webViewLink').execute()
        web_view_link = file.get('webViewLink')

        # Construct the direct download link
        direct_download_link = f"https://drive.google.com/uc?export=view&id={file_id}"

        print('File uploaded successfully.')
        print('Public link:', direct_download_link)
        return direct_download_link
    except Exception as e:
        print(f"Error uploading file to Google Drive: {e}")
        return None

# Function to send data to Google Sheets using Google Apps Script
def send_data_to_sheets(link, vehicle_data):
    try:
        # Define the URL of the Google Apps Script deployment
        url = "Your_Google_Apps_Script_Deployment_url"

        # Define the parameters to send to the script
        params = {
            'action': 'sendmail',
            'vehiclename': vehicle_data['Vehicle_name'],
            'vehiclenumber': vehicle_data['vehicle_id'],
            'vehicleType': vehicle_data['vehicle_type'],
            'ownerAccountNumber': vehicle_data['OwnerAccountNumber'],
            'ownerPhonenumber': vehicle_data['OwnerPhoneNumber'],
            'mapLink': link,
            'ownerName': vehicle_data['OwnerName'],
            'fastTagid': vehicle_data['FastTagID'],
            'ownerEmail': vehicle_data['emailid'],
            'distanceTravelled': vehicle_data['distance_travelled'],
            'tollAmount': vehicle_data['total_toll_amount']
        }

        # Make the GET request to the Google Apps Script
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Print the response from the script
        print(response.text)
    except Exception as e:
        print(f"Error sending data to Google Sheets: {e}")

# Function to load a single route from a file
def load_route(file_path):
    try:
        with open(file_path, 'r') as f:
            return eval(f.read())
    except Exception as e:
        print(f"Error loading route from {file_path}: {e}")
        return None

# Function to load all routes from a folder
def load_routes_from_folder(folder_path):
    routes = []
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                route_path = os.path.join(folder_path, filename)
                route = load_route(route_path)
                if route:
                    routes.append(route)
        return routes
    except Exception as e:
        print(f"Error loading routes from folder {folder_path}: {e}")
        return routes

# Main function to orchestrate the entire process
def main():
    print("Here at main hello")
    try:
        # Read vehicle data from the Excel file
        vehicle_data_df = pd.read_excel('/vehicle_data.xlsx')
        print("Vehicle data loaded successfully")

        # Read simulation results data from the Excel file
        simulation_results_df = pd.read_excel('/vehicle_simulation_results.xlsx')
        print("Simulation results data loaded successfully")

        # Merge the two DataFrames on vehicle_id
        vehicle_data_df = pd.merge(vehicle_data_df, simulation_results_df, on='vehicle_id')
        print("Vehicle data and simulation results merged successfully")

        # Define the folder path where your routes are stored
        paths_folder = '/Data/Paths'
        # Load routes from the folder
        ROUTES = load_routes_from_folder(paths_folder)
        print("Routes loaded successfully")

        colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray', 'white']

        # Path to your service account credentials file
        SERVICE_ACCOUNT_FILE = '/rithostel-d1a072a1d08a.json'  # Update this path

        # Create credentials using the service account file
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive.file'])
        print("Service account credentials created successfully")

        for index, vehicle_data in vehicle_data_df.iterrows():
            try:
                route_index = vehicle_data['route_index']
                vehicle_name = vehicle_data['vehicle_id']
                traveled_paths = [ROUTES[route_index]]  # Get the route for this vehicle

                # Generate and save the Folium map for the traveled paths
                html_file_path = generate_folium_map(traveled_paths, colors[:len(traveled_paths)], vehicle_name)
                if not html_file_path:
                    continue

                # Upload the generated HTML file to Google Drive
                uploaded_link = upload_file_to_drive(html_file_path, credentials)
                if not uploaded_link:
                    continue

                # Send the link to Google Sheets
                send_data_to_sheets(uploaded_link, vehicle_data)
            except Exception as e:
                print(f"Error processing vehicle {vehicle_data['vehicle_id']}: {e}")

    except Exception as e:
        print(f"Error in main process: {e}")

if __name__ == "__main__":
    main()
