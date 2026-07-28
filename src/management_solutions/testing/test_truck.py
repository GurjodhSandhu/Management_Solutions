import pytest
from management_solutions.models.truck import Truck
from pydantic import ValidationError

def test_truck_valid():
    truck = Truck(truck_id=1,vin="1FTFW1EF1EKF51234",brand="Ford",make="F-150",
                  year=2020,mileage=150000,plate="ABC1234",assigned_driver_id=1)
    assert truck.truck_id == 1
    assert truck.vin == "1FTFW1EF1EKF51234"
    assert truck.brand == "Ford"
    assert truck.make == "F-150"
    assert truck.year == 2020
    assert truck.mileage == 150000
    assert truck.plate == "ABC1234"
    assert truck.assigned_driver_id == 1

def test_truck_invalid_vintype():
    with pytest.raises(ValidationError):
        Truck(vin=123)

def test_truck_invalid_vinlength():
    with pytest.raises(ValidationError):
        Truck(vin="123")

def test_truck_invalid_brand():
    with pytest.raises(ValidationError):
        Truck(brand="")
    with pytest.raises(ValidationError):
        Truck(brand=123)

def test_truck_invalid_make():
    with pytest.raises(ValidationError):
        Truck(make="")
    with pytest.raises(ValidationError):
        Truck(make=123)

def test_truck_invalid_year_type():
    with pytest.raises(ValidationError):
        Truck(year="string")

def test_truck_invalid_year_tolow():
    with pytest.raises(ValidationError):
        Truck(year=123)

def test_truck_invalid_year_tohigh():
    with pytest.raises(ValidationError):
        Truck(year=3000)

def test_truck_invalid_mileage_type():
    with pytest.raises(ValidationError):
        Truck(mileage="a")

def test_truck_invalid_mileage_negative():
    with pytest.raises(ValidationError):
        Truck(mileage=-1)

def test_truck_invalid_plate_type():
    with pytest.raises(ValidationError):
        Truck(plate=123456)

def test_truck_invalid_plate_length():
    with pytest.raises(ValidationError):
        Truck(plate="abc123qwe4234fsdf234aaaa")

def test_truck_valid_status():
    Truck(truck_status="available")
    Truck(truck_status="unavailable")
    Truck(truck_location="on_route")

def test_truck_invalid_status():
    with pytest.raises(ValidationError):
        Truck(truck_location="On_route")
        Truck(truck_status="avaailble")