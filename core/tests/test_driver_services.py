from django.core.exceptions import ValidationError

from core.tests import factories
import pytest
from core.services import service_driver
from core.repositories import DriverRepository
from core.models import Truck, Driver, Trip


@pytest.mark.django_db
def test_add_driver():
    service_driver.add_driver({"driver_name": "bob"})

    assert DriverRepository.get_driver(1).driver_name == "bob"

@pytest.mark.django_db
def test_update_driver():
    driver = factories.DriverFactory(driver_name="bob")
    service_driver.update_driver(driver.id,{"driver_name": "greg"})
    driver.refresh_from_db()
    assert driver.driver_name == "greg"

@pytest.mark.django_db
def test_assign_truck_to_driver():
    driver = factories.DriverFactory(driver_name="bob")
    truck = factories.TruckFactory(year=2005)
    service_driver.assign_truck_to_driver(driver.id,truck.id)

    driver.refresh_from_db()
    truck.refresh_from_db()

    assert driver.truck == truck
    assert driver in truck.drivers.all()

@pytest.mark.django_db
def test_assign_truck_to_driver_invalid_preassigned_truck():
    driver = factories.DriverFactory(driver_name="bob", truck=factories.TruckFactory())
    truck = factories.TruckFactory(year=2005)

    with pytest.raises(ValidationError):
        service_driver.assign_truck_to_driver(driver.id,truck.id)


@pytest.mark.django_db
def test_assign_truck_to_driver_invalid_active_trip():
    truck = factories.TruckFactory(year=2005)
    driver = factories.DriverFactory(driver_name="bob")
    trips = factories.TripFactory(status=Trip.TripStatus.IN_PROGRESS)
    driver.trips.add(trips)
    with pytest.raises(ValidationError):
        service_driver.assign_truck_to_driver(driver.id, truck.id)

@pytest.mark.django_db
def test_remove_driver_from_truck():
    driver = factories.DriverFactory(driver_name="bob")
    truck = factories.TruckFactory(year=2005)
    driver.truck = truck
    service_driver.remove_truck_from_driver(driver.id)
    driver.refresh_from_db()
    assert driver.truck != truck

@pytest.mark.django_db
def test_remove_driver_from_truck_invalid():
    driver = factories.DriverFactory(driver_name="bob")
    truck = factories.TruckFactory(year=2005)
    factories.TripFactory(driver=driver, status=Trip.TripStatus.IN_PROGRESS)
    driver.truck = truck

    with pytest.raises(ValidationError):
        service_driver.remove_truck_from_driver(driver.id)
