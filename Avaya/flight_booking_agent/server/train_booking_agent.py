from tools import ToolExecutor

class TrainBookingAgent:
    def __init__(self):
        self.tool_executor = ToolExecutor()

    def process_query(self, user_query):
        """
        Process the user query to find and book trains.
        """
        print("Train Booking Agent: Processing user query...")

        # 1. Check weather and calendar
        weather_ok = self.tool_executor.run("check_weather", date=user_query["date"], city=user_query.get("destination", "Mumbai"))
        calendar_free = self.tool_executor.run("check_calendar", date=user_query["date"])

        if not weather_ok or not calendar_free:
            print("Train Booking Agent: Weather or calendar not suitable for travel.")
            return

        # 2. Find available trains
        available_trains = self.tool_executor.run("find_trains", source=user_query["source"], destination=user_query["destination"], date=user_query["date"])

        if not available_trains:
            print("Train Booking Agent: No trains available.")
            return {"status": "no_trains_found"}

        # 3. Get user confirmation
        if not user_query.get("user_confirmation"):
            print("Train Booking Agent: User confirmation required.")
            return {"status": "confirmation_required", "trains": available_trains}

        # If user has confirmed, book the selected train
        if user_query.get("user_confirmation"):
            selected_train = user_query.get("selected_train")
            if selected_train:
                booking_details = self.tool_executor.run("book_train", train=selected_train)
                self.tool_executor.run("save_booking", booking_details=booking_details)
                print("Train Booking Agent: Train booked successfully!")
                return {"status": "booked", "booking_details": booking_details}
            else:
                print("Train Booking Agent: No train selected for booking.")
                return {"status": "booking_failed", "message": "No train selected for booking."}
        else:
            print("Train Booking Agent: User confirmation required.")
            return {"status": "confirmation_required", "trains": available_trains}

    
