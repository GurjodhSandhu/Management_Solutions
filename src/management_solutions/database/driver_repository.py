from management_solutions.database import connect
import sqlite3

def add_driver(driver_name=None,driver_licensenumber=None):
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO drivers 
        (driver_name,driver_licensenumber) 
        VALUES (?,?)
        """,
        (driver_name,driver_licensenumber))
        conn.commit()

def list_all_drivers():
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM drivers""")
        all_drivers = cursor.fetchall()
        print(all_drivers)

def update_driver(driver_id: int,changes: dict):
    allowed_fields = {"driver_name", "driver_licensenumber", "assigned_truck_id"}
    set_clauses = []
    params = []

    for key, value in changes.items():
        if key not in allowed_fields:
            raise ValueError(f"[REPO]Invalid field for update: {key}")
        set_clauses.append(f"{key} = ?")
        params.append(value)

    params.append(driver_id)

    sql = f"UPDATE drivers SET {', '.join(set_clauses)} WHERE driver_id = ?"

    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        if cursor.rowcount == 0:
            raise ValueError(f"[REPO] Driver with ID {driver_id} does not exist")
        conn.commit()

def retrieve_driver(driver_id = None):
    with connect.connect_fleet() as conn:
        conn.row_factory = sqlite3.Row #retrieve rows in dict format
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM drivers WHERE driver_id = ?""",(driver_id,))
        values = cursor.fetchone()
        if values is None:
            raise ValueError(f"[REPO]Driver with ID {driver_id} does not exist")
        driver = {
            "driver_id": values["driver_id"],
            "driver_name": values["driver_name"],
            "driver_licensenumber": values["driver_licensenumber"],
            "assigned_truck_id": values["assigned_truck_id"],
        }
        return driver