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
        IN_SERVICE = 'IS',"In Service"
        AVAILABLE = 'AV',"Available"
        UNAVAILABLE = 'UNAV',"Unavailable"
        OUT_OF_SERVICE = 'OOS',"Out of Service"

    class TruckLocation(models.TextChoices):
        In_TRANSIT = 'IT',"In Transit"
        AT_DEPOT = 'AT',"At Depot"
        ARRIVED_DESTINATION = 'AD',"Arrived Destination"
        ON_ROUTE = 'OR', "On Route"

    truck_status = models.CharField(choices = TruckStatus.choices,default=TruckStatus.IN_SERVICE, max_length= 5)
    truck_location = models.CharField(choices=TruckLocation.choices,default=TruckLocation.AT_DEPOT, max_length=3)

    def get_drivers(self):
        return self.driver.all()

    def __str__(self):
        return f"{self.vin}"