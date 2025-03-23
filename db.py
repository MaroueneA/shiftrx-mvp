# db.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from logger import logger  # Ensure logger is imported

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_NAME = os.getenv("DB_NAME", "shiftrx")


def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            dbname=DB_NAME
        )
        logger.info("Database connection established.")
        return conn
    except Exception as e:
        logger.error("Failed to connect to the database: %s", e)
        raise


def insert_shift(position, start_time, end_time, rate, facility_name="unknown", location="unknown"):
    conn = None
    shift_id = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            INSERT INTO shifts (position, start_time, end_time, rate, facility_name, location)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cur.execute(query, (position, start_time, end_time,
                    rate, facility_name, location))
        shift_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        logger.info("Inserted shift with id %s", shift_id)
    except Exception as e:
        logger.error("Error inserting shift: %s", e)
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")
    return shift_id
