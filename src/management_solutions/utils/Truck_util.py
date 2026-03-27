def get_truck_input():
    vin = input("VIN: ")
    brand = input("Brand: ")
    make = input("Make: ")
    year = input("Year: ")
    mileage = input("Mileage: ")
    plate = input("Plate Number: ")

    kwargs = {}
    if vin:
        kwargs["vin"] = vin
    if brand:
        kwargs["brand"] = brand
    if make:
        kwargs["make"] = make
    if year:
        kwargs["year"] = int(year)
    if mileage:
        kwargs["mileage"] = float(mileage)
    if plate:
        kwargs["plate"] = plate

    return kwargs

