from rest_framework import viewsets
from core.models import Truck, Driver, Trip
from .serializers import TruckSerializer, DriverSerializer, TripSerializer


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer