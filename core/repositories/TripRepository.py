from django.db.models.query import QuerySet

from core.models.trip import Trip

def get_trip(trip_id: int) -> QuerySet | None:
    return Trip.objects.filter(id=trip_id).first()

def get_all_trips() -> QuerySet | None:
    return Trip.objects.all()

def delete_trip(trip_id: int) -> QuerySet | None:
    return Trip.objects.filter(id=trip_id).delete()
