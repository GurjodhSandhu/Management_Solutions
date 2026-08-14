from django.core.exceptions import ValidationError

from core.models import Driver,Truck
from core.repositories import DriverRepository
from models import Truck


def add_driver(data):
    driver = Driver(**data)
    driver.clean()
    driver.save()
    return driver

def update_driver(driver_id,data):
    driver = DriverRepository.get_driver(driver_id)
    if driver is None:
        return None
    else:
        for key, value in data.items():
            setattr(driver, key, value)
        driver.save()
        return driver

def assign_truck_to_driver(driver_id,truck_id):
    driver = DriverRepository.get_driver(driver_id)
    if driver is None:
        return None
    truck = Truck.objects.filter(id=truck_id).first()
    if truck is None:
        return None
    if driver.truck:
        raise ValidationError("driver already assigned a truck: clear truck if needed")
    if driver.get_trips_active():
        raise ValidationError("driver is on an active trip")

    driver.truck = truck
    driver.validate_truck()
    driver.clean()
    driver.save()
    return driver

def remove_truck_from_driver(driver_id):
    driver = DriverRepository.get_driver(driver_id)
    if driver is None:
        return None
    if driver.get_trips_active():
        raise ValidationError("driver is on an active trip")
    driver.truck = None
    driver.clean()
    driver.save()
    return driver
