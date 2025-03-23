# prompt.py

import os
import json
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_shift_details(user_input):
    """
    Sends the user's input to the LLM and expects a JSON response with the following structure:

    {
      "position": "...",
      "start_time": "...",
      "end_time": "...",
      "rate": "..."
    }

    If any field is missing in the LLM's output, it defaults to "unknown".
    """
    system_prompt = (
        "You are an assistant that extracts shift details from a user's message. "
        "Return a JSON object with the keys: position, start_time, end_time, rate. "
        "If a key is missing, set its value to 'unknown'."
    )

    try:
        # Use the ChatCompletion endpoint for GPT-3.5 Turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0
        )
        # Extract the message content from the response
        content = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("Error communicating with OpenAI:", e)
        # If there's an error, default to unknown values
        return {
            "position": "unknown",
            "start_time": "unknown",
            "end_time": "unknown",
            "rate": "unknown"
        }

    # Try parsing the response as JSON
    try:
        shift_data = json.loads(content)
    except json.JSONDecodeError:
        print("Failed to parse LLM response as JSON. Response was:")
        print(content)
        shift_data = {
            "position": "unknown",
            "start_time": "unknown",
            "end_time": "unknown",
            "rate": "unknown"
        }

    return shift_data
