from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Model
from core.repositories import TripRepository

from core.models import Trip,Driver,Truck


def new_trip(data):
    new_trip = Trip(**data)
    new_trip.full_clean()
    new_trip.save()
    return new_trip

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
    trip.validate_planned_time()
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

    driver = trip.driver
    truck = driver.truck
    driver.mark_unavailable()
    truck.mark_unavailable()

    truck.full_clean()
    trip.full_clean()

    driver.save()
    truck.save()
    trip.save()
    #todo add logic to update departure time
    return trip

@transaction.atomic
def complete_trip(trip_id):
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        raise ValidationError("No trip found")

    trip.validate_complete()
    trip.status = trip.TripStatus.COMPLETE
    driver = trip.driver
    truck = driver.truck

    driver.mark_available()
    truck.mark_available()

    truck.full_clean()
    trip.full_clean()

    driver.save()
    truck.save()
    trip.save()

    #todo add logic to update arrival time
    return trip

@transaction.atomic
def incomplete_trip(trip_id):
    trip = TripRepository.get_trip(trip_id)
    if trip is None:
        raise ValidationError("No trip found")

    trip.validate_incomplete()
    trip.status = trip.TripStatus.INCOMPLETE

    driver = trip.driver
    truck = driver.truck

    driver.mark_available()
    truck.mark_available()

    trip.full_clean()
    truck.full_clean()

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
    truck = driver.truck

    driver.mark_available()
    truck.mark_available()

    trip.full_clean()
    truck.full_clean()

    driver.save()
    truck.save()
    trip.save()
    return trip

#TRIP STATE MACHINE END --------

