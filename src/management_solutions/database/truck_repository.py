import connect

conn = connect.connect_fleet()
cursor = conn.cursor()

def add_truck(vin=None,brand=None,make=None,year=None,mileage=None,plate=None,assigned_driver_id=None):
    cursor.execute("""INSERT INTO trucks (vin,brand,make,year,mileage,plate,assigned_driver_id) VALUES (?,?,?,?,?,?,?)""",(vin,brand,make,year,mileage,plate,assigned_driver_id))
    conn.commit()


