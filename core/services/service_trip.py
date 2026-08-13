from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Model
from core.repositories import TripRepository

from core.models import Trip,Driver,Truck
from models import Driver, Truck

def new_trip(data):
    new_trip = Trip(**data)
    new_trip.full_clean()
    new_trip.save()
    return new_trip

@transaction.atomic
def start_trip(trip_id):
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        raise ValidationError("No trip found")

    trip.validate_start()
    trip.start()
    driver = trip.driver
    truck = trip.truck
    driver.mark_unavailable()
    truck.mark_unavailable()

    truck.full_clean()
    trip.full_clean()

    driver.save()
    truck.save()
    trip.save()
    return trip

def validate_planned_time(trip_id):
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        raise ValidationError("No trip found")
    driver = trip.driver
    if driver is None:
        raise ValidationError("No driver found")
    for planned_trip in driver.get_trips_planned():
       if planned_trip.id == trip_id:
           continue
       if planned_trip.departure_time < trip.arrival_time and planned_trip.arrival_time > trip.departure_time:
           raise ValidationError("driver has conflicting trip planned")

    return trip


def complete_trip(trip_id):
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        return None
    trip.status = trip.TripStatus.COMPLETE
    trip.full_clean()
    trip.save()
    return trip

def incomplete_trip(trip_id):
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        return None
    trip.status = trip.TripStatus.INCOMPLETE
    trip.full_clean()
    trip.save()
    return trip

def cancel_trip(trip_id):
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        return None
    trip.status = "canceled"
    trip.full_clean()
    trip.save()
    return trip

def update_trip(trip_id,data):
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        return None
    for key,value in data.items():
        setattr(trip,key,value)
    trip.full_clean()
    trip.save()
    return trip

def delete_trip(trip_id):
    delete_trip(trip_id)

def validate_trip_information():
    #validation rules here
    return True

def assign_driver_to_trip(trip_id,driver_id):
    trip = TripRepository.get_trip(trip_id)
    driver = Driver.objects.filter(id=driver_id).first()
    if driver is None:
        raise ValidationError("No driver found")
    if trip is None:
        raise ValidationError("No trip found")
    validate_planned_time(trip_id)
    trip.driver_id = driver_id
    trip.full_clean()
    trip.save()

    return trip