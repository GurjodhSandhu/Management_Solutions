import pytest
from django.core.exceptions import ValidationError
from core.tests import factories
from core.models import Trip,Truck,Driver
from core.services import service_trip
from datetime import datetime
from django.utils import timezone



@pytest.mark.django_db
def test_start_trip_valid():
    driver = factories.DriverFactory()
    truck = factories.TruckFactory()

    trip = factories.TripFactory(driver=driver,truck=truck,)
    service_trip.start_trip(trip.id)

    assert Trip.objects.get(id=trip.id).status == Trip.TripStatus.IN_PROGRESS
    assert Trip.objects.get(id=trip.id).driver == driver
    assert Trip.objects.get(id=trip.id).truck == truck

@pytest.mark.django_db
def test_start_trip_valid_datetime():
    driver = factories.DriverFactory()
    truck = factories.TruckFactory()

    trip = factories.TripFactory(driver=driver, truck=truck,
                                 departure_time=timezone.make_aware(datetime(2026,1,1)),
                                 arrival_time=timezone.make_aware(datetime(2026,1,2)))
    service_trip.start_trip(trip.id)

    assert Trip.objects.get(id=trip.id).status == Trip.TripStatus.IN_PROGRESS
    assert Trip.objects.get(id=trip.id).departure_time.date() == timezone.now().date()
    assert Trip.objects.get(id=trip.id).arrival_time == timezone.make_aware(datetime(2026,1,2))

@pytest.mark.django_db
def test_start_trip_invalid_missing_truck_driver():
    driver = factories.DriverFactory()
    truck = factories.TruckFactory()

    trip1 = factories.TripFactory(truck=truck)
    trip2 = factories.TripFactory(driver=driver)
    trip3 = factories.TripFactory(truck=truck,driver=driver)
    with pytest.raises(ValidationError):
        service_trip.start_trip(trip1.id)
    with pytest.raises(ValidationError):
        service_trip.start_trip(trip2.id)

    service_trip.start_trip(trip3.id)
    assert Trip.objects.get(id=trip3.id).status == Trip.TripStatus.IN_PROGRESS

@pytest.mark.django_db
def test_start_trip_invalid_unavailable_truck():
    driver = factories.DriverFactory()
    truck = factories.TruckFactory(truck_status=Truck.TruckStatus.UNAVAILABLE)
    trip3 = factories.TripFactory(truck=truck,driver=driver)
    with pytest.raises(ValidationError):
        service_trip.start_trip(trip3.id)

    truck.truck_status = Truck.TruckStatus.AVAILABLE
    truck.save()
    service_trip.start_trip(trip3.id)
    assert Trip.objects.get(id=trip3.id).status == Trip.TripStatus.IN_PROGRESS

@pytest.mark.django_db
def test_start_trip_invalid_unavailable_driver():
    driver = factories.DriverFactory(driver_status=Driver.DriverStatus.UNAVAILABLE)
    truck = factories.TruckFactory()
    trip3 = factories.TripFactory(truck=truck,driver=driver)
    with pytest.raises(ValidationError):
        service_trip.start_trip(trip3.id)

    driver.driver_status = Driver.DriverStatus.AVAILABLE
    driver.save()
    service_trip.start_trip(trip3.id)
    assert Trip.objects.get(id=trip3.id).status == Trip.TripStatus.IN_PROGRESS

@pytest.mark.django_db
def test_start_trip_invalid_not_planned_state():
    driver = factories.DriverFactory()
    truck = factories.TruckFactory()
    trip = factories.TripFactory(truck=truck,driver=driver,status=Trip.TripStatus.COMPLETE)
    trip2 = factories.TripFactory(truck=truck,driver=driver,status=Trip.TripStatus.IN_PROGRESS)
    trip3 = factories.TripFactory(truck=truck,driver=driver,status=Trip.TripStatus.CANCELED)

    with pytest.raises(ValidationError):
        service_trip.start_trip(trip.id)
    with pytest.raises(ValidationError):
        service_trip.start_trip(trip2.id)
    with pytest.raises(ValidationError):
        service_trip.start_trip(trip3.id)

