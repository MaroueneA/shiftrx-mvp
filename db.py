# db.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get database configuration from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_NAME = os.getenv("DB_NAME", "shiftrx")


def get_connection():
    """
    Establish a connection to the PostgreSQL database.
    """
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME
    )
    return conn


def insert_shift(position, start_time, end_time, rate):
    """
    Insert a new shift into the shifts table.

    Args:
        position (str): Job title, e.g., "Pharmacist".
        start_time (str): Start time for the shift.
        end_time (str): End time for the shift.
        rate (str): Payment rate.

    Returns:
        shift_id (int): The ID of the inserted shift record.
    """
    conn = None
    shift_id = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            INSERT INTO shifts (position, start_time, end_time, rate)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """
        cur.execute(query, (position, start_time, end_time, rate))
        shift_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
    except Exception as e:
        print("Error inserting shift:", e)
    finally:
        if conn:
            conn.close()
    return shift_id
