from management_solutions.models.Driver import driver
from management_solutions.utils.exceptions import ValidationError
from management_solutions.database import driver_repository

def get_driver_input():
    fields = ["driver_name","driver_licensenumber"]

    kwargs = {} #empty dictionary
    for field in fields:
        value = input(f'{field}: ')
        if value:
            kwargs[field] = value
    return kwargs

def create_driver(kwarg):
    try:
        return driver(**kwarg)
    except ValidationError as e:
        for values in e.errors.values():
            for message in values:
                print(message)
        # iterate through the dictionary and print errors
    return None

def add_driver(driver): #add truck objects information into the database
    try:
        driver_repository.add_driver(**driver.to_dict())
        return ("succesfully added driver")
    except:
        return ("failed to add driver")

def get_driver(driver_id): #function to create a driver object from database via the driver_id
    try:
        driver = driver_repository.retrieve_driver(driver_id)
        driver_object = create_driver(driver)
        return driver_object

    except ValueError as e:
        raise ValueError(f"Failed to get driver object from database: {e}")

def list_drivers():
    try:
        print(driver_repository.list_all_drivers())
    except ValueError as e:
        print(e)

def update_drivers(driver_id,changes):
    try:
        driver_repository.update_driver(driver_id,**changes)
    except ValueError as e:
        print(e)