@pytest.mark.django_db
def test_start_trip_invalid_truck_driver_ontrip():
    driver = factories.DriverFactory()
    truck = factories.TruckFactory()
    trip = factories.TripFactory(truck=truck,driver=driver,status=Trip.TripStatus.IN_PROGRESS)
    trip2 = factories.TripFactory(truck=factories.TruckFactory(),driver=driver)
    trip3 = factories.TripFactory(truck=truck,driver=factories.DriverFactory())

    with pytest.raises(ValidationError) as e1:
        service_trip.start_trip(trip2.id)
    assert "Driver already has an active trip" in str(e1.value)

    with pytest.raises(ValidationError)as e2:
        service_trip.start_trip(trip3.id)
    assert "Truck already has an active trip" in str(e2.value)


#complete state test
@pytest.mark.django_db
def test_complete_trip_valid():
    driver = factories.DriverFactory()
    truck = factories.TruckFactory()
    trip = factories.TripFactory(truck=truck,driver=driver)

    service_trip.start_trip(trip.id)
    service_trip.complete_trip(trip.id)

    driver.refresh_from_db()
    truck.refresh_from_db()
    assert Trip.objects.get(id=trip.id).status == Trip.TripStatus.COMPLETE
    assert driver.driver_status == Driver.DriverStatus.AVAILABLE
    assert truck.truck_status == Truck.TruckStatus.AVAILABLE

@pytest.mark.django_db
def test_complete_trip_invalid_not_started():
    driver = factories.DriverFactory()
    truck = factories.TruckFactory()
    trip = factories.TripFactory(truck=truck, driver=driver)

    with pytest.raises(ValidationError) as e1:
        service_trip.complete_trip(trip.id)
    assert "The trip must be started to end it" in str(e1.value)

#incomplete state test
@pytest.mark.django_db
def test_incomplete_trip_valid():
    driver = factories.DriverFactory()
    truck = factories.TruckFactory()
    trip = factories.TripFactory(truck=truck,driver=driver)
    service_trip.start_trip(trip.id)

    service_trip.incomplete_trip(trip.id)
    assert Trip.objects.get(id=trip.id).status == Trip.TripStatus.INCOMPLETE
    assert driver.driver_status == Driver.DriverStatus.AVAILABLE
    assert truck.truck_status == Truck.TruckStatus.AVAILABLE

@pytest.mark.django_db
def test_incomplete_trip_invalid():
    driver = factories.DriverFactory()
    truck = factories.TruckFactory()
    trip = factories.TripFactory(truck=truck,driver=driver,status=Trip.TripStatus.COMPLETE)
    trip2 = factories.TripFactory(truck=factories.TruckFactory(),driver=driver,status=Trip.TripStatus.CANCELED)

    with pytest.raises(ValidationError) as e1:
        service_trip.incomplete_trip(trip.id)
    assert "The trip was already completed" in str(e1.value)

    with pytest.raises(ValidationError) as e2:
        service_trip.incomplete_trip(trip2.id)
    assert "The trip was already Canceled" in str(e2.value)

#cancels state test

@pytest.mark.django_db
def test_canceled_trip_valid():
    driver = factories.DriverFactory()
    truck = factories.TruckFactory()
    trip = factories.TripFactory(truck=truck,driver=driver)

    service_trip.cancel_trip(trip.id)
    assert Trip.objects.get(id=trip.id).status == Trip.TripStatus.CANCELED

@pytest.mark.django_db
def test_canceled_trip_invalid():
    driver = factories.DriverFactory()
    truck = factories.TruckFactory()
    trip = factories.TripFactory(truck=truck,driver=driver,status=Trip.TripStatus.COMPLETE)
    trip2 = factories.TripFactory(truck=factories.TruckFactory(),driver=driver,status=Trip.TripStatus.IN_PROGRESS)

    with pytest.raises(ValidationError) as e1:
        service_trip.cancel_trip(trip.id)
    assert "The trip was already completed" in str(e1.value)

    with pytest.raises(ValidationError) as e2:
        service_trip.cancel_trip(trip2.id)
    assert "only planned trips can be cancelled" in str(e2.value)