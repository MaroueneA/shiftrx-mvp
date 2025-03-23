import json
import pytest
import openai
from prompt import extract_shift_details
from logger import logger

# Define a fake ChatCompletion.create function


def fake_chat_completion_create(**kwargs):
    messages = kwargs.get("messages", [])
    if not messages:
        return {"choices": [{"message": {"content": '{"position": "unknown", "start_time": "unknown", "end_time": "unknown", "rate": "unknown", "facility_name": "unknown", "location": "unknown"}'}}]}

    user_message = messages[-1]["content"]

    # Return a fake response based on the user message
    if user_message == "We need a Pharmacist at City Hospital in Denver from 9AM to 5PM at $50/hr":
        fake_output = (
            '{"position": "Pharmacist", '
            '"start_time": "9AM", '
            '"end_time": "5PM", '
            '"rate": "$50/hr", '
            '"facility_name": "City Hospital", '
            '"location": "Denver"}'
        )
    elif user_message == "Need a Technician at General Hospital in New York from 2PM to 10PM at $45/hr":
        fake_output = (
            '{"position": "Technician", '
            '"start_time": "2PM", '
            '"end_time": "10PM", '
            '"rate": "$45/hr", '
            '"facility_name": "General Hospital", '
            '"location": "New York"}'
        )
    else:
        fake_output = (
            '{"position": "unknown", '
            '"start_time": "unknown", '
            '"end_time": "unknown", '
            '"rate": "unknown", '
            '"facility_name": "unknown", '
            '"location": "unknown"}'
        )
    return {
        "choices": [{
            "message": {"content": fake_output}
        }]
    }

# Fixture to patch openai.ChatCompletion.create automatically


@pytest.fixture(autouse=True)
def patch_openai(monkeypatch):
    monkeypatch.setattr(openai.ChatCompletion, "create",
                        fake_chat_completion_create)


@pytest.fixture
def gold_standard_data():
    with open("gold_standard.json", "r") as f:
        return json.load(f)


def test_gold_standard_evaluation(gold_standard_data):
    """
    For each record in the gold standard dataset, call the LLM extraction function
    and compare its output to the expected output.
    """
    for record in gold_standard_data:
        user_input = record["user_input"]
        expected = record["expected"]
        # Log the test case for easier debugging
        logger.info("Testing gold standard input: %s", user_input)

        # Get the LLM extraction output using the patched fake API call
        result = extract_shift_details(user_input)

        # For each expected key, check that the result matches
        for key in expected:
            # Optionally, normalize the strings (e.g., strip whitespace)
            assert result.get(key) == expected[key], (
                f"Mismatch for key '{key}' for input: {user_input}. "
                f"Expected: {expected[key]}, Got: {result.get(key)}"
            )
