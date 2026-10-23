import pytest
from core.models import Truck,Trip
from django.forms.models import model_to_dict

bad_payload = [
    ({"vin": "short", "year": 2020, "mileage": 200}, "vin"),
    ({"vin": "1HGCM82633A004353", "year": 1800, "mileage": 300}, "year"),
    ({"vin": "1HGCM82633A004354", "year": "1m", "mileage": 400}, "year"),
    ({"vin": "1HGCM82633A004355", "year": 2020, "mileage": -5}, "mileage"),
]
bad_ids = ["bad-vin","bad-year-too-low","bad-year-not-int","bad-mileage-negative"]
def test_add_truck(admin_client):
    res = admin_client.post("/api/trucks/",{"vin":"1HGCM82633A004352", "mileage":100}, format='json')
    assert res.status_code == 201
    assert res.data["vin"] == "1HGCM82633A004352"
    assert res.data["mileage"] == 100
    truck_id = res.data["id"]
    assert Truck.objects.filter(id=truck_id).exists()
    assert res.data["truck_status"] == Truck.TruckStatus.AVAILABLE

@pytest.mark.parametrize("payload, bad_field",bad_payload, ids= bad_ids)
def test_add_truck_with_bad_field(admin_client, payload, bad_field):
    res = admin_client.post("/api/trucks/", payload, format='json')
    assert res.status_code == 400
    assert bad_field in res.data, res.data
    assert Truck.objects.count() == 0

@pytest.mark.parametrize("payload, field", [
    ({"mileage": 1500}, "mileage"),
    ({"vin": "5FRTM82123A004352"}, "vin"),
    ({ "year": 2001}, "year"),
    ({"brand": "Volvo"}, "brand"),
], ids=["update-mileage",
    "update-vin",
    "update-year",
    "update-brand",
     ] )
def test_update_truck(admin_client,payload,field):
    truck = Truck.objects.create(vin="1HGCM82633A004352", mileage=100)
    before = model_to_dict(truck)
    res = admin_client.patch(f"/api/trucks/{truck.id}/",payload, format="json")
    assert res.status_code == 200
    assert res.data[field] == payload[field]
    truck.refresh_from_db()
    after = model_to_dict(truck)
    expected = {**before, field: payload[field]}
    assert after == expected

@pytest.mark.parametrize("payload, bad_field",bad_payload,ids = bad_ids)
def test_update_truck_with_bad_field(admin_client, payload, bad_field):
    truck = Truck.objects.create(vin="1HGCM82633A004352", mileage=100)
    before = model_to_dict(truck)
    res = admin_client.patch(f"/api/trucks/{truck.id}/",payload, format='json')
    assert res.status_code == 400
    assert bad_field in res.data, res.data
    truck.refresh_from_db()
    after = model_to_dict(truck)
    assert before == after

def test_delete_truck(admin_client):
    truck = Truck.objects.create(vin="1HGCM82633A004888", mileage=500)
    res = admin_client.delete(f"/api/trucks/{truck.id}/")
    assert res.status_code == 204
    assert not Truck.objects.filter(id=truck.id).exists()
    assert admin_client.get(f"/api/trucks/{truck.id}/").status_code == 404

def test_delete_truck_nonexistent(admin_client):
    truck = Truck.objects.create()
    truck_id = truck.id
    truck.delete()
    res = admin_client.delete(f"/api/trucks/{truck_id}/")
    assert res.status_code == 404
    assert not Truck.objects.filter(id=truck_id).exists()

def test_delete_truck_active(admin_client):
    truck = Truck.objects.create()
    Trip.objects.create(truck=truck, status=Trip.TripStatus.IN_PROGRESS)
    res = admin_client.delete(f"/api/trucks/{truck.id}/")
    assert res.status_code == 400
    assert Truck.objects.filter(id=truck.id).exists()
