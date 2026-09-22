import pytest
from core.models import Truck, Driver, Trip
from tests import factories
from core.services import service_truck
from core.repositories import TruckRepository

@pytest.mark.django_db
def test_add_truck():
    truck = {"year": 2005}
    service_truck.add_truck(truck)

    assert len(TruckRepository.get_all_trucks()) > 0


@pytest.mark.django_db
def test_delete_truck():
    truck = {"year": 2005}
    service_truck.add_truck(truck)
    service_truck.add_truck(truck)
    assert len(TruckRepository.get_all_trucks()) == 2
    service_truck.delete_truck(1)
    assert len(TruckRepository.get_all_trucks()) == 1

@pytest.mark.django_db
def test_update_truck():
    truck = {"year": 2005}
    service_truck.add_truck(truck)
    service_truck.update_truck(1, {"year": 2010})
    assert TruckRepository.get_truck(1).year == 2010

@pytest.mark.django_db
def test_remove_all_drivers():
    truck1 = factories.TruckFactory(year=2005)
    truck2 = factories.TruckFactory()
    driver1 = factories.DriverFactory(truck=truck1)
    driver2 = factories.DriverFactory(truck=truck1)
    driver3 = factories.DriverFactory(truck=truck2)
    service_truck.remove_all_drivers_from_truck(truck1.id)

    driver1.refresh_from_db()
    driver2.refresh_from_db()
    driver3.refresh_from_db()
    assert driver1.truck == None
    assert driver2.truck == None
    assert driver3.truck == truck2




