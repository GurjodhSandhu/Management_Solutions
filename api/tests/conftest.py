import pytest
from django.contrib.auth.models import Group, User
from django.core.cache import cache
from rest_framework.test import APIClient

@pytest.fixture(autouse=True)
def clear_throttle_cache():
    cache.clear()

@pytest.fixture
def admin_client(db):
    user = User.objects.create_user(username='admin', email='', password='1234')
    user.groups.add(Group.objects.get_or_create(name="admin")[0])
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def dispatcher_client(db):
    user = User.objects.create_user(username='dispatch', email='', password='321')
    user.groups.add(Group.objects.get_or_create(name="dispatcher")[0])
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def regular_client(db):
    user = User.objects.create_user(username='regular', email='', password='')
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def anon_client(db):
    client = APIClient()
    return client