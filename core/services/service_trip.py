from core.models import Trip,Driver

def new_trip(data):
    new_trip = Trip(**data)
    new_trip.full_clean()
    new_trip.save()
    return new_trip

def start_trip(trip_id):
    trip = Trip.objects.filter(id=trip_id).first()
    if trip is None:
        return None
    trip.status = "inprogress"
    trip.full_clean()
    trip.save()
    return trip

def complete_trip(trip_id):
    trip = Trip.objects.filter(id=trip_id).first()
    if trip is None:
        return None
    trip.status = "completed"
    trip.full_clean()
    trip.save()
    return trip

def incomplete_trip(trip_id):
    trip = Trip.objects.filter(id=trip_id).first()
    if trip is None:
        return None
    trip.status = "incomplete"
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
    if Driver.objects.filter(id=driver_id).exists(): #if driver exists
        #more validation rules if driver is valid for the trip i.e check status
        trip.driver_id = driver_id
        trip.full_clean()
        trip.save()

    return trip