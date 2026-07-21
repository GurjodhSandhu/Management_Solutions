from management_solutions.database import connect


def add_truck(vin=None,brand=None,make=None,year=None,mileage=None,plate=None):
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO trucks (vin,brand,make,year,mileage,plate) VALUES (?,?,?,?,?,?)""",(vin,brand,make,year,mileage,plate))
        conn.commit()

def list_all_trucks():
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT truck_id,vin,brand,make,year,mileage,plate FROM trucks""")
        all_trucks = cursor.fetchall()
        print(all_trucks)
        return all_trucks

def update_trucks(truck_id = None,vin=None,brand=None,make=None,year=None,mileage=None,plate=None):
    with connect.connect_fleet() as conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE trucks SET vin = ?,brand = ?,make = ?,year = ?, mileage = ?, plate = ? WHERE truck_id = ? """,(vin,brand,make,year,mileage,plate,truck_id))
        if cursor.rowcount == 0:
            raise ValueError(f"truck_id with ID {truck_id} does not exist")
        conn.commit()

def retrieve_truck(truck_id):
    with connect.connect_fleet() as conn:
        parameters = ["truck_id","vin","brand","make","year","mileage","plate"]
        cursor = conn.cursor()
        cursor.execute("""Select * FROM trucks WHERE truck_id = ?""",(truck_id))
        if not cursor.fetchone():
            raise ValueError(f"Truck with ID {truck_id} does not exist")
        #take list output format as a dict into dic
        values = cursor.fetchall()
        dict = zip(parameters,values) #create a dictionary of the truck information for the give truck id
        return dict