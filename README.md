# Trip Calculator

Trip Calculator is a Python application that calculates the total fuel needed and the total cost for a trip based on the origin, stops, fuel efficiency, and fuel price. The application uses the OpenRouteService API to get road distances.

## Features

- Calculate total fuel needed for a trip
- Calculate total trip cost
- Save trip data to an Excel file
- Load and save activities
- GUI built with Tkinter

## Requirements

- Python 3.9+
- Tkinter
- Requests
- Openpyxl

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/Ethan-Olowo/trip-calculator.git
   cd trip-calculator

   ```

2. Install the required packages:
   pip install -r requirements.txt

## Usage

1. Run the application:

   ```sh
   python TripCalc.py
   ```

2. Fill in the required fields in the GUI:

   - Select an activity
   - Enter the origin
   - Enter stops (one per line)
   - Enter fuel efficiency (km/l)
   - Enter fuel price 
   - Check the "Round Trip" checkbox if applicable

3. Click the "Calculate" button to get the total fuel needed and total trip cost.

## Configuration

- Rename config.example.py to config.py
- OpenRouteService API Key: Update the ORS_API_KEY variable in config.py with your own API key.

## Usage

1. Run the application
   python TripCalc.py

2. Fill in the required fields in the GUI:

- Select an activity
- Enter the origin
- Enter stops (one per line)
- Enter fuel efficiency (km/l)
- Enter fuel price 
- Check the "Round Trip" checkbox if applicable

3. Click the "Calculate" button to get the total fuel needed and total trip cost.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
