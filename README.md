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
   git clone https://github.com/yourusername/trip-calculator.git
   cd trip-calculator

   ```

2. Install the required packages:
   pip install -r requirements.txt

## Configuration

Collecting workspace information

### .gitignore

Create a `.gitignore` file to exclude unnecessary files and directories from being tracked by Git:

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# dotenv
.env

# virtualenv
venv/
ENV/
env/
.venv/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
```

### README.md

Create a `README.md` file to provide an overview and instructions for the project:

````markdown
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
   git clone https://github.com/yourusername/trip-calculator.git
   cd trip-calculator
   ```
````

2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

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

- OpenRouteService API Key: Update the ORS_API_KEY variable in TripCalc.py with your own API key.

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
