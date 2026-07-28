from management_solutions.database import connect
import sqlite3

def add_truck(vin=None,brand=None,make=None,year=None,mileage=None,plate=None,truck_status=None,truck_location=None):
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO trucks (vin,brand,make,year,mileage,plate,truck_status,truck_location) VALUES (?,?,?,?,?,?,?,?)""",(vin,brand,make,year,mileage,plate,truck_status,truck_location))
        conn.commit()

def list_all_trucks():
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM trucks""")
        all_trucks = cursor.fetchall()
        return all_trucks

def update_trucks(truck_id:int ,changes: dict):
    allowed_fields = ["vin","brand","make","year","mileage","plate","assigned_driver_id","truck_status","truck_location"]

    set_clauses = []
    params = []

    for key, value in changes.items():
        if key not in allowed_fields:
            raise ValueError(f"[REPO]Invalid field for update: {key}")
        set_clauses.append(f"{key} = ?")
        params.append(value)

    params.append(truck_id)

    sql = f"UPDATE trucks SET {', '.join(set_clauses)} WHERE truck_id = ?"
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute(sql,params)
        if cursor.rowcount == 0:
            raise ValueError(f"[REPO] truck_id with ID {truck_id} does not exist")
        conn.commit()

def retrieve_truck(truck_id):
    with connect.connect_fleet() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""Select * FROM trucks WHERE truck_id = ?""",(truck_id,))
        #take list output format as a dict into dic
        values = cursor.fetchone()
        if values is None:
            raise ValueError(f"[REPO]Truck with ID {truck_id} does not exist")
        truck = {
                 "truck_id": values["truck_id"],
                 "vin": values["vin"],
                 "brand": values["brand"],
                 "make": values["make"],
                 "year": values["year"],
                 "mileage": values["mileage"],
                 "plate": values["plate"],
                 "assigned_driver_id": values["assigned_driver_id"],
                 "truck_status": values["truck_status"],
                 "truck_location": values["truck_location"]
                 }
        return truck