from . import connect


def add_driver(assigned_truck_id = None,driver_name=None,driver_licensenumber=None):
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO drivers (assigned_truck_id,driver_name,driver_licensenumber) VALUES (?,?,?)""",(assigned_truck_id,driver_name,driver_licensenumber))
        conn.commit()
        