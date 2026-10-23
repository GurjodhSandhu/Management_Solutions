import pytest

from core.models import Trip
from core.services import service_trip
from core.tests import factories


def make_trip(state: str) -> Trip:
    """Build a trip in the given state the same way the app would: through the services."""
    trip = factories.TripFactory(
        driver=factories.DriverFactory(),
        truck=factories.TruckFactory(),
        start="vancouver",
        end="calgary",
    )
    if state == "cancelled":
        service_trip.cancel_trip(trip.id)
    elif state != "planned":
        service_trip.start_trip(trip.id)
        if state == "completed":
            service_trip.complete_trip(trip.id)
        elif state == "incomplete":
            service_trip.incomplete_trip(trip.id)
    trip.refresh_from_db()
    return trip


# (state, fields that SHOULD change, fields that should be IGNORED)
# Mirrors ALLOWED_TRIP_UPDATE_FIELDS_PLANNED / _INPROGRESS / _OTHER in service_trip.py.
# Planned trips allow almost everything, so their "ignored" set is covered by the
# status/driver/truck test below.
WHITELIST_CASES = [
    pytest.param(
        "planned",
        {"start": "toronto", "planned_miles": 250.0},
        {},
        id="planned",
    ),
    pytest.param(
        "in_progress",
        {"end": "edmonton", "actual_miles": 120.0},
        {"start": "toronto", "planned_miles": 999.0},
        id="in_progress",
    ),
    pytest.param(
        "completed",
        {"actual_miles": 120.0, "pay": 500.0},
        {"start": "toronto", "end": "edmonton"},
        id="completed",
    ),
    pytest.param(
        "cancelled",
        {"actual_miles": 120.0, "pay": 500.0},
        {"start": "toronto", "end": "edmonton"},
        id="cancelled",
    ),
    pytest.param(
        "incomplete",
        {"actual_miles": 120.0, "pay": 500.0},
        {"start": "toronto", "end": "edmonton"},
        id="incomplete",
    ),
]


@pytest.mark.django_db
@pytest.mark.parametrize("state, allowed, ignored", WHITELIST_CASES)
def test_update_trip_applies_only_fields_allowed_for_status(state, allowed, ignored):
    trip = make_trip(state)
    original_status = trip.status
    ignored_before = {field: getattr(trip, field) for field in ignored}

    service_trip.update_trip(trip.id, {**allowed, **ignored})
    trip.refresh_from_db()

    for field, value in allowed.items():
        assert getattr(trip, field) == value, f"{field} should be editable while {state}"
    for field, original in ignored_before.items():
        assert getattr(trip, field) == original, f"{field} should be ignored while {state}"
    assert trip.status == original_status


ALL_STATES = ["planned", "in_progress", "completed", "cancelled", "incomplete"]


@pytest.mark.django_db
@pytest.mark.parametrize("state", ALL_STATES)
def test_update_trip_never_changes_status_driver_or_truck(state):
    trip = make_trip(state)
    original = (trip.status, trip.driver_id, trip.truck_id)

    # Try to move the trip to a different status than the one it is in
    other_status = (
        Trip.TripStatus.COMPLETE
        if trip.status == Trip.TripStatus.PLANNED
        else Trip.TripStatus.PLANNED
    )
    service_trip.update_trip(
        trip.id,
        {
            "status": other_status,
            "driver": factories.DriverFactory(),
            "truck": factories.TruckFactory(),
        },
    )
    trip.refresh_from_db()

    assert (trip.status, trip.driver_id, trip.truck_id) == original