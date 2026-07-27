from management_solutions.exceptions import TruckServiceError
from management_solutions.models.truck import Truck
from pydantic import ValidationError
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
        return Truck(**kwargs)

    except ValidationError as e:
        print(e)
        #iterate through the dictionary and print errors
        return None

def add_truck(truck): #add truck objects information into the database
    try:
        truck_repository.add_truck(**truck.model_dump(exclude={"truck_id","assigned_driver_id"}))
        return ("succesfully added truck")
    except Exception as e:
        raise ValueError(f"Failed to add truck: {e}")
def get_truck(truck_id): #function to create a truck object from database via the truck_id RETRIEVE TRUCK
    try:
        truck = truck_repository.retrieve_truck(truck_id)
        truck_object = create_truck(truck)
        return truck_object

    except Exception as e:
        raise TruckServiceError(f"Failed to get truck object from database: {e}")

def list_trucks():
    try:
        print(truck_repository.list_all_trucks())
    except Exception as e:
        raise TruckServiceError(f"Failed to list all trucks: {e}")

def update_trucks(truck_id: int,changes: dict): #take a dictionary of changes and updates the database of trucks
    try:
        truck_repository.update_trucks(truck_id,changes)
    except Exception as e:
       raise TruckServiceError(f"Failed to update truck: {e}")