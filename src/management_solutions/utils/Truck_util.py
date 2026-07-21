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

def add_truck(truck): #add truck objects information into the database
    try:
        truck_repository.add_truck(**truck.to_dict())
        return ("succesfully added truck")
    except:
        return ("failed to add truck")

def get_truck(truck_id): #function to create a truck object from database via the truck_id RETRIEVE TRUCK
    try:
        truck = truck_repository.retrieve_truck(truck_id)
        truck_object = create_truck(truck)
        return truck_object

    except ValueError as e:
        raise ValueError(f"Failed to get truck object from database: {e}")

def list_trucks():
    try:
        print(truck_repository.list_all_trucks())
    except ValueError as e:
        print(e)

def update_trucks(truck_id,changes): #take a dictionary of changes and updates the database of trucks
    try:
        truck_repository.update_trucks(truck_id,**changes)
    except ValueError as e:
        print(e + "failed to update truck")
