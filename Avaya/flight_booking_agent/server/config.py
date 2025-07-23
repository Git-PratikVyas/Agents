import os

# Get the absolute path of the directory where this file is located
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the absolute path to the data directory
DATA_DIR = os.path.join(_CURRENT_DIR, "data")

# Define the absolute paths to the data files
BOOKINGS_FILE = os.path.join(DATA_DIR, "bookings.json")
CALENDAR_FILE = os.path.join(DATA_DIR, "calendar.json")
FLIGHTS_FILE = os.path.join(DATA_DIR, "flights.json")
