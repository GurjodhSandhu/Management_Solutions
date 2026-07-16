from . import connect


def add_driver(assigned_driver_id = None,assigned_truck_id=None,driver_name=None,driver_licensenumber=None):
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO drivers 
        (assigned_driver_id,assigned_truck_id,driver_name,driver_licensenumber) 
        VALUES (?,?,?,?)
        """,
        (assigned_driver_id,assigned_truck_id,driver_name,driver_licensenumber))
        conn.commit()
