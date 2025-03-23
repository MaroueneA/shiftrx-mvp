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
        "You are an assistant that extracts shift details from a user's message. "
        "Return only valid JSON without any additional commentary or markdown formatting, "
        "with the keys: position, start_time, end_time, rate. "
        "If any key is missing, set its value to 'unknown'."
    )

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
