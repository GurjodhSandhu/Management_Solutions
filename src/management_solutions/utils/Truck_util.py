from management_solutions.models.Truck import truck
from management_solutions.utils.exceptions import InvalidVinError
from management_solutions.utils.exceptions import InvalidYearError
from management_solutions.utils.exceptions import InvalidMileageError
from management_solutions.utils.exceptions import InvalidPlateError



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
        kwargs["year"] = year
    if mileage:
        kwargs["mileage"] = mileage
    if plate:
        kwargs["plate"] = plate

    return kwargs

def new_truck(kwargs): #method to create truck object
    try:
        return truck(**kwargs)
    except InvalidVinError as e:
        print(e)
        return None
    except InvalidYearError as e:
        print(e)
        return None
    except InvalidMileageError as e:
        print(e)
        return None
    except InvalidPlateError as e:
        print(e)
        return None
