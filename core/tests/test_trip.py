from datetime import timedelta
from django.utils import timezone
import pytest
from django.core.exceptions import ValidationError

from core.models import Truck, Driver, Trip
from core.tests import factories

@pytest.mark.django_db
def test_validate_complete():
    trip_valid = factories.TripFactory(status=Trip.TripStatus.IN_PROGRESS, departure_time=timezone.now(), arrival_time=timezone.now() + timedelta(hours=1))
    trip_invalid1 = factories.TripFactory(status= Trip.TripStatus.PLANNED)
    trip_invalid2 = factories.TripFactory(status= Trip.TripStatus.CANCELED)
    trip_invalid3 = factories.TripFactory(status= Trip.TripStatus.COMPLETE)
    trip_missing_times = factories.TripFactory(status=Trip.TripStatus.IN_PROGRESS, departure_time=None, arrival_time=None)


    trip_valid.validate_complete()

    with pytest.raises(ValidationError):
        trip_invalid1.validate_complete()
    with pytest.raises(ValidationError):
        trip_invalid2.validate_complete()
    with pytest.raises(ValidationError):
        trip_invalid3.validate_complete()
    with pytest.raises(ValidationError):
        trip_missing_times.validate_complete()


@pytest.mark.django_db
def test_validate_incomplete():
    trip_valid = factories.TripFactory(status=Trip.TripStatus.IN_PROGRESS)
    trip_invalid1 = factories.TripFactory(status=Trip.TripStatus.CANCELED)
    trip_invalid2 = factories.TripFactory(status=Trip.TripStatus.COMPLETE)

    trip_valid.validate_incomplete()
    with pytest.raises(ValidationError):
        trip_invalid1.validate_incomplete()
    with pytest.raises(ValidationError):
        trip_invalid2.validate_incomplete()

@pytest.mark.django_db
def test_validate_cancel():
    trip_valid = factories.TripFactory(status=Trip.TripStatus.PLANNED)
    trip_invalid1 = factories.TripFactory(status=Trip.TripStatus.CANCELED)
    trip_invalid2 = factories.TripFactory(status=Trip.TripStatus.COMPLETE)
    trip_invalid3 = factories.TripFactory(status=Trip.TripStatus.IN_PROGRESS)

    trip_valid.validate_cancel()
    with pytest.raises(ValidationError):
        trip_invalid1.validate_cancel()
    with pytest.raises(ValidationError):
        trip_invalid2.validate_cancel()
    with pytest.raises(ValidationError):
        trip_invalid3.validate_cancel()

@pytest.mark.django_db
def test_mark_in_progress():
    trip = factories.TripFactory(status=Trip.TripStatus.PLANNED)
    trip.mark_in_progress()
    assert trip.status == Trip.TripStatus.IN_PROGRESS

