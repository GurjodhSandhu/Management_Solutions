from typing import Any

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from core.models import Truck, Driver, Trip
from .serializers import TruckSerializer, DriverSerializer, TripSerializer

from core.services import service_truck, service_driver, service_trip
from api.permission import IsAdminOrDispatcher

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import ScopedRateThrottle

class LoginThrottleView(TokenObtainPairView):
    throttle_scope = "login"

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = user.groups.first().name if user.groups.exists() else None

        return Response({
            "id": user.id,
            "username": user.username,
            "role": role,
        })

class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    permission_classes = [IsAuthenticated,IsAdminOrDispatcher]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        truck = service_truck.add_truck(serializer.validated_data)

        output = self.get_serializer(truck)
        return Response(output.data, status=status.HTTP_201_CREATED)


    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        truck_id = kwargs.get('pk')
        truck = service_truck.update_truck(truck_id, serializer.validated_data)

        output = self.get_object()

        return Response(output.data, status=status.HTTP_200_OK)


    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        truck_id = kwargs["pk"]
        service_truck.delete_truck(truck_id)
        return Response(status=status.HTTP_204_NO_CONTENT)



class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated,IsAdminOrDispatcher]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        driver = service_driver.add_driver(serializer.validated_data)
        output = self.get_serializer(driver)
        return Response(output.data, status=status.HTTP_201_CREATED)



    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        driver_id = kwargs.get('pk')

        driver = service_driver.update_driver(driver_id, serializer.validated_data)
        output = self.self.get_object()
        return Response(output.data, status=status.HTTP_200_OK)


    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        driver_id = kwargs["pk"]
        service_driver.delete_driver(driver_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated,IsAdminOrDispatcher]


    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        trip = service_trip.new_trip(serializer.validated_data)
        output = self.get_serializer(trip)
        return Response(output.data, status=status.HTTP_201_CREATED)


    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        trip_id = kwargs['pk']
        trip = service_trip.update_trip(trip_id, serializer.validated_data)

        output = self.self.get_object()
        return Response(output.data, status=status.HTTP_200_OK)


    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        trip_id = kwargs['pk']
        service_trip.delete_trip(trip_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['post'])
    def start(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        trip = self.get_object()
        trip_id = trip.id
        service_trip.start_trip(trip_id)
        output = self.self.get_object()
        return Response(output.data,status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'])
    def complete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        trip = self.get_object()
        trip_id = trip.id
        service_trip.complete_trip(trip_id)
        output = self.self.get_object()
        return Response(output.data,status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'])
    def incomplete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        trip = self.get_object()
        trip_id = trip.id
        service_trip.incomplete_trip(trip_id)
        output = self.self.get_object()
        return Response(output.data,status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'])
    def canceltrip(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        trip = self.get_object()
        trip_id = trip.id
        service_trip.cancel_trip(trip_id)
        output = self.self.get_object()
        return Response(output.data,status=status.HTTP_200_OK)

