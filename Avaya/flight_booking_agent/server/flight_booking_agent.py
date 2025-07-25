from tools import ToolExecutor
from train_booking_agent import TrainBookingAgent

class FlightBookingAgent:
    def __init__(self):
        self.tool_executor = ToolExecutor()

    def process_query(self, user_query):
        """
        Process the user query to find and book flights.
        """
        print("Flight Booking Agent: Processing user query...")

        # 1. Check weather and calendar
        weather_ok = self.tool_executor.run("check_weather", date=user_query["date"], city=user_query.get("destination", "Mumbai"))
        calendar_free = self.tool_executor.run("check_calendar", date=user_query["date"])

        if not weather_ok or not calendar_free:
            print("Flight Booking Agent: Weather or calendar not suitable for travel.")
            return {"status": "booking_failed", "message": "Weather or calendar not suitable for travel."}

        # 2. Find available flights
        available_flights = self.tool_executor.run("find_flights", source=user_query["source"], destination=user_query["destination"], date=user_query["date"])

        if not available_flights:
            print("-->Flight Booking Agent: No flights available.")
            return {"status": "no_flights_found"}

        # 4. Get user confirmation
        if not user_query.get("user_confirmation"):
            print("Flight Booking Agent: User confirmation required.")
            # In a real application, you would return a response to the client
            # asking for confirmation. For this POC, we'll just print a message.
            return {"status": "confirmation_required", "flights": available_flights}

        # If user has confirmed, book the selected flight
        if user_query.get("user_confirmation"):
            selected_flight = user_query.get("selected_flight")
            if selected_flight:
                booking_details = self.tool_executor.run("book_flight", flight=selected_flight)
                self.tool_executor.run("save_booking", booking_details=booking_details)
                print("Flight Booking Agent: Flight booked successfully!")
                return {"status": "booked", "booking_details": booking_details}
            else:
                print("Flight Booking Agent: No flight selected for booking.")
                return {"status": "booking_failed", "message": "No flight selected for booking."}
        else:
            print("Flight Booking Agent: User confirmation required.")
            return {"status": "confirmation_required", "flights": available_flights}

    
