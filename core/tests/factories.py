import factory
from core.models import Truck, Driver, Trip

class TruckFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Truck

    truck_status = Truck.truck_status = Truck.TruckStatus.AVAILABLE

class DriverFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Driver

class TripFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trip

    departure_time = None
    arrival_time = None