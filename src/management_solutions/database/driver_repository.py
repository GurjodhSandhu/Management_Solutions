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

def update_driver(driver_id: int,changes: dict):
    allowed_fields = {"driver_name", "driver_licensenumber", "assigned_truck_id"}
    set_clauses = []
    params = []

    for key, value in changes.items():
        if key not in allowed_fields:
            raise ValueError(f"Invalid field for update: {key}")
        set_clauses.append(f"{key} = ?")
        params.append(value)

    params.append(driver_id)

    sql = f"UPDATE drivers SET {', '.join(set_clauses)} WHERE driver_id = ?"

    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
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