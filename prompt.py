# prompt.py
import os
import json
import openai
from dotenv import load_dotenv
from logger import logger  # Import our logger

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_shift_details(user_input):
    system_prompt = (
        "You are a precise assistant for extracting shift details. "
        "From the user's input, return a single line of valid JSON with exactly the following keys: "
        '"position", "start_time", "end_time", "rate", "facility_name", "location". '
        "Do not include any additional text or markdown formatting. "
        "If a detail is not provided in the input, set its value to 'unknown'. "
        "The output must be a valid JSON object. For example: "
        '{"position": "Pharmacist", "start_time": "9AM", "end_time": "5PM", "rate": "$50/hr", "facility_name": "City Hospital", "location": "Denver"}.')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0
        )
        content = response["choices"][0]["message"]["content"].strip()
        logger.info("LLM raw response: %s", content)
    except Exception as e:
        logger.error("Error communicating with OpenAI: %s", e)
        return {
            "position": "unknown",
            "start_time": "unknown",
            "end_time": "unknown",
            "rate": "unknown"
        }

    # Remove Markdown formatting if present
    if content.startswith("```"):
        lines = content.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        content = "\n".join(lines).strip()

    try:
        shift_data = json.loads(content)
    except json.JSONDecodeError:
        logger.error(
            "Failed to parse LLM response as JSON. Response was: %s", content)
        shift_data = {
            "position": "unknown",
            "start_time": "unknown",
            "end_time": "unknown",
            "rate": "unknown"
        }

    return shift_data
