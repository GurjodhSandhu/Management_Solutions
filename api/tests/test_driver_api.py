import pytest
from core.models import Driver, Trip, Truck
from django.forms.models import model_to_dict


bad_payload = [({"driver_name": [321,2123]},"driver_name")
               ,({"driver_licensenumber": {"invalid": "dict"}},"driver_licensenumber")]
bad_id = ["bad_name_list","bad_licensenumber_dict"]

def test_add_driver(admin_client):
    res = admin_client.post(f"/api/drivers/",{"driver_name": "testing", "driver_licensenumber": "abc 321"}, format="json")
    assert res.status_code == 201
    assert Driver.objects.filter(id = res.data["id"]).exists()
    driver = Driver.objects.get(id=res.data["id"])
    assert driver.driver_name == "testing"
    assert driver.driver_licensenumber == "abc 321"
    assert driver.driver_status == Driver.DriverStatus.AVAILABLE

@pytest.mark.parametrize('payload, bad_field',bad_payload,ids=bad_id)
def test_add_driver_with_bad_field(admin_client,payload,bad_field):
    res = admin_client.post(f"/api/drivers/",payload, format="json")
    assert res.status_code == 400
    assert Driver.objects.count() == 0
    assert bad_field in res.data, res.data

def test_update_driver(admin_client):
    driver = Driver.objects.create(driver_name="testing", driver_licensenumber="abc 321")
    before = model_to_dict(driver)
    res = admin_client.patch(f"/api/drivers/{driver.id}/",{"driver_name":"update"}, format="json")
    assert res.status_code == 200
    driver.refresh_from_db()
    after = model_to_dict(driver)
    expected = {**before, "driver_name": "update"}
    assert after == expected

def test_update_driver_valid_truck(admin_client):
    truck = Truck.objects.create(vin="123456789abcdefgh")
    driver = Driver.objects.create(driver_name="testing", driver_licensenumber="abc 321")
    before = model_to_dict(driver)
    res = admin_client.patch(f"/api/drivers/{driver.id}/",{"truck":truck.id}, format="json")
    assert res.status_code == 200
    driver.refresh_from_db()
    after = model_to_dict(driver)
    expected = {**before, "truck": truck.id}
    assert after == expected
    #clear truck
    res = admin_client.patch(f"/api/drivers/{driver.id}/",{"truck": None}, format="json")
    assert res.status_code == 200
    driver.refresh_from_db()
    assert driver.truck == None

def test_update_driver_nonexistent_truck(admin_client):
    truck = Truck.objects.create(vin="123456789abcdefgh")
    truck_id = truck.id
    truck.delete()
    driver = Driver.objects.create(driver_name="testing", driver_licensenumber="abc 321")
    before = model_to_dict(driver)
    res = admin_client.patch(f"/api/drivers/{driver.id}/",{"truck":truck_id}, format="json")
    assert res.status_code == 400
    driver.refresh_from_db()
    after = model_to_dict(driver)
    assert before == after

@pytest.mark.parametrize('payload, bad_field',bad_payload,ids=bad_id)
def test_update_driver_with_bad_field(admin_client,payload,bad_field):
    driver = Driver.objects.create(driver_name="testing", driver_licensenumber="abc 321")
    before = model_to_dict(driver)
    res = admin_client.patch(f"/api/drivers/{driver.id}/",payload, format="json")
    assert res.status_code == 400
    driver.refresh_from_db()
    after = model_to_dict(driver)
    assert before == after
    assert bad_field in res.data, res.data

def test_delete_driver(admin_client):
    driver = Driver.objects.create(driver_name="testing", driver_licensenumber="abc 321")
    driver_id = driver.id
    res = admin_client.delete(f"/api/drivers/{driver_id}/",format="json")
    assert res.status_code == 204
    assert not Driver.objects.filter(id = driver_id).exists()
    assert admin_client.get(f"/api/drivers/{driver_id}/").status_code == 404

def test_delete_driver_nonexistent(admin_client):
    driver = Driver.objects.create(driver_name="testing", driver_licensenumber="abc 321")
    driver_id = driver.id
    driver.delete()
    res = admin_client.delete(f"/api/drivers/{driver_id}/",format="json")
    assert res.status_code == 404
    assert not Driver.objects.filter(id = driver_id).exists()

def test_delete_driver_active(admin_client):
    driver = Driver.objects.create(driver_name="testing", driver_licensenumber="abc 321")
    Trip.objects.create(status=Trip.TripStatus.IN_PROGRESS, driver=driver)
    driver_id = driver.id
    res = admin_client.delete(f"/api/drivers/{driver_id}/",format="json")
    assert res.status_code == 400
    assert Driver.objects.filter(id = driver_id).exists()
    assert admin_client.get(f"/api/drivers/{driver_id}/").status_code == 200
