from config import settings
import psycopg2
from psycopg2 import sql
from contextlib import closing
from typing import List, Dict
from logger import logger


def process_in_logfile(message: str) -> None:
    """
    Documentation
    """
    logger.info(f"record: {message}")



def process_in_db(messages: List[Dict]) -> None:
    """
    Processes and stores the message in PostgreSQL database.
    
    Params:
        message (str): The message to be processed.
    """
    try:
        with closing(psycopg2.connect(**settings.DB_SETTINGS)) as conn:
            with conn.cursor() as cursor:
                insert_query = sql.SQL(
                    "INSERT INTO transactions (amount, description) VALUES %s"
                )
                # Create a list of tuples to insert
                values = [(msg['amount'], msg['description']) for msg in messages]
                # Convert the list of tuples to a string for the query
                values_str = ','.join(cursor.mogrify("(%s,%s)", val).decode('utf-8') for val in values)
                cursor.execute(insert_query.as_string(conn) % values_str)
                conn.commit()
        logger.info(f"{len(messages)} messages stored in database.")
    except Exception as e:
        logger.error(f"Error storing message in database: {e}")
        raise Exception(e)
