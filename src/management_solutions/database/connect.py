import sqlite3
fleet_db = "fleet.db"

def connect_fleet():
    try:
        return sqlite3.connect(fleet_db)
    except sqlite3.OperationalError as e:
        raise RuntimeError("Fleet database failed to connect") from e

