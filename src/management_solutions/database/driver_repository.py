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
