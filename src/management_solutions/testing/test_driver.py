import pytest
from pydantic import ValidationError
from management_solutions.models.driver import Driver

def test_driver_valid():
    driver = Driver(driver_id=1,driver_name="gurjodh",driver_licensenumber="123404",assigned_truck_id=12)
    assert driver.driver_id == 1
    assert driver.driver_name == "gurjodh"
    assert driver.driver_licensenumber == "123404"
    assert driver.assigned_truck_id == 12

def test_driver_invalid_name():
    with pytest.raises(ValidationError):
        Driver(driver_id=1, driver_name=123, driver_licensenumber="123404", assigned_truck_id=12)

def test_driver_invalid_licensenumber():
    with pytest.raises(ValidationError):
        Driver(driver_id=1,driver_name="gurjodh",driver_licensenumber="12",assigned_truck_id=12)
