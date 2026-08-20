import pytest
from core.models import Truck, Driver, Trip
from core.tests import factories


@pytest.mark.django_db
def test_truck_mark_available():
    truck = factories.TruckFactory(truck_status = Truck.TruckStatus.UNAVAILABLE)
    truck.mark_available()

    assert truck.truck_status == Truck.TruckStatus.AVAILABLE

@pytest.mark.django_db
def test_truck_mark_unavailable():
    truck = factories.TruckFactory(truck_status=Truck.TruckStatus.AVAILABLE)
    truck.mark_unavailable()

    assert truck.truck_status == Truck.TruckStatus.UNAVAILABLE

@pytest.mark.django_db
def test_truck_mark_in_repair():
    truck = factories.TruckFactory(truck_status=Truck.TruckStatus.AVAILABLE)
    truck.mark_in_repair()

    assert truck.truck_status == Truck.TruckStatus.IN_REPAIR

@pytest.mark.django_db
def test_truck_mark_out_of_service():
    truck = factories.TruckFactory(truck_status=Truck.TruckStatus.AVAILABLE)
    truck.mark_out_of_service()

    assert truck.truck_status == Truck.TruckStatus.OUT_OF_SERVICE

@pytest.mark.django_db
def test_get_drivers():
    truck = factories.TruckFactory()

    d1 = factories.DriverFactory(truck=truck)
    d2 = factories.DriverFactory(truck=truck)
    d3 = factories.DriverFactory(truck=truck)

    drivers = truck.get_drivers()
    assert len(drivers) == 3
    assert d1 in drivers
    assert d2 in drivers
    assert d3 in drivers

@pytest.mark.django_db
def test_get_drivers_empty():
    truck = factories.TruckFactory()
    drivers = truck.get_drivers()
    assert len(drivers) == 0


@pytest.mark.django_db
def test_get_trips_active():
    truck = factories.TruckFactory()
    trip1 = factories.TripFactory(truck=truck, status = Trip.TripStatus.IN_PROGRESS)
    trip2 = factories.TripFactory(truck=truck)

    active_trips = truck.get_trips_active()
    assert trip1 in active_trips
    assert trip2 not in active_trips

@pytest.mark.django_db
def test_get_trips_active_empty():
    truck = factories.TruckFactory()
    trip1 = factories.TripFactory(truck=truck)
    trip2 = factories.TripFactory(truck=truck)
    active_trips = truck.get_trips_active()
    assert len(active_trips) == 0


@pytest.mark.django_db
def test_get_trips_all():
    truck = factories.TruckFactory()
    trip1 = factories.TripFactory(truck=truck)
    trip2 = factories.TripFactory(truck=truck)
    trip3 = factories.TripFactory(truck=truck)
    trips = truck.get_all_trips()

    assert len(trips) == 3
    assert trip1 in trips
    assert trip2 in trips
    assert trip3 in trips

@pytest.mark.django_db
def test_get_trips_all_empty():
    truck = factories.TruckFactory()
    trips = truck.get_all_trips()
    assert len(trips) == 0

@pytest.mark.django_db
def test_get_trips_does_not_include_other_trucks():
    truck1 = factories.TruckFactory()
    truck2 = factories.TruckFactory()

    trip1 = factories.TripFactory(truck=truck1)
    trip2 = factories.TripFactory(truck=truck2)

    trips = truck1.get_all_trips()

    assert trip1 in trips
    assert trip2 not in trips

@pytest.mark.django_db
def test_get_trips_active_does_not_include_other_trucks():
    truck1 = factories.TruckFactory()
    truck2 = factories.TruckFactory()
    trip1 = factories.TripFactory(truck=truck1, status = Trip.TripStatus.IN_PROGRESS)
    trip2 = factories.TripFactory(truck=truck2, status = Trip.TripStatus.IN_PROGRESS)

    trips = truck1.get_trips_active()

    assert trip1 in trips
    assert trip2 not in trips