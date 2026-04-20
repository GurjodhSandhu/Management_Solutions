def assign_driver_to_truck(driver_id,truck_id,trucks,drivers):
    #lookup driver and truck via their id
    truck = trucks.get(truck_id)
    if not truck:
        return f"truck: {truck_id} not found"

    driver = drivers.get(driver_id)
    if not driver:
        return f"driver: {driver_id} not found"

    #if truck has previously assigned driver
    if truck.assigned_driver_id is not None:
        old_driver = drivers.get(truck.assigned_driver_id)
        if old_driver:
            old_driver.assigned_truck_id = None
        print(f'Cleared previously assigned driver: {truck.assigned_driver_id} from truck: {truck_id}')

    #if driver has previously assigned truck
    if driver.assigned_truck_id is not None:
        old_truck = trucks.get(driver.assigned_truck_id)
        if old_truck:
            old_truck.assigned_driver_id = None
        print(f'cleared previously assigned truck: {driver.assigned_truck_id} from driver: {driver_id}')

    #assign trucks driver id to choosen drivers id and vice versa
    truck.assigned_driver_id = driver.driver_id
    driver.assigned_truck_id = truck.truck_id
    return f"driver: {driver_id} assigned to truck: {truck_id}"

def unassign_truck_from_driver(driver_id, trucks, drivers):  # remove driver-truck link via driver
    # lookup driver
    driver = drivers.get(driver_id)
    if not driver:
        return f"driver {driver_id} doesnt exist"

    # driver has no truck assigned
    if driver.assigned_truck_id is None:
        return f"driver {driver_id} is not assigned to any truck"

    # capture truck_id BEFORE clearing anything
    truck_id = driver.assigned_truck_id

    # lookup truck
    truck = trucks.get(truck_id)
    if not truck:
        # clean driver anyway
        driver.assigned_truck_id = None
        return f"truck {truck_id} doesn't exist"

    # truck has no driver (inconsistent state)
    if truck.assigned_driver_id is None:
        driver.assigned_truck_id = None
        return f"truck {truck_id} has no assigned driver"

    # clear both sides
    truck.assigned_driver_id = None
    driver.assigned_truck_id = None

    return f"driver {driver_id} unassigned from truck {truck_id}"

def unassign_driver_from_truck(truck_id, trucks, drivers):  # remove driver-truck link via driver
    # lookup truck
    truck = trucks.get(truck_id)
    if not truck:
        return f"truck {truck_id} doesnt exist"

    # truck has no driver assigned
    if truck.assigned_driver_id is None:
        return f"truck {truck_id} is not assigned to any driver"

    # capture driver_id BEFORE clearing anything
    driver_id = truck.assigned_driver_id

    # lookup truck
    driver = drivers.get(driver_id)
    if not driver:
        # clean truck anyway
        truck.assigned_driver_id = None
        return f"driver {driver_id} doesn't exist| cleared trucks assigned driver"

    # driver has no assigned truck (inconsistent state)
    if driver.assigned_truck_id is None:
        truck.assigned_driver_id = None
        return f"driver {driver_id} has no assigned truck| cleared trucks assigned driver"

    # clear both sides
    truck.assigned_driver_id = None
    driver.assigned_truck_id = None

    return f"truck {truck_id} unassigned from driver {driver_id}"

