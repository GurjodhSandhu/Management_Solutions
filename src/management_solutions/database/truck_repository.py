from management_solutions.database import connect


def add_truck(vin=None,brand=None,make=None,year=None,mileage=None,plate=None):
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO trucks (vin,brand,make,year,mileage,plate) VALUES (?,?,?,?,?,?)""",(vin,brand,make,year,mileage,plate))
        conn.commit()

def list_all_trucks():
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT vin,brand,make,year,mileage,plate FROM trucks""")
        test = cursor.fetchall()
        print(test)
