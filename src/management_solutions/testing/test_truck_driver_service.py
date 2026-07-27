import pytest
from management_solutions.service import truck_driver_service
from management_solutions.service import driver_service
from management_solutions.service import truck_service

def test_truck_driver_service():
    truck_driver_service.assign_driver_to_truck(1,1)
    print(truck_service.list_trucks())
    print(driver_service.list_drivers())