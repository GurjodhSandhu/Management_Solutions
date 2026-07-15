from . import connect


def add_truck(vin=None,brand=None,make=None,year=None,mileage=None,plate=None,assigned_driver_id=None):
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO trucks (vin,brand,make,year,mileage,plate,assigned_driver_id) VALUES (?,?,?,?,?,?,?)""",(vin,brand,make,year,mileage,plate,assigned_driver_id))
        conn.commit()


