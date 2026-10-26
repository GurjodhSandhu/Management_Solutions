from django.core.exceptions import ValidationError
from django.db import transaction

from core.models import Driver,Truck
from core.repositories import DriverRepository


@transaction.atomic
def add_driver(data: dict) -> Driver:
    driver = Driver(**data)
    driver.full_clean()
    driver.save()
    return driver

ALLOWED_DRIVER_UPDATE_FIELDS = {
    "truck",                 # allow assigning a truck
    "driver_name",
    "driver_licensenumber",
    "driver_status",
}

@transaction.atomic
def update_driver(driver_id: int, data: dict) -> Driver:
    driver = DriverRepository.get_driver(driver_id)
    if driver is None:
        raise ValidationError(f"There is no driver with id: {driver_id}")

    for key, value in data.items():
        if key in ALLOWED_DRIVER_UPDATE_FIELDS:
            if key == "truck":
                if value in (None, ""):
                    new_truck = None
                elif isinstance(value, Truck): #if data gives truck object directly
                    new_truck = value
                else:
                    new_truck = Truck.objects.get(id=int(value)) #if given truck id
                driver.truck = new_truck
                continue
            setattr(driver, key, value)

    driver.full_clean()
    driver.save()
    return driver

@transaction.atomic
def assign_truck_to_driver(driver_id: int, truck_id: int) -> Driver:

    driver = Driver.objects.select_for_update().filter(id=driver_id).first()
    if driver is None:
        raise ValidationError(f"There is no driver with id: {driver_id}")

    truck = Truck.objects.select_for_update().filter(id=truck_id).first()
    if truck is None:
        raise ValidationError(f"There is no truck with id: {truck_id}")

    if driver.truck:
        raise ValidationError("driver already assigned a truck: clear truck if needed")
    if driver.get_trips_active():
        raise ValidationError("driver is on an active trip")

    driver.truck = truck
    driver.validate_truck()
    driver.full_clean()
    driver.save()
    return driver

@transaction.atomic
def remove_truck_from_driver(driver_id: int) -> Driver:
    driver = DriverRepository.get_driver(driver_id)
    if driver is None:
        raise ValidationError(f"There is no driver with id: {driver_id}")
    if driver.get_trips_active():
        raise ValidationError("driver is on an active trip")
    driver.truck = None
    driver.full_clean()
    driver.save()
    return driver

@transaction.atomic
def delete_driver(driver_id: int) -> Driver:
    driver = DriverRepository.get_driver(driver_id)
    if driver is None:
        raise ValidationError(f"There is no driver with id: {driver_id}")
    if driver.get_trips_active():
        raise ValidationError("driver is on an active trip")
    DriverRepository.delete_driver(driver_id)
    return driver