import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

endpoint = ["/api/trucks/", "/api/drivers/", "/api/trips/"]

@pytest.mark.parametrize("endpoint", endpoint)
def test_admin_client_permission(admin_client, endpoint):
    res = admin_client.get(endpoint)
    assert res.status_code == 200

@pytest.mark.parametrize("endpoint", endpoint)
def test_dispatcher_client_permission(dispatcher_client,endpoint):
    res = dispatcher_client.get(endpoint)
    assert res.status_code == 200

@pytest.mark.parametrize("endpoint", endpoint)
def test_regular_client_permission(regular_client,endpoint):
    res = regular_client.get(endpoint)
    assert res.status_code == 403

@pytest.mark.parametrize("endpoint", endpoint)
def test_anon_client_permission(anon_client,endpoint):
    res = anon_client.get(endpoint)
    assert res.status_code == 401

@pytest.mark.django_db
def test_real_login():
    User.objects.create_user(username="testing", password="test")
    client = APIClient()
    res = client.post("/api/token/", {"username": "testing", "password": "test"}, format="json")
    assert res.status_code == 200
    assert "access" in res.data
    assert "refresh" in res.data
    #refresh token check -- replace old access token with new
    res2 = client.post("/api/token/refresh/", {"refresh": res.data["refresh"]}, format="json")
    assert res2.status_code == 200
    assert "access" in res2.data

    #check user data
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {res2.data['access']}")
    res2 = client.get("/api/me/")
    assert res2.status_code == 200
    assert res2.data["username"] == "testing"
    assert res2.data["role"] == None


def test_logout(db):
    User.objects.create_user(username="testing", password="test")
    client = APIClient()

    #login get refresh and access
    res = client.post("/api/token/", {"username": "testing", "password": "test"}, format="json")
    assert res.status_code == 200
    refresh = res.data["refresh"]  # get token
    access = res.data["access"]

    #test login by doing api/me with access given
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    res2 = client.get("/api/me/")
    assert res2.status_code == 200

    #test logout by sending refresh token to logout view
    res3 = client.post("/api/logout/", {"refresh": refresh}, format="json")
    assert res3.status_code == 204

    #test that the refresh token is blacked out
    res4 = client.post("/api/token/refresh/", {"refresh": refresh}, format="json")
    assert res4.status_code == 401 #unauthorized

def test_logout_empty_body(admin_client):
    res = admin_client.post("/api/logout/", {}, format="json")
    assert res.status_code == 400
    assert res.data["error"]["message"] == "Refresh token required."  # empty body

def test_logout_invalid_token(admin_client):
    res = admin_client.post("/api/logout/", {"refresh": "fake_token"}, format="json")
    assert res.status_code == 400
    assert res.data["error"]["message"] == "Invalid or expired token."  # fake token

def test_logout_unauthorized(db):
    client = APIClient()
    res = client.post("/api/logout/", {"refresh": "fake_token"}, format="json")
    assert res.status_code == 401