from management_solutions.models.Truck import truck
from management_solutions.utils.exceptions import TruckValidationError

def get_truck_input():
    vin = input("VIN: ")
    brand = input("Brand: ")
    make = input("Make: ")
    year = input("Year: ")
    if year.isdigit():
        year = int(year)
    mileage = input("Mileage: ")
    if mileage.isdigit():
        mileage = int(mileage)
    plate = input("Plate Number: ")

    #validate inputs

    kwargs = {}
    if vin:
        kwargs["vin"] = vin
    if brand:
        kwargs["brand"] = brand
    if make:
        kwargs["make"] = make
    if year:
        kwargs["year"] = year
    if mileage:
        kwargs["mileage"] = mileage
    if plate:
        kwargs["plate"] = plate

    return kwargs

def new_truck(kwargs): #method to create truck object
    try:
        return truck(**kwargs)

    except TruckValidationError as e:
        for values in e.errors.values():
            for message in values:
                print(message)
        #iterate through the dictionary and print errors

