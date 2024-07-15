# SIMTOLL DYNAMICS - GPS Toll-Based System Simulation
## Overview
This project, developed as part of the Intel Unnati Industrial Training Programme by Team Classic Coders, is a GPS-based toll system simulation using Python. 
The primary aim is to create an efficient and accurate system to streamline toll collection, reduce congestion, and improve the overall driving experience.
## Introduction
Traditional toll collection methods such as fast tag, often plagued by congestion and delays, are gradually being replaced by innovative technology-driven solutions. This project focuses on developing a GPS-based toll system simulation that can handle real-time vehicle movement, automate toll calculations based on distance traveled, and support dynamic pricing and multiple payment options.

## Features
**Live GPS Integration:**

Real-time data feed for accurate and up-to-date tracking.

Enhanced accuracy in simulation.

**Real-Time Vehicle Movement Simulation:**

Accurate modeling of traffic flow and toll collection scenarios.

Continuous dynamic tracking of vehicles.

**Automated Toll Calculations:**

Distance-based tolling for fair and precise charges.

Transparent transactions with detailed toll calculation reports.

**Dynamic Pricing:**

Variable toll rates based on distance, vehicle type, and traffic conditions.

Congestion-based toll rates with discounts for high traffic zones.

**Payment Options:**

Seamless integration with existing payment infrastructure.

**Advanced Data Analytics:**

User reports on toll charges and payment confirmation.

Detailed revenue reports for strategic planning.

**Scalability and Flexibility:**

Modular design for easy expansion.

Customizable settings for administrators.

**Security and Privacy:**

Login feature for admin access.

Secure processing of transactions.

**Additional feature

We have developed an android application which will send the live GPS Coordinates to the local server every 1.5 seconds. This coordinate is used to visualise the vehicle in a map and also it is used to calculate the toll prices dynamically.

## Installation
To set up the project locally, follow these steps:

**1. Clone the repository:**
```
git clone https://github.com/yourusername/GPS-Toll-Based-System-Simulation.git
cd GPS-Toll-Based-System-Simulation
```
**2. Create and activate a virtual environment:**
```
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
**3. Install the required dependencies:**
```
pip install  pandas geopandas openpyxl simpy plotly shapely geopy matplotlib pillow folium
```
**4. Ensure that all the Excel sheets, shapefiles, and photo logo are defined using their full directory paths before execution.**

**5. ADMIN SIDE INTERFACE:**
   Run the code interface.py to get the admin side interface
          
   **The username is admin and the password is password.**
          
**6. USER SIDE REPORT:**

   6.1. For the execution of user-side report
          
  **Add the required email address in the vehicle_data.xlsx, so that the user report email is sent to that mail address.**
          
   6.2. Set up a Google Console project using the following instructions:
## Google API Project Setup
This guide provides detailed instructions on how to create a project in Google Cloud Console, enable the Google Drive API and Google Sheets API, create OAuth credentials, and download the JSON file for your project.

Step-by-Step Instructions
Creating a Project in Google Cloud Console
Open Google Cloud Console:

Navigate to the Google Cloud Console.
Create a New Project:

Click on the project drop-down at the top of the page.
Click on "New Project."
Enter the Project Name (e.g., My Google API Project).
(Optional) Set the location (e.g., your organization).
Click on "Create."
Enabling APIs
Enable Google Drive API:

In the Google Cloud Console, select your project.
Navigate to the API & Services Dashboard.
Click on "+ ENABLE APIS AND SERVICES" at the top.
Search for "Google Drive API."
Click on "Google Drive API" from the search results.
Click on "Enable."
Enable Google Sheets API:

Go back to the API & Services Dashboard.
Click on "+ ENABLE APIS AND SERVICES" at the top.
Search for "Google Sheets API."
Click on "Google Sheets API" from the search results.
Click on "Enable."
Creating OAuth Credentials
Navigate to Credentials:

Go to the Credentials page.
Click on "Create Credentials."
Select "OAuth 2.0 Client IDs."
Configure OAuth Consent Screen:

If you haven't configured the OAuth consent screen yet, you'll be prompted to do so.
Click on "Configure consent screen."
Select "External" if you're planning to allow access to anyone with a Google account, or "Internal" if limited to users within your organization.
Click "Create."
Fill in the required fields (e.g., App name, User support email).
(Optional) Fill in additional fields like logo, homepage, privacy policy, and terms of service.
Click "Save and Continue."
(Optional) Add scopes if needed and click "Save and Continue."
(Optional) Add test users if needed and click "Save and Continue."
Click "Back to Dashboard" or "Save."
Create OAuth Client ID:

After configuring the OAuth consent screen, go back to the Credentials page.
Click on "Create Credentials."
Select "OAuth 2.0 Client ID."
Select "Application type" as "Web application."
Provide a name for the OAuth client (e.g., My OAuth Client).
(Optional) Add "Authorized JavaScript origins" if needed.
Add "Authorized redirect URIs" (e.g., http://localhost:8080/ or your deployment URL).
Click "Create."
Download the JSON File:

After creating the credentials, you will see a dialog with your Client ID and Client Secret.
Click on "Download" to download the JSON file containing your credentials.
Save this file in the project directory and rename it to something appropriate like credentials.json.
Then paste the credentials.json file path in User_report.py line 162

 6.3. Set up a Google Sheet and paste the code in AppScript using the following instructions:
## Set Up Your Google Apps Script
Create a New Google Sheet:

Go to Google Sheets.
Click on New Sheet.
Click on “Extensions” and press "App Script," which opens a new window for typing your script code.
Paste Your Code:

Delete any code in the editor and paste this code:

```javascript
var spreadSheet = SpreadsheetApp.openByUrl("YOUR_GOOGLE_SHEET_URL");
var sheet1 = spreadSheet.getSheetByName("Sheet1");

