from management_solutions.database import connect


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

def update_driver(driver_id = None,driver_name = None, driver_licensenumber=None):
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE drivers SET driver_name = ?, driver_licensenumber = ? WHERE driver_id = ?""",(driver_name,driver_licensenumber,driver_id))
        if cursor.rowcount == 0:
            raise ValueError(f"Driver with ID {driver_id} does not exist")
        conn.commit()

def retrieve_driver(driver_id = None):
    with connect.connect_fleet() as conn:
        keys = ["driver_id","driver_name","driver_licensenumber","assigned_truck_id"]
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM drivers WHERE driver_id = ?""",(driver_id,))
        values = cursor.fetchone()
        if values is None:
            raise ValueError(f"Driver with ID {driver_id} does not exist")
        pairs = dict(zip(keys,values))
        return pairs