from management_solutions.models.Truck import truck
from management_solutions.utils.exceptions import ValidationError
from management_solutions.database import truck_repository

def get_truck_input():

    fields = ["vin","brand","make","year","mileage", "plate"]
    kwargs = {}
    for field in fields:
        value = input(f"{field}:")
        if value:
            kwargs[field] = value

    return kwargs

def create_truck(kwargs): #method to create truck object
    try:
        return truck(**kwargs)

    except ValidationError as e:
        for values in e.errors.values():
            for message in values:
                print(message)
        #iterate through the dictionary and print errors
        return None

def get_truck(truck_id): #function to retrieve truck from database via the truck_id
    truck = truck_repository.retrieve_truck(truck_id)
    truck_object = create_truck(**truck)
    return truck_object

