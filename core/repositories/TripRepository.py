from core.models.trip import Trip

def get_trip(trip_id):
    return Trip.objects.filter(trip_id=trip_id).first()

def delete_trip(trip_id):
    return Trip.objects.filter(id=trip_id).delete()
