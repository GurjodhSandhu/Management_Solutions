from django.conf import settings

from core.tests.factories import TripFactory

PAGE_SIZE = settings.REST_FRAMEWORK["PAGE_SIZE"]


def test_trip_list_pagination(admin_client):
    # Two more trips than fit on one page, so there is a second page.
    # TripFactory makes trips with no driver or truck, which also checks that
    # the serializer renders unassigned trips without crashing.
    trips = TripFactory.create_batch(PAGE_SIZE + 2)
    created_ids = {trip.id for trip in trips}

    res1 = admin_client.get("/api/trips/")
    res2 = admin_client.get("/api/trips/?page=2")
    assert res1.status_code == 200
    assert res2.status_code == 200
    page1, page2 = res1.data, res2.data

    # Envelope shape the front end reads
    for page in (page1, page2):
        assert {"count", "next", "previous", "results"} <= set(page)

    # Page 1: full page, points forward only
    assert page1["count"] == PAGE_SIZE + 2
    assert len(page1["results"]) == PAGE_SIZE
    assert page1["next"] is not None
    assert page1["previous"] is None

    # Page 2: the remainder, points backward only
    assert len(page2["results"]) == 2
    assert page2["next"] is None
    assert page2["previous"] is not None

    # Stable order: ids ascend across both pages, with no repeats or gaps
    ids = [trip["id"] for trip in page1["results"] + page2["results"]]
    assert ids == sorted(ids)
    assert set(ids) == created_ids