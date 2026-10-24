from datetime import datetime, timezone
from core.services.service_trip import start_trip
from rest_framework import status

from api.serializers import TripSerializer

import pytest
from core.models import Trip, Driver, Truck

def test_add_trip(admin_client):
    res = admin_client.post(f"/api/trips/", {"start": "vancouver", "end": "Calgary","arrival_time":"2026-11-22T18:00:00Z","departure_time":"2026-10-22T18:00:00Z",
                                             "status": "inpro"}, format="json")
    assert res.status_code == 201
    assert Trip.objects.filter(id = res.data["id"]).exists()
    trip = Trip.objects.get(id=res.data["id"])
    assert trip.start == "vancouver"
    assert trip.end == "Calgary"
    assert trip.arrival_time == datetime(2026,11,22,18,0, tzinfo=timezone.utc)
    assert trip.departure_time == datetime(2026,10,22,18,0, tzinfo=timezone.utc)
    assert trip.status == Trip.TripStatus.PLANNED #cannot change state without state machine
    assert res.data['start'] == "vancouver"
    assert res.data['end'] == "Calgary"
    assert res.data['arrival_time'] == "2026-11-22T18:00:00Z"
    assert res.data['departure_time'] == "2026-10-22T18:00:00Z"

#bad_payload contains all the broken validation rules
bad_payload = [
    ({"start":"vancouver","end":"calgary","departure_time":"2026-12-25T18:00:00Z","arrival_time": "2026-12-22T18:00:00Z"})
    ,({"start": "vancouver"}),
    ({"end": "Calgary"})
]
bad_id = ['arrival_time_after_depature',"missing_end","missing_start"]
@pytest.mark.parametrize("payload",bad_payload,ids=bad_id)
def test_add_trip_bad_field(admin_client,payload):
    res = admin_client.post(f"/api/trips/", payload, format="json")
    assert res.status_code == 400
    assert Trip.objects.count() == 0

def test_update_trip(admin_client):
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","arrival_time":"2026-11-22T18:00:00Z","departure_time":"2026-10-22T18:00:00Z"})
    update = {"start": "toronto", "end": "Calgary",
              "arrival_time":"2027-12-22T18:00:00Z",
              "departure_time":"2027-12-22T18:00:00Z",
              "status":"inpro"
                                            }
    res = admin_client.patch(f"/api/trips/{trip.id}/", update, format="json")
    trip.refresh_from_db()
    assert trip.start == "toronto"
    assert trip.end == "Calgary"
    assert trip.arrival_time == datetime(2027, 12, 22, 18, 0, tzinfo=timezone.utc)
    assert trip.departure_time == datetime(2027, 12, 22, 18, 0, tzinfo=timezone.utc)
    assert trip.status == Trip.TripStatus.PLANNED
    assert res.status_code == 200
    assert Trip.objects.filter(id = res.data["id"]).exists()
    assert trip.status == Trip.TripStatus.PLANNED #cannot change state without state machine even with update
    assert res.data['start'] == "toronto"
    assert res.data['end'] == "Calgary"
    assert res.data['arrival_time'] == "2027-12-22T18:00:00Z"
    assert res.data['departure_time'] == "2027-12-22T18:00:00Z"

bad_payload_update = [
    ({"start":"vancouver","end":"calgary","departure_time":"2026-12-25T18:00:00Z","arrival_time": "2026-12-22T18:00:00Z"})
    ,({"start": [123,321]}),
    ({"end": {"location": "calgary"}})
]
bad_update_id = ['arrival_time_after_depature',"invalid_start_list","invalid_end_dict"]
@pytest.mark.parametrize('payload',bad_payload_update,ids=bad_update_id)
def test_update_trip_bad_field(admin_client,payload):
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","arrival_time":"2026-11-22T18:00:00Z","departure_time":"2026-10-22T18:00:00Z"})
    before = TripSerializer(trip).data
    res = admin_client.patch(f"/api/trips/{trip.id}/", payload, format="json")
    trip.refresh_from_db()
    after = TripSerializer(trip).data
    assert res.status_code == 400
    assert before == after

def test_update_trip_bad_field_driver(admin_client):
    trip = Trip.objects.create()
    driver = Driver.objects.create()
    before = TripSerializer(trip).data
    res = admin_client.patch(f"/api/trips/{trip.id}/", {"driver": driver.id}, format="json")
    assert res.status_code == 400
    trip.refresh_from_db()
    after = TripSerializer(trip).data
    assert before == after

def test_update_trip_bad_field_truck(admin_client):
    trip = Trip.objects.create()
    truck = Truck.objects.create()
    before = TripSerializer(trip).data
    res = admin_client.patch(f"/api/trips/{trip.id}/", {"driver": truck.id}, format="json")
    assert res.status_code == 400
    trip.refresh_from_db()
    after = TripSerializer(trip).data
    assert before == after


def test_delete_trip(admin_client):
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","arrival_time":"2026-11-22T18:00:00Z","departure_time":"2026-10-22T18:00:00Z"})
    trip_id = trip.id
    res = admin_client.delete(f"/api/trips/{trip_id}/",format="json")
    assert res.status_code == 204
    assert not Trip.objects.filter(id = trip_id).exists()
    assert admin_client.get(f"/api/trips/{trip_id}/").status_code == 404

