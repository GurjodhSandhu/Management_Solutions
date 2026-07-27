import pytest
from management_solutions.service import truck_service


def test_driver_service_update_driver():
    changes = {}
    changes['make'] = "testing_truck"
    truck_service.update_trucks(1,changes)
    print(truck_service.list_trucks())