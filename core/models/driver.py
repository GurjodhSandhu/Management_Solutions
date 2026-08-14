from django.core.exceptions import ValidationError
from django.db import models

from .truck import Truck

class Driver(models.Model):
    truck = models.ForeignKey(Truck,on_delete=models.SET_NULL,null=True,blank=True,related_name='drivers')
    driver_name = models.CharField(max_length=255, null=True,blank=True)
    driver_licensenumber = models.CharField(max_length=30, null=True,blank=True)

    class DriverStatus(models.TextChoices):
        AVAILABLE =  "av",  "AVAILABLE"
        UNAVAILABLE =  "ua",  "UNAVAILABLE"

    driver_status = models.CharField(choices=DriverStatus.choices,default=DriverStatus.AVAILABLE,max_length=25)

    def validate_truck(self):
        if self.truck is None:
            raise ValidationError("Driver has no truck")
        if self.truck.truck_status == Truck.TruckStatus.UNAVAILABLE:
            raise ValidationError("Truck is unavailable")
        if self.truck.truck_status == Truck.TruckStatus.OUT_OF_SERVICE:
            raise ValidationError("Truck is out of service")
        if self.truck.truck_status == Truck.TruckStatus.IN_REPAIR:
            raise ValidationError("Truck is being repaired")

    def get_trips(self):
        return self.trips.all()

    def get_trips_active(self):
        return self.trips.filter(status="inpro")

    def get_trips_planned(self):
        return self.trips.filter(status="plan")

    def mark_unavailable(self):
        self.driver_status = Driver.DriverStatus.UNAVAILABLE

    def mark_available(self):
        self.driver_status = Driver.driver_status.AVAILABLE

    def validate_available(self):
        if self.driver_status == Driver.DriverStatus.UNAVAILABLE:
            raise ValidationError("Driver unavailable")

    def __str__(self):
        return f"Driver {self.id}: {self.driver_name}"

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()  # ensures clean() runs
        super().save(*args, **kwargs)
