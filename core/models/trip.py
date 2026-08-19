from django.core.exceptions import ValidationError
from django.db import models

from . import Driver, Truck
from .driver import Driver

class Trip(models.Model):
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    arrival_time = models.DateTimeField(null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)

    driver = models.ForeignKey(Driver,on_delete=models.SET_NULL,null=True,blank=True,related_name='trips')
    truck = models.ForeignKey(Truck,on_delete=models.SET_NULL,null=True,blank=True,related_name='trips')

    planned_miles = models.FloatField(default=0)
    actual_miles = models.FloatField(default=0)
    loaded_miles = models.FloatField(default=0)
    empty_miles = models.FloatField(default=0)

    cpm = models.FloatField(default=0)
    pay = models.FloatField(default=0, null = True, blank = True)


    class TripStatus(models.TextChoices):
        IN_PROGRESS = 'inpro', "inprogress"
        PLANNED = 'plan',"planned"
        COMPLETE = 'com',"completed"
        CANCELED = 'can',"canceled"
        INCOMPLETE = 'inc',"incomplete"

    status = models.CharField(choices = TripStatus.choices,default=TripStatus.PLANNED, max_length= 10)


    #Trip state machine validation -----------------
    def validate_complete(self):
        if self.status != Trip.TripStatus.IN_PROGRESS:
            raise ValidationError("The trip must be started to end it")
        if not self.arrival_time or not self.departure_time:
            raise ValidationError("The trip missing arrival or departure time")

    def validate_incomplete(self):
        if self.status == Trip.TripStatus.COMPLETE:
            raise ValidationError("The trip was already completed")

    def validate_cancel(self):
        if self.status == Trip.TripStatus.COMPLETE:
            raise ValidationError("The trip was already completed")
        if self.status != Trip.TripStatus.PLANNED:
            raise ValidationError("only planned trips can be cancelled")

    def mark_in_progress(self):
        self.status = Trip.TripStatus.IN_PROGRESS

    #Truck/Driver assignment --------------
    def validate_driver_available(self):
        driver = self.driver
        if driver is None:
            raise ValidationError("No driver found")
        if driver.driver_status != Driver.DriverStatus.AVAILABLE:
            raise ValidationError("Driver not available")

    def validate_truck_available(self):
        truck = self.truck
        if truck is None:
            raise ValidationError("No truck found")
        if truck.truck_status != Truck.TruckStatus.AVAILABLE:
            raise ValidationError("Truck not available")

    def validate_driver_time_conflicts(self):
        driver = self.driver
        if driver is None:
            raise ValidationError("No driver found")
        if not self.departure_time or not self.arrival_time:
            return
        for planned_trip in driver.get_trips_planned():
            if planned_trip.id == self.id: #if this trip
                continue
            elif not planned_trip.departure_time or not planned_trip.arrival_time:
                continue
            elif planned_trip.departure_time < self.arrival_time and planned_trip.arrival_time > self.departure_time:
                raise ValidationError("driver has conflicting trip planned")

    def validate_truck_time_conflicts(self):
        truck = self.truck
        if truck is None:
            raise ValidationError("No truck found")
        if not self.departure_time or not self.arrival_time:
            return
        for planned_trip in truck.get_all_trips():
            if planned_trip.id == self.id: continue
            elif not planned_trip.departure_time or not planned_trip.arrival_time: continue
            elif planned_trip.departure_time < self.arrival_time and planned_trip.arrival_time > self.departure_time:
                raise ValidationError("truck has conflicting trip planned")

    def validate_start(self):
        driver = self.driver
        truck = self.truck
        self.validate_driver_available()
        self.validate_truck_available()
        if driver.get_trips_active().exclude(id=self.id).exists():
            raise ValidationError("Driver already has an active trip")
        if truck.get_trips_active().exclude(id=self.id).exists():
            raise ValidationError("Truck already has an active trip")

    def clean(self):
        if self.status == Trip.TripStatus.PLANNED:
            self.validate_driver_time_conflicts()
            self.validate_truck_time_conflicts()
        if self.status == Trip.TripStatus.IN_PROGRESS:
            if self.departure_time is None:
                raise ValidationError("departure_time is required")

    def __str__(self):
        return f"Trip {self.id}: {self.start} → {self.end} ({self.status})"