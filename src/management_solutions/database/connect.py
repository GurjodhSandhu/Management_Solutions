import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of connect.py
DB_PATH = os.path.join(BASE_DIR, "fleet.db")           # database inside /database
def connect_fleet():
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.OperationalError as e:
        raise RuntimeError("Fleet database failed to connect") from e

