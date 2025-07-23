from flask import Flask, request, jsonify
from flight_booking_agent import FlightBookingAgent
from train_booking_agent import TrainBookingAgent
import io
import contextlib
import sys

app = Flask(__name__)

@app.route("/invoke", methods=["POST"])
def invoke_agent():
    try:
        user_query = request.get_json()
        if not user_query:
            return jsonify({"error": "Invalid input"}), 400

        flight_agent = FlightBookingAgent()
        train_agent = TrainBookingAgent()
        
        s = io.StringIO()
        with contextlib.redirect_stdout(s):
            result = {}
            if user_query.get("user_confirmation"):
                # If confirmation is provided, re-route to the agent that requested it
                if user_query.get("agent_type") == "flight":
                    result = flight_agent.process_query(user_query)
                elif user_query.get("agent_type") == "train":
                    result = train_agent.process_query(user_query)
                else:
                    # Fallback if agent_type is not specified for confirmation
                    # Try flight first, then train
                    result = flight_agent.process_query(user_query)
                    if result.get("status") == "confirmation_required" and not result.get("flights"):
                        result = train_agent.process_query(user_query)
            else:
                # Initial query
                result = {}
                # Always try flight agent first for initial queries
                flight_result = flight_agent.process_query(user_query)

                if flight_result.get("status") == "no_flights_found":
                    # If no flights found, try train agent
                    train_result = train_agent.process_query(user_query)
                    if train_result.get("status") == "confirmation_required":
                        train_result["message"] = "No flights found for your query. Here are available train options."
                        result = train_result
                    elif train_result.get("status") == "no_trains_found":
                        result = {"status": "no_options_found", "message": "No flights or trains found for your query."}
                    else:
                        result = train_result
                else:
                    result = flight_result
            
            # Add agent_type to the response if confirmation is required
            if result.get("status") == "confirmation_required":
                if "flights" in result:
                    result["agent_type"] = "flight"
                elif "trains" in result:
                    result["agent_type"] = "train"

        captured_output = s.getvalue()

        response = result if isinstance(result, dict) else {}
        response["logs"] = captured_output

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)