def test_delete_trip_ontrip(admin_client):
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","arrival_time":"2026-11-22T18:00:00Z","departure_time":"2026-10-22T18:00:00Z","status":"inpro"})
    trip_id = trip.id
    res = admin_client.delete(f"/api/trips/{trip_id}/",format="json")
    trip.refresh_from_db()
    assert trip.status == Trip.TripStatus.IN_PROGRESS
    assert res.status_code == 400
    assert Trip.objects.filter(id = trip_id).exists()
    assert admin_client.get(f"/api/trips/{trip_id}/").status_code == 200

def test_delete_trip_nonexistent(admin_client):
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","arrival_time":"2026-11-22T18:00:00Z","departure_time":"2026-10-22T18:00:00Z","status":"inpro"})
    trip_id = trip.id
    trip.delete()
    assert not Trip.objects.filter(id = trip_id).exists()
    res = admin_client.delete(f"/api/trips/{trip_id}/",format="json")
    assert res.status_code == 404

def test_trip_start_valid(admin_client):
    driver = Driver.objects.create()
    truck = Truck.objects.create()
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","truck":truck,"driver":driver})
    assert trip.status == Trip.TripStatus.PLANNED
    res = admin_client.post(f"/api/trips/{trip.id}/start/")
    trip.refresh_from_db()
    truck.refresh_from_db()
    driver.refresh_from_db()
    assert res.status_code == 200
    assert trip.status == Trip.TripStatus.IN_PROGRESS
    assert truck.truck_status == Truck.TruckStatus.UNAVAILABLE
    assert driver.driver_status == Driver.DriverStatus.UNAVAILABLE
    assert trip.departure_time is not None

def test_trip_start_invalid(admin_client):
    driver = Driver.objects.create()
    truck = Truck.objects.create()
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","truck":truck,}) #missing driver
    assert trip.status == Trip.TripStatus.PLANNED
    res = admin_client.post(f"/api/trips/{trip.id}/start/")
    trip.refresh_from_db()
    truck.refresh_from_db()
    driver.refresh_from_db()
    assert res.status_code == 400
    assert trip.status == Trip.TripStatus.PLANNED
    assert truck.truck_status == Truck.TruckStatus.AVAILABLE
    assert driver.driver_status == Driver.DriverStatus.AVAILABLE
    assert trip.departure_time is None

def test_trip_complete_valid(admin_client):
    driver = Driver.objects.create()
    truck = Truck.objects.create()
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","truck":truck,"driver":driver})
    assert trip.status == Trip.TripStatus.PLANNED
    admin_client.post(f"/api/trips/{trip.id}/start/")
    trip.refresh_from_db()
    assert trip.status == Trip.TripStatus.IN_PROGRESS
    res = admin_client.post(f"/api/trips/{trip.id}/complete/")
    trip.refresh_from_db()
    truck.refresh_from_db()
    driver.refresh_from_db()
    assert res.status_code == 200
    assert trip.status == Trip.TripStatus.COMPLETE
    assert truck.truck_status == Truck.TruckStatus.AVAILABLE
    assert driver.driver_status == Driver.DriverStatus.AVAILABLE
    assert trip.departure_time is not None
    assert trip.arrival_time is not None

def test_trip_complete_invalid(admin_client): #plan -> inpro -> incomplete -x-> complete
    driver = Driver.objects.create()
    truck = Truck.objects.create()
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","truck":truck,"driver":driver})

    admin_client.post(f"/api/trips/{trip.id}/start/")
    admin_client.post(f"/api/trips/{trip.id}/incomplete/")
    trip.refresh_from_db()
    assert trip.status == Trip.TripStatus.INCOMPLETE #if trip is already set to incomplete

    res = admin_client.post(f"/api/trips/{trip.id}/complete/")

    trip.refresh_from_db()
    truck.refresh_from_db()
    driver.refresh_from_db()
    assert res.status_code == 400
    assert truck.truck_status == Truck.TruckStatus.AVAILABLE #make sure status remained the same
    assert driver.driver_status == Driver.DriverStatus.AVAILABLE
    assert trip.status == Trip.TripStatus.INCOMPLETE

def test_trip_cancel_valid(admin_client): #plan -> cancel
    driver = Driver.objects.create()
    truck = Truck.objects.create()
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","truck":truck,"driver":driver})
    assert trip.status == Trip.TripStatus.PLANNED
    res = admin_client.post(f"/api/trips/{trip.id}/cancel/")
    trip.refresh_from_db()
    truck.refresh_from_db()
    driver.refresh_from_db()
    assert res.status_code == 200
    assert trip.status == Trip.TripStatus.CANCELED
    assert truck.truck_status == Truck.TruckStatus.AVAILABLE
    assert driver.driver_status == Driver.DriverStatus.AVAILABLE

def test_trip_cancel_invalid(admin_client): #plan ---> inpro -x-> cancel
    driver = Driver.objects.create()
    truck = Truck.objects.create()
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","truck":truck,"driver":driver})
    assert trip.status == Trip.TripStatus.PLANNED
    admin_client.post(f"/api/trips/{trip.id}/start/")
    trip.refresh_from_db()
    assert trip.status == Trip.TripStatus.IN_PROGRESS
    res = admin_client.post(f"/api/trips/{trip.id}/cancel/")
    trip.refresh_from_db()
    assert res.status_code == 400
    assert trip.status == Trip.TripStatus.IN_PROGRESS