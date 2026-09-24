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
def delete_truck(truck_id: int) -> bool:
    truck = TruckRepository.get_truck(truck_id)
    if truck is None:
        return False
    if truck.get_trips_active():
        raise ValidationError("Truck is on an active trip cannot remove")
    TruckRepository.delete_truck(truck_id)
    return True

@transaction.atomic
def update_truck(truck_id: int,data: dict) -> Truck|None:
    truck = TruckRepository.get_truck(truck_id)
    if truck is None:
        return None
    else:
        for key, value  in data.items():
            setattr(truck,key, value)
        truck.full_clean()
        truck.save()
        return truck

@transaction.atomic
def remove_all_drivers_from_truck(truck_id: int) -> bool | None:
    truck = TruckRepository.get_truck(truck_id)
    if truck is None:
        raise ValidationError("Truck not found")
    drivers = truck.get_drivers()
    if not drivers.exists():
        return True
    else:
        for driver in drivers:
            if driver.get_trips_active().exists():
                raise ValidationError("Driver is on an active trip cannot remove from truck")
            driver.truck = None
            driver.save()
        return True


