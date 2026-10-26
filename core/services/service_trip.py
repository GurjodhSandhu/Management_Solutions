from datetime import  datetime
from django.utils import timezone
from typing import Optional
from django.core.exceptions import ValidationError
from django.db import transaction
from core.repositories import TripRepository

from core.models import Trip,Driver,Truck
from core.repositories import DriverRepository, TruckRepository

@transaction.atomic
def new_trip(data: dict) -> Trip:
    new_trip = Trip(**data)
    new_trip.full_clean()
    new_trip.save()
    return new_trip

def make_aware_if_naive(dt) -> Optional[datetime]:
    if dt is None:
        return None
    if timezone.is_naive(dt):
        return timezone.make_aware(dt)
    return dt
ALLOWED_TRIP_UPDATE_FIELDS_PLANNED = {
    "start",
    "end",
    "arrival_time",
    "departure_time",

    "planned_miles",
    "actual_miles",
    "loaded_miles",
    "empty_miles",
    "cpm",
    "pay",
}
ALLOWED_TRIP_UPDATE_FIELDS_INPROGRESS = {
    "end",
    "arrival_time",

    "actual_miles",
    "loaded_miles",
    "empty_miles",
    "cpm",
    "pay",
}
ALLOWED_TRIP_UPDATE_FIELDS_OTHER = {

    "actual_miles",
    "loaded_miles",
    "empty_miles",
    "cpm",
    "pay",
}

@transaction.atomic
def update_trip(trip_id: int,data: dict) -> Trip:
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        raise ValidationError(f"There is no trip with id: {trip_id}")
    if trip.status == Trip.TripStatus.PLANNED:
        ALLOWED_TRIP_UPDATE_FIELDS = ALLOWED_TRIP_UPDATE_FIELDS_PLANNED
    elif trip.status == Trip.TripStatus.IN_PROGRESS:
        ALLOWED_TRIP_UPDATE_FIELDS = ALLOWED_TRIP_UPDATE_FIELDS_INPROGRESS
    elif trip.status in [Trip.TripStatus.COMPLETE, Trip.TripStatus.CANCELED, Trip.TripStatus.INCOMPLETE]:
        ALLOWED_TRIP_UPDATE_FIELDS = ALLOWED_TRIP_UPDATE_FIELDS_OTHER
    else:
        raise ValueError(f"Unknown trip status: {trip.status}")
    for key,value in data.items():
        # HANDLE DATETIME FIELDS
        if key in ALLOWED_TRIP_UPDATE_FIELDS:
            if key in ("departure_time", "arrival_time"):
                # Convert string → datetime
                dt = value
                if isinstance(dt, str):
                    dt = datetime.fromisoformat(dt)
                # Convert naive → aware
                aware_dt = make_aware_if_naive(dt)
                setattr(trip, key, aware_dt)
            else:
                setattr(trip,key,value)
    trip.full_clean()
    trip.save()
    return trip

@transaction.atomic
def delete_trip(trip_id: int) -> None:
    trip = TripRepository.get_trip(trip_id)
    if not trip:
        raise ValidationError(f"There is no trip with id: {trip_id}")
    if trip.status == Trip.TripStatus.IN_PROGRESS:
        raise ValidationError("Trip is active please cancel or set incomplete first: ")
    TripRepository.delete_trip(trip_id)

@transaction.atomic
def assign_driver_to_trip(trip_id: int,driver_id: int) -> Trip:
    trip = Trip.objects.select_for_update().filter(id=trip_id).first()
    driver = Driver.objects.select_for_update().filter(id=driver_id).first()
    if driver is None:
        raise ValidationError(f"There is no driver with id: {driver_id}")
    if trip is None:
        raise ValidationError(f"There is no trip with id: {trip_id}")
    if trip.status != Trip.TripStatus.PLANNED:
        raise ValidationError("Trip is not in planning process: ")
    trip.driver = driver
    trip.full_clean()
    trip.save()
    return trip

@transaction.atomic
def assign_truck_to_trip(trip_id: int,truck_id: int) -> Trip:
    trip = Trip.objects.select_for_update().filter(id=trip_id).first()
    truck = Truck.objects.select_for_update().filter(id=truck_id).first()
    if truck is None:
        raise ValidationError(f"There is no truck with id: {truck_id}")
    if trip is None:
        raise ValidationError(f"There is no trip with id: {trip_id}")
    if trip.status != Trip.TripStatus.PLANNED:
        raise ValidationError("Trip is not in planning process: ")
    trip.truck = truck
    trip.full_clean()
    trip.save()
    return trip
#TRIP STATE MACHINE SERVICES --------

@transaction.atomic
def start_trip(trip_id: int) -> Trip: #planned -> start
    trip = Trip.objects.select_for_update().filter(id=trip_id).first()
    if trip is None:
        raise ValidationError(f"There is no trip with id: {trip_id}")
    trip.validate_start()

    driver = Driver.objects.select_for_update().filter(id=trip.driver_id).first()
    truck = Truck.objects.select_for_update().filter(id=trip.truck_id).first()

    trip.mark_in_progress()
    trip.departure_time = timezone.now()

    driver.mark_unavailable()
    truck.mark_unavailable()

    trip.full_clean()

    driver.save()
    truck.save()
    trip.save()
    return trip

@transaction.atomic
def complete_trip(trip_id: int) -> Trip: #inprogress -> complete
    trip = Trip.objects.select_for_update().filter(id=trip_id).first()
    if trip is None:
        raise ValidationError(f"There is no trip with id: {trip_id}")

    if trip.driver is None:
        raise ValidationError("Trip has no driver assigned")
    if trip.truck is None:
        raise ValidationError("Trip has no truck assigned")
    driver = Driver.objects.select_for_update().filter(id=trip.driver_id).first()
    truck = Truck.objects.select_for_update().filter(id=trip.truck_id).first()

    trip.arrival_time = timezone.now()
    trip.validate_complete()
    trip.status = trip.TripStatus.COMPLETE


    driver.mark_available()
    truck.mark_available()

    trip.full_clean()

    driver.save()
    truck.save()
    trip.save()

    return trip

@transaction.atomic
def incomplete_trip(trip_id: int) -> Trip: #inprogress -> incomplete
    trip = Trip.objects.select_for_update().filter(id=trip_id).first()

    if trip is None:
        raise ValidationError(f"There is no trip with id: {trip_id}")
    if trip.driver is None:
        raise ValidationError("Trip has no driver assigned")
    if trip.truck is None:
        raise ValidationError("Trip has no truck assigned")
    driver = Driver.objects.select_for_update().filter(id=trip.driver_id).first()
    truck = Truck.objects.select_for_update().filter(id=trip.truck_id).first()

    trip.validate_incomplete()
    trip.status = trip.TripStatus.INCOMPLETE

    driver.mark_available()
    truck.mark_available()

    trip.full_clean()

    driver.save()
    truck.save()
    trip.save()
    return trip

@transaction.atomic
def cancel_trip(trip_id: int) -> Trip: #planned -> canceled
    trip = Trip.objects.select_for_update().filter(id=trip_id).first()
    if trip is None:
        raise ValidationError(f"There is no trip with id: {trip_id}")

    trip.validate_cancel()
    trip.status =  Trip.TripStatus.CANCELED

    trip.full_clean()


    trip.save()
    return trip

#TRIP STATE MACHINE END --------

