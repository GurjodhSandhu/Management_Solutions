from core.models.trip import Trip

def get_trip(trip_id):
    return Trip.objects.filter(id=trip_id).first()

def get_all_trips():
    return Trip.objects.all()

def delete_trip(trip_id):
    return Trip.objects.filter(id=trip_id).delete()
