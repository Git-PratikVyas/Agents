import requests
import json

def main():
    # Get user input
    source = input("Enter source: ")
    destination = input("Enter destination: ")
    date = input("Enter date (YYYY-MM-DD): ")
    travel_class = input("Enter class (Economy, Business, First): ")

    user_query = {
        "source": source,
        "destination": destination,
        "date": date,
        "class": travel_class
    }

    # Send the query to the server
    try:
        response = requests.post("http://127.0.0.1:5000/invoke", json=user_query)
        response.raise_for_status()  # Raise an exception for bad status codes
        response_data = response.json()

        print("--- Server Logs ---")
        print(response_data.get("logs"))
        print("--- End Server Logs ---")

        if response_data.get("status") == "confirmation_required":
            print("Server response:")
            if "message" in response_data:
                print(response_data["message"])
            if "flights" in response_data:
                print("Available flights:")
                for i, flight in enumerate(response_data["flights"]):
                    print(f"{i+1}. {flight}")
                
                if len(response_data["flights"]) > 1:
                    while True:
                        try:
                            selection = int(input("Enter the number of the flight you want to book: "))
                            if 1 <= selection <= len(response_data["flights"]):
                                user_query["selected_flight"] = response_data["flights"][selection - 1]
                                break
                            else:
                                print("Invalid selection. Please try again.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                elif len(response_data["flights"]) == 1:
                    user_query["selected_flight"] = response_data["flights"][0]

            if "trains" in response_data:
                print("Available trains:")
                for i, train in enumerate(response_data["trains"]):
                    print(f"{i+1}. {train}")
                
                if len(response_data["trains"]) > 1:
                    while True:
                        try:
                            selection = int(input("Enter the number of the train you want to book: "))
                            if 1 <= selection <= len(response_data["trains"]):
                                user_query["selected_train"] = response_data["trains"][selection - 1]
                                break
                            else:
                                print("Invalid selection. Please try again.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                elif len(response_data["trains"]) == 1:
                    user_query["selected_train"] = response_data["trains"][0]
            
            while True:
                confirm = input("Do you want to book? (yes/no): ").lower()
                if confirm in ["yes", "no"]:
                    break
            
            if confirm == "yes":
                user_query["user_confirmation"] = True
                user_query["agent_type"] = response_data.get("agent_type")
                response = requests.post("http://127.0.0.1:5000/invoke", json=user_query)
                response.raise_for_status()
                response_data = response.json()
                print("--- Server Logs ---")
                print(response_data.get("logs"))
                print("--- End Server Logs ---")
                print("Server response:")
                print(response_data.get("status"))
                if "booking_details" in response_data:
                    print(response_data["booking_details"])
            else:
                print("Booking cancelled.")

        else:
            print("Server response:")
            if response_data.get("status") == "no_options_found":
                print(response_data.get("message"))
            else:
                print(response_data.get("status"))

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the server: {e}")

if __name__ == "__main__":
    main()