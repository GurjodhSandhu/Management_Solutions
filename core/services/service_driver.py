from models import Driver,Truck

def add_driver(data):
    driver = Driver(**data)
    driver.clean()
    driver.save()
    return driver

def delete_driver(driver_id):
    Driver.objects.filter(id=driver_id).delete()
    return True

def update_driver(driver_id,data):
    driver = Driver.objects.filter(id=driver_id).first()
    if driver is None:
        return None
    else:
        for key, value in data.items():
            setattr(driver, key, value)
        driver.clean()
        driver.save()
        return driver

def assign_truck_to_driver(driver_id,truck_id):
    driver = Driver.objects.filter(id=driver_id).first()
    if driver is None:
        return None
    truck = Truck.objects.filter(id=truck_id).first()
    if truck is None:
        return None
    else:
        driver.truck = truck
        driver.clean()
        driver.save()
        return driver

def remove_truck_from_driver(driver_id):
    driver = Driver.objects.filter(id=driver_id).first()
    if driver is None:
        return None
    driver.truck = None
    driver.clean()
    driver.save()
    return driver
