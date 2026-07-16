from . import connect


def add_truck(vin=None,brand=None,make=None,year=None,mileage=None,plate=None):
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO trucks (vin,brand,make,year,mileage,plate) VALUES (?,?,?,?,?,?)""",(vin,brand,make,year,mileage,plate))
        conn.commit()


