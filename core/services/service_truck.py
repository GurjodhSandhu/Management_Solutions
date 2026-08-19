from django.core.exceptions import ValidationError

from core.models import Truck, Driver
from core.repositories import TruckRepository


def add_truck(data):
    truck = Truck(**data)
    truck.full_clean()
    truck.save()
    return truck

def delete_truck(truck_id):
    truck = TruckRepository.get_truck(truck_id)
    if truck is None:
        return None
    for driver in truck.get_drivers():
        if driver.get_trips_active().exists():
            raise ValidationError("Truck and driver are on an active trip")
    TruckRepository.delete_truck(truck_id)
    return True

def update_truck(truck_id,data):
    truck = TruckRepository.get_truck(truck_id)
    if truck is None:
        return None
    else:
        for key, value  in data.items():
            setattr(truck,key, value)
        truck.full_clean()
        truck.save()
        return truck

def remove_all_drivers_from_truck(truck_id):
    truck = TruckRepository.get_truck(truck_id)
    if truck is None:
        return None
    drivers = truck.get_drivers()
    if not drivers.exists():
        return None
    else:
        for driver in drivers:
            if driver.get_trips_active().exists():
                raise ValidationError("Driver is on an active trip cannot remove from truck")
            driver.truck = None
            driver.save()
        return True


