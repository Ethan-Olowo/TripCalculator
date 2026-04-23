# Trip Calculator

**Trip Calculator** is a Python desktop application that helps you estimate the total fuel required and the cost for a trip based on your route, stops, fuel efficiency, and fuel price. It features a user-friendly GUI built with PySide6 and leverages the OpenRouteService API for accurate road distances.

## Features

- Calculate total fuel needed for a trip
- Calculate total trip cost
- Save trip data to an Excel file
- Load and save activities
- Simple GUI (PySide6)

## Requirements

- Python 3.9+
- PySide6
- requests
- openpyxl

## Setup & Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Ethan-Olowo/trip-calculator.git
   cd trip-calculator
   ```

2. **Create and activate a virtual environment (recommended):**

   On macOS/Linux:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install the required packages:**

   ```sh
   pip install -r Requirements.txt
   ```

4. **Configuration:**
   - Rename `config.example.py` to `config.py`.
   - Open `config.py` and set your OpenRouteService API key in the `ORS_API_KEY` variable.

## Usage

1. **Run the application:**
   ```sh
   python TripCalc.py
   ```

2. **Using the GUI:**
   - Select an activity
   - Enter the origin
   - Enter stops (one per line)
   - Enter fuel efficiency (km/l)
   - Enter fuel price
   - Check the "Round Trip" box if needed
   - Click "Calculate" to see the total fuel needed and trip cost

## License

This project is licensed under the MIT License. See the LICENSE file for details.
