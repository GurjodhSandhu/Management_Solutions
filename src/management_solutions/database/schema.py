import connect

def initialize_fleetDB():
    conn = connect.connect_fleet()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS trucks ( 
    truck_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vin TEXT,
    brand TEXT,
    make TEXT,
    year INTEGER,
    mileage INTEGER,
    plate TEXT,
    assigned_driver_id INTEGER,
    truck_status TEXT,
    truck_location TEXT);
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS drivers (driver_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    assigned_truck_id INTEGER,
    driver_name TEXT, 
    Driver_licensenumber TEXT);
    """)

    # Insert starter data ONLY if empty
    cursor.execute("SELECT COUNT(*) FROM trucks")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO trucks (vin, brand, make, year, mileage, plate, assigned_driver_id)
            VALUES
                ('1FTFW1E50JFC12345', 'Ford', 'F-150', 2018, 120000, 'ABC123', NULL),
                ('3C63RRGL8JG123456', 'Ram', '3500', 2019, 90000, 'XYZ789', NULL);
            """)


    cursor.execute("SELECT COUNT(*) FROM drivers")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO drivers (assigned_truck_id, driver_name, driver_licensenumber)
        VALUES
            (NULL, 'John Doe', 'LIC123'),
            (NULL, 'Sarah Smith', 'LIC456');
        """)
    conn.commit()
    conn.close()

initialize_fleetDB()
