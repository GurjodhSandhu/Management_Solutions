from django.utils import timezone
from datetime import datetime

import pytest
from core.models import Trip, Driver, Truck
from django.forms.models import model_to_dict

def test_add_trip(admin_client):
    res = admin_client.post(f"/api/trips/", {"start": "vancouver", "end": "Calgary","arrival_time":"2026-11-22T18:00:00Z","departure_time":"2026-10-22T18:00:00Z",
                                             "status": "inpro"}, format="json")
    assert res.status_code == 201
    assert Trip.objects.filter(id = res.data["id"]).exists()
    trip = Trip.objects.get(id=res.data["id"])
    assert trip.start == "vancouver"
    assert trip.end == "Calgary"
    assert trip.arrival_time == datetime(2026,11,22,18,0, tzinfo=timezone.UTC)
    assert trip.departure_time == datetime(2026,10,22,18,0, tzinfo=timezone.UTC)
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
                                            }
    res = admin_client.patch(f"/api/trips/{trip.id}/", update, format="json")
    trip.refresh_from_db()
    assert trip.start == "toronto"
    assert trip.end == "Calgary"
    assert trip.arrival_time == datetime(2027, 12, 22, 18, 0, tzinfo=timezone.UTC)
    assert trip.departure_time == datetime(2027, 12, 22, 18, 0, tzinfo=timezone.UTC)
    assert trip.status == Trip.TripStatus.PLANNED
    assert res.status_code == 200
    assert Trip.objects.filter(id = res.data["id"]).exists()
    assert trip.status == Trip.TripStatus.PLANNED #cannot change state without state machine even with update
    assert res.data['start'] == "toronto"
    assert res.data['end'] == "Calgary"
    assert res.data['arrival_time'] == "2027-12-22T18:00:00Z"
    assert res.data['departure_time'] == "2027-12-22T18:00:00Z"


@pytest.mark.parametrize('payload',bad_payload,ids=bad_id)
def test_update_trip_bad_field(admin_client,payload):
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","arrival_time":"2026-11-22T18:00:00Z","departure_time":"2026-10-22T18:00:00Z"})
    before = model_to_dict(trip)
    res = admin_client.patch(f"api/trips/{trip.id}/", payload, format="json")
    after = model_to_dict(trip)
    assert res.status_code == 404
    assert before == after

def test_delete_driver(admin_client):
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","arrival_time":"2026-11-22T18:00:00Z","departure_time":"2026-10-22T18:00:00Z"})
    trip_id = trip.id
    res = admin_client.delete(f"/api/trips/{trip_id}/",format="json")
    assert res.status_code == 204
    assert not Driver.objects.filter(id = trip_id).exists()
    assert admin_client.get(f"/api/trips/{trip_id}/").status_code == 404

def test_delete_driver_ontrip(admin_client):
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","arrival_time":"2026-11-22T18:00:00Z","departure_time":"2026-10-22T18:00:00Z","status":"inpro"})
    trip_id = trip.id
    res = admin_client.delete(f"/api/trips/{trip_id}/",format="json")
    assert trip.status == Trip.TripStatus.IN_PROGRESS
    assert res.status_code == 400
    assert Trip.objects.filter(id = trip_id).exists()
    assert admin_client.get(f"/api/trips/{trip_id}/").status_code == 200

def test_delete_driver_nonexistent(admin_client):
    trip = Trip.objects.create(**{"start": "vancouver", "end": "Calgary","arrival_time":"2026-11-22T18:00:00Z","departure_time":"2026-10-22T18:00:00Z","status":"inpro"})
    trip_id = trip.id
    trip.delete()
    assert not Trip.objects.filter(id = trip_id).exists()
    res = admin_client.delete(f"/api/trips/{trip_id}/",format="json")
    assert res.status_code == 404
