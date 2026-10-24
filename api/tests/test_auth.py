import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


endpoint = "/api/trips/"
def test_admin_client_permission(admin_client):
    res = admin_client.get(endpoint)
    assert res.status_code == 200

def test_dispatcher_client_permission(dispatcher_client):
    res = dispatcher_client.get(endpoint)
    assert res.status_code == 200

def test_regular_client_permission(regular_client):
    res = regular_client.get(endpoint)
    assert res.status_code == 403

def test_anon_client_permission(anon_client):
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
    #refresh token check
    res2 = client.post("/api/token/refresh/", {"refresh": res.data["refresh"]}, format="json")
    assert res2.status_code == 200
    assert "access" in res2.data

    #check user data
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {res2.data['access']}")
    res2 = client.get("/api/me/")
    assert res2.status_code == 200
    assert res2.data["username"] == "testing"
    assert res2.data["role"] == None



