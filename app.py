# app.py

from flask import Flask, request, jsonify
from db import insert_shift
from prompt import extract_shift_details

app = Flask(__name__)


@app.route("/shifts/create", methods=["POST"])
def create_shift():
    # Get user input from the request body
    data = request.get_json()
    user_input = data.get("user_input", "")

    if not user_input:
        return jsonify({"error": "No user_input provided"}), 400

    # Use the LLM to extract shift details from the user input
    shift_details = extract_shift_details(user_input)

    # Extract fields with defaults if missing
    position = shift_details.get("position", "unknown")
    start_time = shift_details.get("start_time", "unknown")
    end_time = shift_details.get("end_time", "unknown")
    rate = shift_details.get("rate", "unknown")

    # Insert the shift into the database
    shift_id = insert_shift(position, start_time, end_time, rate)
    if shift_id:
        return jsonify({"success": True, "shift_id": shift_id}), 201
    else:
        return jsonify({"success": False, "error": "Database insertion failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
