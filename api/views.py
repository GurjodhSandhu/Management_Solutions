from typing import Any

from django.db.models import Model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Truck, Driver, Trip
from .serializers import TruckSerializer, DriverSerializer, TripSerializer, AssignDriverSerializer, AssignTruckSerializer

from core.services import service_truck, service_driver, service_trip
from api.permission import IsAdminOrDispatcher

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class LoginThrottleView(TokenObtainPairView):
    throttle_scope = "login"

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"error": {"code": "invalid_token", "message": "Refresh token required."}},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            RefreshToken(request.data.get("refresh")).blacklist()
        except TokenError:
            return Response({"error": {"code": "invalid_token", "message": "Invalid or expired token."}},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
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
    queryset = Truck.objects.all().order_by("id")
    serializer_class = TruckSerializer
    permission_classes = [IsAuthenticated,IsAdminOrDispatcher]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        truck = service_truck.add_truck(serializer.validated_data)
        return Response(self.get_serializer(truck).data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        truck = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        truck = service_truck.update_truck(truck.id, serializer.validated_data)
        return Response(self.get_serializer(truck).data, status=status.HTTP_200_OK)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        truck = self.get_object()
        service_truck.delete_truck(truck.id)
        return Response(status=status.HTTP_204_NO_CONTENT)



class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all().order_by("id")
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated,IsAdminOrDispatcher]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        driver = service_driver.add_driver(serializer.validated_data)
        output = self.get_serializer(driver)
        return Response(output.data, status=status.HTTP_201_CREATED)


    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        driver = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        driver = service_driver.update_driver(driver.id, serializer.validated_data)
        return Response(self.get_serializer(driver).data, status=status.HTTP_200_OK)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        driver = self.get_object()
        service_driver.delete_driver(driver.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.select_related("driver", "truck").order_by("id")
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated,IsAdminOrDispatcher]


    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trip = service_trip.new_trip(serializer.validated_data)
        return Response(self.get_serializer(trip).data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        trip = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if {"driver", "truck"} & set(request.data):
            return Response(
                {"error": {"code": "validation_error",
                           "messages": ["Use the assignment endpoints to assign drivers or trucks."]}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        trip = service_trip.update_trip(trip.id, serializer.validated_data)

        return Response(self.get_serializer(trip).data, status=status.HTTP_200_OK)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        trip = self.get_object()
        service_trip.delete_trip(trip.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['post'])
    def start(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        trip = self.get_object()
        trip = service_trip.start_trip(trip.id)
        return Response(self.get_serializer(trip).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def complete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        trip = self.get_object()
        trip = service_trip.complete_trip(trip.id)
        return Response(self.get_serializer(trip).data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'])
    def incomplete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        trip = self.get_object()
        trip = service_trip.incomplete_trip(trip.id)
        return Response(self.get_serializer(trip).data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'])
    def cancel(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        trip = self.get_object()
        trip = service_trip.cancel_trip(trip.id)
        return Response(self.get_serializer(trip).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def assign_truck(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = AssignTruckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        trip = self.get_object()

        service_trip.assign_truck_to_trip(trip.id, serializer.validated_data["truck"].id,)
        trip.refresh_from_db()
        return Response(self.get_serializer(trip).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def assign_driver(self, request, *args, **kwargs):
        serializer = AssignDriverSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trip = self.get_object()
        service_trip.assign_driver_to_trip(trip.id, serializer.validated_data["driver"].id,)
        trip.refresh_from_db()
        return Response(self.get_serializer(trip).data, status=status.HTTP_200_OK)