from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class Truck(models.Model):
    vin = models.CharField(validators=[MinLengthValidator(17),MaxLengthValidator(17)],max_length=17, null=True,blank=True)
    brand = models.CharField(max_length=20, null=True,blank=True)
    make = models.CharField(max_length=20, null=True,blank=True)
    year = models.IntegerField(validators=[MinValueValidator(1900),MaxValueValidator(2100)], null=True,blank=True)
    mileage = models.IntegerField(validators=[MinValueValidator(0)], null=True,blank=True)
    plate = models.CharField(max_length=10, null=True,blank=True)

    class TruckStatus(models.TextChoices):
        IN_REPAIR = 'IR',"In Repair"
        AVAILABLE = 'AV',"Available"
        UNAVAILABLE = 'UNAV',"Unavailable"
        OUT_OF_SERVICE = 'OOS',"Out of Service"

    class TruckLocation(models.TextChoices):
        In_TRANSIT = 'IT',"In Transit"
        AT_DEPOT = 'AT',"At Depot"
        ARRIVED_DESTINATION = 'AD',"Arrived Destination"
        ON_ROUTE = 'OR', "On Route"

    truck_status = models.CharField(choices = TruckStatus.choices,default=TruckStatus.AVAILABLE, max_length= 5)
    truck_location = models.CharField(choices=TruckLocation.choices,default=TruckLocation.AT_DEPOT, max_length=3)

    def mark_in_repair(self):
        self.check_on_trip()
        self.Truck_status = Truck.TruckStatus.IN_REPAIR

    def mark_unavailable(self):
        self.Truck_status = Truck.TruckStatus.UNAVAILABLE

    def mark_available(self):
        self.check_on_trip() #cannot change state to avaiable until trip states matchs logic
        self.Truck_status = Truck.TruckStatus.AVAILABLE

    def mark_out_of_service(self):
        self.check_on_trip()
        self.TruckStatus = Truck.TruckStatus.OUT_OF_SERVICE

    def get_drivers(self):
        return self.drivers.all()

    def check_on_trip(self):
        if not self.get_drivers().exist():
            return None
        for driver in self.get_drivers():
            if driver.get_trips_active().exists():
                raise ValidationError("Truck and driver are on an active trip")
        return False

    def get_trips_active(self):
        return self.trips.filter(status="inpro")
    def get_all_trips(self):
        return self.trips.all()

    def __str__(self):
        return f"{self.vin}"