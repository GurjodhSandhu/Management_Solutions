import pytest
from core.models import Driver, Trip, Truck
from core.tests import factories

@pytest.mark.django_db
def test_get_trips():
    driver = factories.DriverFactory()
    trip1 = factories.TripFactory(driver=driver)
    trip2 = factories.TripFactory(driver=driver)
    trip3 = factories.TripFactory(driver=driver)
    trips = driver.get_trips()

    assert len(trips) == 3
    assert trip1 in trips
    assert trip2 in trips
    assert trip3 in trips

@pytest.mark.django_db
def test_get_trips_empty():
    driver = factories.DriverFactory()
    trips = driver.get_trips()
    assert len(trips) == 0

@pytest.mark.django_db
def test_get_trips_active():
    driver = factories.DriverFactory()
    trip1 = factories.TripFactory(driver=driver, status=Trip.TripStatus.PLANNED)
    trip2 = factories.TripFactory(driver=driver, status=Trip.TripStatus.IN_PROGRESS)
    trip3 = factories.TripFactory(driver=driver, status=Trip.TripStatus.IN_PROGRESS)

    trips = driver.get_trips_active()

    assert len(trips) == 2
    assert trip1 not in trips
    assert trip2 in trips
    assert trip3 in trips

@pytest.mark.django_db
def test_get_trips_active_empty():
    driver = factories.DriverFactory()
    trips = driver.get_trips_active()
    assert len(trips) == 0

@pytest.mark.django_db
def test_trips_planned():
    driver = factories.DriverFactory()
    trip1 = factories.TripFactory(driver=driver, status=Trip.TripStatus.PLANNED)
    trip2 = factories.TripFactory(driver=driver, status=Trip.TripStatus.IN_PROGRESS)
    trip3 = factories.TripFactory(driver=driver, status=Trip.TripStatus.IN_PROGRESS)

    trips = driver.get_trips_planned()

    assert len(trips) == 1
    assert trip1 in trips
    assert trip2 not in trips
    assert trip3 not in trips

@pytest.mark.django_db
def test_trips_planned_empty():
    driver = factories.DriverFactory()
    trips = driver.get_trips_planned()
    assert len(trips) == 0


@pytest.mark.django_db
def test_mark_unavailable():
        driver = factories.DriverFactory(driver_status=Driver.DriverStatus.AVAILABLE)
        driver.mark_unavailable()

        assert driver.driver_status == Driver.DriverStatus.UNAVAILABLE


@pytest.mark.django_db
def test_mark_available():
    driver = factories.DriverFactory(driver_status=Driver.DriverStatus.UNAVAILABLE)
    driver.mark_available()

    assert driver.driver_status == Driver.DriverStatus.AVAILABLE



@pytest.mark.django_db
def test_get_trips_does_not_include_other_drivers():
    driver1 = factories.DriverFactory()
    driver2 = factories.DriverFactory()

    trip1 = factories.TripFactory(driver=driver1)
    trip2 = factories.TripFactory(driver=driver2)

    trips = driver1.get_trips()

    assert trip1 in trips
    assert trip2 not in trips

@pytest.mark.django_db
def test_get_trips_active_does_not_include_other_drivers():
    driver1 = factories.DriverFactory()
    driver2 = factories.DriverFactory()

    trip1 = factories.TripFactory(driver=driver1, status=Trip.TripStatus.IN_PROGRESS)
    trip2 = factories.TripFactory(driver=driver2, status=Trip.TripStatus.IN_PROGRESS)

    trips = driver1.get_trips_active()

    assert trip1 in trips
    assert trip2 not in trips

@pytest.mark.django_db
def test_get_trips_planned_does_not_include_other_drivers():
    driver1 = factories.DriverFactory()
    driver2 = factories.DriverFactory()

    trip1 = factories.TripFactory(driver=driver1, status=Trip.TripStatus.PLANNED)
    trip2 = factories.TripFactory(driver=driver2, status=Trip.TripStatus.PLANNED)

    trips = driver1.get_trips_planned()

    assert trip1 in trips
    assert trip2 not in trips

