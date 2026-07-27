import pytest
from management_solutions.service import truck_driver_service
from management_solutions.service import driver_service
from management_solutions.service import truck_service

def test_truck_driver_service():
    truck_driver_service.assign_driver_to_truck(1,1)
    assert truck_service.get_truck(1).assigned_driver_id == 1
    assert driver_service.get_driver(1).assigned_truck_id == 1

def test_clear_driver_truck():
    truck_driver_service.clear_driver_assigned_truck(1)
    truck_driver_service.clear_driver_assigned_truck(1) #repeated to check if it works on an empty location
    truck_driver_service.clear_truck_assigned_driver(1)
    truck_driver_service.clear_truck_assigned_driver(1)
    assert truck_service.get_truck(1).assigned_driver_id == None
    assert driver_service.get_driver(1).assigned_truck_id == None