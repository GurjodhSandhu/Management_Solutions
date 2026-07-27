import pytest
from management_solutions.service import driver_service


def test_driver_service_update_driver():
    changes = {}
    changes['driver_name'] = "updated name"
    driver_service.update_drivers(1,changes)
    print(driver_service.list_drivers())