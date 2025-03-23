# app.py
from flask import Flask, request, jsonify
from db import insert_shift
from prompt import extract_shift_details
from logger import logger

app = Flask(__name__)


@app.route("/shifts/create", methods=["POST"])
def create_shift():
    data = request.get_json()
    user_input = data.get("user_input", "")

    if not user_input:
        logger.warning("No user_input provided in the request.")
        return jsonify({"error": "No user_input provided"}), 400

    logger.info("Received user input: %s", user_input)
    shift_details = extract_shift_details(user_input)

    # Existing fields
    position = shift_details.get("position", "unknown")
    start_time = shift_details.get("start_time", "unknown")
    end_time = shift_details.get("end_time", "unknown")
    rate = shift_details.get("rate", "unknown")
    # New fields (if present in LLM response; else default to "unknown")
    facility_name = shift_details.get("facility_name", "unknown")
    location = shift_details.get("location", "unknown")

    shift_id = insert_shift(position, start_time, end_time,
                            rate, facility_name, location)
    if shift_id:
        logger.info("Shift created with id: %s", shift_id)
        return jsonify({"success": True, "shift_id": shift_id}), 201
    else:
        logger.error("Database insertion failed for input: %s", user_input)
        return jsonify({"success": False, "error": "Database insertion failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
