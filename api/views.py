from typing import Any

from django.db.migrations import serializer
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from core.models import Truck, Driver, Trip
from .serializers import TruckSerializer, DriverSerializer, TripSerializer

from core.services import service_truck, service_driver, service_trip

class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            truck = service_truck.add_truck(serializer.validated_data)

            output = self.get_serializer(truck)
            return Response(output.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            truck_id = kwargs.get('pk')
            truck = service_truck.update_truck(truck_id, serializer.validated_data)

            output = self.get_serializer(truck)

            return Response(output.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            truck_id = kwargs["pk"]
            service_truck.delete_truck(truck_id)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            driver = service_driver.add_driver(serializer.validated_data)
            output = self.get_serializer(driver)
            return Response(output.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            driver_id = kwargs.get('pk')

            driver = service_driver.update_driver(driver_id, serializer.validated_data)
            output = self.get_serializer(driver)
            return Response(output.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            driver_id = kwargs["pk"]
            service_driver.delete_driver(driver_id)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        try:
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            trip = service_trip.new_trip(serializer.validated_data)
            output = self.get_serializer(trip)
            return Response(output.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        try:
            trip_id = kwargs['pk']
            trip = service_trip.update_trip(trip_id, serializer.validated_data)
            output = self.get_serializer(trip)
            return Response(output.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            trip_id = kwargs['pk']
            service_trip.delete_trip(trip_id)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)