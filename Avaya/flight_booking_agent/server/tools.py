import requests
import json
import os

# Get the absolute path of the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "data")

DB_FILE = os.path.join(data_dir, "bookings.json")
CALENDAR_FILE = os.path.join(data_dir, "calendar.json")
FLIGHTS_FILE = os.path.join(data_dir, "flights.json")


# Tool Implementations

def check_weather(date: str, city: str):
    """Check the weather for a given date and city."""
    # In a real app, you'd use a geocoding API to get lat/lon from the city
    # For this POC, we'll use hardcoded coordinates for Mumbai.
    print(f"TOOL: Checking weather for {city} on {date}...")
    latitude = 19.0760
    longitude = 72.8777
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode&timezone=GMT&start_date={date}&end_date={date}"
    try:
        response = requests.get(url)
        print(f"Weather API response: {response.json()}")
        response.raise_for_status()  # Raise an exception for bad status codes
        weather_code = response.json()["daily"]["weathercode"][0]
        # WMO Weather interpretation codes (WW). > 60 is considered bad weather.
        print("->Weather is suitable" if weather_code <= 60 else "->Weather is not suitable")
        return weather_code <= 60
    except requests.exceptions.RequestException as e:
        print(f"Error checking weather: {e}")
        return False # Assume weather is bad if API fails

def check_calendar(date: str):
    """Check the user's calendar for availability on a given date."""
    print(f"TOOL: Checking calendar for {date}...")
    try:
        with open(CALENDAR_FILE, "r") as f:
            calendar_data = json.load(f)
            for event in calendar_data.get("events", []):
                if event.get("date") == date:
                    print(f"User has an event on {date}: {event.get('title')}")
                    print("->calendar not suitable")
                    return False
        print("->calendar is suitable")
        return True
    except FileNotFoundError:
        print(f"Calendar file not found at {CALENDAR_FILE}. Assuming user is free.")
        return True

def find_flights(source: str, destination: str, date: str):
    """Find available flights based on the user query."""
    print(f"TOOL: Finding flights from {source} to {destination} on {date}...")
    try:
        with open(FLIGHTS_FILE, "r") as f:
            flights_data = json.load(f)
            available_flights = []
            for flight in flights_data.get("flights", []):
                if (
                    flight.get("source").lower() == source.lower()
                    and flight.get("destination").lower() == destination.lower()
                    and flight.get("date") == date
                ):
                    available_flights.append(flight)
            return available_flights
    except FileNotFoundError:
        print(f"Flights data file not found at {FLIGHTS_FILE}.")
        return []

def book_flight(flight: dict):
    """Book the selected flight."""
    print(f"TOOL: Booking flight {flight.get('flight_number')}...")
    # Mock implementation
    return {"booking_id": "FL-12345", "flight_details": flight}

TRAINS_FILE = os.path.join(data_dir, "trains.json")

def find_trains(source: str, destination: str, date: str):
    """Find available trains based on the user query."""
    print(f"TOOL: Finding trains from {source} to {destination} on {date}...")
    try:
        with open(TRAINS_FILE, "r") as f:
            trains_data = json.load(f)
            available_trains = []
            for train in trains_data.get("trains", []):
                if (
                    train.get("source").lower() == source.lower()
                    and train.get("destination").lower() == destination.lower()
                    and train.get("date") == date
                ):
                    available_trains.append(train)
            return available_trains
    except FileNotFoundError:
        print(f"Trains data file not found at {TRAINS_FILE}.")
        return []

def book_train(train: dict):
    """Book the selected train."""
    print(f"TOOL: Booking train {train.get('train_number')}...")
    # Mock implementation
    return {"booking_id": "TR-67890", "train_details": train}

def save_booking_to_db(booking_details: dict):
    """Save the booking details to the database."""
    print(f"TOOL: Saving booking {booking_details.get('booking_id')} to database...")
    try:
        with open(DB_FILE, "a") as f:
            f.write(json.dumps(booking_details) + "\n")
        return True
    except IOError as e:
        print(f"Error saving booking to database: {e}")
        return False

# Available Tools Mapping
AVAILABLE_TOOLS = {
    "check_weather": check_weather,
    "check_calendar": check_calendar,
    "find_flights": find_flights,
    "book_flight": book_flight,
    "find_trains": find_trains,
    "book_train": book_train,
    "save_booking": save_booking_to_db,
}

class ToolExecutor:
    """A class to execute tools based on the Model Context Protocol concept."""
    def run(self, tool_name: str, **kwargs):
        """Runs a tool with the given name and arguments."""
        if tool_name not in AVAILABLE_TOOLS:
            raise ValueError(f"Tool '{tool_name}' not found.")
        
        tool_function = AVAILABLE_TOOLS[tool_name]
        return tool_function(**kwargs)