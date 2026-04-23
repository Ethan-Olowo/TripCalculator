def process_trip(activity_name, origin, stops, fuel_efficiency, fuel_price, round_trip, file_dialog_func=None, save_to_excel=True, register_activity=True):
    """
    Handles the entire trip calculation and saving process.
    Returns a results string for display.
    Raises exceptions for the UI to catch and display.
    Optional: saving to Excel and activity registration.
    """
    # New optional parameters for saving and registering
    import inspect
    frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)
    save_to_excel = values.get('save_to_excel', True)
    register_activity = values.get('register_activity', True)

    # If not registering activity, allow activity_name to be None
    if not register_activity:
        activity_name = None

    # Fetch coordinates and exact names for all locations
    locations = [origin] + stops
    coordinates = []
    location_names = []
    for loc in locations:
        coord, name = get_coordinates(loc)
        coordinates.append(coord)
        location_names.append(name)

    # Calculate distances and fuel for each leg
    results = f"Trip calculation for activity: {activity_name if activity_name else '(not registered)'}\n\n"
    total_distance = 0
    trip_legs = []
    for i in range(len(coordinates) - 1):
        leg_distance = get_road_distance(coordinates[i], coordinates[i + 1])
        total_distance += leg_distance
        fuel_needed_leg = calculate_fuel_needed(leg_distance, fuel_efficiency)
        leg_cost = fuel_needed_leg * fuel_price
        trip_legs.append([
            f"Leg {i + 1}",
            f"{location_names[i]} to {location_names[i + 1]}",
            leg_distance,
            fuel_efficiency,
            fuel_needed_leg,
            fuel_price,
            leg_cost
        ])
        results += (
            f"Leg {i + 1}: {location_names[i]} → {location_names[i + 1]}\n"
            f"  Distance: {leg_distance:.2f} km\n"
            f"  Fuel Needed: {fuel_needed_leg:.2f} liters\n\n"
        )

    # Add round trip distance if enabled
    if round_trip:
        return_distance = get_road_distance(coordinates[-1], coordinates[0])
        total_distance += return_distance
        fuel_needed_leg = calculate_fuel_needed(return_distance, fuel_efficiency)
        leg_cost = fuel_needed_leg * fuel_price
        trip_legs.append([
            "Return Leg",
            f"{location_names[-1]} to {location_names[0]}",
            return_distance,
            fuel_efficiency,
            fuel_needed_leg,
            fuel_price,
            leg_cost
        ])
        results += (
            f"Return Leg: {location_names[-1]} → {location_names[0]}\n"
            f"  Distance: {return_distance:.2f} km\n"
            f"  Fuel Needed: {fuel_needed_leg:.2f} liters\n\n"
        )

    # Calculate total fuel and cost
    total_fuel_needed = calculate_fuel_needed(total_distance, fuel_efficiency)
    total_cost = total_fuel_needed * fuel_price

    # Save trip data to Excel if enabled
    trip_data = {
        "legs": trip_legs,
        "total_distance": total_distance,
        "total_fuel": total_fuel_needed,
        "total_cost": total_cost,
    }
    if save_to_excel:
        save_trip_to_excel(activity_name, trip_data, file_dialog_func=file_dialog_func, register_activity=register_activity)

    # Prepare results string
    results += (
        f"Total Distance: {total_distance:.2f} km\n"
        f"Total Fuel Needed: {total_fuel_needed:.2f} liters\n"
        f"Total Trip Cost: {total_cost:.2f} "
    )
    return results
import os
import requests
import openpyxl
from openpyxl import Workbook
from config import ORS_API_KEY

base_dr = os.path.dirname(__file__)
ACTIVITIES_FILE = os.path.join(base_dr, "Activities.txt")

def get_coordinates(address):
    url = "https://api.openrouteservice.org/geocode/search"
    params = {"api_key": ORS_API_KEY, "text": address}
    response = requests.get(url, params=params)
    data = response.json()
    if response.status_code != 200 or "features" not in data:
        raise Exception(f"Error geocoding address: {data.get('error', 'Unknown error')}")
    try:
        feature = data["features"][0]
        coordinates = feature["geometry"]["coordinates"]
        location_name = feature["properties"]["label"]
        return (coordinates[1], coordinates[0]), location_name  # Return (lat, lon) and name
    except (IndexError, KeyError):
        raise Exception("Invalid geocoding response structure")

def get_road_distance(start, end):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": ORS_API_KEY}
    body = {"coordinates": [[start[1], start[0]], [end[1], end[0]]]}
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    if response.status_code != 200 or "routes" not in data:
        raise Exception(f"Error fetching route distance: {data.get('error', 'Unknown error')}")
    try:
        route = data["routes"][0]
        distance_meters = route["summary"]["distance"]
        return distance_meters / 1000  # Convert to kilometers
    except (IndexError, KeyError):
        raise Exception("Invalid response structure from API")

def calculate_fuel_needed(distance, fuel_efficiency):
    return distance / fuel_efficiency

def load_activities():
    activities = {}
    if os.path.exists(ACTIVITIES_FILE):
        with open(ACTIVITIES_FILE, "r") as file:
            for line in file:
                name, path = line.strip().split("=", 1)
                activities[name] = path
    return activities

def save_activity(activity_name, file_path):
    with open(ACTIVITIES_FILE, "a") as file:
        file.write(f"{activity_name}={file_path}\n")

def save_trip_to_excel(activity_name, trip_data, file_dialog_func=None, register_activity=True):
    if activity_name is None:
        # Not registering activity, just prompt for file path
        if file_dialog_func is not None:
            file_path = file_dialog_func()
        else:
            raise Exception("No file dialog function provided for saving trip.")
        if not file_path:
            raise Exception("No file selected for saving trip.")
    else:
        activities = load_activities()
        if activity_name in activities:
            file_path = activities[activity_name]
        else:
            if file_dialog_func is not None:
                file_path = file_dialog_func()
            else:
                raise Exception("No file dialog function provided for new activity.")
            if not file_path:
                raise Exception("No file selected for the new activity.")
            if register_activity:
                save_activity(activity_name, file_path)

    if os.path.exists(file_path):
        workbook = openpyxl.load_workbook(file_path)
    else:
        workbook = Workbook()

    sheet_name = f"Trip {len(workbook.sheetnames) + 1}"
    sheet = workbook.create_sheet(title=sheet_name)

    headers = ["Leg", "Description", "Distance (km)","Ltrs/Km", "Fuel Needed (liters)", "Fuel Price ", "Cost"]
    sheet.append(headers)
    for leg in trip_data["legs"]:
        sheet.append(leg)
    sheet.append([])
    sheet.append(["Total Distance (km)", trip_data["total_distance"]])
    sheet.append(["Total Fuel Needed (liters)", trip_data["total_fuel"]])
    sheet.append(["Total Trip Cost ", trip_data["total_cost"]])

    workbook.save(file_path)
