from django.db import models

from core.models import Truck, Driver


class Trip(models.Model):
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    arrival_time = models.DateTimeField(null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    truck = models.ForeignKey(Truck,on_delete=models.SET_NULL,null=True,blank=True,related_name='trips')
    driver = models.ForeignKey(Driver,on_delete=models.SET_NULL,null=True,blank=True,related_name='trips')

    planned_miles = models.FloatField(default=0)
    actual_miles = models.FloatField(default=0)
    loaded_miles = models.FloatField(default=0)
    empty_miles = models.FloatField(default=0)

    cpm = models.FloatField(default=0)
    pay = models.FloatField(default=0, null = True, blank = True)


    class TripStatus(models.TextChoices):
        active = 'act',"active"
        completed = 'com',"completed"
        canceled = 'can',"canceled"
        incomplete = 'inc',"incomplete"

    status = models.CharField(choices = TripStatus.choices,default=TripStatus.active, max_length= 10)

    def get_load_pay(self):
        load_pay = self.cpm * self.planned_miles / 100
        return load_pay

    def __str__(self):
        return f"Trip {self.id}: {self.start} → {self.end} ({self.status})"

