from management_solutions.models.Driver import driver
from management_solutions.utils.exceptions import ValidationError

def get_driver_input():
    fields = ["driver_id"]

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