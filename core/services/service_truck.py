from django.core.exceptions import ValidationError
from django.db import transaction

from core.models import Truck
from core.repositories import TruckRepository

@transaction.atomic
def add_truck(data: dict) -> Truck:
    truck = Truck(**data)
    truck.full_clean()
    truck.save()
    return truck

@transaction.atomic
def delete_truck(truck_id: int) -> Truck:
    truck = TruckRepository.get_truck(truck_id)
    if truck is None:
        raise ValidationError(f"There is no truck with id: {truck_id}")

    if truck.get_trips_active():
        raise ValidationError("Truck is on an active trip cannot remove")

    TruckRepository.delete_truck(truck_id)
    return truck
ALLOWED_TRUCK_UPDATE_FIELDS = {
    "vin",
    "brand",
    "year",
    "make",
    "mileage",
    "plate",
    "truck_status",
    "truck_location",
}
@transaction.atomic
def update_truck(truck_id: int,data: dict) -> Truck:
    truck = TruckRepository.get_truck(truck_id)
    if truck is None:
        raise ValidationError(f"There is no truck with id: {truck_id}")

    for key, value  in data.items():
        if key in ALLOWED_TRUCK_UPDATE_FIELDS:
            setattr(truck,key, value)


    truck.full_clean()
    truck.save()
    return truck

@transaction.atomic
def remove_all_drivers_from_truck(truck_id: int) -> Truck:
    truck = TruckRepository.get_truck(truck_id)
    if truck is None:
        raise ValidationError(f"There is no truck with id: {truck_id}")

    drivers = truck.get_drivers()
    if not drivers.exists():
        return truck

    for driver in drivers:
        if driver.get_trips_active().exists():
            raise ValidationError("Driver is on an active trip cannot remove from truck")
        driver.truck = None
        driver.full_clean()
        driver.save()
    return truck