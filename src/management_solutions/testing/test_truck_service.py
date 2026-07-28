import pytest
from management_solutions.service import truck_service
from management_solutions.models  import truck

def test_truck_service_update_truck():
    changes = {}
    changes['make'] = "testing_truck"
    truck_service.update_trucks(1,changes)
    print(truck_service.list_trucks())

def test_truck_service_get_truck():
    truck = truck_service.get_truck(1)
    print(truck_service.list_trucks())
    print(truck)

def test_truck_service_add_truck():
    test_truck = truck.Truck(year=2021,make="testing_truck",mileage=1000)
    truck_service.add_truck(test_truck)

def test_truck_service_update_truckstatus():
    truck_service.change_truck_status(1,"unavailable")
    assert truck_service.get_truck(1).truck_status.value == "unavailable"
    truck_service.change_truck_status(1, "available")
    assert truck_service.get_truck(1).truck_status.value == "available"
    truck_service.change_truck_status(1, "in_service")
    assert truck_service.get_truck(1).truck_status.value == "in_service"
    truck_service.change_truck_status(1, "out_of_service")
    assert truck_service.get_truck(1).truck_status.value == "out_of_service"