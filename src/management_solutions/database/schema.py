import connect

def initialize_fleetDB():
    conn = connect.connect_fleet()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTs trucks ( 
    truck_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vin TEXT,
    brand TEXT,
    make TEXT,
    year INTEGER,
    mileage INTEGER,
    plate TEXT,
    assigned_driver_id INTEGER);
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS drivers (driver_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    assigned_truck_id INTEGER,
    driver_name TEXT, 
    Driver_licensenumber TEXT);
    """)
    conn.commit()
    conn.close()

initialize_fleetDB()
