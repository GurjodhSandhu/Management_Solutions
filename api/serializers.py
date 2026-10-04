from rest_framework import serializers
from core.models import Truck, Trip, Driver

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = ['id', 'vin', 'brand', 'make', 'year', 'mileage',
                  'truck_status', 'truck_location']
        read_only_fields = ['id']


class DriverSerializer(serializers.ModelSerializer):
    truck_id = serializers.IntegerField(source='truck.id', read_only=True)

    class Meta:
        model = Driver
        model = Driver
        fields = ['id', 'driver_name', 'driver_licensenumber',
                  'driver_status', 'truck', 'truck_id']
        read_only_fields = ['id']

class TripSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='driver.driver_name', read_only=True)
    truck_vin = serializers.CharField(source='truck.vin', read_only=True)

    class Meta:
        model = Trip
        fields = ['id', 'start', 'end', 'status', 'departure_time', 'arrival_time',
                  'driver', 'driver_name', 'truck', 'truck_vin', 'planned_miles',
                  'actual_miles', 'cpm', 'pay']
        read_only_fields = ['id']
