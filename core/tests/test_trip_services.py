import pytest
from django.core.exceptions import ValidationError

from core.tests import factories
from core.models import Trip
from core.services import service_trip
from datetime import datetime,timezone

@pytest.mark.django_db
def test_update_trip_datatime():
    trip = factories.TripFactory(start="vancouver",end="calgary",departure_time=datetime(2026,1,1,tzinfo=timezone.utc), arrival_time=datetime(2026,1,2, tzinfo=timezone.utc))

    service_trip.update_trip(trip.id,{"start": "chilliwack","arrival_time": datetime(2026,1,3,tzinfo=timezone.utc)})
    trip.refresh_from_db()
    assert trip.arrival_time == datetime(2026,1,3,tzinfo=timezone.utc)
    assert trip.start == "chilliwack"

@pytest.mark.django_db
def test_update_trip_truck_driver():
    driver = factories.DriverFactory()
    truck = factories.TruckFactory()
    trip = factories.TripFactory(start="vancouver",end="calgary")

    service_trip.update_trip(trip.id,{"driver": driver.id,"truck": truck.id})
    trip.refresh_from_db()
    assert trip.driver == driver
    assert trip.truck == truck

@pytest.mark.django_db
def test_update_trip_driver_nonexistent():
    trip = factories.TripFactory()

    with pytest.raises(ValidationError):
        service_trip.update_trip(trip.id,{"driver": 100})

@pytest.mark.django_db
def test_update_trip_truck_nonexistent():
    trip = factories.TripFactory()
    with pytest.raises(ValidationError):
        service_trip.update_trip(trip.id,{"truck": 100})

@pytest.mark.django_db
def test_delete_trip():
    trip = factories.TripFactory()
    trip2 = factories.TripFactory()
    service_trip.delete_trip(trip.id)
    assert Trip.objects.filter(id=trip.id).first() is None
    assert Trip.objects.filter(id=trip2.id).first() == trip2 #check for side effect - deleting other trips

@pytest.mark.django_db
def test_assign_driver_to_trip():
    trip = factories.TripFactory()
    driver = factories.DriverFactory()

    service_trip.assign_driver_to_trip(trip.id,driver.id)
    trip.refresh_from_db()

    assert trip.driver == driver

@pytest.mark.django_db
def test_assign_truck_to_trip():
    trip = factories.TripFactory()
    truck = factories.TruckFactory()

    service_trip.assign_truck_to_trip(trip.id,truck.id)
    trip.refresh_from_db()

    assert trip.truck == truck
