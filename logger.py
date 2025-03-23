# logger.py
import logging
import sys

# Create a custom logger
logger = logging.getLogger("shiftrx")
logger.setLevel(logging.DEBUG)  # Set the desired logging level

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# You could also add a FileHandler if you want to log to a file:
# file_handler = logging.FileHandler('shiftrx.log')
# file_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)
# file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
# logger.addHandler(file_handler)
