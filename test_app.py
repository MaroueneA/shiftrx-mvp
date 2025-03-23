# test_app.py

import json
import pytest
from app import app  # Import your Flask app
from db import get_connection


@pytest.fixture
def client():
    # Set up the Flask test client in testing mode
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_create_shift_success(client):
    """Test that a valid request returns a successful response and shift_id."""
    payload = {
        "user_input": "We need a Pharmacist at City Hospital in Denver from 9AM to 5PM at $50/hr"
    }
    response = client.post(
        "/shifts/create", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert "shift_id" in data


def test_create_shift_no_input(client):
    """Test that a request without user_input returns a 400 error."""
    payload = {}
    response = client.post(
        "/shifts/create", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_database_entry(client):
    """
    Test that after a successful API call, the shift record is actually inserted into the database.
    This test queries the database to verify the record.
    """
    payload = {
        "user_input": "We need a Technician at General Hospital in New York from 2PM to 10PM at $45/hr"
    }
    response = client.post(
        "/shifts/create", data=json.dumps(payload), content_type="application/json")
    data = response.get_json()
    shift_id = data.get("shift_id")

    # Connect to the database and query for the shift record.
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM shifts WHERE id = %s", (shift_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    assert result is not None, "Shift record was not found in the database."
    # Optionally, verify some fields if needed. For example:
    # assert "Technician" in result[1]  # Assuming result[1] is the position field.
