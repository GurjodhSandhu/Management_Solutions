from datetime import timezone, datetime
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.db import transaction
from core.repositories import TripRepository

from core.models import Trip,Driver,Truck
from core.repositories import DriverRepository, TruckRepository


def new_trip(data):
    new_trip = Trip(**data)
    new_trip.full_clean()
    new_trip.save()
    return new_trip

def make_aware_if_naive(dt):
    if dt is None:
        return None
    if timezone.is_naive(dt):
        return timezone.make_aware(dt)
    return dt


def update_trip(trip_id,data):
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        return None
    for key,value in data.items():
        # HANDLE DATETIME FIELDS
        if key in ("departure_time", "arrival_time"):
            # Convert string → datetime
            dt = datetime.fromisoformat(value)
            # Convert naive → aware
            aware_dt = make_aware_if_naive(dt)
            setattr(trip, key, aware_dt)

        elif key == 'driver':
            setattr(trip, key, DriverRepository.get_driver(value))
            if value is None:
                raise ValidationError("Driver not found")
        elif key == 'truck':
            setattr(trip, key, TruckRepository.get_truck(value))
            if value is None:
                raise ValidationError("Truck not found")
        else:
            setattr(trip,key,value)
    trip.full_clean()
    trip.save()
    return trip

def delete_trip(trip_id):
    TripRepository.delete_trip(trip_id)

def assign_driver_to_trip(trip_id,driver_id):
    trip = TripRepository.get_trip(trip_id)
    driver = Driver.objects.filter(id=driver_id).first()
    if driver is None:
        raise ValidationError("No driver found")
    if trip is None:
        raise ValidationError("No trip found")
    if trip.status != Trip.TripStatus.PLANNED:
        raise ValidationError("Trip is not in planning process: ")
    trip.driver = driver
    trip.full_clean()
    trip.save()

    return trip
#TRIP STATE MACHINE SERVICES --------

@transaction.atomic
def start_trip(trip_id):
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        raise ValidationError("No trip found")

    trip.validate_start()
    trip.mark_in_progress()
    trip.departure_time = timezone.now()

    driver = trip.driver
    truck = trip.truck
    driver.mark_unavailable()
    truck.mark_unavailable()

    trip.full_clean()

    driver.save()
    truck.save()
    trip.save()
    return trip

@transaction.atomic
def complete_trip(trip_id):
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        raise ValidationError("No trip found")

    trip.validate_complete()
    trip.status = trip.TripStatus.COMPLETE
    trip.arrival_time = timezone.now()

    driver = trip.driver
    truck = trip.truck

    driver.mark_available()
    truck.mark_available()

    trip.full_clean()

    driver.save()
    truck.save()
    trip.save()

    return trip

@transaction.atomic
def incomplete_trip(trip_id):
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        raise ValidationError("No trip found")

    trip.validate_incomplete()
    trip.status = trip.TripStatus.INCOMPLETE

    driver = trip.driver
    truck = trip.truck

    driver.mark_available()
    truck.mark_available()

    trip.full_clean()

    driver.save()
    truck.save()
    trip.save()
    return trip

@transaction.atomic
def cancel_trip(trip_id):
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        raise ValidationError("No trip found")

    trip.validate_cancel()
    trip.status =  Trip.TripStatus.CANCELED

    driver = trip.driver
    truck = trip.truck

    driver.mark_available()
    truck.mark_available()

    trip.full_clean()

    driver.save()
    truck.save()
    trip.save()
    return trip

#TRIP STATE MACHINE END --------

