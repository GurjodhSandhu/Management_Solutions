import pytest
from management_solutions.service import driver_service
from management_solutions.models.driver import Driver

def test_driver_service_update_driver():
    changes = {}
    changes['driver_name'] = "updated name"
    driver_service.update_drivers(1,changes)
    assert driver_service.get_driver(1).driver_name == "updated name"

def test_driver_dervice_add_driver():
    driver = Driver(driver_name="test driver",driver_licensenumber="12345")
    driver_service.add_driver(driver)

def test_driver_service_get_driver():
    driver_service.get_driver(1)
    print(driver_service.list_drivers())
