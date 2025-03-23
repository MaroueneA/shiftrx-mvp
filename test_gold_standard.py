import json
import pytest
from prompt import extract_shift_details
from logger import logger


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

        # Get the LLM extraction output
        result = extract_shift_details(user_input)

        # For each expected key, check that the result matches
        for key in expected:
            # You may want to apply normalization (e.g., stripping whitespace) as needed.
            assert result.get(key) == expected[key], (
                f"Mismatch for key '{key}' for input: {user_input}. "
                f"Expected: {expected[key]}, Got: {result.get(key)}"
            )
