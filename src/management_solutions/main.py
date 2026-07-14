from management_solutions.database import connect

conn = connect.connect_fleet()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS trucks (
    truck_id INTEGER PRIMARY KEY,
    brand TEXT,
    year INTEGER,
    assigned_driver_id INTEGER
);
""")

cursor.execute("""
INSERT INTO trucks (truck_id, brand, year)
VALUES (2, 'Chevy', 2020);
""")

conn.commit()
conn.close()
#testing code:







