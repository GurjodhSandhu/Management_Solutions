from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from rest_framework import status

from core.tests import factories
from core.models import Trip
from core.services import service_trip
from datetime import datetime,timezone

#service trip update
@pytest.mark.django_db
def test_update_trip_datatime():
    trip = factories.TripFactory(start="vancouver",end="calgary",departure_time=datetime(2026,1,1,tzinfo=timezone.utc), arrival_time=datetime(2026,1,2, tzinfo=timezone.utc))

    service_trip.update_trip(trip.id,{"start": "chilliwack","arrival_time": datetime(2026,1,3,tzinfo=timezone.utc)})
    trip.refresh_from_db()
    assert trip.arrival_time == datetime(2026,1,3,tzinfo=timezone.utc)
    assert trip.start == "chilliwack"

@pytest.mark.django_db
def test_update_planned_trip():
    # Create a PLANNED trip
    trip = factories.TripFactory(
        start="Vancouver",
        end="Calgary",
        departure_time=datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc),
        arrival_time=datetime(2026, 1, 1, 18, 0, tzinfo=timezone.utc),
        status=Trip.TripStatus.PLANNED,
        planned_miles=600,
        actual_miles=0,
        loaded_miles=0,
        empty_miles=0,
        cpm=Decimal("0.4"),
        pay=Decimal("840.00"),
    )

    update_data = {
        "start": "Abbotsford",
        "end": "Edmonton",
        "departure_time": "2026-01-02T07:30:00",
        "arrival_time": "2026-01-02T20:45:00",
        "planned_miles": 720,
        "actual_miles": 10,
        "loaded_miles": 5,
        "empty_miles": 5,
        "cpm": Decimal("1.55"),
        "pay": Decimal("1116.00"),
    }

    updated = service_trip.update_trip(trip.id, update_data)

    # Assertions
    assert updated.start == "Abbotsford"
    assert updated.end == "Edmonton"

    # Datetime fields should be aware
    assert updated.departure_time == datetime(2026,1,2,7,30,tzinfo=timezone.utc)

    assert updated.arrival_time == datetime(2026,1,2,20,45,tzinfo=timezone.utc)


    assert updated.planned_miles == 720
    assert updated.actual_miles == 10
    assert updated.loaded_miles == 5
    assert updated.empty_miles == 5
    assert updated.cpm == Decimal("1.55")
    assert updated.pay == Decimal("1116.00")

@pytest.mark.django_db
def test_update_other_trip():
    # Create a COMPLETED trip
    trip = factories.TripFactory(
        start="Vancouver",
        end="Calgary",
        departure_time=datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc),
        arrival_time=datetime(2026, 1, 1, 18, 0, tzinfo=timezone.utc),
        status=Trip.TripStatus.COMPLETE,
        planned_miles=600,
        actual_miles=100,
        loaded_miles=80,
        empty_miles=20,
        cpm=Decimal("1.40"),
        pay=Decimal("840.00"),
    )

    update_data = {
        # Allowed fields
        "actual_miles": 150,
        "loaded_miles": 120,
        "empty_miles": 30,
        "cpm": Decimal("1.55"),
        "pay": Decimal("1116.00"),

        # Disallowed fields
        "start": "Abbotsford",
        "end": "Edmonton",
        "arrival_time": "2026-01-02T20:45:00",
        "departure_time": "2026-01-02T07:30:00",
        "planned_miles": 720,
        "driver": 999,
        "truck": 999,
    }

    updated = service_trip.update_trip(trip.id, update_data)

    # Allowed updates
    assert updated.actual_miles == 150
    assert updated.loaded_miles == 120
    assert updated.empty_miles == 30
    assert updated.cpm == Decimal("1.55")
    assert updated.pay == Decimal("1116.00")

    # Disallowed updates should NOT change
    assert updated.start == "Vancouver"
    assert updated.end == "Calgary"
    assert updated.arrival_time == datetime(2026, 1, 1, 18, 0, tzinfo=timezone.utc)
    assert updated.departure_time == datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc)
    assert updated.planned_miles == 600

@pytest.mark.django_db
def test_update_trip_driver_nonexistent():
    trip = factories.TripFactory()

    with pytest.raises(ValidationError):
        service_trip.assign_driver_to_trip(trip.id,999999)

@pytest.mark.django_db
def test_assign_trip_truck_nonexistent():
    trip = factories.TripFactory()
    with pytest.raises(ValidationError):
        service_trip.assign_truck_to_trip(trip.id,9999999)

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

@pytest.mark.django_db
def test_delete_trip():
    trip = factories.TripFactory()
    trip2 = factories.TripFactory()
    service_trip.delete_trip(trip.id)
    assert Trip.objects.filter(id=trip.id).first() is None
    assert Trip.objects.filter(id=trip2.id).first() == trip2 #check for side effect - deleting other trips