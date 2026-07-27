from exceptions import DriverServiceError
from management_solutions.service import truck_service, driver_service


def assign_driver_to_truck(truck_id: int,driver_id: int):
    truck = truck_service.get_truck(truck_id)
    driver = driver_service.get_driver(driver_id)

    if driver.driver_id == truck.assigned_driver_id and driver.assigned_truck_id == truck.truck_id:
        return ("driver and truck already assigned to each other")

    if driver.assigned_truck_id is not None: #if previously assigned truck:
        clear_driver_assigned_truck(driver_id) #clear out the previously assigned truck
    if truck.assigned_driver_id is not None:
        clear_truck_assigned_driver(truck_id)
    #all assignments cleared

    driver_service.update_drivers(driver_id,{"assigned_truck_id": truck_id})
    truck_service.update_trucks(truck_id,{"assigned_driver_id": driver_id})



def clear_driver_assigned_truck(driver_id: int):
    driver = driver_service.get_driver(driver_id) #retrieve driver object via provided driver_id
    assigned_truck_id = driver.assigned_truck_id #get the connected truck_id

    if assigned_truck_id is None:
        return "No truck assigned"
    truck_service.update_trucks(assigned_truck_id,{"assigned_driver_id": None})
    driver_service.update_drivers(driver_id,{"assigned_truck_id": None})

    return "successfully cleared drivers assigned truck"

def clear_truck_assigned_driver(truck_id: int):
    truck = truck_service.get_truck(truck_id)
    assigned_driver_id = truck.assigned_driver_id

    if assigned_driver_id is None:
        return "No driver assigned"

    truck_service.update_trucks(truck_id,{"assigned_driver_id": None})
    driver_service.update_drivers(assigned_driver_id,{"assigned_truck_id": None})
    return "successfully cleared trucks assigned driver"

assign_driver_to_truck(1, 1)


try:
    assign_driver_to_truck(1, 1)
except Exception as e:
    print(e)

print(driver_service.list_drivers())
print(truck_service.list_trucks())