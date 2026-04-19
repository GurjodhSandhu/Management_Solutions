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


