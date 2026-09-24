from django.core.exceptions import ValidationError
from django.db import transaction

from core.models import Driver,Truck
from core.repositories import DriverRepository


@transaction.atomic
def add_driver(data: dict) -> Driver:
    driver = Driver(**data)
    driver.clean()
    driver.save()
    return driver

@transaction.atomic
def update_driver(driver_id: int, data: dict) -> Driver | None:
    driver = DriverRepository.get_driver(driver_id)
    if driver is None:
        return None
    else:
        for key, value in data.items():
            if key == "truck":
                truck = Truck.objects.get(id=int(value))
                setattr(driver,key,truck)
                continue
            setattr(driver, key, value)
        driver.clean()
        driver.save()
        return driver

@transaction.atomic
def assign_truck_to_driver(driver_id: int, truck_id: int) -> Driver | None:
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

@transaction.atomic
def remove_truck_from_driver(driver_id: int) -> Driver | None:
    driver = DriverRepository.get_driver(driver_id)
    if driver is None:
        return None
    if driver.get_trips_active():
        raise ValidationError("driver is on an active trip")
    driver.truck = None
    driver.clean()
    driver.save()
    return driver