function doGet(e) {
  var action = e.parameter.action;
  if(action == "sendmail"){
    return se(e);
  }
}

function se(e){
  var vehiclename = e.parameter.vehiclename;
  var vehiclenumber = e.parameter.vehiclenumber;
  var vehicleType = e.parameter.vehicleType;
  var ownerAccountNumber = e.parameter.ownerAccountNumber;
  var ownerPhonenumber = e.parameter.ownerPhonenumber;
  var mapLink = e.parameter.mapLink;
  var ownerName = e.parameter.ownerName;
  var fastTagid = e.parameter.fastTagid;
  var ownerEmail = e.parameter.ownerEmail;
  var distanceTravelled = e.parameter.distanceTravelled;
  var tollAmount = e.parameter.tollAmount;
  sheet1.appendRow([vehiclename, vehiclenumber, vehicleType, ownerAccountNumber, ownerPhonenumber, mapLink, ownerName, fastTagid, ownerEmail, distanceTravelled, tollAmount]);
  var subject = "Report for your travel on National highway";
  var body = "Vehicle name: " + vehiclename + "\nVehicle number: " + vehiclenumber + "\nVehicle type: " + vehicleType + "\nOwner Name: " + ownerName + "\nOwner Phone number: " + ownerPhonenumber + "\nHas travelled a distance of: " + distanceTravelled + "\nToll amount debited is: " + tollAmount + "\nMap link: " + mapLink;
  MailApp.sendEmail(ownerEmail, subject, body);
  return ContentService.createTextOutput("Created").setMimeType(ContentService.MimeType.TEXT);
}
```
 6.4. Deploy the Script as a Web App:
Click on Deploy in the top-right corner.
Select New deployment.
Click on the Select type dropdown and choose Web app.
Enter a description for the deployment (e.g., Initial deployment).
Click on Deploy.
Set Access Permissions:

In the Who has access section, choose "Anyone."
Click Deploy.
Authorize the Script:

You will be prompted to review permissions.
Click Authorize.
Choose your Google account.
Click Allow to grant permissions.
Copy the Web App URL:

After deployment, a URL will be generated.
Copy this URL and paste it in User_report.py line 86

**7. GPS APP:**
   7.1. App setup:
       For getting GPS coordinates directly into simulation first install the GPS app using the following repo and set it up to get live gps location.
       https://github.com/Aswinraj040/GPS_Toll

   7.2. GPS simulation execution:
       Run the server.py code and then GPS.py code to open the matplotlib visualisation and toll zone price calculations.

## Project directory:

GPS-Toll-based-System-Simulation/

├── data/

│   ├── MAP_NETWORK/

│   │   ├── national_highways.shp

│   │   ├── state_highways.shp

│   │   ├── toll_zones.shp

│   ├── PATHS/

│   │   ├── rh_bus_1.txt

│   │   ├── rh_bus_2.txt

│   │   ├── rh_bus_3.txt

│   │   ├── ...

│   ├── toll_coordinates.xlsx

│   ├── report_data.xlsx

│   ├── vehicle_data.xlsx

│   ├── vehicle_simulation_result.xlsx

├── docs/

│   ├── PROJECT_REPORT.docx

│   ├── presentation.pptx

│   ├── class_diagrams/

│   ├── flowcharts/

│   ├── output_photos/

│   ├── output_videos/

├── src/

│   ├── main.py

│   ├── toll_calculation.py

│   ├── vehicle_movement.py

│   ├── distance_calculation.py

│   ├── simulation.py

│   ├── account.py

│   ├── server.py

│   ├── user_report.py

│   ├── interface.py

│   ├── gps.py

│   ├── geospatial.py

│   ├── utils.py

│   ├── visualization.py

├── README.md


**Explanation of the Updated Project Structure:**

data/: This directory contains all the necessary data files for the simulation.

MAP_NETWORK/: Contains shapefiles for national and state highways, and toll zones.

national_highways.shp: Shapefile for national highways.

state_highways.shp: Shapefile for state highways.

toll_zones.shp: Shapefile for toll zones.

PATHS/: Contains text files with different routes.

rh_bus_1.txt: Route for rh bus 1.

rh_bus_2.txt: Route for rh bus 2.

rh_bus_3.txt: Route for rh bus 3.

toll_coordinates.xlsx: Contains coordinates for toll points.

report_data.xlsx: Contains data used in reports.

vehicle_data.xlsx: Contains data about the vehicles used in the simulation.

vehicle_simulation_result.xlsx: Contains the results of the vehicle simulations.

docs/: This directory contains documentation files.

PROJECT_REPORT.docx: The main project report document.

presentation.pptx: A presentation file for the project.

class_diagrams/: Contains UML class diagrams.

flowcharts/: Contains flowcharts for the project.

output_photos/: Contains photos of the simulation output.

output_videos/: Contains videos of the simulation output.

src/: This directory contains the source code for the project.

main.py: The main entry point for the simulation.

toll_calculation.py: Contains the logic for toll calculation.

vehicle_movement.py: Manages vehicle movement in the simulation.

distance_calculation.py: Functions for calculating distances between points.

simulation.py: Runs the simulation using the provided vehicle data.

account.py: Manages vehicle accounts and toll debiting.

user_report.py: Generates reports and uploads data.

interface.py: Manages the user interface for running simulations.

gps.py: Tracks live GPS data for the simulation.

geospatial.py: Handles geospatial data loading and manipulation.

utils.py: Contains utility functions.

visualization.py: Manages data visualization.

README.md: The README file with detailed project information.

This structure ensures that all relevant files and documentation are organized in a clear and logical manner.

## Contributions:
**Aswin**: Project manager and app developer

**Athika**: Data analyst

**Dhiksha**: Geospatial analyst

**Harsha Vardhan**: UI and visualization expert

**Tejaswini**: Simulation engineer

## Conclusion:

The GPS Toll-Based System Simulation project not only addresses the current challenges of toll collection but also sets the stage for future innovations in traffic management and urban mobility. By harnessing the power of technology, we aim to create a more efficient, transparent, and sustainable tolling ecosystem.
