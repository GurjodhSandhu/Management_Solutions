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

    def get_load_pay(self):
        load_pay = self.cpm * self.planned_miles / 100
        return load_pay

    def validate_start(self):
        driver = self.driver
        if driver is None:
            raise ValidationError("Trip has No driver")
        driver.validate_truck()
        driver.validate_available()
        if driver.get_trips_active().exclude(id=self.id).exists():
            raise ValidationError("Driver already has an active trip")

    def validate_complete(self):
        if self.status != Trip.TripStatus.IN_PROGRESS:
            raise ValidationError("The trip must be started to end it")

    def validate_incomplete(self):
        if self.status == Trip.TripStatus.COMPLETE:
            raise ValidationError("The trip was already completed")

    def validate_cancel(self):
        if self.status == Trip.TripStatus.COMPLETE:
            raise ValidationError("The trip was already completed")
        if self.status != Trip.TripStatus.PLANNED:
            raise ValidationError("only planned trips can be cancelled")

    def validate_planned_time(self):
        driver = self.driver
        if driver is None:
            raise ValidationError("No driver found")
        for planned_trip in driver.get_trips_planned():
            if planned_trip.id ==self.id:
                continue
            if planned_trip.departure_time < self.arrival_time and planned_trip.arrival_time > self.departure_time:
                raise ValidationError("driver has conflicting trip planned")


    def clean(self):
        if self.status == Trip.TripStatus.IN_PROGRESS: #if trip's state is in progress check if its valid
            if not self.driver:
                raise ValidationError("Trip has no driver")
            if not self.driver.truck:
                raise ValidationError("No truck found")
            if self.driver.driver_status != Driver.DriverStatus.UNAVAILABLE:
                raise ValidationError("Trips's driver has incorrect status: trips active but drivers not unavailable")
            if self.driver.truck.truck_status != Truck.TruckStatus.UNAVAILABLE:
                raise ValidationError("Trip's truck has incorrect status: trips active but trucks not unavailable")

        if self.driver and self.status == Trip.TripStatus.PLANNED or self.driver and self.status == Trip.TripStatus.IN_PROGRESS: #if trip is still active or planed
            self.validate_planned_time() #check if driver has conflicts with a previous planned trip *


    def mark_in_progress(self):
        self.status = Trip.TripStatus.IN_PROGRESS

    def __str__(self):
        return f"Trip {self.id}: {self.start} → {self.end} ({self.status})"






