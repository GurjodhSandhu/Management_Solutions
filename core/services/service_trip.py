from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Model

from core.models import Trip,Driver,Truck

def new_trip(data):
    new_trip = Trip(**data)
    new_trip.full_clean()
    new_trip.save()
    return new_trip

@transaction.atomic
def start_trip(trip_id):

    trip = Trip.objects.filter(id=trip_id).first()
    if trip is None:
        return None

    driver = trip.driver
    if driver is None:
        raise ValidationError("No driver found")

    truck = driver.truck
    if truck is None:
        raise ValidationError("Driver is not assigned a truck")

    if driver.driver_status == Driver.DriverStatus.UNAVAILABLE:
        raise ValidationError("driver unavailable")
    if driver.get_trips_active().exclude(id=trip.id).first() is not None:
        raise ValidationError("Driver already has an active trip")

    driver.validate_truck() #make sure truck is correctly setup

    trip.status = Trip.TripStatus.IN_PROGRESS
    driver.driver_status = Driver.DriverStatus.UNAVAILABLE
    truck.truck_status = truck.TruckStatus.UNAVAILABLE

    truck.full_clean()
    trip.full_clean()

    truck.save()
    driver.save()
    trip.save()
    return trip

def validate_planned_time(trip_id):
    trip = Trip.objects.filter(id=trip_id).first()
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
    trip = Trip.objects.filter(id=trip_id).first()
    if trip is None:
        return None
    trip.status = trip.TripStatus.COMPLETE
    trip.full_clean()
    trip.save()
    return trip

def incomplete_trip(trip_id):
    trip = Trip.objects.filter(id=trip_id).first()
    if trip is None:
        return None
    trip.status = trip.TripStatus.INCOMPLETE
    trip.full_clean()
    trip.save()
    return trip

def cancel_trip(trip_id):
    trip = Trip.objects.filter(id=trip_id).first()
    if trip is None:
        return None
    trip.status = "canceled"
    trip.full_clean()
    trip.save()
    return trip

def update_trip(trip_id,data):
    trip = Trip.objects.filter(id=trip_id).first()
    if trip is None:
        return None
    for key,value in data.items():
        setattr(trip,key,value)
    trip.full_clean()
    trip.save()
    return trip

def delete_trip(trip_id):
    Trip.objects.filter(id=trip_id).delete()

def validate_trip_information():
    #validation rules here
    return True

def assign_driver_to_trip(trip_id,driver_id):
    trip = Trip.objects.filter(id=trip_id).first() #get trip
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