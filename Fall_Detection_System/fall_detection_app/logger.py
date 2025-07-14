# logger.py
import sqlite3
from datetime import datetime

DB_PATH = "fall_events.db"

def log_event(filename, mode):
    """
    Inserts a fall event into the database with current timestamp.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS fall_events
                 (timestamp TEXT, mode TEXT, filename TEXT)''')
    # Prepare data
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO fall_events VALUES (?, ?, ?)", 
              (timestamp, mode, filename))
    conn.commit()
    conn.close()

def get_events():
    """
    Retrieves all fall events from the database.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, mode, filename FROM fall_events ORDER BY timestamp DESC")
    events = c.fetchall()
    conn.close()
    return events
