from models import Truck, Driver

def add_truck(data):
    truck = Truck(**data)
    truck.clean()
    truck.save()
    return truck

def delete_truck(truck_id):
    Truck.objects.filter(id=truck_id).delete()
    return True

def update_truck(truck_id,data):
    truck = Truck.objects.filter(id=truck_id).first()
    if truck is None:
        return None
    else:
        for key, value  in data.items():
            setattr(truck,key, value)
        truck.clean()
        truck.save()
        return truck

def assign_driver_to_truck(truck_id,driver_id):
    driver = Driver.objects.filter(id=driver_id).first()
    if driver is None:
        return None
    truck = Truck.objects.filter(id = truck_id).first()
    if truck is None:
        return None
    else:
        driver.truck = truck
        driver.clean()
        driver.save()
        return driver

def get_driver_truck(truck_id):
    return list(Driver.objects.filter(truck_id = truck_id))

def remove_driver_from_truck(truck_id):
    drivers = Driver.objects.filter(truck_id = truck_id)
    if not drivers.exists():
        return None
    else:
        for driver in drivers:
            driver.truck = None
            driver.clean()
            driver.save()
        return list(drivers)